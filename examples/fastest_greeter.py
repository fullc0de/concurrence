from concurrence import dispatch, Tasklet
from concurrence.io import Buffer, Socket

import os

HTTP_PORT = 8080
HTTP_WORKERS = 4

def handle(client_socket):
    buffer = Buffer(1024)
    client_socket.read(buffer)
    buffer.clear()
    buffer.write_bytes(
            "HTTP/1.0 200 OK\r\n"                     \
            "Server: c-raw/0.0\r\n"                   \
            "Date: Sat, 12 Dec 2009 21:29:00 GMT\r\n" \
            "Content-Type: text/plain\r\n"            \
            "Content-Length: 13\r\n"                  \
            "Connection: close\r\n"                   \
            "\r\n"                                    \
            "Hello World!\n"
        )
    buffer.flip()
    client_socket.write(buffer)
    client_socket.close()

def server():
    """accepts connections on a socket, and dispatches
    new tasks for handling the incoming requests"""
    #listen
    server_socket = Socket.server(('localhost', 8100), backlog=2048)
    #and fork off some workers to accept requests
    for i in range(HTTP_WORKERS):
        pid = os.fork()
        if pid == 0:
            #i am a worker, accept and handle connections
            try:
                for client_socket in server_socket.accept_iter():
                    Tasklet.defer(handle, client_socket)
            finally:
                return
    #i am the parent
    while True:
        Tasklet.sleep(1.0)

if __name__ == '__main__':
    import logging
    logging.basicConfig()
    dispatch(server)
