import os
import app as project
import unittest
import tempfile


def login(self, username, password):
    return self.app.post('/process_login', data=dict(username=username, password=password), follow_redirects=True)


def register(self, username, password):
    return self.app.post('/create_account', data=dict(username=username, password=password), follow_redirects=True)


class Project(unittest.TestCase):

    def setUp(self):
        self.db_fd, project.app.config['DATABASE'] = tempfile.mkstemp()
        project.app.testing = True
        self.app = project.app.test_client()
        with project.app.app_context():
            project.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(project.app.config['DATABASE'])

    def test_home(self):
        rv = self.app.get('/')
        assert b'CYOA GEN' in rv.data

    def test_account_page(self):
        rv = self.app.get('/account')
        assert b'username' in rv.data

    def test_login_page(self):
        rv = self.app.get('/login')
        assert b'username' in rv.data

    def test_create_page(self):
        register(self,'testUser', 'verySecure')
        login(self, 'testUser', 'verySecure')
        rv = self.app.get('/create_game')
        assert b'Situation' in rv.data

    def test_create_title_page(self):
        rv = self.app.post('/title', data=dict(id=0), follow_redirects=True)
        assert b'Title' in rv.data


if __name__ == '__main__':
    unittest.main()
