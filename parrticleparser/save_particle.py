import json
from particle_model import Particle

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
    if alias == []:
        alias.append(name)        
    db_part = Particle( name = name,
                        charge = charge,
                        mass = mass,
                        alias = alias,
                        antiparticle = antiparticle)
    try: 
        db_part.save()
    except:
        print "Failed to save particle:"
        print json.dumps(db_part.to_dict(),sort_keys=True, indent=4)
        return False
    if not antiparticle == name:
        if antiparticle_alias == []:
            antiparticle_alias.append(antiparticle)        
        db_part = Particle( name = antiparticle,
                            charge = -charge,
                            mass = mass,
                            alias = antiparticle_alias,
                            antiparticle = name)
        try: 
            db_part.save()
        except:
            print "Failed to save particle:"
            print json.dumps(db_part.to_dict(),sort_keys=True, indent=4)
            return False
    return True


if __name__ == '__main__':
    print "Example of adding particle to DB"
    print "We will add particle 'Delta-'"
    for p in Particle.objects(name = 'Delta-'):
        p.printparticle()    
    print "First, let's remove if from DB together with its CC"
    Particle.objects(name = 'Delta-').delete()
    Particle.objects(name = 'Delta~+').delete()
    print "Ans let's check if it is deleted:"
    for p in Particle.objects(name__in = ['Delta-','Delta~+']):
        p.printparticle()
    print "Now let's add it:"
    save_particle_to_db(
    name = "Delta-",
    charge = -1.0,
    mass = 1232.0,
    antiparticle = "Delta~+")
    print "And let's check if Delta- is here:"
    for p in Particle.objects(name = 'Delta-'):
        p.printparticle()    
    print "And it's antiparticle:"
    for p in Particle.objects(name = 'Delta~+'):
        p.printparticle()        