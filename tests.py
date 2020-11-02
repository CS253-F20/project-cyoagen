import os
import app as project
import unittest
import tempfile


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

    def login(self, username, password):
        return self.app.post('/process_login', data=dict(username=username, password=password), follow_redirects=True)

    def register(self, username, password):
        return self.app.post('/create_account', data=dict(username=username, password=password), follow_redirects=True)

    def test_home(self):
        rv = self.app.get('/')
        assert b'CYOA GEN' in rv.data  # Load the homepage and confirm the page is loading
        assert b'Play' in rv.data  # Play Button is Rendered
        assert b'Create' in rv.data  # Create Button is Rendered
        assert b'nav' in rv.data  # Ensure that the navigation bar is being loaded

    def test_account_page(self):
        rv = self.app.get('/account')
        assert b'username' in rv.data  # Load the accounts page and ensure the user has labeled fields
        self.register('testUser', 'verySecure')  # Register a user
        rv = self.register('testUser', 'verySecure')
        assert b'Username is already taken' in rv.data  # Test for duplicate username checks
        rv = self.register('', 'verySecure')
        assert b'Invalid Username!' in rv.data  # Make sure empty username fields are not allowed
        rv = self.register('testUserTwo', '')
        assert b'You must have a password!' in rv.data  # Check for an empty password field

    def test_login_page(self):
        rv = self.app.get('/login')
        assert b'username' in rv.data  # Check for basic page rendering
        self.register('testUser', 'verySecure')
        rv = self.login('testUser', 'veryUnsecure')
        assert b'You were logged in' not in rv.data  # Bad password check
        assert b'Invalid Password' in rv.data  # Error displays
        rv = self.login('testNotAUser', 'verySecure')
        assert b'Invalid Username' in rv.data  # Bad username error displayed
        rv = self.login('', '')
        assert b'Invalid Username' in rv.data  # Fields must be filled
        rv = self.login('testUser', 'verySecure')
        assert b'You were logged in' in rv.data  # Successful login
        assert b'CYOA GEN' in rv.data  # Page redirect back to home screen

    def test_logout(self):
        self.register('testUser', 'verySecure')
        self.login('testUser', 'verySecure')  # Register and Login a user for proper use
        rv = self.app.get('/process_logout', follow_redirects=True)  # Log out of the app
        assert b'You were logged out' in rv.data
        assert b'CYOA GEN' in rv.data

    def test_create_title_page(self):
        rv = self.app.get('/title')
        assert b'Title' not in rv.data  # Make sure user is logged in
        self.register('testUser', 'verySecure')
        self.login('testUser', 'verySecure')  # Register and Login a user for proper use
        rv = self.app.get('/title')
        assert b'Title' in rv.data  # Ensure page loads for logged in users

    def test_process_title(self):
        self.register('testUser', 'verySecure')
        self.login('testUser', 'verySecure')  # Register and Login a user for proper use
        rv = self.app.post('/process_title',
                           data=dict(title='title', description='desc'),
                           follow_redirects=True)
        assert b'Situation' in rv.data  # Correct usage of page redirects to next page
        rv = self.app.post('/process_title',
                           data=dict(title='', description='desc'),
                           follow_redirects=True)
        assert b'Situation' not in rv.data
        assert b'Invalid Title!' in rv.data  # Title field must be filled
        rv = self.app.post('/process_title',
                           data=dict(title='title', description=''),
                           follow_redirects=True)
        assert b'Situation' not in rv.data
        assert b'Invalid Description!' in rv.data  # Description field must be filled

    def test_create_page(self):
        self.register('testUser', 'verySecure')
        self.login('testUser', 'verySecure')
        self.app.post('/process_title',
                      data=dict(title='title', description='desc', username='testUser'),
                      follow_redirects=True)
        rv = self.app.get('create_game?game_id=0')
        assert b'Situation' in rv.data  # Page loads!
        assert b'select' not in rv.data  # No choices already exist on this page
        rv = self.app.post('/create_handler',
                           data=dict(Situation_Title='question', Situation='Do You?', ChoiceOne='Yes', ChoiceTwo='No',
                                     game_id=0),
                           follow_redirects=True)
        assert b'select' in rv.data  # Choices exist on the page
        assert b'Do You?' in rv.data  # Situation saves
        assert b'Yes' in rv.data  # There are options on the page


if __name__ == '__main__':
    unittest.main()
