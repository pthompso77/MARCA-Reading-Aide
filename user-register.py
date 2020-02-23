#!/usr/bin/env python3
"""user-register.py"""
print('Content-type: text/html\r\n\r\n')

import cgi, cgitb, dbConnect, html
from User import User
cgitb.enable()

def getFormDataByName(cgiFieldStorageObject, fieldName):
    dataOut = cgiFieldStorageObject.getfirst(fieldName, "empty").upper()
    return html.escape(dataOut)

def registerNewUser():
    form = cgi.FieldStorage()
    email_in = getFormDataByName(form, 'email_in')
    pw_in = getFormDataByName(form, 'pw_in')
    user = User(email_in, pw_in)
    con = dbConnect.getDBConnection()
    message, successful = dbConnect.insertUser(con, userObj=user)
    return message, successful
    #user._putMeInDB()




def isSuccess():
    message, successful = registerNewUser()
    responseDict = dict()
    if successful:
        responseDict['h1'] = 'placeholder1'
        responseDict['successMessage'] = 'placeholder2'
        responseDict['linkToNext'] = 'placeholder3'
    else:
        responseDict['h1'] = 'placeholder4'
        responseDict['successMessage'] = 'placeholder5'
        responseDict['linkToNext'] = 'placeholder6'
    return responseDict

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
""".format(**isSuccess()))
