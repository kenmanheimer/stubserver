#!/usr/bin/env python

"""Minimal http server that logs the request headers to stdout.

Adapted from http://stackoverflow.com/a/12786032/1052133
"""

PORT = 80

import SimpleHTTPServer, SocketServer
import logging
import sys

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        logging.debug(self.headers)

    do_POST = do_GET

if __name__ == "__main__":
    httpd = SocketServer.TCPServer(("", PORT), ServerHandler)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    try:
        print "\nServing at port", PORT
        httpd.serve_forever()
    finally:
        print "\n\n... INTERRUPTED. Shutting down...\n\n"
        httpd.shutdown()
