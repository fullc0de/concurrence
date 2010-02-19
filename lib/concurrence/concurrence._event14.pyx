# adds libevent1.4 supported API's

from concurrence._event import EventError

cdef extern from "event.h":
    void *event_init() nogil
    int event_reinit(void *) nogil

cdef void* main_event_base
main_event_base = NULL

def reinit():
    #reinit libevent in a forked process (libevent1.4+)
    cdef int result
    if main_event_base == NULL:
        raise EventError("mmm, can only re-init when we did init first")
    result = event_reinit(main_event_base)
    if result == -1:
        raise EventError("could not reinit main event base")

def init():
    #init libevent
    global main_event_base
    main_event_base = event_init()
