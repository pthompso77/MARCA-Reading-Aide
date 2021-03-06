"""Sets up connection to database"""

#from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
#from mysql import connector
#print('got mysql',connector)

import click # Click is a simple Python module inspired by the stdlib optparse to make writing command line scripts fun.
from flask import current_app, g
'''current_app is a special object that points to the Flask application handling the request.
g is a special object that is unique for each request.
It is used to store data that might be accessed by multiplefunctions during the request.
'''
from flask.cli import with_appcontext
'''with_appcontext Wraps a callback so that it's guaranteed to be executed
with the script's application context
'''


def get_db():
    '''get_db will be called when the application has been created and is handling a request,
    so current_app can be used
    '''
    #with current_app.app_context():
    if 'db' not in g: #yeah
        #: Establish a connection to the file pointed at by the DATABASE configuration key
        try:
            #print('''trying: `g.db = current_app.config['DATABASE']`''')
#            g.db = connect
            #g.db = MySQL(current_app)
            g.db = current_app.config['DATABASE']
                #current_app.config['DATABASE'],
#                detect_types=sqlite3.PARSE_DECLTYPES
#            )
            #print(f'''success with connector?\n\tg.db = {g.db}''')
        except Exception as e:
            print('mysql connector failed... E=',e)
            print('''--------
            trying: g.db = mysql''')
            try:
                print('current_app=',current_app)
                with current_app.app_context():
                    print(current_app.config)
                    g.db = mysql.connect.cursor()
            except Exception as e:
                print('FAILED, e = ',e)
        #: Tell the connection to return rows that behave like dicts. This allows accessing the columns by name.
        # REPLACING: g.db.row_factory = sqlite3.Row
        #print(f'''
        # REPLACING: g.db.row_factory = sqlite3.Row''')
        def make_dicts(cursor, row):
            return dict((cursor.description[idx][0], value)
                       for idx, value in enumerate(row))

        #g.db.row_factory = make_dicts
        #print('success: `g.db.row_factory = make_dicts`')

    return g.db


#def get_db_trying(includeCursor=False):
    #dbConnect = get_db()
    #cursor = dbConnect.cursor()
    #if includeCursor:
        #return dbConnect, cursor
    #else:
        #return dbConnect


def close_db(e=None):
    '''Checks if a connection was created by checking if g.db was set.
    If the connection exists, it is closed.
    Later we will tell the application about the close_db function in the application factory
    so that it is called after each request.
    '''
    db = g.pop('db', None)

    if db is not None:
        try:
            db.close()
        except:
            pass


def init_db(schemaFile='schema.sql'):
    print('''

    -----------
    DO WE EVER GET HERE?
    -----------
    ''')
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


def escape(query):
    #TODO better escapes
    return query
    #return query.replace("'","''")

