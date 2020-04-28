import traceback
import os, sys
import logging as log
log.basicConfig(filename='marcaBP.log', level=log.DEBUG, format='%(asctime)s %(message)s')
log.info('''


=======================

Starting __init__.py

''')
from flask import Flask, request, session, g, abort, render_template
#from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
import flask_sijax
import hmac
from hashlib import sha1
from werkzeug.security import safe_str_cmp
try:
    from marca.SijaxHandler import SijaxHandler
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print(f'''Exception importing marca.SijaxHandler: {e}
          with traceback: {traceback.print_tb(exc_traceback)}''')
# DB credentials
from pymysql.cursors import DictCursor

try:
    from marca.myDBConnect import host, user, pw, schema
except Exception as e:
    log.info(f'''{e}
             error in `from marca.myDBConnect import host, user, pw, schema`
             trying: from myDBConnect import host, user, pw, schema''')
    try:
        from myDBConnect import host, user, pw, schema
    except Exception as e:
        log.info(f'''Nope38, still... {e}''')




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

    app = Flask(import_name=__name__,
                static_url_path= '/~pthompso/MARCA-Reading-Aide/marca-flask/marca/static',
                static_host=None, host_matching=False, subdomain_matching=True,
                template_folder="templates", instance_path=None,
                instance_relative_config=True, root_path=None)



    #: set some default configuration that the app will use
    #app.config.from_mapping(
        #SECRET_KEY='dev', #TODO set to a random value when deploying
        #MYSQL_HOST = host,
        #MYSQL_USER = user,
        #MYSQL_PASSWORD = pw,
        #MYSQL_DB = schema,
        #MYSQL_CURSORCLASS = 'DictCursor'
    #)
    app.config.from_mapping(
        SECRET_KEY= os.urandom(128),#'dev',
        MYSQL_DATABASE_HOST = host,
        MYSQL_DATABASE_USER = user,
        MYSQL_DATABASE_PASSWORD = pw,
        MYSQL_DATABASE_DB = schema,
        MYSQL_DATABASE_CURSORCLASS = 'DictCursor'#,
        #SESSION_COOKIE_HTTPONLY = false
    )

    #'''Added 2020-04-12'''
    # .htaccess redirect to "MARCA-Reading-Aide/marca-flask/marca.cgi/$1" [L]
    #app.config.from_mapping(APPLICATION_ROOT = '/MARCA-Reading-Aide/marca-flask')


    #mysql = MySQL(app)
    mysql = MySQL(app, cursorclass=DictCursor)
    app.config.from_mapping(DATABASE = mysql) # yep


    # Sijax
    flask_sijax.Sijax(app)
    app.config["SIJAX_STATIC_PATH"] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
    app.config["SIJAX_JSON_URI"] = os.path.join('.', os.path.dirname(__file__), '/static/js/sijax/json2.js')
    #print(f'app.config["SIJAX_STATIC_PATH"]{app.config["SIJAX_STATIC_PATH"]}')

    if test_config is None: # overrides the default configuration
        pass
        #: load the instance config, if it exists, when not testing
        #app.config.from_pyfile('config.py', silent=True)
    else: #tests can be configured independently of any development values
        #: load the test config if supplied above
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    #@flask_sijax.route(app, "/hello")
    ##@app.route('/hello')
    #def hello():
        #if g.sijax.is_sijax_request:
            #g.sijax.register_object(SijaxHandler)
            #return g.sijax.process_request()

        #return render_template('chat.html')
        ##return 'Hello, World!'

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


    try:
        from . import jax
    except Exception as e:
        log.exception(f'''Exception in importing jax from __init__
                      e: {e}''')
    app.register_blueprint(jax.bp)




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


    log.info(app.config)
    logAppDetails(app)






    '''TODO address this (uncomment?)'''
    @app.template_global('csrf_token')
    def csrf_token():
        """
        Generate a token string from bytes arrays. The token in the session is user
        specific.
        """
        if "_csrf_token" not in session:
            session["_csrf_token"] = os.urandom(128)
        return hmac.new(app.secret_key, session["_csrf_token"],
                        digestmod=sha1).hexdigest()


    '''TODO address this'''
    #@app.before_request
    def check_csrf_token():
        """Checks that token is correct, aborting if not"""
        if request.method in ("GET",): # not exhaustive list
            return
        token = request.form.get("csrf_token")
        if token is None:
            app.logger.warning("Expected CSRF Token: not present")
            abort(400)
        if not safe_str_cmp(token, csrf_token()):
            app.logger.warning("CSRF Token incorrect")
            abort(400)


    return app

def get_db(app):
    return MySQL(app, cursorclass=DictCursor)


def runAndGetApp():
    from wsgiref.handlers import CGIHandler
    app = create_app()
    app = create_app()
    app.config['DEBUG']=True
    app.config['TESTING']=True
    CGIHandler().run(app)
    return app


app = create_app()

if __name__ == '__main__':
    app = runAndGetApp()
    #stopHere=True

