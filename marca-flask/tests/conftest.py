import os, sys
verbose = sys.argv[1] == '-v'
import tempfile

import pytest
try:
	from marca import create_app
	print('success marca')
except:
	print('fail marca')
from marca.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')
    

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    '''mkstemp creates and opens a temporary file, returning the file object
	and the path to it.
	The DATABASE path is overridden so it points to this temporary path
	instead of the instance folder.
	After setting the path, the database tables are created and the test data 
	is inserted. 
	After the test is over, the temporary file is closed and removed.
	'''
    app = create_app({
		#: tell Flask that the app is in test mode
        'TESTING': True,
        'DATABASE': db_path,
    })
    
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
        
    yield app
    
    os.close(db_fd)
    os.unlink(path=db_path)

	
    
@pytest.fixture
def client(app):
	'''The client fixture calls app.test_client() with the application object 
	created by the app fixture.
	Tests will use the client to make requests to the application without 
	running the server.
	'''
	return app.test_client()


@pytest.fixture
def runner(app):
	'''The runner fixture is similar to client fixture. 
	app.test_cli_runner() creates a runner that can call the 
	Click commands registered with the application.
	'''
	return app.test_cli_runner()


# Testing
if __name__ == '__main__':
	if verbose:
		print(f'''finished
		marca? {create_app}
		{get_db}
		{init_db}
		''')