#This function transform output of parser to DB command


def CmdToDB(x):
    #len(x.split(" "));
    i = 0
    for word in x.split(" "):
        if i == 0:
            st = "father:\"" + word + "\""
        elif i > 0:
            st = st + ", D%i" % i + ":\"" + word + "\""
        i = i + 1
    return st = "j={" + st + "}"
