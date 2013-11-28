from itertools import izip
from copy import deepcopy
from database import *
from make_fstates import db


def get_fstates(decay):
    if decay['branching'][0] < 1E-30:
        return

    #print decay['history'], decay['products']

    try:
        fstates.insert({
            'scheme': decay['history'],
            'branching': decay['branching'],
            'fstate': ' '.join(decay['products']),
            'father': decay['father']
        })
    except pymongo.errors.DuplicateKeyError:
        return

    if not 1 < len(decay['products']) < 6: # Not full db build
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

            work_copy['branching'][0] *= k['branching'][0]

            get_fstates(work_copy)
