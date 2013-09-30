def pm0(decay_str):
    if '(K pi)+-' in decay_str:    
             return [
                    decay_str.replace('(K pi)+-', 'K+ pi-'),
                    decay_str.replace('(K pi)+-', 'K- pi+'),
                    ]
    else:
        return decay_str

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

def gamma(decay_str):
    if '(gamma)' in decay_str:    
             return [
                    decay_str.replace('(gamma)', ''),
                    decay_str.replace('(gamma)', 'gamma')                    
                    ]
    else:
        return decay_str

def pi0(decay_str):
    if '(pi0)' in decay_str:    
             return [
                    decay_str.replace('(pi0)', ''),
                    decay_str.replace('(pi0)', 'pi0')                    
                    ]
    else:
        return decay_str

def kkbar(decay_str):
    if '(KKbar)+-' in decay_str:    
             return [
                    decay_str.replace('(KKbar)+-', 'K Kbar'),
                    decay_str.replace('(KKbar)+-', 'K+ K-')                    
                    ]
    else:
        return decay_str