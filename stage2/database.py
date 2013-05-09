import pymongo
from pymongo import MongoClient
from pymongo.database import DBRef

client = MongoClient()
db = client.fstate


# Decays collection
decays = db.decays
decays.drop()

# Fstates collection
fstates = db.fstates
fstates.drop()
fstates.create_index("fstate")
fstates.create_index("scheme", unique=True)
