def sigma (decay_str):
    while True:
        if ' sigma ' in decay_str:
            decay_str = decay_str.replace(" sigma ", " f_0()(500) ")
        if ' Sigma ' in decay_str:
            decay_str = decay_str.replace(" Sigma ", " f_0()(500) ")
        if ' f_0(500) ' in decay_str:
            decay_str = decay_str.replace(" f_0(500) ", " f_0()(500) ")
        if decay_str.find(" sigma ") == -1:
            if decay_str.find(" f_0(500) ") == -1:
                if decay_str.find(" Sigma ") == -1:
                    break
    return decay_str



def sigmahimass (decay_str):
    if decay_str.count('0**,++') != 0:    
             return [
                    decay_str.replace('0**,++', '++'),
                    decay_str.replace('0**,++', '0**')
                    ]
    else:
        return decay_str
