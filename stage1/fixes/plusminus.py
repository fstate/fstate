def pm(decay_str):
    if decay_str.count('+-') + decay_str.count('-+') != 0:    
             return [
                    decay_str.replace('+-', '+').replace('-+', '-'),
                    decay_str.replace('+-', '-').replace('-+', '+')
                    ]
    else:
        return decay_str