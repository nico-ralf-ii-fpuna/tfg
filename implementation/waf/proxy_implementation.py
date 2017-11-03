# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Nico Epp and Ralf Funk
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
import os
from sklearn.externals import joblib
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
from ..base import BASE_PATH, Request
from . import proxy_base, feature_extraction


class CustomWAF(proxy_base.CherryProxy):

    def __init__(self, do_detection, block_unknowns, block_anomalies, **kwargs):
        super().__init__(**kwargs)
        self._do_detection = do_detection
        self._block_unknowns = block_unknowns
        self._block_anomalies = block_anomalies
        self._detection_models = {}

    def _load_trained_detection_models(self):
        try:
            self._detection_models = joblib.load(os.path.join(
                BASE_PATH, 'waf', 'trained_models', 'latest_models.pkl'))
        except FileNotFoundError:
            self._detection_models = {}

    def train_new_detection_model(self, req_list, nu, gamma):
        key_set = set(str(req) for req in req_list)
        if len(key_set) != 1:
            self.log('ERROR: training data needs exactly one key')
            return

        key = key_set.pop()
        self.log('Training new detection model for key "{}" ...'.format(key))

        self._load_trained_detection_models()
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        joblib.dump(
            self._detection_models,
            os.path.join(BASE_PATH, 'waf', 'trained_models', 'models_till_{}.pkl'.format(
                current_time)))

        clf = make_pipeline(
            make_union(*[class_() for class_ in feature_extraction.NUMBERS_TF_LIST]),
            StandardScaler(),
            OneClassSVM(random_state=0, nu=nu, gamma=gamma))
        clf.fit(req_list)
        self._detection_models[key] = clf
        joblib.dump(
            self._detection_models,
            os.path.join(BASE_PATH, 'waf', 'trained_models', 'latest_models.pkl'))

    def start_detection(self):
        if self._do_detection:
            self.log('Loading detection models ...')
            self._load_trained_detection_models()
            self.log('{} detection models loaded.'.format(len(self._detection_models)))
            for i, key in enumerate(sorted(self._detection_models)):
                self.log('   {:2d} {}'.format(i+1, key))
        else:
            self.log('"do_detection" is False')

        super().start()

    def filter_request(self):
        if not self._do_detection:
            self.log_debug('filter_request', '"do_detection" is FALSE')
            return

        # build obtained Request object
        obt_req = Request(method=self.req.method, url=self.req.path)
        obt_req._headers = dict(self.req.headers)
        obt_req.query_params = self.req.query
        if self.req.data:
            obt_req.body_params = self.req.data.decode()

        key = str(obt_req)
        self.log_debug('filter_request', 'do filtering for key "{}"'.format(key))

        if key not in self._detection_models:
            if self._block_unknowns:
                aux_str = 'request blocked'
                self.set_response_forbidden()
            else:
                aux_str = '"block_unknowns" is FALSE'

            self.log_debug('filter_request', 'no detection model found - {}'.format(aux_str))
            return

        clf = self._detection_models[key]
        y = clf.predict(obt_req)[0]
        self.log_debug('filter_request', 'prediction {}'.format(y))

        if y == -1:
            if self._block_anomalies:
                self.log_debug('filter_request', 'request blocked')
                self.set_response_forbidden()
            else:
                self.log_debug('filter_request', '"block_anomalies" is FALSE')
