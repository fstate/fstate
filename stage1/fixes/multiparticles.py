import re


def multiparticle_fix(decay_str):
    """
        Fixes things like 4pi+ to pi+ pi+ pi+ pi+
    """

    def repl(m):
        num = int(m.group(1))
        return " ".join([m.group(2)] * num)

    prog = re.compile(r'(\d)([a-zA-Z]{1,2}[\+\-\0])')

    while True:
        decay_str = re.sub(prog, repl, decay_str)
        if re.match(prog, decay_str) == None:
            break
    return decay_str
