from mongoengine import *

class Decay(Document):
    parent = StringField(required=True)
    fstate = StringField(required=True)
    branching = FloatField(required=True)

    meta = {
        'ordering': ['branching'],
        'indexes': ['fstate']
    }

    def __unicode__(self):
        return "{} -> {}".format(self.parent, self.fstate)



connect("fstate")
