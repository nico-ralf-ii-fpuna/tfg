# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Nico Epp and Ralf Funk
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from . import base, char_distribution, entropy, length, raw_data


NUMBERS_TF_LIST = (
    char_distribution.RqCharDisTransformer,
    char_distribution.QpCharDisTransformer,
    char_distribution.BpCharDisTransformer,
    # char_distribution.HeCharDisTransformer,
    entropy.RqEntropyTransformer,
    entropy.QpEntropyTransformer,
    entropy.BpEntropyTransformer,
    # entropy.HeEntropyTransformer,
    length.RqLengthTransformer,
    length.QpLengthTransformer,
    length.BpLengthTransformer,
    # length.HeLengthTransformer,
)
RAW_DATA_TF_LIST = (
    raw_data.RqRawDataTransformer,
    raw_data.QpRawDataTransformer,
    raw_data.BpRawDataTransformer,
    # raw_data.HeRawDataTransformer,
)
