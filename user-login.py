#!/usr/bin/env python3

'''
this file holds the logic to enable users to log in, including
 - getting user input from html form
 - querying the database
 - hashing user passwords
 - comparing the hash digests
 - ...
'''

import cgitb; cgitb.enable()
import cgi, os, traceback, sys
import dbConnect as db


# references HTML field storage element (placeholder) for later retrieval
html_form = cgi.FieldStorage()

#set nameOfThisFile to the name of this file
nameOfThisFile = "user-login.py"


username_in = html_form.getvalue('username_in')
password_in = html_form.getvalue('password_in')

#for testing
if username_in is None:
    username_in = 'myUsername'
    
messageOut = 'got username = {} and password = {}'.format(username_in, password_in)

def authenticateUser():
    ''' (for every page being loaded)
	reads cookie value
    select from DB SESSION where userid
    if returns 1 row, ok, else except
    (unsetting = change exp to yesterday)
	'''
    userAuthDict = dict()
    #TODO finish the authentication process
    
    return userAuthDict

""" connecting to DB """
dbConnect = db.getDBConnection()
cursor = dbConnect.cursor()

#dbResult = cursor.callproc(procName, procArgs) #this isn't working
q = "SELECT `password`, `NaCl` FROM `pthompsoDB`.`userAccounts` WHERE `email` = '{}';".format(username_in)

dbResult = db.runGetQuery(dbConnect, q)



print("""
<!doctype html>
<head>
	<title>Register</title>
	<meta charset="utf-8">
</head>
<body>
	<h1>{h1}</h1>
	<p id="success_YN">
        {successMessage} <br>
        {linkToNext}
	</p>
</body>
""".format(**authenticateUser()))
