def pm(decay_str):
    if decay_str.count('+-') + decay_str.count('-+') != 0:    
             return [
                    decay_str.replace('+-', '+').replace('-+', '-'),
                    decay_str.replace('+-', '-').replace('-+', '+')
                    ]
    else:
        return decay_str

def lepton(decay_str):
    if 'lepton' in decay_str:    
             return [
                    decay_str.replace('lepton', 'e'),
                    decay_str.replace('lepton', 'mu'),
                    decay_str.replace('lepton', 'tau'),
                    ]
    else:
        return decay_str