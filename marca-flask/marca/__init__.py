import os

from flask import Flask
#from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
# DB credentials
try:
    print('trying: `from marca.myDBConnect import host, user, pw, schema`')
    from marca.myDBConnect import host, user, pw, schema
    print('success __init__.py 1')
except Exception as e:
    print(f'''{e}
        error in `from marca.myDBConnect import host, user, pw, schema`
        trying: from myDBConnect import host, user, pw, schema''')
    try:
        from myDBConnect import host, user, pw, schema
        print('success __init__.py 2')
    except Exception as e:
        print(f'''Nope, still... {e}''')

import logging as log
log.basicConfig(filename='marcaBP.log', level=log.DEBUG, format='%(asctime)s %(message)s')
log.info('''




=======================



Starting __init__.py
''')


def logAppDetails(appp):
    logmessage=(f'''

    DEFAULTS : CURRENT SETTING
        #app.import_name : {appp.import_name}
        #app.static_url_path=None : {appp.static_url_path}
        #app.static_folder='static' : {appp.static_folder}
        #app.subdomain_matching=False : {appp.subdomain_matching}
        #app.template_folder='templates' : {appp.template_folder}
        #app.instance_path=None : {appp.instance_path}
        #app.root_path=None : {appp.root_path}''')

    try:
        deet = appp.instance_relative_config
    except Exception as e:
        deet = e
    logmessage += f'''
        #app.instance_relative_config=False : {deet}'''


    try:
        deet = appp.static_host
    except Exception as e:
        deet = e
    logmessage += f'''
        #app.static_host=None : {deet}'''


    try:
        deet = appp.host_matching
    except Exception as e:
        deet = e
    logmessage += f'''
        #app.host_matching=False : {deet}

        '''


    log.info(logmessage)


def create_app(test_config=None):
    path = os.path
    #: create and configure the app
    app1 = Flask(__name__)

    app = Flask(import_name=__name__, static_url_path='/~pthompso/MARCA-Reading-Aide/marca-flask/marca/static', static_host=None, host_matching=False, subdomain_matching=True, template_folder="templates", instance_path=None, instance_relative_config=True, root_path=None)

    testApp = Flask(import_name=__name__,
                static_url_path='/~pthompso/MARCA-Reading-Aide/marca-flask/marca/static',
                static_folder='static',
                static_host=None,
                host_matching=False,
                subdomain_matching=False,
                #subdomain_matching=True,
                template_folder='templates',

                #instance_path=None,
                instance_path = '/home/pthompso/public_html/MARCA-Reading-Aide/marca-flask/instance',
                #instance_relative_config=False,
                instance_relative_config=True,
                root_path=None)
    #testApp.config['SERVER_NAME'] = 'cs.unca.edu/~pthompso'
    #testApp.config['SERVER_NAME'] = 'cs.unca.edu'
    #testApp.config['SERVER_NAME'] = '0.0.0.0'

    #app = testApp

    #: set some default configuration that the app will use
    print('trying to     app.config.from_mapping')
    app.config.from_mapping(
        SECRET_KEY='dev', #TODO set to a random value when deploying
        MYSQL_HOST = host,
        MYSQL_USER = user,
        MYSQL_PASSWORD = pw,
        MYSQL_DB = schema,
        MYSQL_CURSORCLASS = 'DictCursor'
    )
    app.config.from_mapping(
        SECRET_KEY='dev', #TODO set to a random value when deploying
        MYSQL_DATABASE_HOST = host,
        MYSQL_DATABASE_USER = user,
        MYSQL_DATABASE_PASSWORD = pw,
        MYSQL_DATABASE_DB = schema,
        MYSQL_DATABASE_CURSORCLASS = 'DictCursor' #prob not necessary
    )
    #mysql = MySQL(app)
    mysql = MySQL(app, cursorclass=DictCursor)
    app.config.from_mapping(DATABASE = mysql) # yep
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
    #app.register_blueprint(auth.bp, url_prefix='/~pthompso')
    '''Blueprint imported and registered from auth.py using
    app.register_blueprint().
    '''

    #from . import blog
    #app.register_blueprint(blog.bp)
    ##: this has no url_prefix because we want it to be the index
    #app.add_url_rule('/', endpoint='index')


    '''Now registering marca Blueprint'''
    #import logging as log
    #log.basicConfig(filename='marcaBP.log', level=log.DEBUG, format='%(asctime)s %(message)s')
    #log.info('Now registering marca Blueprint')
    from . import marcaBP
    app.register_blueprint(marcaBP.bp)
    #: this has no url_prefix because we want it to be the index
    app.add_url_rule('/', endpoint='index')


    #log.info(app1.config)
    #logAppDetails(app1)
    log.info(app.config)
    logAppDetails(app)

    return app

if __name__ == '__main__':
    app = create_app()
    #stopHere=True

