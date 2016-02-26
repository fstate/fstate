from mongoengine import *
import json

class Decay(Document):

    father = StringField(required = True)
    scheme = StringField(required = True)
    branching = FloatField(required = True)
    fstate = StringField(required = True)

    meta = {
        'ordering': ['branching'],
        'indexes': ['fstate']
    }
    def printdecay(self):
        decay = {
            "father" : self.father,
            "scheme" : self.scheme,
            "branching" : self.branching,
            "fstate" : self.fstate}
        print json.dumps(decay,sort_keys=True, indent=4)
        return True

    def to_dict(self):
        decay = {
            "father" : self.father,
            "scheme" : self.scheme,
            "branching" : self.branching,
            "fstate" : self.fstate}
        return decay

    def do_cc(self):
        return True

connect("fstate")
