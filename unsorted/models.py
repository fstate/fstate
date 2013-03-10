from mongoengine import *


#Additional class
class RawDecay(DynamicDocument):
    #name of father
    father = StringField()

    #List of daughers names
    daughters = ListField(StringField())

    #Branching ratio
    rate = FloatField()

    #Known or just limit
    known = BooleanField()

    #magic
    allow_inheritance = False
    meta = {'collection': 'RawDecay'}


#Additional class, containing all known particles
class Particle(Document):
    name = StringField()
    mass = FloatField()
    allow_inheritance = False
    meta = {'collection': 'Particle'}
    #_id   = StringField()
    #_type = StringField()
    #_ignored_scraped_sessions = ListField()


#Main class connecting all DB
class Decay(DynamicDocument):
    #Father name, normally fname==father.name
    fname = StringField()

    #father of decay
    father = ReferenceField(Particle)

    #List of daughter Decays
    daughters = ListField()

    #Branching ratio
    rate = FloatField()

    #Precise value or just limit
    known = BooleanField()

    #magic
    allow_inheritance = False
    meta = {'collection': 'Decay'}

    #List of final state. Used in search.
    fstate = ListField()

connect('tdb5')
