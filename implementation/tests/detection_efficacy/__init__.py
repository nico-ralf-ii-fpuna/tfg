# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Nico Epp and Ralf Funk
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .classification import run_test as inner_run_test


BEST_TRAINING_SAMPLES = 1500
BEST_TRAINING_ANOMALIES = 0.0
BEST_FILTER_CONSTRAINTS = 'RK'
BEST_WITH_SCALING = True


def run_test():
    df = inner_run_test()
    df = df[df['training_samples'] == BEST_TRAINING_SAMPLES]
    df = df[df['training_anomalies'] == BEST_TRAINING_ANOMALIES]
    df = df[df['filter_constraints'] == BEST_FILTER_CONSTRAINTS]
    df = df[df['with_scaling'] == BEST_WITH_SCALING]

    print()
    print('{:5s} | {:4s} | {:4s} | {}'.format('', 'TPR', 'FPR', 'f_score'))
    print('=' * 30)

    for key1, sub_df in df.groupby(['ds_url', ]):
        print('{:5s} | {:4.2f} | {:4.2f} | {:4.2f}'.format(
            key1,
            sub_df['TPR'].mean(),
            sub_df['FPR'].mean(),
            sub_df['f_score'].mean()))

    print('=' * 30)
    print('{:5s} | {:4.2f} | {:4.2f} | {:4.2f}'.format(
        'TOTAL',
        df['TPR'].mean(),
        df['FPR'].mean(),
        df['f_score'].mean()))
