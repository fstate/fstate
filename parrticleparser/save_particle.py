import json
from particle_model import Particle
from database import *

def save_particle_to_db(name, charge, mass, antiparticle, alias=[], antiparticle_alias=[]):
    """
    This function save particle to db.
    name - name of a partilce, string
    charge - charge of a particle, float
    mass - mass of a particle in MeV, float
    antiparticle - name of a charge-conjugate particle. 
    In case if particle is self-conjugate, antiparticle == name
    alias - possible names for this particle. 
    antiparticle_alias - possible names for its anti-particle. 
    """
    db_part = Particle( name = name,
                        charge = charge,
                        mass = mass,
                        alias = alias,
                        antiparticle = antiparticle)
    try: 
        db_part.save()
    except:
        print "Failed to save particle:"
        print json.dumps(part,sort_keys=True, indent=4)
        return False
    if not antiparticle == name:
        db_part = Particle( name = antiparticle,
                            charge = -charge,
                            mass = mass,
                            alias = antiparticle_alias,
                            antiparticle = name)
        try: 
            db_part.save()
        except:
            print "Failed to save particle:"
            print json.dumps(part,sort_keys=True, indent=4)
            return False
    return True
