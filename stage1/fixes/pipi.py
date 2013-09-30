import re


def pipi(decay_str):
    """
        Fixes pipi -> pi pi
    """
    return re.sub(r'pipi', "pi pi", decay_str)