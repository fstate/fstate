from operator import mul
from copy import deepcopy
from datetime import datetime
from multiprocessing import Pool, cpu_count
from ParcticleDescriptors import *

from weight_split import get_jobs
from database import *
from NameConjugate import *


particles.drop()
particles.create_index("keys", unique=True)

def AddToDB(prt,aprt):
    try:
        particles.insert({
                        'mass': prt[0],
                        'particle': prt[1],
                        'antiparticle': aprt[1],
                        'keys': [prt[1], aprt[1]]
                        })
        print 'added '+prt[1]+' and '+aprt[1]
    except pymongo.errors.DuplicateKeyError:
    	print 'Dublicate exceprion!'
        return

for x in open("../data/masses-fin.txt").readlines():
    prt = ['mass','name','isBaryon','isNeutral']
    aprt = ['mass','name','isBaryon','isNeutral']
    prt[0] = x.split(', ')[0][1:]
    prt[1] = x.split(', ')[2][:-2]
    for b in baryons:
        if b in prt[1] or b == prt[2]:
            prt[2] = 'baryon'
    if prt[1] in ['p', 'n']:
        prt[2] = 'baryon'

    prt[3] = 0

    for n in neutrals:
    	if n in prt[1] or n == prt[1]:
    		prt[3] = 1
    
    aprt = deepcopy(prt)
    if prt[2] == 'baryon':
        aprt[1] = BaryonNameConjugate(aprt[1])
    else:
        if prt[3] != 1 or '+' in prt[1] or '-' in prt[1]:
            aprt[1] = NormalNameConjugate(aprt[1])

    #Here should be check for exclusions

    AddToDB(prt,aprt)
