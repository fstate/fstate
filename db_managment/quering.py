from mongoengine import connect
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from createdatabase.decay_model import Decay, order_particles
from createdatabase.config import br_cutoff, max_decay_chain
from parrticleparser.particle_model import Particle
from copy import copy
from datetime import datetime
from itertools import permutations, combinations
result = {}
list_result = []

def query_with_ME(query, energy = 100):
    start = datetime.now()
    queries = []
    for p in Particle.objects(mass__lt = energy):
        queries.append(query+" "+p.name)
    for q in queries:
        do_search(q, False)
    end = datetime.now()
    print "Search for "+query+" with missed energy "+str(energy)+" MeV took {}".format(end-start)
    return True

def query_with_MISID(query):
    return True

def iterative_search(particles, history="", br = 1, last_hist=False):
    global list_result
    query_permutations = order_particles(particles)
    for d in Decay.objects(__raw__ = {'childs':query_permutations}):
        if br*d.branching>=br_cutoff:
            list_result.append({'parent':d.parent, 'branching':br*d.branching, 'scheme':d.nice_decay+"; "+history})
            #if d.nice_decay+"; "+history not in result:
            #    result[d.nice_decay+"; "+history]=br*d.branching
            #else:
            #    result[d.nice_decay+"; "+history]+=br*d.branching
    small_query_subsets = []
    for len_part in range(2, len(particles)):
        for comb in set(combinations(particles, len_part)):
            small_query_subsets.append(comb)
    for i in set(small_query_subsets):
        b = copy(particles)
        for j in i:
            b.remove(j)
        subset_permutations = order_particles(i)
        for d in Decay.objects(childs = subset_permutations):
            c = copy(b)
            c.append(d.parent)
            if br*d.branching>=br_cutoff:
                iterative_search(c, d.nice_decay+"; "+history, br*d.branching)
    return True


def do_search(query, verbose = False):
    global list_result
    list_result = []
    if str(type(query)) == "<type 'str'>":
        particles = query.split(" ")    
    else:
        particles = query
    start = datetime.now()
    iterative_search(particles)
    end = datetime.now()
    #
    if verbose:
        for l in list_result:
            print l
        print "Search for "+' '.join(particles)+" took {}".format(end-start)
        print "found "+str(len(list_result))

    return list_result

if __name__ == "__main__":
    from createdatabase.config import db_name
    connect(db_name)
    print "connected"
    do_search("pi+ pi- mu+ mu-", True)
