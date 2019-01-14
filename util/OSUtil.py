import sys

def getOSTYpe():

    if sys.platform == "darwin":
        return "MAC"
    else:
        return "WINDOWS"



if __name__ == "__main__":
    print (sys.platform)
    pass
