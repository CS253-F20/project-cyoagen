# -*- coding: utf-8 -*-
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash


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
    return render_template('Home.html')

@app.route('/account')
def account_page():
    return render_template('create_account.html')

@app.route('/create_account', methods=["POST"])
def create_account():
    db = get_db()
    db.execute('INSERT INTO account (username, password) VALUES (?, ?)',
               [request.form['username'], request.form['password']])
    db.commit()
    flash('Account created!')
    return redirect(url_for('homepage'))

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/process_login')
def login_handler():
    return redirect(url_for('homepage'))

@app.route('/process_logout')
def logout_handler():
    return redirect(url_for('homepage'))

@app.route('/create_game')
def create_page():
    return render_template('create_game.html')


if __name__ == '__main__':
    app.run()
