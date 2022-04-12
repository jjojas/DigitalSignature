def readKey(file:str) -> str:
    try:
        f = open(f"{file}","rb")
        data = f.read().decode("ISO-8859-1")
        if ("<DS>" in data) and ("</DS" in data):
            key = data.split("<DS>")[-1].split("</DS>")[0]
            return key
        else:
            raise(Exception("No digital signature found!"))
    except Exception as E:
        raise(E)


if __name__ == "__main__":
    print(readKey("signed_example.png"))
    