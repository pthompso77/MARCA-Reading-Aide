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
'''Blueprint is imported and registered from the factory using app.register_blueprint().

Represents a blueprint, a collection of routes and other app-related functions that can be registered on a real application later.

A blueprint is an object that allows defining application functions without requiring an application object ahead of time. It uses the same decorators as :class:`~flask.Flask`, but defers the need for an application by recording them for later registration.

Decorating a function with a blueprint creates a deferred function that is called with :class:`~flask.blueprints.BlueprintSetupState` when the blueprint is registered on an application.
'''

