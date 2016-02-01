import pymongo
from pymongo import MongoClient
from pymongo.database import DBRef

client = MongoClient()
db = client.fstate

# Particle collection
particles = db.particles
particles.drop()
