#!/usr/bin/env python3
"""user-register.py"""
print('Content-type: text/html\r\n\r\n')
import cgi, cgitb, dbConnect
import cgi, cgitb, dbConnect, html
from User import User
cgitb.enable()

'''
class User:
    def __init__(self, email, password):
        self.email = email
        self.password_hashed, self.pwSalt = crypt.hash_password(password)
        #put me in the DB (or getme out)
        dbUser = self._putMeInDB()
    def _putMeInDB(self):
        initDict = {'email':self.email, 'password':self.password_hashed, 'NaCl':self.pwSalt}
        dbUser = dbObj.userAccount(initDict)
        dbUser.updateDB(initDict)
        return dbUser
    def authenticateMe(self, sessionID):
        dbUser = dbObj.userAccount.getEmailBySessionID(sessionID)
        return dbUser is not None
'''
def getFormDataByName(cgiFieldStorageObject, fieldName):
    dataOut = cgiFieldStorageObject.getfirst(fieldName, "empty").upper()
    return html.escape(dataOut)

def registerNewUser():
    form = cgi.FieldStorage()
    email_in = getFormDataByName(form, 'email_in')
    pw_in = getFormDataByName(form, 'pw_in')
    user = User(email_in, pw_in)
    con = dbConnect.getDBConnection()
    dbConnect.insertUser(con, userObj=user)
    #user._putMeInDB()




def isSuccess():
    registerNewUser()
    return "something"

print("""
<!doctype html>
<head>
	<title>Register</title>
	<meta charset="utf-8">
</head>
<body>
	<h1>Register Success??</h1>
	<p id="success_YN">
        {success_YN}
	</p>
</body>
""".format(success_YN=isSuccess()))
