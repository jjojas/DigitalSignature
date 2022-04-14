'''
RSA Key Generator Algorithm
 
Generate key from given P, Q and E Value"
'''

from typing import Tuple
import random

def checkPrime(n : int) -> bool:
    '''
    Memeriksa apakah N merupakan bilangan prima
    '''
    try:
        if (n == 1):
            return False
        i = 2
        while (i*i <= n):
            if (n%i ==0):
                return False
            i += 1
        return True
    except Exception as e:
        raise e

def pickKeyforMe() -> Tuple:
    '''
    Pengacak kunci dari kumpulan bilangan prima terdefinisi
    '''
    try:
        f = open("modules/primelist.txt","r")
        primes = f.read().split()
        p,q,e = random.choices(primes, k=3)
        p = int(p)
        q = int(q)
        e = int(e)
        while (not relativePrime((p-1)*(q-1),e)):
            p,q,e = random.choices(primes, k=3)
        return (p,q,e)
    except Exception as e:
        raise e

def relativePrime(a:int, b:int) -> bool:
    '''
    Memeriksa apakah A dan B relatif prima
    '''
    try:
        while (b):
            a, b = b, a% b
        return (a==1)
    except Exception as e:
        raise e


def genKeys(p : int, q : int ,e : int) -> Tuple:
    '''
    Membangkitkan kunci publik dan privat
    '''
    d = 0
    if (p!=q):
        if (checkPrime(p) and checkPrime(q)):
            n = p*q
            toit = (p-1)*(q-1)
            if (relativePrime(toit,e)):
                d = (pow(e, -1, toit))
                return (int(d),n)
            else:
                raise Exception("E dan Toitent tidak relatif prima. Pilih E lain!")
        else:
            raise Exception("P atau Q bukan bilangan prima. Pilih bilangan lain!")
    else:
        raise Exception("P atau Q tidak boleh sama!")

def saveKeys(name: str,e : int, d : int, n : int):
    '''
    Menyimpan kunci ke dalam file
    '''
    try:
        f = open(f"key/{name}.pub","w")
        pubKeystring = str(e) + '|' + str(n)
        f.write(pubKeystring)
        f.close()

        g = open(f"key/{name}.pri","w")
        privKeyString = str(d) + '|' + str(n)
        g.write(privKeyString)
        g.close()
    except Exception as e:
        raise e

def createKeyFile(name:str,p:int,q:int,e:int):
    '''
    Membuat file kunci dari input
    '''
    try:
        priv,pub = genKeys(p,q,e)
        saveKeys(name,e,priv,pub)
    except Exception as e:
        raise e

def openKeyFile(dir:str) -> Tuple:
    '''
    Membuka file kunci untuk ditampilkan
    '''
    try:
        f = open(dir,"r")
        content = f.read()
        keytype = dir.split(".",10)[-1]
        if (keytype == "pub" or keytype == "pri"):
            if ("|" in content):
                e,n = content.split("|",1)
                f.close()
                return(int(e),int(n))
            else:
                if (keytype == "pub"):
                    raise Exception("Bukan kunci publik yang valid!")
                else:
                    raise Exception("Bukan kunci privat yang valid!")
        else:
            raise Exception("Bukan file kunci!")
    except Exception as e:
        raise e

if __name__ == "__main__":
    pass
    # print(openKeyFile("../key/TestKey.pub"))
    # createKeyFile("TestKey",47,71,79)
    # print(checkPrime(int(input())))