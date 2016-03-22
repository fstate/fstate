from mongoengine import *
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from createdatabase.config import db_name

class Particle(Document):
    name = StringField(required=True)
    charge = FloatField(required=True)
    mass = FloatField(required=True)
    alias = ListField(required=True)
    antiparticle = StringField(required=True)

    def printparticle(self):
        particle = {
            "name" : self.name,
            "charge" : self.charge,
            "mass" : self.mass,
            "alias" : self.alias,
            "antiparticle" : self.antiparticle}
        print(json.dumps(particle,sort_keys=True, indent=4))
        return True

    def to_dict(self):
        particle = {
            "name" : self.name,
            "charge" : self.charge,
            "mass" : self.mass,
            "alias" : self.alias,
            "antiparticle" : self.antiparticle}
        return particle

    def to_print(self):
        if self.mass<1:
            mass = str(float(self.mass)*1000)+" keV"
        else:
            if self.mass > 1000:
                if self.mass > 1000000:
                    mass = str(float(self.mass)/1000000)+" TeV"    
                else:
                    mass = str(float(self.mass)/1000)+" GeV"
            else:
                mass = str(self.mass)+" MeV"
        particle = {
            "name" : self.name,
            "name_js" : "\""+self.name.replace("'","\'")+"\"",
            "name_html" : self.name.replace("/","__"),
            "charge" : self.charge,
            "mass" : mass,
            "alias" : self.alias,
            "antiparticle" : self.antiparticle}
        return particle

connect(db_name)
