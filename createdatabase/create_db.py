import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parrticleparser.particle_model import Particle
import pickle
import json
from decay_model import Decay
import copy
from config import br_cutoff, max_decay_chain
#class Decay(Document):
#    father = StringField(required = True)
#    scheme = StringField(required = True, unique = True)
#    branching = FloatField(required = True)
#    fstate = ListField(required = True)



with open('../decaydecparser/parsed_decays.pkl', 'r') as basket:
    test_set = pickle.load(basket)


def add_decay(father, decay, history = "", uniterated_daughters = []):
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
    """
    global br_cutoff
    if history == "":
        history = "{} --> {}".format(father, ' '.join(decay['daughters']))
    #if uniterated_daughters == []:
    #    uniterated_daughters = decay["daughters"]
    if ((decay["branching"]>br_cutoff) and (1<len(decay["daughters"])<max_decay_chain)):
        db_dec = Decay(father = father, scheme = history, branching = decay["branching"], fstate = ' '.join(decay["daughters"]))
        #db_dec.printdecay()
        try:
            db_dec.save()
        except:
            print "Failed to save decay!"
            db_dec.printdecay()
        if uniterated_daughters:
            for i, daughter in enumerate(uniterated_daughters):
                for saved_dec in Decay.objects(father = daughter):
                    subst = history.split('; ') + saved_dec.scheme.split('; ')
                    new_history = '; '.join(subst[:1] + sorted(subst[1:]))
                    daughters = []
                    for d in decay["daughters"]:
                        if d!=daughter:
                            daughters.append(d)
                    for d in saved_dec.fstate.split(' '):
                        daughters.append(d)
                    #print "Was : "
                    #print decay["daughters"]
                    #print "Became : "
                    #print daughters
                    new_uniterated_daughters = []
                    for d in uniterated_daughters:
                        if d!=daughter:
                            new_uniterated_daughters.append(d)
                    branching = decay["branching"]*saved_dec.branching
                    new_decay = {"branching":branching, "daughters":copy.deepcopy(daughters)}
                    if i == 0:
                        add_decay(father, new_decay, new_history, new_uniterated_daughters)
                    else:
                        add_decay(father, new_decay, new_history, [])
    return True





def main():
    Decay.objects().delete()
    for part in Particle.objects().order_by('mass'):
        print "Working on "+part.name
        if part.name in test_set['decays']:
            for dec in test_set['decays'][part.name]:                
                add_decay(part.name, dec, "", dec["daughters"])
            #print part.name + " found!"        
        #else:
            #print part.name + " not found!"        
    #print json.dumps(test_set, sort_keys=True, indent=4)



if __name__ == '__main__':
    main()