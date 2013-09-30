def phi(decay_str):
    if ' phi ' in decay_str:
        decay_str = decay_str.replace(" phi ", " phi(1020) ")
    if decay_str[-4:] == ' phi':
        decay_str = decay_str.replace(" phi", " phi(1020)")
    return decay_str
                