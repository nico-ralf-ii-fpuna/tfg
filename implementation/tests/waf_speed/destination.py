# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Nico Epp and Ralf Funk
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from http.server import HTTPServer, BaseHTTPRequestHandler
from . import config


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        self.send_response(200)
        self.end_headers()


def run():
    httpd = HTTPServer(
        (config.DESTINATION_ADDRESS, config.DESTINATION_PORT),
        RequestHandler)

    print('starting server on {} ...'.format(httpd.server_address))
    httpd.serve_forever()
