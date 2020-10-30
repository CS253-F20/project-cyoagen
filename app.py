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
    else:  # Else display "welcome user"
        return render_template('Home.html', Page="Home", User="User")


# Renders homepage


@app.route('/account')
def account_page():
    return render_template('create_account.html', Page="Account Creation")


@app.route('/create_account', methods=["POST"])
def create_account():
    db = get_db()
    username = request.form['username']
    password = werkzeug.security.generate_password_hash(request.form['password'])
    # Search for entered username in the database
    cur = db.execute('SELECT username FROM accounts where username = ?', [username])
    user_list = cur.fetchall()
    # If username is not already taken, create account and return homepage
    if not user_list:
        db.execute('INSERT INTO accounts (username, password) VALUES (?, ?)',
                   [username, password])
        db.commit()
        return redirect(url_for('homepage'))
    # If username is taken, flash a message and return the account creation page
    else:
        flash('Username is already taken')
        return redirect(url_for('account_page'))


@app.route('/login')
def login_page():
    return render_template('login.html', Page="Login")


@app.route('/process_login', methods=['POST'])
def login_handler():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    # Search Database for entered username to see if account exists
    cur = db.execute('SELECT username FROM accounts where username = ?', [username])
    user_list = cur.fetchall()
    if not user_list:  # If no account exists with that name
        error = 'Invalid Username'
    else:  # If an account is found with that username
        cur = db.execute('SELECT password FROM accounts where username = ?', [username])
        pass_hashed = cur.fetchone()  # Grab the stored password hash
        if not werkzeug.security.check_password_hash(pass_hashed[0], password):
            error = 'Invalid Password'
        else:  # If password matches
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


@app.route('/process_title', methods=['POST'])
def process_title():
    db = get_db()
    title = request.form['title']
    desc = request.form['description']
    username = session['username']
    db.execute('INSERT INTO games (title, description, username) VALUES (?, ?, ?)', [title, desc, username])
    cur = db.execute('SELECT id from games where title = ? AND description = ? AND username = ?',
                     [title, desc, username])
    game_id = cur.fetchone()["id"]
    db.commit()
    return redirect(url_for("create_page", game_id=game_id))


@app.route('/create_game', methods=['GET'])
def create_page():
    db = get_db()
    game_id = request.args['game_id']
    cur = db.execute('SELECT option1, option2, situation, id, linked_situation1, linked_situation2 FROM choices '
                     'where username = ? AND game_id = ?', [session['username'], game_id])
    choices = cur.fetchall()
    return render_template('create_game.html', gameID=game_id, choices=choices, Page='Game Creation')


@app.route('/create_handler', methods=['POST'])
def create_handler():
    db = get_db()
    game_id = request.form['game_id']
    db.execute('INSERT INTO choices (situation, option1, option2, username, game_id) VALUES (?, ?, ?, ?,?)',
               [request.form['Situation'], request.form['ChoiceOne'], request.form['ChoiceTwo'], session['username'],
                game_id])
    # Add the choices back to the database with new entries.
    db.commit()
    flash('Situation was successfully saved!')
    return redirect(url_for("create_page", game_id=game_id))


@app.route('/browse_game')
def browse_game():
    return render_template('browse_game.html', Page="Browse Games")


@app.route('/search_game', methods=['POST'])
def search():
    db = get_db()
    search_game = request.form['search_game']
    cur = db.execute('SELECT title FROM games where title = ?', [search_game])
    user_list = cur.fetchall()
    if not user_list:
        flash('No games like this')
        return redirect(url_for('browse_game'))
    else:
        account = user_list
        return render_template('search_game.html', accounts=account)


@app.route('/title')
def create_title_page():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    else:
        return render_template('create_title.html', Page='Title Creation')


@app.route('/linking_handler', methods=['POST'])
def linking_handler():
    db = get_db()
    db.execute('UPDATE choices SET linked_situation1 = ?, linked_situation2 = ? where id = ?',
               [request.form['linked_situation1'], request.form['linked_situation2'], request.form['id']])
    db.commit()
    game_id = request.form['game_id']
    return redirect(url_for("create_page", game_id=game_id))


@app.route('/clearlink_handler', methods=['POST'])
def clearlink_handler():
    db = get_db()
    # Update choices to set linked situations to null
    db.execute('UPDATE choices SET linked_situation1 = NULL , linked_situation2 = NULL where id = ?',
               [request.form['id']])
    db.commit()
    game_id = request.form['game_id']
    return redirect(url_for("create_page", game_id=game_id))
    # Function that clears linked situations for a choice


if __name__ == '__main__':
    app.run()
