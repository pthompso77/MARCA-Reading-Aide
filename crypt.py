import hashlib, os, binascii
from hmac import compare_digest


def hash_password(password, optionalSalt_str = -1):
    """Hash a password for storing in database.
    Uses hashlib.pbkdf2_hmac sha256 with blocksize=32, parallelization=1
    
    Parameters:
        password (str): plaintext password
        optionalSalt_str: optionally provide the salt to use when hashing [default = -1]
        (optionalSalt_str will be generated if not provided)
        
    Returns:
        tuple: 
            [0] hash digest of password (str),
            [1] salt used to hash the password (str)
    
    """
    block_size = 32
    parallelization_factor = 1
    saltIsProvided = not (optionalSalt_str == -1)
    if saltIsProvided:
        salt_bytes = bytes(optionalSalt_str, 'utf-8')
    else: #TODO need to check if this is the right encoding?
        salt_bytes = hashlib.sha256(os.urandom(60)).hexdigest().encode('utf-8')        
    salt_str = salt_bytes.decode('utf-8')
    password_bytes = bytes(password, 'utf-8')
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt_bytes, 100000)
    pwdhash2 = hashlib.scrypt(password=password_bytes, salt=salt_bytes, n=16, r=block_size,
                             p=parallelization_factor)
    pwdhash_str = pwdhash.hex()
    return pwdhash_str, salt_str


def verify_password(stored_password_hash, stored_salt_str, provided_password):
    """Verifies a plaintext password matches the hash digest of a stored password
    
    Parameters:
        stored_password_hash (str): hash digest of stored password
        stored_salt_str (str): the salt parameter that was used to create the stored_password_hash
        provided_password (str): plaintext password to verify
    
    Returns:
        True if the passwords match, False if not

    """
    isMatch = False
    stored_pw_hash_Bytes = bytes(stored_password_hash, 'utf-8')
    provided_pwHash = hash_password(provided_password, optionalSalt_str=stored_salt_str)[0]
    isMatch = compare_digest(stored_password_hash, provided_pwHash)
    return isMatch


def doTesting():
    testpass = 'Hello!77459*Bye'
    hashed = hash_password(testpass)


if __name__ == "__main__":
    doTesting()
    