import json
import pickle
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#from database import *
from parrticleparser.particle_model import Particle

DECAY_DEC_PATH = "DECAY.DEC"
MODELS = set(["PHSP", "PHSP;", "PHSP; ", "HELAMP", "ISGW2;", "PHOTOS", "SVS", "SVS;", "SVV_HELAMP", "PYTHIA", "HQET2", "HQET2;", "ISGW2;","VVS_PWAVE","TAUSCALARNU","VSP_PWAVE;","VUB","VUB;","BTOXSGAMMA","SLN;","SLN","CB3PI-MPP","VSS","VSS;", "VSS; ","VSS_BMIX","VVPIPI;","VVPIPI;2","PARTWAVE","BTO3PI_CP","CB3PI-P00","STS;","SVP_HELAMP","BTOSLLALI;","TAUSCALARNU;","TAUHADNU","TAUVECTORNU;","D_DALITZ;","D_DALITZ;","PARTWAVE","PI0_DALITZ;","ETA_DALITZ;","OMEGA_DALITZ;","SVP_HELAMP","VVPIPI;","PARTWAVE","VVP","VLL;","BaryonPCR","TSS;","TVS_PWAVE"])

ALIAS = {"K*L": "K*0",
         "K*S": "K*0",
         "K*BL": "anti-K*0",
         "K*BS": "anti-K*0",
         "K*0T": "K*0",
         "anti-K*0T": "anti-K*0",
         "K*BR": "anti-K*0",
         "K*0R": "K*0",
         "anti-K_0*0N": "anti-K_0*0",
         "K_0*0N": "K_0*0"}

# Global dict to return
result = {
    'Define': {},
    'Alias': {},
    'ChargeConj': {},
    'decays': {}
}

particles = []

current_particle = None

def fill_particles():
    """
    Fill particles list from known particles in data/particles.txt
    """
    return True

def check_if_particle_exist(particle):
    """
    Check if this particle is known before add it to list!
    """
    for p in Particle.objects(alias=particle):
        return p.name
    for p in Particle.objects(name=particle):
        return p.name
    if particle in ALIAS.keys():
        return check_if_particle_exist(ALIAS[particle])
    return False

def read_lines_from_decaydec():
    f = open(DECAY_DEC_PATH)
    lines = f.readlines()
    f.close()
    return lines


def split_line_to_tokens(line):
    # Remove commented part
    line = line.strip().split("#")[0]
    if line == "":
        return None

    # Split line by spaces, remove empty parts
    return [tok for tok in line.split() if tok != ""]


def process_decay(tokens):
    # Example: ['0.000127000', 'anti-Sigma+', 'gamma', 'PHSP;']
    result = {
        "branching": float(tokens[0]),
        "daughters": []
    }
    for d in tokens[1:]:
        if d in MODELS:
            break
        if d in ALIAS:
            d = ALIAS[d]
        #We have a big enough list of Models, we need to add more smart things here.
        if not check_if_particle_exist(d):
            print("Unknown particle "+d)
            #break
            return False
        d=check_if_particle_exist(d)
        result['daughters'].append(d)
    if result['daughters'] == []:
        print("Empty fstate!")
        return False
    return result


def process_tokens(tokens):
    global current_particle

    if tokens[0] in set(["Define", "Alias", "ChargeConj"]):
        assert len(tokens) == 3, str(tokens)
        key = tokens[1]
        value = tokens[2]
        result[tokens[0]][key] = value
    elif tokens[0] == "Decay":
        if not check_if_particle_exist(tokens[1]):
            print ("Please add alias for "+tokens[1])
            current_particle = None
            return "Please add alias for "+tokens[1]
        current_particle = check_if_particle_exist(tokens[1])
        result["decays"][current_particle] = []
    elif tokens[0] == "Enddecay":
        current_particle = None
    elif current_particle:
        if process_decay(tokens):
            result['decays'][current_particle].append(process_decay(tokens))
        else:
            print("problem with decay of "+current_particle)
    else:
        print("Dont know what to do with:", tokens)


def main():
    lines = read_lines_from_decaydec()

    for line in lines:
        tokens = split_line_to_tokens(line)
        if not tokens:
            continue

        process_tokens(tokens)
    #print json.dumps(result, sort_keys=True, indent=4)
    with open('parsed_decays.pkl', 'wb') as basket:
        pickle.dump(result, basket)
    #    return p.name
    #print result['decays'].keys()


if __name__ == '__main__':
    print("Check c-hadrons: "+str(check_if_particle_exist('c-hadron')))
    main()