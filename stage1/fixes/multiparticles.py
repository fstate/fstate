import re


def multiparticle_fix(decay_str):
    """
        Fixes things like 4pi+ to pi+ pi+ pi+ pi+
    """

    #def repl(m):
    #    num = int(m.group(1))
    #    return num * (m.group(2) + m.group(3) + " ")
    #return re.sub(r'(\d+)(pi|mu|e|K)([{0,+,-}]*)^\d', repl, decay_str)

    def repl(m):
        num = int(m.group(2))
        multip = m.group(3)
        if multip[0] == "(":
            multip = multip[1::-2]+" "
        return m.group(1) + num * multip + m.group(4)

    prog = re.compile(r'(.*?\s)(\d)(\(.*?\)\s|[a-zA-Z].*?\s)(.*)')

    while True:
        decay_str = re.sub(prog, repl, decay_str)
        if re.match(prog, decay_str) == None:
            break
    return decay_str
