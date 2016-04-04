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
    if len(decay['products'])>max_decay_chain:
        return
    if len(decay['products'])<1:
        return 
    #print decay['history'], decay['products']
    db_dec = Decay(father = decay['father'], scheme = decay['history'], branching = decay["branching"], fstate = ' '.join(decay['products'])).order_history()
    #db_dec.printdecay()
    try:
        db_dec.save()
    except:
        #print "Failed to save decay!"
        #db_dec.printdecay()
        return
