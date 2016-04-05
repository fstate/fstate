from operator import mul
from copy import deepcopy
from datetime import datetime
from multiprocessing import Pool, cpu_count
from mongoengine import connect
from weight_split import get_jobs
from lazy_decay_model import Decay
from config import br_cutoff, db_name, max_decay_chain
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parrticleparser.particle_model import Particle


import pickle


db = {}

with open('../decaydecparser/parsed_decays.pkl', 'r') as basket:
    test_set = pickle.load(basket)

for parent in test_set['decays']:
    if not parent in db:
            db[parent] = []

    for d in test_set['decays'][parent]:
        if d['branching'] < br_cutoff:
            continue    
        if d['branching'] > 1:
            continue
        db[parent].append({
            'branching': d['branching'],
            'parent': parent,
            'childs': d['childs']
        })


def do_work(parents):
    global db
    connect(db_name)
    for parent in parents:
        start = datetime.now()
        if not parent in db:
            print ("Parent not found in db: "+parent)
            continue
        for decay in db[parent]:
            work_copy = deepcopy(decay)
            #work_copy['history'] = "{} --> {}".format(
            #    parent, ' '.join(decay['products']))

            get_fstates(work_copy)

        end = datetime.now()

        print "{}\t{}".format(parent, end-start)


if __name__ == "__main__":
    from fstate_lazy import get_fstates
    #from fstate import get_fstates
    connect(db_name)
    Decay.objects().delete()
    #fstates.drop()
    #fstates.create_index("fstate")
    #fstates.create_index("scheme", unique=True)


    #do_work(test_set['decays'].keys())
    
    print "DB build started on {}.".format(datetime.now())
    
    start = datetime.now()
    
    workers  = cpu_count()
    p = Pool(processes=workers)
    p.map(do_work, get_jobs(workers))
    
    
    end = datetime.now()
    print "Took {} to build!".format(end - start)
    #print "Cleaning partilce DB starte at {}.".format(datetime.now())
    #start = datetime.now()
    #for p in Particle.objects():
        #remove_part = True
        #for d in Decay.objects(parent = p.name):
            #remove_part = False
            #break
        #for d in Decay.objects(fstate__contains = p.name):
            #remove_part = False
            #break
        #if remove_part:
            #print "Unused particle "+p.name
            #p.delete()
    #end = datetime.now()
    #print "Took {} to clean!".format(end - start)

    