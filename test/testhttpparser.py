from __future__ import with_statement

from concurrence import unittest
from concurrence.io import Buffer
from concurrence.http import _http

class TestHTTPParser(unittest.TestCase):
    def testParser(self):
        N = 100000
        with unittest.timer() as tmr:
            for i in range(N):
                b = Buffer(1024)
                p = _http.HTTPParser(b)
                b.write_bytes("GET /bla.html?piet=blaat&jaap=aap#blaataap HTTP/1.1\r\n")
                b.write_bytes("Content-length: 10\r\n")
                b.write_bytes("\r\n")
                b.flip()
                p.execute()
        print tmr.sec(N)

if __name__ == '__main__':
    unittest.main(timeout = 10)












