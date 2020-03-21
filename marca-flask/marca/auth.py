"""
This creates a Blueprint named 'auth'.
Like the application object, the blueprint needs to know where it’s defined,
  so __name__ is passed as the second argument.
The url_prefix will be prepended to all the URLs associated with the blueprint.
"""

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
    from db import get_db
except:
    try:
        from marca.db import get_db
    except Exception as e:
        print("Exception in auth.py:", e)


bp = Blueprint('auth', __name__, url_prefix='/auth')
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
userTable = 'user'

# SQL dictionary associated with HTML form input names
SQLdict = {
    'TODO':'maybe'
    }


'''=========================The First View: Register========================='''

@bp.route('/register', methods=(GET, POST))
def register():
    if request.method == POST:
        username = request.form[uname]
        password = request.form[pw]
        db = get_db()
        error = None

        if not username:
            error = uname_empty_err
        elif not password:
            error = pw_empty_err
        # TODO come back to this... what is this funky thing with the ? in the string???
        elif db.execute(
            f'SELECT id FROM {userTable} WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f'User {username} is already registered.'

        if error is None:
            db.execute(
                f'INSERT INTO {userTable} (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

'''=========================The Second View: Login========================='''

@bp.route('/login', methods=(GET, POST))
def login():
    onSuccess_redirectTo = 'index'

    if request.method == POST:
        username = request.form[uname]
        password = request.form[pw]
        db = get_db()
        error = None
        #: get user from database
        user = db.execute(
            f'SELECT * FROM {userTable} WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = uname_wrong_err
        elif not check_password_hash(user['password'], password):
            error = pw_wrong_err

        if error is None:
            # things are good, user checks out
            session.clear()
            #: set the session
            session['user_id'] = user['id']
            '''session is a dict that stores data across requests.'''
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
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            f'SELECT * FROM {userTable} WHERE id = ?', (user_id,)
        ).fetchone()
