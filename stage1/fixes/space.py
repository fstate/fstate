import re


def space(decay_str):
    """
        Fix 4 gamma
    """

    def repl(m):
        return m.group(1) + m.group(3)

    return re.sub(r'(\s\d)(\s)([a-zA-Z].*?\s)', repl, decay_str)