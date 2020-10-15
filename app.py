# -*- coding: utf-8 -*-
import os
from sqlite3 import dbapi2 as sqlite3

import werkzeug
from flask import Flask, request, g, redirect, url_for, render_template, flash, session


app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'account.db'),
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('ACCOUNT_SETTINGS', silent=True)


username = ''


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
    global username
    if username != "":
        return render_template('Home.html', User=username) # If user is logged in, display "welcome (username)"
    else:
        return render_template('Home.html', User="User")  # Else display "welcome user"

# Renders homepage


@app.route('/account')
def account_page():
    return render_template('create_account.html')


@app.route('/create_account', methods=["POST"])
def create_account():
    db = get_db()
    entered_username = request.form['username']
    password = werkzeug.security.generate_password_hash(request.form['password'])
    choices = {}
    # Search for entered username in the database
    cur = db.execute('SELECT username FROM accounts where username = ?', [entered_username])
    user_list = cur.fetchall()
    # If username is not already taken, create account and return homepage
    if not user_list:
        db.execute('INSERT INTO accounts (username, password, choices) VALUES (?, ?, ?)',
                   [entered_username, password, str(choices)])
        db.commit()
        return redirect(url_for('homepage'))
    # If username is taken, flash a message and return the account creation page
    else:
        flash('Username is already taken')
        return redirect(url_for('account_page'))


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/process_login', methods=['POST'])
def login_handler():
    entered_username = request.form['username']
    password = request.form['password']
    db = get_db()
    cur = db.execute('SELECT username FROM accounts where username = ?', [entered_username])
    user_list = cur.fetchall()
    if not user_list:
        error = 'Invalid Username'
    else:
        cur = db.execute('SELECT password FROM accounts where username = ?', [entered_username])
        pass_hashed = cur.fetchone()
        if not werkzeug.security.check_password_hash(pass_hashed[0], password):
            error = 'Invalid Password'
        else:
            global username
            username = entered_username
            session[username] = True
            flash('You were logged in')
            return redirect(url_for('homepage'))
    flash(error)
    return redirect(url_for('login_page'))


@app.route('/process_logout')
def logout_handler():
    global username
    session.pop(username, None)
    username = ''
    flash('You were logged out')
    return redirect(url_for('homepage'))


@app.route('/create_game')
def create_page():
    return render_template('create_game.html')
# Renders page for game creation


@app.route('/process_handler', methods=['POST'])
def create_handler():
    global username
    db = get_db()
    cur = db.execute('SELECT choices FROM accounts where username = ?', [username])
    current_list = cur.fetchone()[0]
    current_list = eval(current_list)
    current_list[request.form['Situation']] = [request.form['ChoiceOne'], request.form['ChoiceTwo']]
    db.execute('UPDATE accounts set choices = ? where username = ?',
               [str(current_list), username])
    db.commit()
    return redirect(url_for('homepage'))


@app.route('/browse_game')
def browse_game():
    return render_template('browse_game.html')


@app.route('/search_game', methods=['post'])
def search():
    db = get_db()
    search_username = request.form['username']
    cur = db.execute('SELECT username FROM accounts where username = ?', [search_username])
    user_list = cur.fetchall()
    if not user_list:
        flash('No username like this')
        return redirect(url_for('browse_game'))
    else:
        account = user_list
        return render_template('search_game.html', accounts=account)


if __name__ == '__main__':
    app.run()
