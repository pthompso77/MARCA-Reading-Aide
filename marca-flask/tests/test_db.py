import sqlite3

import pytest
from marca.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
        
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
        
    assert 'closed' in str(e.value)

    
def test_init_db_command(runner, monkeypatch):
    '''This test uses Pytest’s monkeypatch fixture to replace the 
    init_db function with one that records that it’s been called. 
    The runner fixture below is used to call the init-db command 
    by name.
    '''
    class Recorder(object):
        called = False
        
    def fake_init_db():
        Recorder.called = True
        
    monkeypatch.setattr('marca.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    '''The init-db command should call the init_db function 
    and output a message.
    '''
    assert 'Initialized' in result.output
    assert Recorder.called
    
