from pymongo import MongoClient
from pymongo.database import DBRef

client = MongoClient()
db = client.temp_db

#decays = db.decays # Decays collection
#fstates = db.fstates # Fstates collection
new_physics = db.new_physics # Auxilary collection for new physics
new_physics.drop()