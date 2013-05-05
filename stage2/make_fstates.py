from database import * # build mongo on-the-go

# First, lets build db:
db = {}

decay_id = 0

for x in open("../stage1/valid.txt").readlines():
    branching, decay = x.split("|")
    branching = tuple([float(x.strip()) for x in branching[1:-1].split(',')])
    father, products = [t.strip() for t in decay.split("-->")]
    
    if not father in db:
        db[father] = []
    
    db[father].append( (decay_id, branching, products.split(' ')) )

    entry = {
        'father': father,
        'decay_id': decay_id,
        'branching': branching,
        'products': products
        }
    decays.insert(entry)
    decay_id += 1

decays.create_index("decay_id")

# Lets suppose that we have only one decay scheme:
# A -> (B -> f1 f2) (C -> f3 f4), where f1,f2,f3,f4 are final state

from fstate import get_fstates

for decay in db['B0']:
    for fs in get_fstates(decay[2], db):
        first = decays.find_one({"decay_id": fs[0]})
        second = decays.find_one({"decay_id": fs[1]})

        if not (first and second):
            print "Bad decay {} and final state {}".format(decay, fs)
            continue
        

        current_fstate = first['products'].split(" ") + second['products'].split(" ")
        Br = first['branching'][0] * second['branching'][0]

        print "B0 --> ({} --> {})({} --> {}) with Br={} and fstate={}".format(
                first['father'], first['products'],
                second['father'], second['products'],
                Br, repr(current_fstate)
            )

        fstates.insert({
            #'scheme': [DBRef('decays', first['_id']), DBRef('decays', second['_id'])],
            'scheme': [fs[0], fs[1]], # write decay_id, instead DBref. Why not?
            'branching': Br,
            'fstate': current_fstate
        })


fstates.create_index("fstate")