import json
from pymongo import MongoClient
from fstate import Decay

client = MongoClient()
db = client.fstate
goodies = db.decays
badies  = db.badies

goodies.drop()
badies.drop()


decays = json.loads(open('../data/alldecays.json').read())

if __name__ == '__main__':
    for dec in decays:
        try:
            d = Decay(dec)
            goodies.insert(dec)
            print "Added:", dec['decay']

        except Exception, e:
    	   badies.insert({"error": str(e), "decay": dec})
           print e ,":", dec['decay']