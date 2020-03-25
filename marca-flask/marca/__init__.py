import os

from flask import Flask
from flask_mysqldb import MySQL
# DB credentials
try:
    print('trying: `myDBConnect import host, user, pw, schema`')
    from myDBConnect import host, user, pw, schema
    print('success __init__.py 1')
except Exception as e:
    print(f'''{e} 
        error in "from myDBConnect import host, user, pw, schema"
        trying: from marca.myDBConnect import host, user, pw, schema''')
    try:
        from marca.myDBConnect import host, user, pw, schema
        print('success __init__.py 2')
    except Exception as e:
        print(f'''Nope, still... {e}''')


def create_app(test_config=None):
    #: create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    mysql = MySQL(app)
    #: set some default configuration that the app will use
    print('trying to     app.config.from_mapping')
    app.config.from_mapping(
        SECRET_KEY='dev', #TODO set to a random value when deploying
        MYSQL_HOST = host, 
        MYSQL_USER = user, 
        MYSQL_PASSWORD = pw, 
        MYSQL_DB = schema
    )
    print('success in __init__.py:create_app()')

    if test_config is None: # overrides the default configuration
        #: load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else: #tests can be configured independently of any development values
        #: load the test config if supplied above
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page to say Helloooo!
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)
    '''adds teardown_appcontext
    and new flask command `init-db` which calls db's init_db_command()
    '''

    from . import auth
    app.register_blueprint(auth.bp)
    '''Blueprint imported and registered from auth.py using
    app.register_blueprint().
    '''
    from . import blog
    app.register_blueprint(blog.bp)
    #: this has no url_prefix because we want it to be the index
    app.add_url_rule('/', endpoint='index')

    return app

