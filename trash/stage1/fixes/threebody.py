import re


def tbody(decay_str):
    """
        remove 3body
    """
    decay_str = re.sub(r'3-body', "", decay_str)
    decay_str = re.sub(r'\(charged decay\)', "", decay_str)
    decay_str = re.sub(r'\(3pi0 decay\)', "", decay_str)
    decay_str = re.sub(r'\(neutral decay\)', "", decay_str)
    decay_str = re.sub(r'nonresonant', "", decay_str)
    return decay_str

