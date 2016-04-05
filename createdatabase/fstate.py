from itertools import izip
from copy import deepcopy
#from database import *
from make_fstates import db
from config import br_cutoff, max_decay_chain
import json
from decay_model import Decay


def get_fstates(decay):
    global db
    global br_cutoff
    if decay['branching'] < br_cutoff:
        return
    if decay['branching'] > 1:
        return
    if len(decay['childs'])>max_decay_chain:
        return
    if len(decay['childs'])<1:
        return 
    #print decay['history'], decay['products']
    db_dec = Decay(parent = decay['parent'], childs = decay['childs'], branching = decay["branching"])
    #db_dec.printdecay()
    #db_dec.save()
    try:
        db_dec.save()
    except:
        print "Failed to save decay!"
        db_dec.printdecay()
        return
