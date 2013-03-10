import re


def multiparticle_fix(decay_str):
    """
        Fixes things like 4pi+ to pi+ pi+ pi+ pi+
    """

    def repl(m):
        num = int(m.group(1))

        return num * (m.group(2) + m.group(3) + " ")

    return re.sub(r'(\d+)(pi|mu|e|K)([{0,+,-}]*)', repl, decay_str)
