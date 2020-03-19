"""
Define the blueprint and register it in the application factory.

Later, define the `index` view
"""

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
'''
If a status code is given, it will be looked up in the list of exceptions and
will raise that exception.
If passed a WSGI application, it will wrap it in a proxy WSGI exception and
raise that:

example:

abort(404)  # 404 Not Found
abort(Response('Hello World'))
'''
try:
    from auth import login_required
    from db import get_db
except:
    try:
        from marca.auth import login_required
        from marca.db import get_db
    except Exception as e:
        print("Error importing login_required or get_db:", e)

bp = Blueprint('blog', __name__)


'''=============================INDEX VIEW============================='''

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u on p.author_id = u.id'
        ' ORDER by created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

