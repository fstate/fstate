from itertools import izip
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
def get_fstates(decay, db, final_db):
    if decay[0] < 1E-15:
        return
    print decay
    final_db.insert({
    'scheme': decay[3],
    'branching': decay[0],
    'fstate': decay[2]
    })
    if len(decay[2]) < 2:
        return
    for p in decay[2]:
        if p not in db:
            return
        decay[2].remove(p)
        for d in db[p]:
            decay[3] = decay[3] + '; ' + p + '-->'
            for k in d[2]:
                decay[2].append(k)
                decay[3] = decay[3] + k
            decay[0] = decay[0] * d[1][0]
            get_fstates(decay, db, final_db)

