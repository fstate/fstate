import json
import pickle
from particle_model import Particle
PARTICLES_LIST_PATH = "particles.txt"
#from database import *

def read_lines_from_decaydec():
    f = open(PARTICLES_LIST_PATH)
    lines = f.readlines()
    f.close()
    return lines


def line_to_dict(line):
    try:
        name = line.split("|")[1].strip()
    except:
        print("Failed to parse name in line \n"+line)
        return False
    try:
        charge = line.split("|")[3].strip()
        if "/" in charge:
            charge = float(charge.split("/")[0])/float(charge.split("/")[1])
        else:
            charge = float(charge)
    except:
        print("Failed to parse charge in line \n"+line)
        return False
    try:
        mass = float(line.split("|")[4].strip().replace(" MeV"," ").replace(" eV","e-6").replace(" GeV","e3").replace(" TeV","e6"))
    except:
        print("Failed to parse mass in line \n"+line)
        return False
    try:
        alias = [line.split("|")[7].strip()]
    except:
        print("Failed to parse alias in line \n"+line)
        return False
    try:
        antiparticle = line.split("|")[9].strip()
        if antiparticle == "self-cc":
            antiparticle=name
    except:
        print("Failed to parse antiparticle in line \n"+line)
        return False

    if antiparticle == '-':
        print("Wrong antiparticle of "+name)
        return False

    particle = {
        "name" : name,
        "charge" : charge,
        "mass" : mass,
        "alias" : alias,
        "antiparticle" : antiparticle}
    return particle


def main():

    lines = read_lines_from_decaydec()
    Particle.objects().delete()
    for part in Particle.objects():
        part.printparticle()

    for line in lines:
        if not line_to_dict(line):
            continue
        part = line_to_dict(line)
        db_part = Particle( name = part["name"],
                            charge = part["charge"],
                            mass = part["mass"],
                            alias = part["alias"],
                            antiparticle = part["antiparticle"])
        try:
            db_part.save()
        except:
            print(json.dumps(part,sort_keys=True, indent=4))
            continue

if __name__ == '__main__':
    main()