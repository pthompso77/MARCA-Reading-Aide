import pytest
from flask import g, session
from marca.db import get_db

#HTML status code
htmlStatus_OK = 200

correctLoginURL = 'http://localhost/auth/login'
correctIndexURL = 'http://localhost/'
dummyUsername = dummyPassword = 'a'
authActions_uname = 'test'
noValue = ''


'''=======================REGISTER TESTS======================='''
def test_register(client, app):
    assert client.get('/auth/register').status_code == htmlStatus_OK
    response = client.post(
        '/auth/register', data={'username': dummyUsername, 'password': dummyPassword}
    )    
    assert response.headers['Location'] == correctLoginURL

    with app.app_context():
        cur = get_db().connect().cursor()
        assert cur.execute(
            f"select * from userAccounts where email = '{dummyUsername}'",
        ).fetchone() is not None
        
        
# This tells Pytest to run the same test function with different arguments. 
@pytest.mark.parametrize(('username', 'password', 'message'), (
    (noValue, noValue, b'Username is required.'),
    (dummyUsername, noValue, b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    # ensure the desired message is in the response
    assert message in response.data


'''=======================LOGIN TESTS======================='''

def test_login(client, auth):
    '''auth is the AuthActions object defined in conftest.py
    '''
    assert client.get('/auth/login').status_code == htmlStatus_OK
    response = auth.login()
    assert response.headers['Location'] == correctIndexURL

    with client:
        '''Using client in a `with` block allows accessing context variables 
        such as session after the response is returned. Normally, accessing
        session outside of a request would raise an error.
        '''
        firstUserIDinDatabase = 1
        client.get('/')
        assert session['user_id'] == firstUserIDinDatabase
        assert g.user['username'] == authActions_uname
    

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    # ensure the desired message is in the response
    assert message in response.data

    
'''=======================LOGOUT TESTS======================='''

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session

