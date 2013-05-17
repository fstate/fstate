import re


def wave(decay_str):
    """
        Fixes cascades like ( A --> B C)(S wave)
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
        Fixes cascades like ( A --> B C)(S wave)
    """

    def repl(m):
        text = m.group(1)
        return text + " "

    return re.sub(r'(.*?)(\([A-Z]\-wave\)\s)', repl, decay_str)