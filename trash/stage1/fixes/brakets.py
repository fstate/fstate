import re


def brakets(decay_str):
    """
        Fixes things like 4pi+ to pi+ pi+ pi+ pi+
    """

    #def repl(m):
    #    num = int(m.group(1))
    #    return num * (m.group(2) + m.group(3) + " ")
    #return re.sub(r'(\d+)(pi|mu|e|K)([{0,+,-}]*)^\d', repl, decay_str)

    def repl(m):
        subdec = m.group(3)
        subdec = subdec[:-1]
        while subdec[0] == " ":
            subdec = subdec[1:]
        parts = subdec.split(" ")
        subdec = ""
        for i in range(0,len(parts)-1):
            subdec+=parts[i]+m.group(4)

        return m.group(1) + " " + subdec + m.group(5)

    prog = re.compile(r'(.*?)(\s\()(.*?\))(\+\s|\-\s|0\s)(.*)')

    while True:
        decay_str = re.sub(prog, repl, decay_str)
        if re.match(prog, decay_str) == None:
            break
    return decay_str

def including(decay_str):
    """
        Fixes things like (including ...)
    """

    return re.sub(r'(\~\[|\()(including|excluding).*', "", decay_str)
