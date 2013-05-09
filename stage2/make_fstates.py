from operator import mul
from copy import deepcopy
from datetime import datetime

from database import *
from fstate import get_fstates


# First, lets build db:
db = {}

for x in open("../stage1/valid.txt").readlines():
#for x in open("../stage1/test.txt").readlines():
    branching, decay = x.split("|")
    branching = tuple([float(x.strip()) for x in branching[1:-1].split(',')])

    if branching[0] < 1E-10:
        continue

    father, products = [t.strip() for t in decay.split("-->")]

    if not father in db:
        db[father] = []

    db[father].append({
        'branching': list(branching),
        'father': father,
        'products': products.split(' ')
    })


if __name__ == "__main__":
    start = datetime.now()

    for father in db.keys():
        for decay in db[father]:
            work_copy = deepcopy(decay)
            work_copy['history'] = "{} --> {}".format(
                father, ' '.join(decay['products']))

            get_fstates(work_copy, db, fstates)

    end = datetime.now()

    print "Took {} to build!".format(end - start)
