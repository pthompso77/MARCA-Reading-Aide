
try:
    import MySQLdb
except:
    import mysql.connector

'''
connection values
'''
from myDBConnect import *
config = {
  'user': user,
  'password': pw,
  'host': host,
  'database': schema,
  'raise_on_warnings': True
}

def getDBConnection(printing = False):
    try:
        dbConnect = MySQLdb.connect(host, user, pw, schema)
        if printing:
            print('success to {} on AVL'.format(schema))
    except:
        try:
            dbConnect = mysql.connector.connect(**config)
            if printing:
                print('success to {} on AVL'.format(schema))
        except Exception as e:
            if printing:
                print('\nerror in connecting to {}:{}'.format(schema,e))
            errMessage = '[error getting keyWordsPhrases]\n' + str(e)
            dbConnect = None
    return dbConnect


def runGetQuery(getQuery, connection=None, multi=False, printing=False):
    if connection is None:
        connection = getDBConnection()
    cursor = connection.cursor()
    cursor.execute(getQuery, multi=multi)
    if printing:
        for tup in cursor:
            print("{}".format(tup))
    output = cursor.lastrowid
    alls = cursor.fetchall()
    #if printing:
        #print(output)
    cursor.close()
    connection.close()
    return output


def runSetQuery(setQuery, connection=None, returnPK=False, multi=False):
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
    try:
        #response = cursor.execute(setQuery)
        cursor.execute(setQuery)
    except Exception as e:
        print('runSetQuery() Exception with setQuery = ',setQuery,'\n')
        print(e)
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
    import random
    testEmail = 'email'+str(random.randint(0,3333))
    test_query0311 = "INSERT INTO userAccounts (email,password,NaCl,sessionID) VALUES ('"+testEmail+"','d342be2fb321a0c5653b76a1a3910a8f674de77c6c5318e8dcb903f55b3a02fa','e28f7bcf5090fa97f53ab0fdc6bf44a2848f3f87a06eb2395ff53d3cb1c53fdf','')"
    #outp = runSetQuery("INSERT INTO `pthompsoDB`.`userAccounts` (email, password, NaCl) VALUES ('email', 'passwordd','saltyfresh');", returnPK=True)
    outp = runSetQuery(test_query0311, returnPK=True)
    print(outp)
    #testing SELECT
    query1 = "SELECT email, create_time FROM pthompsoDB.userAccounts WHERE email = '{}' ORDER BY create_time DESC;"
    query2 = "SELECT email, create_time FROM pthompsoDB.userAccounts WHERE email = %s ORDER BY create_time DESC;"
    query2 = "SELECT * FROM pthompsoDB.userAccounts WHERE email = %s ORDER BY create_time DESC;"
    #query = "SELECT email, create_time FROM pthompsoDB.userAccounts ORDER BY create_time DESC;"
    emailadd = 'email49944'
    curs = connection.cursor()
    #curs.execute(query1.format(emailadd))
    curs.execute(query2,(emailadd,))
    #curs.execute(query)
    #for (email, time) in curs:
        #print("{}".format(time))
    for tup in curs:
        print("{}".format(tup))
    #runGetQuery(query)
    pause = True
