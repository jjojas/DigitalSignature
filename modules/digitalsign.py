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

if __name__ == "__main__":
    key = "0d02cfc3d97f287b6f985c286666bff36a577569"
    embedKey(key,"example.png")
    saveKey(key,"Kuncis")
