"""Sets up connection to database"""

import sqlite3

import click # Click is a simple Python module inspired by the stdlib optparse to make writing command line scripts fun.
from flask import current_app, g
'''current_app is a special object that points to the Flask application handling the request.
g is a special object that is unique for each request.
It is used to store data that might be accessed by multiplefunctions during the request.
'''
from flask.cli import with_appcontext
'''with_appcontextWraps a callback so that it's guaranteed to be executed
with the script's application context
'''


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


def init_db(schemaFile='schema.sql'):
    db = get_db() # returns a database connection

    # open_resource opens a file relative to the marca package
    with current_app.open_resource(schemaFile) as f:
        db.executescript(f.read().decode('utf8'))


# defines a command line command called init-db that calls the init_db function and shows a success message to the user
@click.command('init-db')
@with_appcontext
def init_db_command():
    '''Clear the existing data and create new tables'''
    init_db()
    click.echo('Initialized the database')


def init_app(app):
    '''Imported and called from the factory in __init__.py'''

    #: Tell Flask to call close_db function when cleaning up after returning the response
    app.teardown_appcontext(close_db)
    #: Add a new command that can be called with the flask command
    app.cli.add_command(init_db_command)

