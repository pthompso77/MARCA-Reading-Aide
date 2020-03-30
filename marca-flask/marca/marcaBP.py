"""
Main page for Marca app (index)
"""

import logging as log
log.basicConfig(filename='marcaBP.log', level=log.DEBUG, format='%(asctime)s %(message)s')
log.info('Starting marcaBP.py')


log.info('Starting imports in marcaBP.py')
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)
from werkzeug.exceptions import abort
'''example:
abort(404)  # 404 Not Found
abort(Response('Hello World'))
'''

log.info('Starting importing auth.login_required and db.get_db in marcaBP.py')
try:
    from auth import login_required
    from db import get_db
except:
    try:
        from marca.auth import login_required
        from marca.db import get_db
    except Exception as e:
        log.error("Error importing login_required or get_db:", e)


#: Initialize Blueprint
log.info('Initializing Blueprint in marcaBP.py')
bp = Blueprint('marcaBP', __name__)


'''=======================Variables======================='''

# HTTP request methods
GET = 'GET'
POST = 'POST'
# HTTP codes
http_notFound = 404
http_forbidden = 403


'''=============================INDEX VIEW============================='''

# Database table names
fullTextTable = 'FullText'
userTable = 'userAccounts'


@bp.route('/')
def index():
    log.info('Starting def index()')
    #db = get_db().connect()
    #cur = db.cursor()

    # TODO -

    log.info('Finished def index()')
    return render_template('summary/index.html')


'''=============================DASHBOARD VIEW============================='''


#@bp.route(rule)


'''=======================Actions======================='''

# TODO
@bp.route('/submitText', methods=(POST,))
def submitText():
    log.info('Starting submitText() in marcaBP.py')
    '''takes submitted text
    returns a summary
    form id="text-form"
    '''
    # TODO
    log.info('Finished submitText() in marcaBP.py')
    return('TODO')




