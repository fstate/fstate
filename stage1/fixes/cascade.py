import re


def cascade1(decay_str):
    """
        Fixes cascades like A --> B C, C --> E
    """

    return re.sub(r',\s.*?\-\->.*', "", decay_str)

def cascade2(decay_str):
    """
        Fixes cascades like A --> B C x B(C --> E)
    """
    while True:
        decay_str = re.sub(r'\sx\s.*?B.*?\-\->.*', "", decay_str)
        if re.match(r'\sx\s.*?B.*?\-\->.*', decay_str) == None:
            break
    return decay_str

def cascade3(decay_str):
    """
        Fixes cascades like A --> B C ~[including C --> E]
    """
    while True:
        decay_str = re.sub(r'\~\[.*?\-\->.*?\]', "", decay_str)
        if re.match(r'\~\[.*?\-\->.*?\]', decay_str) == None:
            break
    return decay_str

def cascade4(decay_str):
    """
        Fixes cascades like A --> B C --> C D E
    """
    
    def repl(m):
        return m.group(1)

    return re.sub(r'(.*?\-\->.*?)(\-\->.*)', repl, decay_str)