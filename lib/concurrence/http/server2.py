# Copyright (C) 2009, Hyves (Startphone Ltd.)
#
# This module is part of the Concurrence Framework and is released under
# the New BSD License: http://www.opensource.org/licenses/bsd-license.php

#TODO write timeout

from __future__ import with_statement

import logging
import urlparse
import httplib
import traceback
import rfc822

from concurrence import Tasklet, Message, Channel, TimeoutError, __version__
from concurrence.io import Socket, Buffer, BufferedStream
from concurrence.containers import ReorderQueue
from concurrence.timer import Timeout
from concurrence.http import HTTPError, HTTPParser

SERVER_ID = "Concurrence-Http/%s" % __version__

class HTTPConnection(object):

    def __init__(self, server, client_socket):
        self._server = server
        self._stream = BufferedStream(client_socket)

    def _write_response(self):
        response = "Hello World!"
        with self._stream.get_writer() as writer:
            writer.clear()
            writer.write_bytes("%s %s\r\n" % ('HTTP/1.1', '200 OK'))
            writer.write_bytes("Content-length: %d\r\n" % len(response))
            writer.write_bytes("\r\n")
            writer.write_bytes(response)
            writer.flush()

    def _read_request(self):

        with self._stream.get_reader() as reader:
            reader.fill() #initial fill
            parser = HTTPParser(reader.buffer)
            while True:
                #parse the buffer
                if parser.parse():
                    break #ok
                else:
                    #extra fill, could not parse request with data currently in buffer
                    reader.append() 

        self._write_response()
        self._stream.close()

    def handle(self):
        Tasklet.defer(self._read_request)

class WSGIServer(object):
    """A HTTP/1.1 Web server with WSGI application interface.

    Usage::

        def hello_world(environ, start_response):
            start_response("200 OK", [])
            return ["<html>Hello, world!</html>"]

        server = WSGIServer(hello_world)
        server.serve(('localhost', 8080))
    """
    log = logging.getLogger('WSGIServer')

    def __init__(self, application, request_log_level = logging.DEBUG):
        """Create a new WSGIServer serving the given *application*. Optionally
        the *request_log_level* can be given. This loglevel is used for logging the requests."""
        self._application = application
        self._request_log_level = request_log_level

    def internal_server_error(self, environ, start_response):
        """Default WSGI application for creating a default `500 Internal Server Error` response on any
        unhandled exception.
        The default response will render a traceback with a text/plain content-type.
        Can be overridden to provide a custom response."""
        start_response('500 Internal Server Error', [('Content-type', 'text/plain')])
        return [traceback.format_exc(20)]

    def handle_request(self, request):
        """All HTTP requests pass trough this method.
        This method provides a hook for logging, statistics and or further processing w.r.t. the *request*."""
        response = request.handle_request(self._application)
        self.log.log(self._request_log_level, "%s %s", request.status, request.uri)
        return response

    def handle_connection(self, client_socket):
        """All HTTP connections pass trough this method.
        This method provides a hook for logging, statistics and or further processing w.r.t. the connection."""
        HTTPConnection(self, client_socket).handle()

    def serve(self, endpoint):
        """Serves the application at the given *endpoint*. The *endpoint* must be a tuple (<host>, <port>)."""
        server_socket = Socket.server(endpoint)
        for client_socket in server_socket.accept_iter():
            self.handle_connection(client_socket)


