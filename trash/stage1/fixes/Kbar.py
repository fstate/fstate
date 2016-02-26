import re


def kbar(decay_str):
    """
        Fixes things like Lambda(1810) --> N Kbar^*(892), S=1/2, P-wave
    """

    return re.sub(r', [A-Z]-wave', "", re.sub(r', S=\d\/\d, [A-Z]-wave', "", decay_str))
