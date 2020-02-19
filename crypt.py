
import hashlib, os, binascii

def hashPass(password):
    ''' from https://www.vitoshacademy.com/hashing-passwords-in-python/ '''
    password = bytes(password, 'ascii')
    rand = os.urandom(60)
    salty = hashlib.sha256(rand).hexdigest().encode('ascii')         
    pwdHash = hashlib.pbkdf2_hmac('sha512', password, salty, 1000)
    pwdHash = binascii.hexlify(pwdHash)
    pwdHash = (pwdHash + salty).decode('ascii')
    return (pwdHash, salty)
    
hashPass("pword")