#include "http11_parser_alloc.h"

#include <stdlib.h>

http_parser *http_parser_alloc(void *obj, element_cb request_method,
                                          element_cb request_uri,
                                          element_cb fragment,
                                          element_cb request_path,
                                          element_cb query_string,
                                          element_cb http_version,
                                          element_cb header_done,
                                          field_cb field)
{
    http_parser * parser = calloc(1, sizeof(http_parser));
    parser->data = obj;
    parser->request_method = request_method;
    parser->request_uri = request_uri;
    parser->request_path = request_path;
    parser->fragment = fragment;
    parser->query_string = query_string;
    parser->http_version = http_version;
    parser->header_done = header_done;
    parser->http_field = field;

    return parser;
}

void http_parser_free(http_parser *parser)
{
    free(parser);
}

