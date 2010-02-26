from __future__ import with_statement

import logging
import random
import sys

from concurrence import dispatch, Tasklet
from concurrence.io import Socket, BufferedStream
from concurrence._unittest import timer
from concurrence.statistic import gamma_filter

N = 10000 #the number of clients to connect
B = 2000

KN = 500000 #the number of different keys being set
KV = 1024 * 4 #the max size of a value

#def server():
#    clients = []
#    server = Socket.server(('localhost', 6379))
#    for i, client_socket in enumerate(server.accept_iter()):
#        print 'client accepted', i
#        clients.append(client_socket)

clients = []

def set(stream, key, value):
    with stream.get_writer() as writer:
        writer.write_bytes("SET %s %d\r\n%s\r\n" % (key, len(value), value))
        writer.flush()
    with stream.get_reader() as reader:
        result = reader.read_line()
        assert result == "+OK"

def get(stream, key):
    #print key
    with stream.get_writer() as writer:
        writer.write_bytes("GET %s\r\n" % (key, ))
        writer.flush()
    with stream.get_reader() as reader:
        result = reader.read_line()
        #print 'result'
        assert result[0] == '$'
        n = int(result[1:])
        #print 'len', len
        if n != -1:
            data = reader.read_bytes(n)
            assert '' == reader.read_line()
            return n
        else:
            return 0

def bgrewriteaof(stream):
    with stream.get_writer() as writer:
        writer.write_bytes("BGREWRITEAOF\r\n")
        writer.flush()
    with stream.get_reader() as reader:
        result = reader.read_line()
        assert result == "+Background append only file rewriting started"

def truncator():
    while len(clients) < N:
        Tasklet.sleep(1.0)
    Tasklet.sleep(5.0)
    while True:
        print 'connecting truncator'
        client = Socket.connect(('localhost', 6379))
        stream = BufferedStream(client)
        print 'issueing trunc of append only log'
        bgrewriteaof(stream)
        stream.close()
        Tasklet.sleep(120.0)

def connector():
    for i in range(N):
        client = Socket.connect(('localhost', 6379))
        clients.append(BufferedStream(client))
        print i
    print 'connector done', N

def setter():
    while len(clients) < N:
        Tasklet.sleep(1.0)
    avg_bts_sec = 0.0
    avg_b_sec = 0.0
    while True:
        #set
        with timer() as tmr:
            bts = 0
            for i in range(B):
                stream = random.choice(clients)
                n = random.randint(0, KV)
                bts += n
                set(stream, 'fooblaatpiet%d' % random.randint(0, KN), 'b' * n)
        bts_sec = tmr.sec(bts)
        #print avg_bts_sec, bts_sec
        avg_bts_sec = gamma_filter(avg_bts_sec, bts_sec, 0.90)
        #print avg_bts_sec, bts_sec
        b_sec = tmr.sec(B)
        avg_b_sec = gamma_filter(avg_b_sec, b_sec, 0.90)
        print 'setter', b_sec, '/sec', avg_b_sec, '/sec', bts_sec / 1024.0 / 1024.0, 'Mb/sec', avg_bts_sec / 1024.0 / 1024.0, 'Mb/sec'
        Tasklet.sleep(1.0)

def getter():
    while len(clients) < N:
        Tasklet.sleep(1.0)
    while True:
        #get
        with timer() as tmr:
            bts = 0
            for i in range(B):
                #print i
                stream = random.choice(clients)
                bts += get(stream, 'fooblaatpiet%d' % random.randint(0, KN))
        print 'getter', tmr.sec(B), '/sec', tmr.sec(bts / 1024.0 / 1024.0), 'Mb/sec'
        Tasklet.sleep(1.0)


def main():
    Tasklet.new(connector)()
    if sys.argv[1] == 'setter':
        Tasklet.new(setter)()
    elif sys.argv[1] == 'getter':
        Tasklet.new(getter)()
        Tasklet.new(truncator)()
    else:
        assert False, sys.argv

if __name__ == '__main__':
    logging.basicConfig()
    dispatch(main)
