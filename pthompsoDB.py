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

query = "SELECT * FROM " + tokenDocs_TABLE
print(query)

print('trying to connect')
dbConnect = MySQLdb.connect(host, user, pw, schema)

cursor = dbConnect.cursor()



def runGetQuery(connection, getQuery):
    cursor = connection.cursor()
    cursor.execute(getQuery)
    connection.commit()
    print(cursor.fetchall())
    connection.close()
    
def runSetQuery(connection, setQuery):
    cursor = connection.cursor()
    cursor.execute(getQuery)
    connection.commit()
    connection.close()
    
if (__name__ == '__main__'):
    runGetQuery(dbConnect,query)
    