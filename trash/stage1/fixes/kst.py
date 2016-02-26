def kst(decay_str):
    if ' K^*(892)0 ' in decay_str:
        decay_str = decay_str.replace(" K^*(892)0 ", " K^*(892) ")
    if decay_str[-10:] == ' K^*(892)0':
        decay_str = decay_str.replace(" K^*(892)0", " K^*(892)")
    return decay_str
                