from itertools import izip
from copy import deepcopy

#decay: {'Br':[Br], 'Father':[father], 'fstate':["fstate"], 'history':["history"]}
#    db_2.append([father, decay_id, branching, products.split(' ')])
# decay = [branching, father, products, history]
def get_fstates(decay, db, final_db):
    if decay['branching'][0] < 1E-10:
        return

    print decay['history']
    
    final_db.insert({
        'scheme': decay['history'],
        'branching': decay['branching'],
        'fstate': decay['products'],
        'father': decay['father']
    })

    if len(decay['products']) == 1:
        return

    for p in decay['products']:
        if not p in db:
            continue
        for k in db[p]:
            work_copy = deepcopy(decay)
            work_copy['products'].remove(k['father'])

            work_copy['history'] += '; ' + k['father'] + ' -->'

            for daught in k['products']:
                work_copy['products'].append(daught)
                work_copy['history'] +=  ' ' + daught

            work_copy['branching'][0] *= k['branching'][0]
            get_fstates(work_copy, db, final_db)
