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

    def update_ancestors(self):
        print "Trying to update ancestors"
        for d in Decay.objects(fstate__contains = self.father):
            new_fstate = []
            #d.printdecay()
            print "Oparations of fstate"
            for p in d.fstate.split(" "):
                print p
                #if p == self.father:
                #    print "father in the fstate"
                new_fstate.append(p)
            #print "removing father"
            new_fstate.remove(self.father)
            for p in self.fstate.split(" "):
                new_fstate.append(p)
            new_br = self.branching*d.branching
            subst = self.scheme.split('; ') + d.scheme.split('; ')
            new_scheme = '; '.join(subst)
            new_dec = Decay(father = d.father,
                            scheme = new_scheme,
                            branching = new_br,
                            fstate = ' '.join(new_fstate))
            #new_dec.printdecay()
            new_dec.save()

        return True

    def do_cc(self):
        return True

connect("fstate")
