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

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)


    def test_login_logout(self):
#        rv = self.login(myblog.app.config['USERNAME'], myblog.app.config['PASSWORD'])
        rv = self.login('admin','default')
        assert b'You were logged in' in rv.data

if __name__ == '__main__':
    unittest.main()
