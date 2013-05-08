from database import * # build mongo on-the-go
from operator import mul
from copy import deepcopy

# First, lets build db:
db = {}
db_2=[]
decay_db = {}

decay_id = 0

for x in open("../stage1/valid.txt").readlines():
    branching, decay = x.split("|")
    branching = tuple([float(x.strip()) for x in branching[1:-1].split(',')])

    if branching[0] < 1E-10:
        continue

    father, products = [t.strip() for t in decay.split("-->")]
    

    if not father in db:
        db[father] = []
    
    db_2.append([father, decay_id, branching, products.split(' ')])

    db[father].append({
        'branching': list(branching),
        'father': father,
        'products': products.split(' ')
    })
    decay_id += 1

decays.create_index("decay_id")

# Lets suppose that we have only one decay scheme:
# A -> (B -> f1 f2) (C -> f3 f4), where f1,f2,f3,f4 are final state

from fstate import get_fstates

for father in db.keys():
    for decay in db[father]:
        work_copy = deepcopy(decay)
        work_copy['history'] = "{} --> {}".format(father, ' '.join(decay['products']))

        get_fstates(work_copy, db, fstates)
