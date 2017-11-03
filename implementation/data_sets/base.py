# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Nico Epp and Ralf Funk
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Dict, List


def read_and_group_requests(
        selected_endpoint_list: List[str], ds_url_list: List[str], normal_file_names: List[str],
        anomalous_file_names: List[str], read_func) -> Dict:
    d = {}

    # initialize dict with empty lists
    for key in selected_endpoint_list:
        d[key] = {
            'normal': [],
            'anomalous': [],
        }

    # read requests and group them by key
    for label, file_name_list in zip(
            ('normal', 'anomalous'),
            (normal_file_names, anomalous_file_names)
    ):
        for req in read_func(file_name_list):
            key = str(req)
            if key in selected_endpoint_list:
                d[key][label].append(req)

    # replace keys with ds_url
    new_d = {}
    for key, ds_url in zip(selected_endpoint_list, ds_url_list):
        new_d[ds_url] = d[key]

    return new_d


def group_requests(r_list: List, key_func) -> Dict:
    d = {}
    for r in r_list:
        k = key_func(r)
        d.setdefault(k, [])
        d[k].append(r)

    return d
