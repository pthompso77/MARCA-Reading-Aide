"""
User objects have methods that include database calls

"""
import crypt, DatabaseObject as dbObj
import os #to read cookies

""" Database names """




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

def authenticate():
    #look for sessionID cookie in browser
    sessionCookie = UserSession.getCookie('sessionID')
    #if there: check it against the database
    #if not match: go back to login page
    #if match: break and continue with other process
    #if not there: go back to login page
    return False


class UserSession:
    def getCookie(cookieKey):
        if os.getenv(cookieKey) is not None:
            for cookie in map(strip, split(environ['cookieKey'], ';')):
                (key, value ) = split(cookie, '=');
                if key == "UserID":
                    user_id = value
                    if key == "Password":
                        password = value



"""Testing"""

def doTesting1():
    authenticate()
    #testPW = "morepw"
    #u = User("email@stuff",testPW)


def doTesting():
    testPW = "morepw"
    u = User("email@stuff",testPW)
    authTest = u.authenticateMe('sessionstuff')
    shouldBeTrue = crypt.verify_password(u.password_hashed, u.pwSalt, testPW)
    wrongPW_rightSalt = crypt.verify_password(u.password_hashed, u.pwSalt, "something else")
    wrontPW_wrongSalt = crypt.verify_password(u.password_hashed, "someothersalt", testPW)
    pauseHere = False

if __name__ == '__main__':
    doTesting1()