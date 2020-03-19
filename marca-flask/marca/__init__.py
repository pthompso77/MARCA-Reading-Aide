import os

from flask import Flask


def create_app(test_config=None):
    #: create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    #: set some default configuration that the app will use
    app.config.from_mapping(
        SECRET_KEY='dev', #TODO set to a random value when deploying
        DATABASE = os.path.join(app.instance_path, 'marca.sqlite'),
    )

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
        whom = 'Wooorld'
        return f'Helloooo {whom}!'

    from . import db
    db.init_app(app)
    '''adds teardown_appcontext
    and new flask command `init_db_command`
    '''

    return app

