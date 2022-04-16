'''
RSA (Rivest-Shamir-Adleman) Algorithm

Decryption
'''

from typing import List
import math

def baseDecrypt(c: int, e: int, n: int) -> int:
    '''
    Fungsi basis dekripsi RSA menggunakan kunci privat (d,n)
    '''
    return pow(c, e, n)

def binaryPadding(bits: str, n: int) -> str :
    '''
    Menambahkah padding '0' sebanyak n bit.
    '''
    while len(bits) % n != 0:
        bits = '0'+bits
    return bits
    
def convertBytetoIntArray(bytesInput: bytes, digitDiv: int) -> List[int]:
    '''
    Konversi Byte ke Array of Integer
    '''
    result = []
    binInput = bin(int.from_bytes(bytesInput, "big"))[2:]
    binInput = binaryPadding(binInput, digitDiv)

    for index in range(0, len(binInput), digitDiv):
        result.append(int(binInput[index : index + digitDiv], 2))

    return result

def convertIntArraytoByte(inputList: List[int], digit: int) -> bytes:
    '''
    Konversi Array of Integer menjadi Byte
    '''
    binary = ''
    for i, val in enumerate(inputList):
        if i != len(inputList)-2 :
            binary+=bin(val)[2:].zfill(digit)
        else:
            binary+=bin(val)[2:].zfill(inputList[-1])
            break

    intResult = int(binary, 2)
    result = intResult.to_bytes((len(binary) + 7) // 8, "big", signed=False)

    return result

def digitDivider(n: int) -> int:
    '''
    Menentukan panjang digit/bit awal
    '''
    return math.floor(math.log2(n))

def maxBitLength(n: int) -> int:
    '''
    Menentukan panjang bit maksimal membagi enkripsi binary [0...n-1]
    '''
    return (n-1).bit_length()

def decryptBytes(message: bytes, e: int, n: int):
    '''
    Operasi dekripsi file berdasarkan kunci publik (d,n)
    File disimpan dalam direktori /files/
    '''
    cipherBytes = message
    
    digitDiv = digitDivider(n)
    intValue = convertBytetoIntArray(cipherBytes, maxBitLength(n))
    plainInt = [baseDecrypt(val, e, n) for val in intValue]
    plainBytes = convertIntArraytoByte(plainInt, digitDiv)

    return plainBytes