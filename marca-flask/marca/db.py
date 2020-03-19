"""Sets up connection to database"""

import sqlite3

import click # Click is a simple Python module inspired by the stdlib optparse to make writing command line scripts fun.
from flask import current_app, g
'''current_app is a special object that points to the Flask application handling the request.
g is a special object that is unique for each request.
It is used to store data that might be accessed by multiplefunctions during the request.
'''
from flask.cli import with_appcontext # Wraps a callback so that it's guaranteed to be executed with the script's application context


def get_db():
    '''get_db will be called when the application has been created and is handling a request,
    so current_app can be used
    '''
    if 'db' not in g:
        #: Establish a connection to the file pointed at by the DATABASE configuration key
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        #: Tell the connection to return rows that behave like dicts. This allows accessing the columns by name.
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    '''Checks if a connection was created by checking if g.db was set.
    If the connection exists, it is closed.
    Later we will tell the application about the close_db function in the application factory
    so that it is called after each request.
    '''
    db = g.pop('db', None)

    if db is not None:
        db.close()

