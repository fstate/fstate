def omega(decay_str):
    if ' omega ' in decay_str:
        decay_str = decay_str.replace(" omega ", " omega(782) ")
    if decay_str[-4:] == ' omega':
        decay_str = decay_str.replace(" omega", " omega(782)")
    return decay_str