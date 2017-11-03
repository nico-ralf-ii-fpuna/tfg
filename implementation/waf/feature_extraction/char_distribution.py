# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Nico Epp and Ralf Funk
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import collections
from typing import List, Tuple
from . import base


_MAX_CHAR_LENGTH = 256                          # type: int
_BIN_SIZES = (1, 2, 3, 4, _MAX_CHAR_LENGTH)     # type: Tuple[int]
_NUM_BINS = len(_BIN_SIZES)                     # type: int


class _CharDisMixin:

    @staticmethod
    def _get_features_per_key() -> List[str]:
        return [
            'BIN{}'.format(i)
            for i in range(_NUM_BINS)]

    @staticmethod
    def _evaluate(v: str) -> List[float]:
        """
        Calculates the character distribution of a string.
        """
        return _get_bins(v)


def _get_bins(value: str) -> List[float]:
    """
    Returns a list of bins containing the character distribution of the value.
    """
    d = collections.Counter(value)
    char_distribution = list(sorted(d.values(), reverse=True))

    # normalize
    total = sum(char_distribution)
    char_distribution = [e/total for e in char_distribution]

    # sum the char distribution probabilities for each bin
    bins = []
    j = 0
    for e in _BIN_SIZES:
        i = j
        j += e
        bins.append(sum(char_distribution[i:j]))

    return bins


class RqCharDisTransformer(
        _CharDisMixin,
        base.ReqTransformer):
    pass


class QpCharDisTransformer(
        _CharDisMixin,
        base.QueryParamMixin,
        base.KeyTransformer):
    pass


class BpCharDisTransformer(
        _CharDisMixin,
        base.BodyParamMixin,
        base.KeyTransformer):
    pass


class HeCharDisTransformer(
        _CharDisMixin,
        base.HeaderMixin,
        base.KeyTransformer):
    pass
