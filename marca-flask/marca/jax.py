"""
Blueprint for AJAX requests via SijaxHandler
"""

import logging as log
log.basicConfig(filename='jax.log', level=log.DEBUG, format='%(asctime)s %(message)s')

log.info(f'''
starting jax
''')

from marca.text_tools.FullText import FullText, Highlight, TEST_TEXT
log.info(f'''success in jax.py:create_app() 1''')

from flask import Blueprint, flash, g, session # redirect, render_template, request, url_for
from flask import current_app
from flask.cli import with_appcontext

from werkzeug.exceptions import abort
import flask_sijax
from marca.SijaxHandler import SijaxHandler


try:
    from auth import login_required
    from db import get_db, escape
except:
    try:
        from marca.auth import login_required
        from marca.db import get_db
    except Exception as e:
        log.error("Error importing login_required or get_db:", e)


#: Initialize Blueprint
log.info('Initializing Blueprint in jax.py')
bp = Blueprint('jax', __name__)



#@flask_sijax.route(bp, "/jax")
#@login_required
@bp.route('/jax', methods=('POST',))
def jax():
    if g.sijax.is_sijax_request:
        g.sijax.register_object(SijaxHandler)
        return g.sijax.process_request()

    return str(g.user['userID'])