#!/usr/bin/env python

"""Minimal http server that logs the request headers to stdout.

Based on guidance and clues from:
* Essential server: http://stackoverflow.com/a/12786032/1052133
* SSL server: http://www.piware.de/2011/01/creating-an-https-server-in-python/
* SSL cert: https://www.openssl.org/docs/HOWTO/certificates.txt
"""

PLAIN_PORT = 80
SSL_PORT = 443
SSL_CERT = "~/etc/stubcert.pem"

import SimpleHTTPServer, BaseHTTPServer, SocketServer
import ssl
import logging
import sys
import os.path

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        logging.debug(self.headers)

    do_POST = do_GET

root = logging.getLogger()
root.setLevel(logging.DEBUG)

if __name__ == "__main__":
    if (len(sys.argv) > 1) and (sys.argv[1] == "--ssl"):
        PORT = SSL_PORT
        httpd = BaseHTTPServer.HTTPServer(('localhost', PORT), ServerHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket,
                                       certfile=os.path.expanduser(SSL_CERT),
                                       server_side=True)
    else:
        PORT = PLAIN_PORT
        httpd = SocketServer.TCPServer(("", PORT), ServerHandler)

    try:
        print "\nServing at port", PORT
        httpd.serve_forever()
    finally:
        print "\n\n... INTERRUPTED. Shutting down...\n\n"
        httpd.shutdown()
