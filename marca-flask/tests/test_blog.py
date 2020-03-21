import pytest
from marca.db import get_db

# HTML status code
htmlStatus_Forbidden = 403
htmlStatus_NotFound = 404
htmlStatus_OK = 200

correctLoginURL = 'http://localhost/auth/login'
correctIndexURL = 'http://localhost/'
noValue = ''

# Database table
blogPostTableName = 'post'



def test_index(client, auth):
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on ' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data

    '''A user must be logged in to access the create, update, and delete views.
    The logged in user must be the author of the post to access update and 
    delete, otherwise a 403 Forbidden status is returned. If a post with the 
    given id doesn’t exist, update and delete should return 404 Not Found.
    '''


@pytest.mark.parametrize('path', (
'/create',
'/1/update',
'/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == correctLoginURL


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        imposterAuthorID = 2
        firstBlogPostID = 1
        db = get_db()
        db.execute(
            f'UPDATE post SET author_id = {imposterAuthorID}'
            f' WHERE id = {firstBlogPostID}'
        )
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post('/1/update').status_code == htmlStatus_Forbidden
    assert client.post('/1/delete').status_code == htmlStatus_Forbidden
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == htmlStatus_NotFound

    
    
'''The create and update views should render and return a 200 OK status for
a GET request. 
When valid data is sent in a POST request, create should insert the new post 
data into the database, and update should modify the existing data. 
Both pages should show an error message on invalid data.
'''


def test_create(client, auth, app):
    correctNumberOfBlogPosts = 2
    
    auth.login()
    assert client.get('/create').status_code == htmlStatus_OK
    client.post('/create', data={'title': 'created', 'body': ''})

    with app.app_context():
        db = get_db()
        count = db.execute(
            f'SELECT COUNT(id) FROM {blogPostTableName}'
        ).fetchone()[0]
        assert count == correctNumberOfBlogPosts


def test_update(client, auth, app):
    updatedTitle = 'updated'
    auth.login()
    assert client.get('/1/update').status_code == htmlStatus_OK
    client.post('/1/update', data={'title': updatedTitle, 'body': noValue})

    with app.app_context():
        db = get_db()
        post = db.execute(
            f'SELECT * FROM {blogPostTableName} WHERE id = 1'
        ).fetchone()
        assert post['title'] == updatedTitle


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': noValue, 'body': noValue})
    assert b'Title is required.' in response.data
    
    
'''The delete view should redirect to the index URL and the post should 
no longer exist in the database.
'''


def test_delete(client, auth, app):
    blogPostIDtoDelete = 1
    
    auth.login()
    response = client.post(f'/{blogPostIDtoDelete}/delete')
    assert response.headers['Location'] == correctIndexURL

    with app.app_context():
        db = get_db()
        post = db.execute(
            f'SELECT * FROM {blogPostTableName}'
            f' WHERE id = {blogPostIDtoDelete}'
        ).fetchone()
        assert post is None
        
        