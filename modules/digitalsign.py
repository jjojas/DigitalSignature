from modules.RSA.encrypt import encryptBytes
from modules.filehash import baseHash

def createSignature(filedir: str, d: int, n: int) -> str:
    f = open(f"{filedir}","rb")
    fileBytes = f.read()
    if (b"<DS>" in fileBytes) and (b"</DS>" in fileBytes):
        raise(Exception("file sudah ditandatangani!"))
    else:
        f.close()

    md = baseHash(fileBytes)
    encryptedMd = encryptBytes(md, d, n)
    return encryptedMd.hex()

def embedKey(key,file):
    try:
        f = open(f"{file}", "rb")
        g = open(f"files/signed_{file.split('/')[-1]}","wb")
        g.write(f.read())
        f.close()
        g.close()
        g = open(f"files/signed_{file.split('/')[-1]}","a")
        g.write(f"<DS>{key}</DS>")
    except Exception as E:
        raise(E)

def saveKey(key,name):
    try:
        with open(f"signature/{name}_signature.txt", "w") as myfile:
            myfile.write(f"<DS>{key}</DS>")
    except Exception as E:
        raise(E)