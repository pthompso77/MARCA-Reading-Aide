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

'''=======================Index variables======================='''

# HTTP request methods
GET = 'GET'
POST = 'POST'
# HTTP codes
http_notFound = 404
http_forbidden = 403


'''=============================INDEX VIEW============================='''

# Database table names
blogPostTable = 'post'
userTable = 'user'


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        f' FROM {blogPostTable} p JOIN {userTable} u on p.author_id = u.id'
        ' ORDER by created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


'''=============================CREATE BLOG POST VIEW========================'''

# Error messages
noTitleError = 'Title is required'


@bp.route('/create', methods=[GET, POST])
@login_required
def create():
    # only if a new blog entry is submitted
    if request.method == POST:
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = noTitleError

        if error is not None:
            #: make the error available to display
            flash(error)
        else: # no errors, all is well
            db = get_db()
            db.execute(
                f'INSERT INTO {blogPostTable} (title, body, author_id'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    # only if there is no new blog entry submitted
    return render_template('blog/create.html')


'''=============================UPDATE BLOG POST VIEW========================'''

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        f' FROM {blogPostTable} p JOIN {userTable} u'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    # Post not found
    if post is None:
        abort(http_notFound, f"Post id {id} doesn't exist")

    # User is not the author
    if check_author and post['author-id'] != g.user['id']:
        abort(http_forbidden)

    return post

