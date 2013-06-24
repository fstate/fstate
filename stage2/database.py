import pymongo
from pymongo import MongoClient
from pymongo.database import DBRef

client = MongoClient()
db = client.fstate


# Decays collection
decays = db.decays
decays.drop()

# Particle collection
particles = db.particles

# Fstates collection
fstates = db.fstates
