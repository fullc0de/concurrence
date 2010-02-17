from concurrence import unittest
from concurrence.http import _http

class TestHTTPParser(unittest.TestCase):
    def testParser(self):
        p = _http.HTTPParser()

if __name__ == '__main__':
    unittest.main(timeout = 10)












