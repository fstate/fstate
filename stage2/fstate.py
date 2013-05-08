from itertools import izip
from copy import deepcopy
"""
def get_fstates(products, db):
    if len(products) == 1 and type(products) == list:
        products = products[0]
    
    if type(products) != list:
        if products in db:
            return [x[0] for x in db[products]]
        else:
            return []
    else:
        a = get_fstates(products[:-1], db)
        b = get_fstates(products[-1], db)
        
        fstates = []
        for x in a:
            for y in b:
                if type(x) != list:
                    x = [x]
                if type(y) != list:
                    y = [y]
                fstates.append(x + y)

        return fstates
"""
#decay: {'Br':[Br], 'Father':[father], 'fstate':["fstate"], 'history':["history"]}
#    db_2.append([father, decay_id, branching, products.split(' ')])
def get_fstates(decay,  db_2, final_db):
    if decay[0] < 1E-10:
        return
    print decay[3]
    final_db.insert({
    'scheme': decay[3],
    'branching': decay[0],
    'fstate': decay[2],
    'father': decay[1]
    })
    if len(decay[2]) == 1:
        return
    for p in decay[2]:
        for k in db_2:
            if p == k[0]:
                g_decay = []
                g_decay = deepcopy(decay)
                g_decay[2].remove(k[0])
                g_decay[3] = g_decay[3] + '; ' + k[0] + ' -->'
                for daught in k[3]:
                    g_decay[2].append(daught)
                    g_decay[3] = g_decay[3] + ' ' + daught
                g_decay[0] = g_decay[0] * k[2][0]
                get_fstates(g_decay, db_2, final_db)
        #       for daught in k[3]:
        #            decay[2].remove(daught)
        #decay[2].append


