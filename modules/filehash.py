'''
SHA-1

Hash Function
'''

from hashlib import sha1

def baseHash(message: bytes)->bytes:
    return sha1(message).digest()