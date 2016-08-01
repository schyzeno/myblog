import os
import unittest

from context import myblog

class MyblogTestCase(unittest.TestCase):

    def setUp(self):
        myblog.app.config['TESTING']=True
        self.app = myblog.app.test_client()
    
    def test_index(self):
        rv = self.app.get('/')
        assert b'<title>Home</title>' in rv.data


if __name__ == '__main__':
    unittest.main()
