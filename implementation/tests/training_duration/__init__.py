# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Nico Epp and Ralf Funk
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import pandas as pd
import time
from sklearn.externals import joblib
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
from ... import data_sets, waf
from ...base import BASE_PATH


_file_memory = joblib.Memory(cachedir=os.path.join(BASE_PATH, 'cache'))


@_file_memory.cache
def _fit_one(ds_url: str, n: int) -> float:
    normal_list, _ = data_sets.get(ds_url)

    train_list = []
    while len(train_list) < n:
        train_list += normal_list
    train_list = train_list[:n]
    assert len(train_list) == n

    t_start = time.perf_counter()
    clf = make_pipeline(
        make_union(*[class_() for class_ in waf.feature_extraction.NUMBERS_TF_LIST]),
        StandardScaler(),
        OneClassSVM(random_state=0, nu=0.01, gamma=0.01))
    clf.fit(train_list)
    t_end = time.perf_counter()

    return t_end - t_start


def _fit_all() -> pd.DataFrame:
    result_list = []

    for ds_url in data_sets.DS_URL_LIST:
        for i in range(1, 5):
            n = 10**i
            t_total = _fit_one(ds_url, n)
            t_per_req = t_total / n

            result_list.append([ds_url, n, t_total, t_per_req])

    return pd.DataFrame(
        data=result_list,
        columns=['ds_url', 'n_requests', 't_total', 't_per_req'])


def run_test():
    df = _fit_all()

    print()
    print('| {:10s} | {:25s} | {:25s} | {:25s} | {:25s} |'.format(
        'n_requests',
        'average per request', 'max per request',
        'average total duration', 'max total duration'))
    for n_requests, sub_df in df.groupby(['n_requests', ]):
        print('| {:10,d} | {:12.6f} +/- {:8.6f} | {:25.6f} | {:25.6f} | {:25.6f} |'.format(
            n_requests,
            sub_df['t_per_req'].mean(),
            sub_df['t_per_req'].std(),
            sub_df['t_per_req'].max(),
            sub_df['t_total'].mean(),
            sub_df['t_total'].max()))
