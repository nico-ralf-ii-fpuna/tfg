# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Nico Epp and Ralf Funk
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pandas as pd
import requests
import time
from ... import data_sets
from . import config


def _send(req, destination_address, destination_port):
    t_start = time.perf_counter()

    try:
        options = {
            'url': 'http://{}:{}{}'.format(destination_address, destination_port, req.url),
            'headers': dict(req.headers),
            'timeout': config.REQ_TIMEOUT,
        }

        if req.method == 'GET':
            options['params'] = dict(req.query_params)
            resp = requests.get(**options)
        else:
            options['data'] = dict(req.body_params)
            resp = requests.post(**options)
    except (requests.ConnectionError, requests.Timeout) as err:
        raise ValueError(err)

    t_end = time.perf_counter()
    t = t_end - t_start

    return resp.status_code, t


def run_once() -> pd.DataFrame:
    result_list = []

    for ds_url in data_sets.DS_URL_LIST[:16]:
        normal_req_list, anomalous_req_list = data_sets.get(ds_url)
        data = {
            'normal': normal_req_list,
            'anomalous': anomalous_req_list,
        }

        for req_class, req_n_range in config.REQ_RANGES:
            for req_n in req_n_range:
                req = data[req_class][req_n]

                # destination address and port are specified in the config of the test, so we use
                # relative urls
                req.url = req.url.replace('http://localhost:8080', '')

                status_code_1, t_1 = _send(
                    req,
                    config.DESTINATION_ADDRESS,
                    config.DESTINATION_PORT)
                status_code_2, t_2 = _send(
                    req,
                    config.WAF_WITHOUT_DETECTION_ADDRESS,
                    config.WAF_WITHOUT_DETECTION_PORT)
                status_code_3, t_3 = _send(
                    req,
                    config.WAF_WITH_DETECTION_ADDRESS,
                    config.WAF_WITH_DETECTION_PORT)

                row = [
                    ds_url, req_class, req_n, status_code_1, status_code_2, status_code_3,
                    t_1, t_2, t_3,
                ]
                print(row)
                result_list.append(row)

    return pd.DataFrame(
        data=result_list,
        columns=[
            'ds_url', 'req_class', 'req_n', 'status_code_1', 'status_code_2', 'status_code_3',
            't_1', 't_2', 't_3',
        ])


def run():
    df = run_once()

    # check for errors
    assert df['status_code_1'].unique().shape[0] == 1
    assert df['status_code_2'].unique().shape[0] == 1
    assert df['status_code_3'].unique().shape[0] == 1

    print()
    print('| {:25s} | {:25s} | {:21s} | {:17s} | {:17s} |'.format(
        'scenario', 'number of requests', 'average duration', 'normal', 'anomalous'))
    sub_df_n = df[df['req_class'] == 'normal']
    sub_df_a = df[df['req_class'] == 'anomalous']
    for col, label in (
            ['t_1', 'no WAF'],
            ['t_2', 'with WAF - no detection'],
            ['t_3', 'with WAF - with detection'],
    ):
        print('| {:25s} | {:25d} | {:10.4f} +/- {:6.4f} | {:6.4f} +/- {:6.4f} | {:6.4f} +/- {:6.4f} |'.format(
            label, df[col].shape[0],
            df[col].mean(), df[col].std(),
            sub_df_n[col].mean(), sub_df_n[col].std(),
            sub_df_a[col].mean(), sub_df_a[col].std()))
