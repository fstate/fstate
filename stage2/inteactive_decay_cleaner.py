from itertools import izip
from copy import deepcopy
from database import *
from operator import mul
from datetime import datetime
from multiprocessing import Pool, cpu_count
from weight_split import get_jobs
import re



#from fixes import fixlist, multiplexers

from mfix import *

def process(decay):

    decay += " "
    print decay
    branching = decay.split('|')[0]
    decay = decay.split('|')[1]

    if Wrong(decay):
        ManualFix(decay, branching)
    else:
        NormalRecord(decay, branching)


decays = [re.sub(r'(\([0-9.e-]*, [0-9.e-]*\))', r'\1|', x).rstrip()
          for x in open('../data/decays.txt').readlines()]  # branching check

for decay in decays:
    process(decay)
