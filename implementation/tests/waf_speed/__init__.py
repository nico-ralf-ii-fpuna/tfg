# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Nico Epp and Ralf Funk
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from ... import waf, data_sets
from . import config, destination, source


def start_destination():
    destination.run()


def start_waf_without_detection():
    options = {
        'listen_address': config.WAF_WITHOUT_DETECTION_ADDRESS,
        'listen_port': config.WAF_WITHOUT_DETECTION_PORT,
        'redirect_address': config.DESTINATION_ADDRESS,
        'redirect_port': config.DESTINATION_PORT,
        'verbosity': 1,
        'do_detection': False,
        'block_unknowns': False,
        'block_anomalies': False,
    }
    w = waf.CustomWAF(**options)
    w.start_detection()


def start_waf_with_detection():
    options = {
        'listen_address': config.WAF_WITH_DETECTION_ADDRESS,
        'listen_port': config.WAF_WITH_DETECTION_PORT,
        'redirect_address': config.DESTINATION_ADDRESS,
        'redirect_port': config.DESTINATION_PORT,
        'verbosity': 2,
        'do_detection': True,
        'block_unknowns': False,
        'block_anomalies': False,
    }
    w = waf.CustomWAF(**options)

    for ds_url in data_sets.DS_URL_LIST[:16]:
        normal_req_list, _ = data_sets.get(ds_url)
        training_list = []
        for r in normal_req_list[:500]:
            # destination address and port are specified in the config of the test, so we use
            # relative urls
            r.url = r.url.replace('http://localhost:8080', '')
            training_list.append(r)

        w.train_new_detection_model(req_list=training_list, nu=0.01, gamma=0.01)

    w.start_detection()


def start_source():
    source.run()
