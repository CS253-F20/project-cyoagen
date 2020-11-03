# -*- coding: utf-8 -*-
import os
from sqlite3 import dbapi2 as sqlite3

import werkzeug.security
from flask import Flask, request, g, redirect, url_for, render_template, flash, session

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'account.db'),
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('ACCOUNT_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('init_db')
def init_db_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def homepage():
    if 'username' in session:  # If logged in, display "welcome (username)"
        return render_template('Home.html', Page="Home", User=session['username'])
    else:  # Else display "Welcome user"
        return render_template('Home.html', Page="Home", User="User")
        # Renders homepage


@app.route('/create_account')
def create_account_page():
    return render_template('create_account.html', Page="Account Creation")
    # Renders the account creation page, Page is used to dynamically adjust the navbar.


@app.route('/process_account', methods=["POST"])
def create_account():
    db = get_db()
    username = request.form['username']
    password = request.form['password']
    cur = db.execute('SELECT username FROM accounts where username = ?', [username])
    user_list = cur.fetchall()  # Search for entered username in the database
    if user_list:  # Check if username is taken
        error = 'Username is already taken'
    elif username == '':  # Check if username is null
        error = 'Invalid Username!'
    elif password == '':  # Check if password is null
        error = 'You must have a password!'
    else:  # If the new account passes the checks, create account and return homepage
        password = werkzeug.security.generate_password_hash(password)
        db.execute('INSERT INTO accounts (username, password) VALUES (?, ?)',
                   [username, password])
        db.commit()
        return redirect(url_for('homepage'))
    flash(error)  # If there was an error flash a message
    return redirect(url_for('create_account_page'))  # Return to the page to try again


@app.route('/account')
def account_page():
    db = get_db()
    username = session['username']
    cur = db.execute('SELECT title, id, published FROM games where username = ?', [username])
    games = cur.fetchall()
    return render_template('account.html', games=games, Page="My Games")


@app.route('/publish', methods=['POST'])
def publish():
    db = get_db()
    if request.form['mode'] == 'True':
        mode = True
    else:
        mode = False
    db.execute('UPDATE games SET published = ? where id = ?',
               [mode, request.form['game_id']])
    db.commit()
    return redirect(url_for('account_page'))


@app.route('/login')
def login_page():
    return render_template('login.html', Page="Login")
    # Render the login page for easy login


@app.route('/process_login', methods=['POST'])
def login_handler():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    cur = db.execute('SELECT username FROM accounts where username = ?', [username])
    user_list = cur.fetchall()  # Search Database for entered username to see if account exists
    if not user_list:  # If no account exists with that name
        error = 'Invalid Username'
    else:  # If an account is found with that username
        cur = db.execute('SELECT password FROM accounts where username = ?', [username])
        pass_hashed = cur.fetchone()  # Grab the stored password hash
        if not werkzeug.security.check_password_hash(pass_hashed[0], password):  # If the password doesn't match
            error = 'Invalid Password'
        else:  # If password matches and username checks out
            session['username'] = username  # Set session variable for username to current logged in user
            flash('You were logged in')
            return redirect(url_for('homepage'))
    flash(error)  # If they are not redirected to the home page, display what credential was wrong.
    return redirect(url_for('login_page'))


@app.route('/process_logout')
def logout_handler():
    session.pop('username', None)  # Remove username variable from session, indicating no logged in account
    flash('You were logged out')
    return redirect(url_for('homepage'))


@app.route('/title')
def create_title_page():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    else:
        return render_template('create_title.html', Page='Title Creation')


@app.route('/process_title', methods=['POST'])
def process_title():
    db = get_db()
    title = request.form['title']
    desc = request.form['description']
    username = session['username']
    if desc and title:
        db.execute('INSERT INTO games (title, description, username, published) VALUES (?, ?, ?, ?)',
                   [title, desc, username, False])
        cur = db.execute('SELECT id from games where title = ? AND description = ? AND username = ?',
                         [title, desc, username])
        game_id = cur.fetchone()["id"]
        db.commit()
        return redirect(url_for("create_page", game_id=game_id))
    elif not title:
        flash('Invalid Title!')
    elif not desc:
        flash('Invalid Description!')
    return redirect(url_for('create_title_page'))


@app.route('/create_game', methods=['GET'])
def create_page():
    db = get_db()
    game_id = request.args['game_id']
    cur = db.execute('SELECT title, option1, option2, situation, id, linked_situation1, linked_situation2 FROM choices '
                     'where username = ? AND game_id = ?', [session['username'], game_id])
    choices = cur.fetchall()
    return render_template('create_game.html', gameID=game_id, choices=choices, Page='Game Creation')


@app.route('/create_handler', methods=['POST'])
def create_handler():
    db = get_db()
    game_id = request.form['game_id']
    db.execute('INSERT INTO choices (title, situation, option1, option2, username, game_id) VALUES (?, ?, ?, ?,?,?)',
               [request.form['Situation_Title'], request.form['Situation'], request.form['ChoiceOne'],
                request.form['ChoiceTwo'], session['username'], game_id])
    # Add the choices back to the database with new entries.
    db.commit()
    flash('Situation was successfully saved!')
    return redirect(url_for("create_page", game_id=game_id))


@app.route('/browse_game')
def browse_game():
    db = get_db()
    cur = db.execute('SELECT title,id FROM games where published = ?', [True])
    games = cur.fetchall()
    return render_template('browse_game.html', Page="Browse Games", games=games)


@app.route('/search_game', methods=['POST'])
def search():
    db = get_db()
    search_game = request.form['search_game']
    cur = db.execute('SELECT title,id FROM games where title = ?', [search_game])
    game = cur.fetchall()
    if not game:
        flash('No games like this')
        return redirect(url_for('browse_game'))
    else:
        return render_template('search_game.html', games=game, Page="Browse Games")


@app.route('/linking_handler', methods=['POST'])
def linking_handler():
    db = get_db()
    mode = int(request.form['mode'])
    if mode == 0:
        db.execute('UPDATE choices SET linked_situation1 = ?, linked_situation2 = ? where id = ?',
                   [request.form['linked_situation1'], request.form['linked_situation2'], request.form['id']])
        code = 'Choices have been linked!'
    else:
        db.execute('UPDATE choices SET linked_situation1 = NULL , linked_situation2 = NULL where id = ?',
                   [request.form['id']])
        code = 'Linked choices have been cleared.'
    db.commit()
    game_id = request.form['game_id']
    flash(code)
    return redirect(url_for("create_page", game_id=game_id))


@app.route('/play_game', methods=['GET'])
def play_game():
    db = get_db()
    game_id = request.args['game_id']
    cur = db.execute(' SELECT title FROM games WHERE id = ?', [game_id])
    title = cur.fetchall()
    sur = db.execute(' SELECT description FROM games WHERE id = ?', [game_id])
    description = sur.fetchall()
    return render_template('play_game.html', title=title, description=description, id=game_id)


@app.route('/play', methods=['POST'])
def game_page():
    db = get_db()
    game_id = request.form['game_id']
    key = request.form['key']
    cur = db.execute('SELECT title, situation, option1, option2, linked_situation1, linked_situation2 FROM choices'
                     ' WHERE game_id = ? AND title = ?', [game_id, key])
    choice = cur.fetchone()
    return render_template('game_page.html', choice=choice, game_id=game_id, Page='Play')


if __name__ == '__main__':
    app.run()
