from concurrence import unittest
from concurrence.io import Buffer
from concurrence.http import _http

class TestHTTPParser(unittest.TestCase):
    def testParser(self):
        b = Buffer(1024)
        p = _http.HTTPParser(b)
        b.write_bytes("GET /bla.html?piet=blaat&jaap=aap HTTP/1.1\r\n")
        b.write_bytes("Content-length: 10\r\n")
        b.write_bytes("\r\n")
        b.flip()
        p.execute()

if __name__ == '__main__':
    unittest.main(timeout = 10)












