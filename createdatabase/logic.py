import config
import pickle
from datetime import datetime
from copy import deepcopy

def build_db():
    db = {}
    with open('../decaydecparser/parsed_decays.pkl', 'r') as basket:
        test_set = pickle.load(basket)

    for father in test_set['decays']:
        if not father in db:
                db[father] = []

        for d in test_set['decays'][father]:
            if d['branching'] < 1E-30:
                continue
            if d['branching'] >= 1:
                continue
            db[father].append({
                'branching': d['branching'],
                'father': father,
                'products': d['daughters']
            })

    return db

def get_fstates(decay, db):
    if decay['branching'] < config.br_cutoff:
        return

    #print decay['history'], decay['products']

    # try:
    #print json.dumps(decay) #, sort_keys=True, indent=4)
        # fstates.insert({
        #     'scheme': decay['history'],
        #     'branching': decay['branching'],
        #     'fstate': ' '.join(decay['products']),
        #     'father': decay['father']
        # })
    # except pymongo.errors.DuplicateKeyError:
    #     return

    if not 1 < len(decay['products']) < config.max_decay_chain: # Not full db build
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

            get_fstates(work_copy, db)


def build_father(father):
    db = build_db()

    print "Building", father
    start = datetime.now()

    for decay in db[father]:
        work_copy = deepcopy(decay)
        work_copy['history'] = "{} --> {}".format(
            father,
            ' '.join(decay['products'])
        )

        get_fstates(work_copy, db)

    end = datetime.now()

    print "{}\t{}".format(father, end-start)


def worker(queue):
    for item in iter( queue.get, None ):
        build_father(item)
        queue.task_done()
    queue.task_done()
