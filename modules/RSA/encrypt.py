'''
RSA (Rivest-Shamir-Adleman) Algorithm

Encryption
'''

from typing import List
import math

def baseEncrypt(m: int, d: int, n: int) -> int:
    '''
    Fungsi basis enkripsi RSA menggunakan kunci private (d,n)
    '''
    return pow(m, d, n)
    
def convertBytetoIntArray(bytesInput: bytes, digitDiv: int) -> List[int]:
    '''
    Konversi Byte ke Array of Integer
    '''
    result = []
    binInput = bin(int.from_bytes(bytesInput, "big"))[2:]

    for index in range(0, len(binInput), digitDiv):
        result.append(int(binInput[index : index + digitDiv], 2))
    result.append(len(binInput) % digitDiv)

    return result
    
def convertIntArraytoByte(inputList: List[int], digit: int) -> bytes:
    '''
    Konversi Array of Integer menjadi Byte
    '''
    binary = ''.join([bin(val)[2:].zfill(digit) for val in inputList]) 
    
    intResult = int(binary, 2)
    result = intResult.to_bytes((len(binary) + 7) // 8, "big")

    return result

def digitDivider(n: int) -> int:
    '''
    Menentukan panjang digit/bit untuk membagi binary file
    '''
    return math.floor(math.log2(n))

def maxBitLength(n: int) -> int:
    '''
    Menentukan panjang bit maksimal untuk menyimpan enkripsi [0...n-1]
    '''
    return (n-1).bit_length()

def encryptBytes(message: bytes, d: int, n: int) -> bytes:
    '''
    Operasi enkripsi file berdasarkan kunci publik (e,n)
    File disimpan dalam direktori /files/
    '''
    plainBytes = message
    
    digitDiv = digitDivider(n)
    intValue = convertBytetoIntArray(plainBytes, digitDiv)
    cipherInt = [baseEncrypt(val, d, n) for val in intValue]
    cipherBytes = convertIntArraytoByte(cipherInt, maxBitLength(n))

    return cipherBytes