"""
User objects have methods that include database calls

"""
import crypt, DatabaseObject as dbObj

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
    #if there: check it against the database
    #if not match: go back to login page
    #if match: break and continue with other process
    #if not there: go back to login page
    return False
        
def doTesting():
    testPW = "morepw"
    u = User("email@stuff",testPW)
    authTest = u.authenticateMe('sessionstuff')
    shouldBeTrue = crypt.verify_password(u.password_hashed, u.pwSalt, testPW)
    wrongPW_rightSalt = crypt.verify_password(u.password_hashed, u.pwSalt, "something else")
    wrontPW_wrongSalt = crypt.verify_password(u.password_hashed, "someothersalt", testPW)
    pauseHere = True
    
if __name__ == '__main__':
    doTesting()