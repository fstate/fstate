from mongoengine import *
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parrticleparser.particle_model import Particle
particles = {}
for part in Particle.objects():
    particles[part.name]=part.to_dict()
from config import db_name
from config import br_cutoff, max_decay_chain

def order_particles(p_list):
    DATA=[]
    for p in p_list:
        DATA.append((p, particles[p]['mass'], particles[p]['charge']))
    DATA.sort(key=lambda row:row[2], reverse=True)
    DATA.sort(key=lambda row: row[1], reverse=True)
    o_list=[]
    for d in DATA:
        o_list.append(d[0])
    return o_list



class Decay(Document):

    father = StringField(required = True)
    scheme = StringField(required = True, unique=True)
    branching = FloatField(required = True)
    fstate = StringField(required = True)
    user_keys = StringField(default = "")
    primal_decay = BooleanField(default=False)

    meta = {
        'ordering': ['branching'],
        'indexes': ['fstate',
                    #{'fields': ['$fstate'],
                    #'default_language': 'english',
                    #'weights': {'fstate': 1}
                    #},
                    'father',
                    #'$father',
                    'user_keys']
    }


    def save(self, *args, **kwargs):
        if self.scheme.count("-->")==1:
            self.primal_decay = True
        return super(Decay, self).save(*args, **kwargs)    

    def printdecay(self):
        decay = {
            "father" : self.father,
            "scheme" : self.scheme,
            "branching" : self.branching,
            "fstate" : self.fstate,
            "user_keys": self.user_keys}
        print(json.dumps(decay,sort_keys=True, indent=4))
        return True

    def to_dict(self):
        decay = {
            "father" : self.father,
            "scheme" : self.scheme,
            "branching" : self.branching,
            "fstate" : self.fstate,
            "user_keys": self.user_keys}
        return decay

    def order_history(self):
        """
        This function orders history in standard way:
            - Heavy particles go first
            - Charged prticles ordred as such: + 0 -
        "D(2S)+ --> D*(2010)+ pi0; D*(2010)+ --> D+ pi0; pi0 --> gamma gamma"            
        """
        #return True
        new_history = []
        #print(self.scheme)
        decs = self.scheme.split("; ")
        p_decs={}
        for d in decs:
            father = d.split(" ")[0]
            daughters = d.split(" --> ")[1].split(" ")
            p_decs[father]=father+' --> '+' '.join(order_particles(daughters))
        for f in order_particles(p_decs.keys()):
            new_history.append(p_decs[f])
        #print "history ordered from "+self.scheme+" to "+'; '.join(new_history)
        self.scheme='; '.join(new_history)
        return self

    def update_ancestors(self):
        #print("Trying to update ancestors")
        for d in Decay.objects(fstate__contains = self.father):
        #for d in Decay.objects.search_text(self.father):
            if (len(d.fstate.split(" "))-1+len(self.fstate.split(" "))) >= max_decay_chain:
                #print ("Ancestor has too many daughters")
                continue
            if self.father not in d.fstate:
                #print "Tried to add decay of "+self.father+" to decay, but "+self.father+" not found in final state:"
                #d.printdecay()
                continue
            #print("Updating "+d.scheme)
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
            if new_br < br_cutoff:
                #print ("Ancestor has too small branching.")
                continue
            subst = self.scheme.split('; ') + d.scheme.split('; ')
            new_scheme = '; '.join(subst)
            #print("updated scheme: "+new_scheme)
            new_dec = Decay(father = d.father,
                            scheme = new_scheme,
                            branching = new_br,
                            fstate = ' '.join(new_fstate),
                            user_keys = d.user_keys+self.user_keys).order_history()
            new_dec.printdecay()
            try:
                new_dec.save()
            except NotUniqueError:
                pass

        return True

    def do_cc(self):
        cc_is_done = False
        if particles[self.father]['name']!=particles[self.father]['antiparticle']:
            cc_is_done = True
        cc_father = particles[self.father]['antiparticle']
        cc_fstate = ""
        for part in self.fstate.split(" "):
            if particles[part]['name']!=particles[part]['antiparticle']:
                cc_is_done = True
                cc_fstate += particles[part]['antiparticle']+" "

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

            if particles[part]['name']!=particles[part]['antiparticle']:
                cc_is_done = True 
            if have_comma:
                cc_scheme += particles[part]['antiparticle']+"; "
            else:
                cc_scheme += particles[part]['antiparticle']+" "
        cc_scheme =cc_scheme[:-1]
        new_dec = Decay(father = cc_father,
                        scheme = cc_scheme,
                        branching = self.branching,
                        fstate = cc_fstate,
                        user_keys = self.user_keys).order_history()
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


connect(db_name)
