# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Nico Epp and Ralf Funk
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import shutil
import subprocess
import time


AUX_DIR = 'aux_files'


def _run_cmd(cmd, cwd):
    print()
    print()
    print('#' * 50)
    print('RUN:', cmd)
    t_start = time.perf_counter()
    subprocess.run(cmd, cwd=cwd, shell=True)
    t_end = time.perf_counter()
    print('DURATION: {:4.2f} seconds'.format(t_end - t_start))


def _make_pdf(dir_name, main_filename):
    _run_cmd(
        cmd='pdflatex -interaction batchmode -output-directory "{}" {}'.format(
            AUX_DIR,
            main_filename),
        cwd=dir_name)


def _make_glossaries(dir_name, main_filename):
    _run_cmd(
        cmd='makeglossaries -q -d "{}" {}'.format(
            AUX_DIR,
            main_filename),
        cwd=dir_name)


def _make_bibliography(dir_name, main_filename, files_to_copy):
    for filename in files_to_copy:
        src = os.path.join(dir_name, filename)
        dst = os.path.join(dir_name, AUX_DIR, filename)
        shutil.copy2(src, dst)

    _run_cmd(
        cmd='bibtex {}'.format(
            main_filename),
        cwd=os.path.join(dir_name, AUX_DIR))


def _make_all_parts(dir_name, main_filename, files_to_copy_for_bib):
    t_start = time.perf_counter()

    # Some online forums suggest running the PDF command multiple times to get
    # the bibliography working correctly; that seems to work for us as well
    _make_pdf(dir_name, main_filename)
    _make_glossaries(dir_name, main_filename)
    _make_pdf(dir_name, main_filename)
    _make_bibliography(dir_name, main_filename, files_to_copy_for_bib)
    _make_pdf(dir_name, main_filename)
    _make_pdf(dir_name, main_filename)

    t_end = time.perf_counter()
    print()
    print('TOTAL DURATION: {:4.2f} seconds'.format(t_end - t_start))


def make_pdf_articulo_resumen():
    _make_all_parts(
        dir_name=os.path.join('latex', 'articulo_resumen'),
        main_filename='articulo-resumen',
        files_to_copy_for_bib=[
            'p5_references.bib',
            'IEEEtran.bst',
        ])


def make_pdf_libro():
    _make_all_parts(
        dir_name=os.path.join('latex', 'libro'),
        main_filename='libro',
        files_to_copy_for_bib=[
            'p5_references.bib',
            'spanish.dtx',
            'thesis.cls',
        ])


def make_pdf_propuesta():
    _make_all_parts(
        dir_name=os.path.join('latex', 'propuesta'),
        main_filename='propuesta',
        files_to_copy_for_bib=[
            'p5_references.bib',
            'spanish.dtx',
            'thesis.cls',
        ])
