from __future__ import with_statement

from concurrence import unittest
from concurrence.io import Buffer
from concurrence.http import _http

class TestHTTPParser(unittest.TestCase):
    def testParserSpeed(self):
        N = 500000
        b = Buffer(1024)
        b.write_bytes("GET /bla.html?piet=blaat&jaap=aap HTTP/1.1\r\n")
        b.write_bytes("Content-length: 10\r\n")
        b.write_bytes("\r\n")
        b.flip()
        with unittest.timer() as tmr:
            for i in range(N):
                p = _http.HTTPParser(b)
                p.parse()
                b.position = 0
        print tmr.sec(N)

    def testParser(self):
        b = Buffer(1024)
        b.write_bytes("POST /bla.html?piet=blaat&jaap=aap#blaataap HTTP/1.1\r\n")
        b.write_bytes("Content-length: 10\r\n")
        b.write_bytes("Another-header: blaat: piet\r\n")
        b.write_bytes("Another-header: blaat: piet\r\n")
        b.write_bytes("Content-type: blaat/piet\r\n")
        b.write_bytes("\r\n")
        b.write_bytes("1234567890")
        b.flip()
        print b.limit, b.position
        p = _http.HTTPParser(b)
        print repr(p.environ)
        print 'isfin', repr(p.is_finished())
        print p.parse()
        print 'isfin', repr(p.is_finished())
        print b.limit, b.position
        print repr(p.environ)
        print p.parse()
        #print p.parse()

if __name__ == '__main__':
    unittest.main(timeout = 10)












