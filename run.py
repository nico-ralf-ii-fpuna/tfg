# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Nico Epp and Ralf Funk
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
from implementation.tests import detection_efficacy, training_duration, waf_speed
from latex import make_pdf_articulo_resumen, make_pdf_libro, make_pdf_propuesta


AVAILABLE_COMMANDS = '''{}

Available commands are: 
    test1
    test2 destination
    test2 waf_without_det
    test2 waf_with_det
    test2 source
    test3
    make_pdf
'''
USAGE = AVAILABLE_COMMANDS.format('Usage: python run.py COMMAND')
FALSE_CMD = AVAILABLE_COMMANDS.format('"{}" is not an available command')


def run():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test1':
            detection_efficacy.run_test()
        elif sys.argv[1] == 'test2':
            if len(sys.argv) <= 2:
                print(FALSE_CMD.format(sys.argv[1]))
            elif sys.argv[2] == 'destination':
                waf_speed.start_destination()
            elif sys.argv[2] == 'waf_without_det':
                waf_speed.start_waf_without_detection()
            elif sys.argv[2] == 'waf_with_det':
                waf_speed.start_waf_with_detection()
            elif sys.argv[2] == 'source':
                waf_speed.start_source()
            else:
                print(FALSE_CMD.format('test2 ' + sys.argv[2]))
        elif sys.argv[1] == 'test3':
            training_duration.run_test()
        elif sys.argv[1] == 'make_pdf':
            make_pdf_articulo_resumen()
            make_pdf_libro()
            make_pdf_propuesta()
        elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print(USAGE)
        else:
            print(FALSE_CMD.format(sys.argv[1]))
    else:
        print(USAGE)


if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.realpath(__file__)))
    run()
