#include "http11_parser_alloc.h"

#include <stdlib.h>

http_parser *http_parser_alloc(void)
{
    return calloc(1, sizeof(http_parser));
}
