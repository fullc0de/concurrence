# Copyright (C) 2009, Hyves (Startphone Ltd.)
#
# This module is part of the Concurrence Framework and is released under
# the New BSD License: http://www.opensource.org/licenses/bsd-license.php

cdef extern from "http11_parser.h":
    ctypedef struct http_parser
    ctypedef int size_t
    int http_parser_init(http_parser *parser)
    int http_parser_finish(http_parser *parser)
    size_t http_parser_execute(http_parser *parser, char *data, size_t len, size_t off)
    int http_parser_has_error(http_parser *parser)
    int http_parser_is_finished(http_parser *parser)

cdef extern from "http11_parser_alloc.h":
    http_parser * http_parser_alloc()

cdef extern from "stdlib.h":
    cdef void *calloc(int, int)
    cdef void free(void *)

cdef class HTTPParser:
    """
    """
    cdef http_parser *_parser

    def __cinit__(self):
        self._parser = http_parser_alloc()

    def __dealloc__(self):
        free(self._parser)


