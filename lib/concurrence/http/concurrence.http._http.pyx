# Copyright (C) 2009, Hyves (Startphone Ltd.)
#
# This module is part of the Concurrence Framework and is released under
# the New BSD License: http://www.opensource.org/licenses/bsd-license.php

from concurrence.io._io cimport Buffer

cdef extern from "http11_parser.h":
    ctypedef struct http_parser
    ctypedef int size_t

    int http_parser_init(http_parser *parser)
    int http_parser_finish(http_parser *parser)
    size_t http_parser_execute(http_parser *parser, char *data, size_t len, size_t off)
    int http_parser_has_error(http_parser *parser)
    int http_parser_is_finished(http_parser *parser)

ctypedef void (*element_cb)(void *data, char *at, size_t length)
ctypedef void (*field_cb)(void *data, char *field, size_t flen, char *value, size_t vlen)

cdef extern from "http11_parser_alloc.h":
    http_parser *http_parser_alloc(void *obj, element_cb request_method,
                                              element_cb request_uri,
                                              element_cb fragment,
                                              element_cb request_path,
                                              element_cb query_string,
                                              element_cb http_version,
                                              element_cb header_done)
    void http_parser_free(http_parser *)

cdef extern from "Python.h":
    object PyString_FromStringAndSize(char *, int)

cdef class HTTPParser

cdef void cb_request_method(void *data, char *at, size_t length):
    (<HTTPParser>data).request_method(PyString_FromStringAndSize(at, length))

cdef void cb_request_uri(void *data, char *at, size_t length):
    (<HTTPParser>data).request_uri(PyString_FromStringAndSize(at, length))

cdef void cb_fragment(void *data, char *at, size_t length):
    (<HTTPParser>data).fragment(PyString_FromStringAndSize(at, length))

cdef void cb_request_path(void *data, char *at, size_t length):
    (<HTTPParser>data).request_path(PyString_FromStringAndSize(at, length))

cdef void cb_query_string(void *data, char *at, size_t length):
    (<HTTPParser>data).query_string(PyString_FromStringAndSize(at, length))

cdef void cb_http_version(void *data, char *at, size_t length):
    (<HTTPParser>data).http_version(PyString_FromStringAndSize(at, length))

cdef void cb_header_done(void *data, char *at, size_t length):
    (<HTTPParser>data).header_done(PyString_FromStringAndSize(at, length))

cdef class HTTPParser:
    """
    """
    cdef http_parser *_parser
    cdef Buffer _buffer

    def __cinit__(self, Buffer buffer):
        self._buffer = buffer
        self._parser = http_parser_alloc(<void *>self, cb_request_method,
                                          cb_request_uri,
                                          cb_fragment,
                                          cb_request_path,
                                          cb_query_string,
                                          cb_http_version,
                                          cb_header_done)
        http_parser_init(self._parser)

    def __dealloc__(self):
        http_parser_free(self._parser)

    def request_method(self, method):
        print 'method:', method

    def request_uri(self, uri):
        print 'r_uri', uri

    def http_version(self, version):
        print 'version', repr(version)

    def execute(self):
        return http_parser_execute(self._parser, <char *>self._buffer._buff, self._buffer._remaining(), self._buffer._position)


