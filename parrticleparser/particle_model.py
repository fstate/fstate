from mongoengine import *
import json

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
        print json.dumps(particle,sort_keys=True, indent=4)
        return True

connect("fstate")
