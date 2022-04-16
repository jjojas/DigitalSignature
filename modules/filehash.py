#
from hashlib import sha1

def baseHash(message: bytes)->bytes:
    return sha1(message).digest()

def hashFile(filedir: str)->bytes:
    f = open(f"{filedir}","rb")
    fileInside = f.read()
    f.close()

    return baseHash(fileInside)