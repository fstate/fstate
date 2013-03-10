from models import *


#This function create Particle object
#This function takes line from parsed PDF
#which looks like 'ParticleName_ParticleMass_+/-_ERROR_MeV'
#(_==SPACE)
def AddToPart(x):
    p = Particle()
    x = x[1:-1]
    word = x.split(", ")
    p.name = word[2]
    p.mass = float(word[0])
    return p
