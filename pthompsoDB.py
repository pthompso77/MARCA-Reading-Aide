# connects to pthompsoDB on avl.cs.unca.edu

import MySQLdb

'''
connection values
'''
host = 'avl.cs.unca.edu'
user ='pthompso'
pw = 'sql4you'
schema = 'pthompsoDB'


'''
DB table and column name(s)
'''
tokenDocs_TABLE = 'TokenizedDocs_Pickled'
tokenDocs_pickle_COLUMN = 'TokenizedDocs_Pickledcol'

#query = "SELECT * FROM " + tokenDocs_TABLE
#print('query is'.format(query))

#print('trying to connect')


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
    runGetQuery(dbConnect,query)
    