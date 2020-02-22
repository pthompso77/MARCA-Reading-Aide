"""
User objects have methods that include database calls

"""
import crypt
testPW = "morepw"

class User:
    def __init__(self, email, password):
        self.email = email
        self.password_hashed, self.pwSalt = crypt.hash_password(password)
        
        
def doTesting():
    u = User("email@stuff",testPW)
    shouldBeTrue = crypt.verify_password(u.password_hashed, u.pwSalt, testPW)
    wrongPW_rightSalt = crypt.verify_password(u.password_hashed, u.pwSalt, "something else")
    wrontPW_wrongSalt = crypt.verify_password(u.password_hashed, "someothersalt", testPW)
    pauseHere = True
    
if __name__ == '__main__':
    doTesting()