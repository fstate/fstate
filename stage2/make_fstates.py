from operator import mul
from copy import deepcopy
from datetime import datetime
from multiprocessing import Pool, cpu_count

from weight_split import get_jobs
from database import *


db = {}

for x in open("../stage1/valid.txt").readlines():
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


def do_work(fathers):
    for father in fathers:
        start = datetime.now()

        for decay in db[father]:
            work_copy = deepcopy(decay)
            work_copy['history'] = "{} --> {}".format(
                father, ' '.join(decay['products']))

            get_fstates(work_copy)

        end = datetime.now()

        print "{}\t{}".format(father, end-start)


if __name__ == "__main__":
    from fstate import get_fstates

    fstates.drop()
    fstates.create_index("fstate")
    fstates.create_index("scheme", unique=True)


    print "DB build started on {}.".format(datetime.now())

    start = datetime.now()

    workers  = cpu_count()
    p = Pool(processes=workers)
    p.map(do_work, get_jobs(workers))


    end = datetime.now()

    print "Took {} to build!".format(end - start)
