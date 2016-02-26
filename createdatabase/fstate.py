from itertools import izip
from copy import deepcopy
#from database import *
from make_fstates import db
from config import br_cutoff, max_decay_chain
import json
from decay_model import Decay



def get_fstates(decay):
    global db
    global br_cutoff
    if decay['branching'] < br_cutoff:
        return

    #print decay['history'], decay['products']
    db_dec = Decay(father = decay['father'], scheme = decay['history'], branching = decay["branching"], fstate = ' '.join(decay['products']))
        #db_dec.printdecay()
    try:
        db_dec.save()
    except pymongo.errors.DuplicateKeyError:
        #print "Failed to save decay!"
        #db_dec.printdecay()
        return
    #try:
    #    #print json.dumps(decay, sort_keys=True, indent=4)
    #    fstates.insert({
    #        'scheme': decay['history'],
    #        'branching': decay['branching'],
    #        'fstate': ' '.join(decay['products']),
    #        'father': decay['father']
    #    })
    #except pymongo.errors.DuplicateKeyError:
    #    return

    if not 1 < len(decay['products']) < max_decay_chain: # Not full db build
    #if len(decay['products']) == 1: # Full DB build
        return

    for p in decay['products']:
        if not p in db:
            continue
        for k in db[p]:
            work_copy = deepcopy(decay)

            work_copy['products'].remove(k['father'])
            work_copy['products'] += k['products']

            history = work_copy['history'].split('; ') + \
                ["{} --> {}".format(k['father'], ' '.join(k['products']))]

            work_copy['history'] = '; '.join(history[:1] + sorted(history[1:]))

            work_copy['branching'] *= k['branching']

            get_fstates(work_copy)
