#!/usr/bin/env python3

'''
this file holds the logic to enable users to log in, including
 - getting user input from html form
 - querying the database
 - hashing user passwords
 - comparing the hash digests
 - ...
'''

import cgi, cgitb; cgitb.enable()
import os, traceback, sys
import pthompsoDB as db


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


""" connecting to DB """
dbConnect = db.getDBConnection()
cursor = dbConnect.cursor()
procName = 'getPassword_andSalt_ByUsername'
procArgs = ("'{}'".format(username_in),0,0)

#dbResult = cursor.callproc(procName, procArgs) #this isn't working
q = "SELECT `password`, `NaCl` FROM `pthompsoDB`.`userAccounts` WHERE `username` = '{}';".format(username_in)

dbResult = db.runGetQuery(dbConnect, q)


print('''Content-type: text/html\r\n\r\n
        <!doctype html>
<head>
	<title>Login</title>
	<meta charset="utf-8">
</head>
<body>
	<h1>Success??</h1>
	<p id="success_YN">
    {message}
    {dbResult}
	</p>
</body>'''.format(message = messageOut, dbResult = dbResult))
