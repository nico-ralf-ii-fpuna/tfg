# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Nico Epp and Ralf Funk
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Tuple
from . import csic, torpeda
from .base import read_and_group_requests


DS_URL_LIST = csic.DS_URL_LIST + torpeda.DS_URL_LIST


_in_memory_cache = {}


def get(ds_url: str) -> Tuple:
    if ds_url not in _in_memory_cache:
        if ds_url[0] == 'c':
            _in_memory_cache.update(
                read_and_group_requests(
                    csic.SELECTED_ENDPOINT_LIST,
                    csic.DS_URL_LIST,
                    csic.NORMAL_FILE_NAMES,
                    csic.ANOMALOUS_FILE_NAMES,
                    csic.read_requests))

        if ds_url[0] == 't':
            _in_memory_cache.update(
                read_and_group_requests(
                    torpeda.SELECTED_ENDPOINT_LIST,
                    torpeda.DS_URL_LIST,
                    torpeda.NORMAL_FILE_NAMES,
                    torpeda.ANOMALOUS_FILE_NAMES,
                    torpeda.read_requests))

    # this will raise KeyError for invalid options
    e = _in_memory_cache[ds_url]
    normal_req_list = e['normal']
    anomalous_req_list = e['anomalous']
    assert len(normal_req_list) > 0
    assert len(anomalous_req_list) > 0

    return normal_req_list, anomalous_req_list
