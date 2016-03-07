import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parrticleparser.particle_model import Particle
from decaydecparser.parser import check_if_particle_exist
import pickle
import json
from decay_model import Decay
import copy
from config import br_cutoff, max_decay_chain


def add_decay(father, decay, history = "", uniterated_daughters = [], test_mode=False):
    """
    Father = <Name of a particle from particle DB>
    decay = {
                "branching": 0.0175,
                "daughters": [
                    "e-",
                    "nu_e~",
                    "nu_tau",
                    "gamma"
                ]
            }
    This function add decay to the existing DB (No need to full rebuild)
    Please keep in mind, that all particles in the decay should be in particle DB 
    """
    global br_cutoff

    if history == "":
        history = "{} --> {}".format(father, ' '.join(decay['daughters']))
    for d in decay['daughters']:
        if not check_if_particle_exist(d):
            print "Trying to add decay of "+father
            print json.dumps(decay,sort_keys=True, indent=4)
            print "with unexisting particle   "+d
            return False
    if ((decay["branching"]>br_cutoff) and (1<len(decay["daughters"])<max_decay_chain)):
        db_dec = Decay(father = father, scheme = history, branching = decay["branching"], fstate = ' '.join(decay["daughters"]))
        if test_mode:
            print "Trying to save decay:"
            db_dec.printdecay()
        try:
            db_dec.save()
            if test_mode:
                print "Decay saved!"
        except:
            print "Failed to save decay!"
            db_dec.printdecay()
            
        try:
            #Now need to update all decays having this particle in final state with this mode of decay
            db_dec.update_ancestors()
            if test_mode:
                print "Ancestors updated!"
        except:
            print "Failed to update ancestors"
            db_dec.printdecay()
        
        if test_mode:
            print "cc-ing decay"
        db_dec_cc = db_dec.do_cc()
        if db_dec_cc:
            if test_mode:
                print "decay cc-ed"
            db_dec_cc.save()
            db_dec_cc.update_ancestors()
        elif test_mode:
            print "failed to cc decay"

        if uniterated_daughters:
            if test_mode:
                print "Iterating over the daughters"
            for i, daughter in enumerate(uniterated_daughters):
                if test_mode:
                    print "Daughter "+daughter
                for saved_dec in Decay.objects(father = daughter):
                    if test_mode:
                        print "decay: "+saved_dec.scheme
                    subst = history.split('; ') + saved_dec.scheme.split('; ')
                    new_history = '; '.join(subst[:1] + sorted(subst[1:]))
                    daughters = []
                    for d in decay["daughters"]:
                        if d!=daughter:
                            daughters.append(d)
                    for d in saved_dec.fstate.split(' '):
                        daughters.append(d)
                    new_uniterated_daughters = []
                    for d in uniterated_daughters:
                        if d!=daughter:
                            new_uniterated_daughters.append(d)
                    branching = decay["branching"]*saved_dec.branching
                    new_decay = {"branching":branching, "daughters":copy.deepcopy(daughters)}
                    if i == 0:
                        add_decay(father, new_decay, new_history, new_uniterated_daughters, test_mode)
                    else:
                        add_decay(father, new_decay, new_history, [], test_mode)
    return True

if __name__ == '__main__':
    print "Example of adding decay to DB"

    father = 'K+'
    decay = {"branching":0.99,
            "daughters" : ['e+','gamma' ]}

    print "Lets add this decay:"
    json.dumps(decay, sort_keys=True, indent=4)
    add_decay(father, decay, "", decay['daughters'], test_mode = True)

