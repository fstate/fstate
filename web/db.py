from pymongo import MongoClient
from pymongo.database import DBRef

client = MongoClient()
db = client.fstate

decays = db.decays # Decays collection
fstates = db.fstates # Fstates collection

