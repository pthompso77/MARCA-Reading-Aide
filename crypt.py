
import hashlib, os, binascii


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password



def hashPass(password):
    ''' from https://www.vitoshacademy.com/hashing-passwords-in-python/ '''
    password = bytes(password, 'ascii')
    rand = os.urandom(60)
    salty = hashlib.sha256(rand).hexdigest().encode('ascii')
    print('type 1:', type(password), type(salty))
    pwdHash = hashlib.pbkdf2_hmac('sha512', password, salty, 1000)
    pwdHash = binascii.hexlify(pwdHash)
    pwdHash = (pwdHash + salty).decode('ascii')
    salty = salty.decode('ascii')
    return (pwdHash, salty)
    

def verifyHashPass(passwordFromDB, passwordToVerify):
    """Verify a stored password against one provided by user"""
    #salt = passwordFromDB[:64]
    salt = passwordFromDB[1]
    passwordFromDB = passwordFromDB[0]
    passwordToVerify = passwordToVerify.encode('utf-8')
    print('type 2:',type(passwordToVerify), type(salt))
    pwdHash = hashlib.pbkdf2_hmac('sha512', passwordToVerify, salt.encode('ascii'), 100000)
    pwdHash2 = binascii.hexlify(pwdHash).decode('ascii')
    return pwdHash2 == passwordFromDB    


if __name__ == "__main__":
    testpass = 'Hello!77459*Bye'
    hashed = hashPass(testpass)
    hashed2 = hash_password(testpass)
    
    
    print('hashed password: ',hashed)
    print('hashed password2: ',hashed2)
    
    print(verifyHashPass(hashed, testpass))
    print(verify_password(hashed2, testpass))
    