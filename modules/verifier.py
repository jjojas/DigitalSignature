from modules.RSA.decrypt import decryptBytes
from modules.filehash import baseHash

def extractFile(filedir:str) -> tuple:
    try:
        f = open(f"{filedir}","rb")
        fileInside = f.read()
        byte = fileInside.split(b'<DS>')[0]
        data = fileInside.decode("ISO-8859-1")
        if ("<DS>" in data) and ("</DS" in data):
            key = data.split("<DS>")[-1].split("</DS>")[0]
            return (byte,key)
        else:
            raise(Exception("No digital signature found!"))
    except Exception as E:
        raise(E)

def openFile(bytedir: str, signdir:str) -> tuple:
    try:
        return (open(bytedir,"rb").read(),open(signdir,"r").read())
    except Exception as E:
        raise(E)

def verifyFile(fileBytes: bytes, signature: str, e: int, n: int) -> bool:
    signatureBytes = bytes.fromhex(signature.split("<DS>")[-1].split("</DS>")[0])

    md = baseHash(fileBytes)
    
    decryptedMd = decryptBytes(signatureBytes, e, n)
    return md==decryptedMd

# if __name__ == "__main__":
#     fileSigned,key = extractFile("signed_example.png")
#     f = open("example.png","rb")
#     fileUnsigned = f.read()
#     print(fileSigned==fileUnsigned)
    