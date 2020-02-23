

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
            print('success to {} on AVL'.format(schema))
    except Exception as e:
        if printing:
            print('\nerror in connecting to {}:{}'.format(schema,e))
        errMessage = '[error getting keyWordsPhrases]\n' + str(e)    
        dbConnect = None
    return dbConnect


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
    cursor.execute(setQuery)
    connection.commit()
    connection.close()
    

def insertUser(connection, userObj):
    query = "INSERT INTO userAccounts \
    (email, password, NaCl) \
    VALUES \
    ('{email}', \
    '{pwHash}', \
    '{salt}'); \
    ".format(email= userObj.email\
               , pwHash= userObj.password_hashed\
               , salt= userObj.pwSalt)
    try:
        runSetQuery(connection, query)
    except Exception as ex:
        print("""Error inserting a new user with email: {emailaddress}
        {exception}""".format(emailaddress=userObj.email, exception=ex))
    



if (__name__ == '__main__'):
    connection = getDBConnection()    
    snoutput = runGetQuery(connection,"SELECT * FROM userAccounts")
    print('result type:',type(snoutput))
    print('result type[0]:',type(snoutput[0]))
    for each in snoutput:
        print(each)
    pause = True
