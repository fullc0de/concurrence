from concurrence._event import event, version, method, has_next, next, loop, EventError
from concurrence._event import EV_TIMEOUT, EV_READ, EV_WRITE, EV_SIGNAL, EV_PERSIST

import os

try:
    #try to import some extra features available from libevent14+
    from concurrence._event14 import init
    from concurrence._event14 import reinit

    #monkey path fork, so that we reinit event after fork automatically
    os_fork = os.fork
    def fork():
        pid = os_fork()
        if pid == 0:
            #we are child, we must reinit libevent
            reinit()
        return pid
    os.fork = fork

except ImportError:
    #fall back to <1.4 init
    from concurrence._event import init
    #monkey path fork, to warn that it does not work < libevent14
    os_fork = os.fork
    def fork():
        raise EventError("fork does not work with libevent < 1.4")
    os.fork = fork
    def reinit():
        raise EventError("unavailable with libevent < 1.4")

#make sure libevent is inited
init()


