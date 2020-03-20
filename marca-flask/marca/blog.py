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


@bp.route('/create', methods=(GET, POST))
@login_required
def create():
    # only if a new blog entry is submitted
    if request.method == POST:
        title = request.form['title']
        body = request.form['body']
        error = None

        # set error if title field is empty
        if not title:
            error = noTitleError

        if error is not None:
            #: make the error available to display in HTML
            flash(error)
        else: # no errors, all is well
            db = get_db()
            try:
                userID = g.user['id']
                print("got userID:", userID)
                q = f'''INSERT INTO {blogPostTable} (title, body, author_id) VALUES ('{title}', '{body}', '{userID}')'''
                print('trying to execute:\n',q)
                db.execute(q)
                print('SUCCESS!')
            except Exception as e:
                print("Excepted: ", e)
                db.execute(
                f'INSERT INTO {blogPostTable} (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            #: go back to index after create
            return redirect(url_for('blog.index'))

    # only if there is no new blog entry submitted
    return render_template('blog/create.html')


'''=======================UPDATE/DELETE BLOG POST VIEWS======================'''

def get_post(id, check_author=True):
    '''Returns a blog post from database, searching by post ID
    This method is used by update view and delete view
    '''
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        f' FROM {blogPostTable} p JOIN {userTable} u'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    # Post not found
    if post is None:
        abort(http_notFound, f"Post id {id} doesn't exist")

    try:
        # User is not the author
        if check_author and post['author_id'] != g.user['id']:
            abort(http_forbidden)
    except Exception as e:
        print(f'''Error - {e}
        post keys = {post.keys()}
        g.user keys = {g.user.keys()}''')
        abort(http_forbidden)

    return post


'''==========UPDATE VIEW=========='''

# Error messages



@bp.route('/<int:id>/update', methods=(GET, POST))
@login_required
def update(id):
    post = get_post(id)

    # if there is something to sumbmit (POST data)
    if request.method == POST:
        title = request.form['title']
        body = request.form['body']
        error = None

        # set error if title field is empty
        if not title:
            error = noTitleError

        if error is not None:
            #: make the error available to display in HTML
            flash(error)
        else: # no errors, update the blog post in database
            db = get_db()
            db.execute(
                f'UPDATE {blogPostTable} SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db. commit()
            #: go back to index after update
            return redirect(url_for('blog.index'))

    # only gets here if there is an error
    # assert error is not None # TODO review this assertion
    return render_template('blog/update.html', post=post)

'''==========DELETE VIEW=========='''

@bp.route('/<int:id>/delete', methods=(POST,))
@login_required
def delete(id):
    '''Deletes a post with the id provided'''
    get_post(id)
    db = get_db()
    db.execute(f'DELETE from {blogPostTable} WHERE id = ?', (id,))
    db.commit()
    # after deleting, return to blog index
    return redirect(url_for('blog.index'))

