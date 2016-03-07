from mongoengine import *
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parrticleparser.particle_model import Particle

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
            #print "Oparations of fstate"
            for p in d.fstate.split(" "):
                #print p
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
        cc_is_done = False
        for p in Particle.objects(name = self.father):
            if p.name != p.antiparticle:
                cc_is_done = True 
            cc_father = p.antiparticle
            break
        cc_fstate = ""
        for part in self.fstate.split(" "):
            #if not Particle.objects(name = part):
                #print part+" not in particle db!"
                #print "Failed to cc decay"
                #return False
            for p in Particle.objects(name = part):
                if p.name != p.antiparticle:
                   cc_is_done = True 
                cc_fstate += p.antiparticle+" "                
                break

        cc_fstate =cc_fstate[:-1]
        cc_scheme=""
        for part in self.scheme.split(" "):
            if part == "-->":
                cc_scheme += part+" "
                continue
            have_comma = False
            if part[-1]==";":
                have_comma=True
                part = part[:-1]
            #if not Particle.objects(name = part):
                #print part+" not in particle db!"
                #print "Failed to cc decay"
                #return False
            for p in Particle.objects(name = part):
                if p.name != p.antiparticle:
                   cc_is_done = True 

                if have_comma:
                    cc_scheme += p.antiparticle+"; "
                else:
                    cc_scheme += p.antiparticle+" "
                break
        cc_scheme =cc_scheme[:-1]
        new_dec = Decay(father = cc_father,
                        scheme = cc_scheme,
                        branching = self.branching,
                        fstate = cc_fstate)
        if cc_is_done:
            #print "Decay cc-ed:"
            #self.printdecay()
            #print " to :"
            #new_dec.printdecay()
            return new_dec
        else:
            #print "Failed to cc decay:"
            #self.printdecay()
            return False


connect("fstate")
