"""
Author  :        Thomas Fujise
Date    :        12.04.2022
File    :        util.py
Version :        1.0.0
Brief   :        Util functions file for authentication
"""

import os 
import hashlib
import binascii

def hash_pass(password):
    """
    Function that hash a password for storing
    Encodes a provided password in a way that is safe to store on a database
    """
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    
    return (salt + pwdhash) # return bytes


def verify_pass(provided_password, stored_password):
    """
    Function that verify a stored password against one provided by the user
    Given an encoded password and a plain text one which is provided by the user, it verifies whether the provided password matches the encoded one.
    """

    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)

    pwdhash = binascii.hexlify(pwdhash).decode('ascii')

    return pwdhash == stored_password