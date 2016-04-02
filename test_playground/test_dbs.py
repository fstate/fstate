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
lazy_result = {}


def lazy_query(particles, history=False, br = 1, last_hist=False):
    global lazy_result
    query_permutations = [" ".join(x) for x in set(permutations(particles, len(particles)))]
    for d in Decay.objects(fstate__in = query_permutations):
        if br*d.branching>=br_cutoff:
            #lazy_result.append(d.scheme+"; "+history+"    br: "+str(br*d.branching))
            if history:
                #print d.scheme+"; "+history
                dec = Decay(father = d.father, scheme=d.scheme+"; "+history, branching=br*d.branching, fstate=d.fstate).order_history()
                lazy_result[dec.scheme]=last_hist
            else:
                #print d.scheme
                dec = Decay(father = d.father, scheme=d.scheme, branching=br*d.branching, fstate=d.fstate).order_history()
                lazy_result[dec.scheme]=d.fstate
            #print "added "+d.scheme+"; "+history    
    small_query_subsets = []
    for len_part in range(2, len(particles)):
        for comb in set(combinations(particles, len_part)):
            small_query_subsets.append(comb)
    #    small_query_subsets = set(combinations(particles, len_part))
    for i in set(small_query_subsets):
        b = copy(particles)
        for j in i:
            b.remove(j)
        subset_permutations = [" ".join(x) for x in set(permutations(i, len(i)))]
        for d in Decay.objects(fstate__in = subset_permutations):
            c = copy(b)
            c.append(d.father)
            if br*d.branching>=br_cutoff:
                if history:
                    lazy_query(c, d.scheme+"; "+history, br*d.branching, d.scheme+"  "+history)
                else:
                    lazy_query(c, d.scheme, br*d.branching, d.scheme)
    return True

def normal_query(particles):
    query_permutations = [" ".join(x) for x in set(permutations(particles, len(particles)))]
    result = []
    #for d in Decay.objects(fstate__in = query_permutations):
    for d in Decay.objects(fstate__in = query_permutations):
        #d.printdecay()
        result.append(d.scheme)
    return result

def query_test(query):
    particles = query.split(" ")
    
    start = datetime.now()
    lazy_query(particles)
    end = datetime.now()
    print "Search for "+query+" took {}".format(end-start)
    print "found "+str(len(lazy_result))
    return True

if __name__ == "__main__":
    from config import db_name
    connect(db_name)
    print "connected"

    query_test("pi+ pi- mu+ mu-")
    query_test("pi+ pi-")
    query_test("pi+ pi- K+ K-")    
    query_test("pi+ pi+ pi+ pi- pi- pi-")

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

