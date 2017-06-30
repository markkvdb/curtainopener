import os
import curtainopener
from curtainopener import database_handler
import unittest
import tempfile

class CurtainTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, curtainopener.app.config['DATABASE'] = tempfile.mkstemp()
        curtainopener.app.testing = True
        self.app = curtainopener.app.test_client()
        with curtainopener.app.app_context():
            database_handler.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(curtainopener.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No alarms so far.' in rv.data

    def test_alarm(self):
        rv = self.app.post('/add', data=dict(
            hours='13',
            minutes='30',
            open='1'
        ), follow_redirects=True)
        assert b'No alarms so far.' not in rv.data
        assert b'13:30' in rv.data
        assert b'open' in rv.data


if __name__ == '__main__':
    unittest.main()