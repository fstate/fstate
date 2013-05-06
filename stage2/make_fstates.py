from database import * # build mongo on-the-go
from operator import mul

# First, lets build db:
db = {}
decay_db = {}

decay_id = 0

for x in open("../stage1/valid.txt").readlines():
    branching, decay = x.split("|")
    branching = tuple([float(x.strip()) for x in branching[1:-1].split(',')])

    if branching[0] < 1E-15:
        continue

    father, products = [t.strip() for t in decay.split("-->")]
    
    if not father in db:
        db[father] = []
    
    db[father].append( (decay_id, branching, products.split(' ')) )

    decay_db[decay_id] = {
        'branching': branching,
        'father': father,
        'products': products
        }
    decay_id += 1

decays.create_index("decay_id")

# Lets suppose that we have only one decay scheme:
# A -> (B -> f1 f2) (C -> f3 f4), where f1,f2,f3,f4 are final state

from fstate import get_fstates

for k in db.keys():
    for decay in db[k]:
        for fs in get_fstates(decay[2], db):
            if type(fs) != list:
                fs = [fs]

            try:
                scheme = [decay_db[decay[0]]] + [decay_db[x] for x in fs]
            except TypeError:
                print "Error with fs={}, decay={}".format(fs, decay)
                raw_input()

            if None in scheme:
                print "Bad decay {} and final state {}".format(decay, fs)
                continue
        
            Br = reduce(mul, [x['branching'][0] for x in scheme])
            
            if Br < 1E-15:
                continue

            current_fstate = []

            for d in scheme[1:]:
                for p in d['products'].split(' '):
                    current_fstate.append(p)


            print "{} --> {} with Br={} and fstate={}".format(
                    scheme[0]['father'],
                    " ".join([x['father'] for x in scheme[1:]]),
                    Br, repr(current_fstate)
                )

            fstates.insert({
                'scheme': scheme,
                'branching': Br,
                'fstate': current_fstate
            })
