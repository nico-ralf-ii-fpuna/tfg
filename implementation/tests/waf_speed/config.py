# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Nico Epp and Ralf Funk
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

DESTINATION_ADDRESS = 'localhost'
DESTINATION_PORT = 8881
WAF_WITHOUT_DETECTION_ADDRESS = 'localhost'
WAF_WITHOUT_DETECTION_PORT = 8882
WAF_WITH_DETECTION_ADDRESS = 'localhost'
WAF_WITH_DETECTION_PORT = 8883
REQ_TIMEOUT = 10
REQ_RANGES = (
    ('normal', range(5)),
    ('anomalous', range(5)),
)
