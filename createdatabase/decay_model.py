from mongoengine import *
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from web.db import ctc
from parrticleparser.particle_model import Particle
particles = {}
for part in Particle.objects():
    particles[part.name]=part.to_dict()
from config import db_name
from config import br_cutoff, max_decay_chain
from parrticleparser.nice_name import nice_name


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

    parent = StringField(required = True)
    childs = ListField(StringField(),required = True)
    nice_decay = StringField(default = "", unique = True)
    branching = FloatField(required = True)
    user_keys = StringField(default = "")

    meta = {
        #'ordering': ['branching'],
        'indexes': ['parent',
                    #{'fields': ['$fstate'],
                    #'default_language': 'english',
                    #'weights': {'fstate': 1}
                    #},
                    'childs',
                    #'$father',
                    'user_keys']
    }


    def save(self, *args, **kwargs):
        #print "Saving decay"
        self.childs = order_particles(self.childs)
        self.nice_decay = nice_name(self.parent)+" $\\to$ "+' '.join(nice_name(x) for x in self.childs)
        #self.printdecay()
        return super(Decay, self).save(*args, **kwargs)    

    def printdecay(self):
        decay = {
            "parent" : self.parent,
            "childs" : self.childs,
            "branching" : self.branching,
            "nice_decay" : self.nice_decay,
            "user_keys": self.user_keys}
        print(json.dumps(decay,sort_keys=True, indent=4))
        return True

    def to_dict(self):
        decay = {
            "parent" : self.parent,
            "childs" : self.childs,
            "branching" : self.branching,
            "nice_decay" : self.nice_decay,
            "user_keys": self.user_keys}
        return decay

    def do_cc(self):
        cc_is_done = False
        if particles[self.parent]['name']!=particles[self.parent]['antiparticle']:
            cc_is_done = True
        cc_parent = particles[self.parent]['antiparticle']
        cc_childs = []
        for part in self.childs:
            if particles[part]['name']!=particles[part]['antiparticle']:
                cc_is_done = True
            cc_childs.append(particles[part]['antiparticle'])

        new_dec = Decay(parent = cc_parent,
                        childs = cc_childs,
                        branching = self.branching,
                        user_keys = self.user_keys)
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
