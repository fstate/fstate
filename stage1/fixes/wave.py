import re


def wave(decay_str):
    """
        Fixes decays like ( A --> B C)(S wave)
    """

    def repl(m):
        text = m.group(2)
        while True:
            if text[0] == " ":
               text = text[1:]
            if text[0] != " ":
                break
        while True:
            if text[-1] == " ":
                text = text[:-1]
            if text[-1] != " ":
                break

        return " " + text + " "

    return re.sub(r'(\s\()(.*?)(\)\([A-Z].*?wave\)\s)', repl, decay_str)

def wave2(decay_str):
    """
        Fixes decays like ( A --> B C)(S wave)
    """

    def repl(m):
        text = m.group(1)
        return text + " "

    return re.sub(r'(.*?)(\([A-Z]\-wave\)\s)', repl, decay_str)

def wave3(decay_str):
    """
        Fixes decays like  A --> B C S-wave
    """

    def repl(m):
        text = m.group(1)
        return text + " "

    return re.sub(r'(.*?)(\s[A-Z]\-wave.*?)', repl, decay_str)


def wavel(decay_str):
    """
        Fixes decays like  A --> B C longitudinal
    """

    def repl(m):
        text = m.group(1)
        return text + " "

    return re.sub(r'(.*?)(\slongitudinal.*?|\slong\..*?|\stransverse.*?|\svia\sDbar0.*?)', repl, decay_str)
