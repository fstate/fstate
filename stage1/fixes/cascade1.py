import re


def cascade1(decay_str):
    """
        Fixes things like Lambda(1810) --> N Kbar^*(892), S=1/2, P-wave
    """

    return re.sub(r',\s.*?\-\->.*', "", decay_str)
