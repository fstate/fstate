from mongoengine import connect
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from createdatabase.lazy_decay_model import Decay, order_particles
from createdatabase.config import br_cutoff, max_decay_chain
from parrticleparser.particle_model import Particle
from copy import copy
from datetime import datetime
from itertools import permutations, combinations
lazy_result = {}

def query_with_ME(query, energy = 100):
    start = datetime.now()
    queries = []
    for p in Particle.objects(mass__lt = energy):
        queries.append(query+" "+p.name)
    for q in queries:
        query_test(q, False)
    end = datetime.now()
    print "Search for "+query+" with missed energy "+str(energy)+" MeV took {}".format(end-start)
    return True

def query_with_MISID(query):
    return True

def lazy_query(particles, history="", br = 1, last_hist=False):
    global lazy_result
    query_permutations = order_particles(particles)
    for d in Decay.objects(__raw__ = {'childs':query_permutations}):
        if br*d.branching>=br_cutoff:
            if d.nice_decay+"; "+history not in lazy_result:
                lazy_result[d.nice_decay+"; "+history]=br*d.branching
            else:
                lazy_result[d.nice_decay+"; "+history]+=br*d.branching
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
                lazy_query(c, d.nice_decay+"; "+history, br*d.branching)
    return True


def query_test(query, verbose = True):
    particles = query.split(" ")
    
    start = datetime.now()
    lazy_query(particles)
    end = datetime.now()
    print "Search for "+query+" took {}".format(end-start)
    print "found "+str(len(lazy_result))
    if verbose:
        for l in lazy_result:
            print l+"  :  "+str(lazy_result[l])

    return True

if __name__ == "__main__":
    from createdatabase.config import db_name
    connect(db_name)
    print "connected"
    #for d in Decay.objects():
    #    d.printdecay()
    query_test("pi+ pi- mu+ mu-")
    #query_test("pi+ pi-")
    #query_test("pi+ pi- K+ K-")    
    #query_test("K+ pi+ pi- mu+ mu-")
    #query_with_ME("pi+ pi- mu+", 200)

    #connect("fstate_big")
    #start = datetime.now()
    #normal_results = normal_query(particles)
    #end = datetime.now()
    #print "Normal query took {}".format(end-start)
    #print "found "+str(len(normal_results))

    #for l in lazy_result:
        #if l not in normal_results:
            #print l+"  :  "+lazy_result[l]
#
    #print order_particles(['omega(782)','omega(782)'])

