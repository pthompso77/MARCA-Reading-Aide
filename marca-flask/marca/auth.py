"""
This creates a Blueprint named 'auth'.
Like the application object, the blueprint needs to know where it’s defined,
  so __name__ is passed as the second argument.
The url_prefix will be prepended to all the URLs associated with the blueprint.
"""

import functools # Tools for working with functions and callable objects
from flask import (
    Blueprint,
    flash,
    g,
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

Represents a blueprint, a collection of routes and other app-related functions
that can be registered on a real application later.

A blueprint is an object that allows defining application functions without
requiring an application object ahead of time. It uses the same decorators
as :class:`~flask.Flask`, but defers the need for an application by recording
them for later registration.

Decorating a function with a blueprint creates a deferred function that is
called with :class:`~flask.blueprints.BlueprintSetupState` when the blueprint
is registered on an application.
'''


'''=========================The First View: Register========================='''

# HTTP request methods
GET = 'GET'
POST = 'POST'

# HTML form input names and errors
uname = 'username'
uname_empty_err = 'Username is required.'
pw = 'password'
pw_empty_err = 'Password is required.'

# Database table names
userTable = 'user'


# SQL dictionary associated with HTML form input names
SQLdict = {
    'TODO':'maybe'
    }


@bp.route('/register', methods=['GET', 'POST'])
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

