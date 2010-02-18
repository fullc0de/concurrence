#ifndef http11_parser_alloc_h
#define http11_parser_alloc_h

#include "http11_parser.h"

http_parser *http_parser_alloc(void *obj, element_cb request_method,
                                          element_cb request_uri,
                                          element_cb fragment,
                                          element_cb request_path,
                                          element_cb query_string,
                                          element_cb http_version,
                                          element_cb header_done,
                                          field_cb field);
void http_parser_free(http_parser *);

#endif
