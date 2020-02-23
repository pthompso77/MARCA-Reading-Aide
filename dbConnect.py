

import MySQLdb

'''
connection values
'''
from myDBConnect import *


'''
DB table and column name(s)
'''
tokenDocs_TABLE = 'TokenizedDocs_Pickled'
tokenDocs_pickle_COLUMN = 'TokenizedDocs_Pickledcol'

def getDBConnection(printing = False):
    try:
        dbConnect = MySQLdb.connect(host, user, pw, schema)
        if printing:
            rint('success to {} on AVL'.format(schema))
    except Exception as e:
        if printing:
            print('\nerror in connecting to {}:{}'.format(schema,e))
        errMessage = '[error getting keyWordsPhrases]\n' + str(e)    
    
    return dbConnect

connection = getDBConnection()

def runGetQuery(connection, getQuery, printing=False):
    cursor = connection.cursor()
    cursor.execute(getQuery)
    connection.commit()
    output = cursor.fetchall()
    if printing:
        print(output)
    connection.close()
    return output
    
    
def runSetQuery(connection, setQuery):
    cursor = connection.cursor()
    cursor.execute(getQuery)
    connection.commit()
    connection.close()
    
if (__name__ == '__main__'):
    runGetQuery(connection,"SELECT * FROM userAccounts")
    
