
from modules.RSA.encrypt import encryptBytes
from modules.filehash import baseHash

def createSignature(filedir: str, d: int, n: int) -> str:
    f = open(f"{filedir}","rb")
    fileBytes = f.read()
    f.close()

    md = baseHash(fileBytes)
    print(md)
    encryptedMd = encryptBytes(md, d, n)
    return encryptedMd.hex()

def embedKey(key,file):
    try:
        f = open(f"{file}", "rb")
        g = open(f"signed_{file}","wb")
        g.write(f.read())
        f.close()
        g.close()
        g = open(f"signed_{file}","a")
        g.write(f"<DS>{key}</DS>")
    except Exception as E:
        raise(E)

def saveKey(key,name):
    try:
        with open(f"{name}_key.txt", "w") as myfile:
            myfile.write(f"<DS>{key}</DS>")
    except Exception as E:
        raise(E)

# if __name__ == "__main__":
#     key = "0d02cfc3d97f287b6f985c286666bff36a577569"
#     embedKey(key,"example.png")
#     saveKey(key,"Kuncis")

# print(createSignature("./modules/example.png", 62093, 39203))