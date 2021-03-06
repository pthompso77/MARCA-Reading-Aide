"""
This creates a Blueprint named 'auth'.
Like the application object, the blueprint needs to know where it’s defined,
  so __name__ is passed as the second argument.
The url_prefix will be prepended to all the URLs associated with the blueprint.
"""

import logging as log
log.basicConfig(filename='auth.log', level=log.DEBUG, format='%(asctime)s %(message)s')


import functools # Tools for working with functions and callable objects
from flask import g
'''Whenever something is bound to g.user / g.request the proxy objects
will forward all operations.
If no object is bound a :exc:`RuntimeError` will be raised.
'''
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
try:
    from marca.db import get_db
except Exception as e:
    log.info("Exception: ",e)
    try:
        from db import get_db
    except Exception as e:
        log.info("Exception in auth.py:", e)


'''Log File'''
import logging as log
log.basicConfig(filename='auth.log', level=log.DEBUG, format='%(asctime)s %(message)s')
log.info('Starting auth.py')


bp = Blueprint('auth', __name__, url_prefix='/auth')
#bp = Blueprint('auth', __name__, url_prefix = '/~pthompso/MARCA-Reading-Aide/marca-flask/marca.cgi/auth')

'''Blueprint is imported and registered from the factory
using app.register_blueprint().

Represents a blueprint, a collection of routes and other app-related
functions that can be registered on a real application later.

A blueprint is an object that allows defining application functions without
requiring an application object ahead of time. It uses the same decorators
as :class:`~flask.Flask`, but defers the need for an application by
recording them for later registration.

Decorating a function with a blueprint creates a deferred function that is
called with :class:`~flask.blueprints.BlueprintSetupState` when the
blueprint is registered on an application.
'''


@bp.route('/logout')
def logout():
    '''Logs the user out (clears the session)
    and returns to index page
    '''
    session.clear()
    return redirect(url_for('index'))


'''=======================Register and Login variables======================='''

# HTTP request methods
GET = 'GET'
POST = 'POST'

# HTML form input names and errors
uname = 'username'
uname_empty_err = 'Username is required.'
uname_wrong_err = 'Incorrect username.'
pw = 'password'
pw_empty_err = 'Password is required.'
pw_wrong_err = "Incorrect password."

# Database table names
userTable = 'userAccounts'


# SQL dictionary associated with HTML form input names
SQLdict = {
    'TODO':'maybe'
    }


'''=========================The First View: Register========================='''

@bp.route('/register', methods=(GET, POST))
def register():
    onSuccess_redirectTo = 'marcaBP.dashboard'
    if request.method == POST:
        username = request.form[uname]
        password = request.form[pw]
        db = get_db().connect()
        cur = db.cursor()
        error = None

        if not username:
            error = uname_empty_err
        elif not password:
            error = pw_empty_err
        elif cur.execute(f'''SELECT userID FROM {userTable}
            WHERE email = "{username}"'''
            ) > 0:
            error = f'User {username} is already registered.'

        if error is None:
            cur.execute(
                f'''INSERT INTO {userTable} (email, password)
                VALUES ("{username}", "{generate_password_hash(password)}")'''
            )
            db.commit()

            #: get the new userID from DB
            q = f'''SELECT * FROM {userTable} WHERE email = "{username}"'''
            cur.execute(q)
            user = cur.fetchone()

            #: set the session
            session.clear()
            #from flask import make_response
            #resp = make_response(render_template(...))
            #resp.set_cookie('username', 'the username')
            try:
                flash(f'''looked for user {user}''')
                session['user_id'] = user['userID']
                flash(f'''now session['user_id'] is {session['user_id']}''')
            except Exception as e:
                log.info(f'''(failed in /register: Exception={e}) trying session['user_id'] = user['userID']''')
                session['user_id'] = user['userID']
                log.info('''(success)''')
            '''session is a dict that stores data across requests.'''
            log.info(f'''
            We good here? error = {error}''')

            return redirect(url_for(onSuccess_redirectTo))

        flash(error)

    return render_template('auth/register.html')

'''=========================The Second View: Login========================='''

@bp.route('/login', methods=(GET, POST))
def login():
    log.info('Starting login()')
    onSuccess_redirectTo = 'marcaBP.dashboard'


    if request.method == POST:
        log.info(f'''   GOT POST request:
            {request}
            {request.form}''')
        username = request.form[uname]
        password = request.form[pw]
        db = get_db()
        error = None
        #: get user from database
#        user = db.execute(
#            f'SELECT * FROM {userTable} WHERE email = ?', (username,)
#        ).fetchone()
        db = get_db().connect()
        cur = db.cursor()
        q = f'''SELECT * FROM {userTable} WHERE email = "{username}"'''

        cur.execute(q)
        user = cur.fetchone()

        # test
        log.info(f'''
            SUCCESS in @route /login
            with query: {q}
            got user: {user}''')
        # done test

        if user is None:
            error = uname_wrong_err
            log.error('''   Error in auth.py
            user is None''')
        elif not check_password_hash(user['password'], password):
            error = pw_wrong_err

        if error is None:
            # things are good, user checks out
            session.clear()
            #: set the session
            try:
                log.info('''trying session['user_id'] = user['id']''')
                session['user_id'] = user['userID']
                log.info('''(success)''')
            #except:
            except Exception as e:
                log.info(f'''(failed in /login: Exception={e}) trying session['user_id'] = user['userID']''')
                session['user_id'] = user['userID']
                log.info('''(success)''')
            '''session is a dict that stores data across requests.'''
            log.info(f'''
            We good here? error = {error}''')
            return redirect(url_for(onSuccess_redirectTo))

        flash(error)

    return render_template('auth/login.html')


def login_required(view):
    '''This decorator returns a new view function that wraps the original
    view it’s applied to.
    The new function checks if a user is loaded and redirects to the login
    page otherwise.
    If a user is loaded the original view is called and continues normally.
    '''
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('Sorry, you need to be logged in.')
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


# before_app_request is executed before each request, even if outside of a blueprint
@bp.before_app_request
def load_logged_in_user():
    '''bp.before_app_request() registers a function that runs before the view
    function, no matter what URL is requested.

    load_logged_in_user checks if a user id is stored in the session and gets
    that user’s data from the database, storing it on g.user, which lasts for
    the length of the request. If there is no user id, or if the id doesn’t
    exist, g.user will be None.
    '''
    try:
        logClientRequest()
    except:
        log.info('some problem in trying logClientRequest')

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        #new
        db = get_db().connect()
        cur = db.cursor()
        cur.execute(
            f'SELECT * FROM {userTable} WHERE userID = {user_id}'
        )
        db.commit()
        g.user = cur.fetchone()
        #log.info(f'''GOT user = {g.user}''')

    return


def logClientRequest():
    try:
        logformat = log.Formatter('%(asctime)s %(message)s')
    except Exception as e:
        log.info(f'some problem in logClientRequest1: {e}')
        return

    try:
        handler = log.FileHandler('request_activity.log')
        handler.setFormatter(logformat)
        requestLog = log.getLogger('request_activity')
        requestLog.addHandler(handler)
    except Exception as e:
        log.info(f'''some problem in logClientRequest2: {e}''')
        return



    from os import environ
    client = ""
    try:
        #client = environ['REMOTE_HOST']
        client = environ['REMOTE_ADDR']
    except Exception as e:
        client = f"? {e}"
    try:
        requestLog.info(f'''request from IP: {client}''')
    except Exception as e:
        log.info(f'''some problem in logClientRequest3: {e}''')

