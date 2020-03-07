

try:
    import MySQLdb
except:
    print('importing pymysql as MySQLdb instead')
    import pymysql as MySQLdb

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


def runSetQuery(setQuery, connection=None, returnPK=False):
    """runs a set query (or insert...)

    parameters:
      setQuery (str): SQL statement

    returns:
      primary Key of last inserted
    """
    if connection is None:
        connection = getDBConnection()
    else:
        try:
            if not isinstance(pymysql.connections.Connection, connection):
                connection = getDBConnection()
        except:
            connection = getDBConnection()
    cursor = connection.cursor()
    # TODO handle an exception from the DB (like where PK already exists)
    print(setQuery)
    response = cursor.execute(setQuery)
    rowcount = cursor.rowcount
    connection.commit()
    lastrowID = cursor.lastrowid
    connection.close()
    if returnPK:
        return lastrowID # lastrowID=0 if the table does not have an auto-increment ID


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
        return("""Error inserting a new user with email: {emailaddress}
        {exception}""".format(emailaddress=userObj.email, exception=ex), False)
    return "Success", True




"""__main__ for testing"""
if (__name__ == '__main__'):
    connection = getDBConnection()
    #testing INSERT
    outp = runSetQuery("INSERT INTO `pthompsoDB`.`userAccounts` (email, password, NaCl) VALUES ('email', 'passwordd','saltyfresh');", returnPK=True)
    print(outp)
    #testing SELECT
    snoutput = runGetQuery(connection,"SELECT * FROM userAccounts")
    print('result type:',type(snoutput))
    print('result type[0]:',type(snoutput[0]))
    for each in snoutput:
        print(each)
    pause = True
