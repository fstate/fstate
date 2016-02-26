#sudo mongod --fork --syslog
from models import *
from mongoengine import *
from AddToRawDec import *
from AddToPart import *
from AddToDec import *
from SaveDec import *

#connect('tdb6')
connect('DBFORRAWDEC')
Decay.objects.delete()
RawDecay.objects.delete()
Particle.objects.delete()

xfile = open("decays.txt")
xList = xfile.readlines()
for i in range(0, len(xList)):
    print xList[i].replace('\n', '')
    AddToRawDec(xList[i].replace('\n', '')).save()

xfile = open("masses-fin.txt")
xList = xfile.readlines()
for i in range(0, len(xList)):
    print xList[i].replace('\n', '')
    AddToPart(xList[i].replace('\n', '')).save()
    
"""
AddToPart('a 100').save()
AddToPart('b 70').save()
AddToPart('c 25').save()
AddToPart('d 10').save()

AddToRawDec('= 0.5 a b c').save()
AddToRawDec('= 0.3 a c c').save()
AddToRawDec('< 0.2 a c c d').save()
AddToRawDec('= 0.5 b c c').save()
AddToRawDec('= 0.2 b d d').save()
AddToRawDec('< 0.1 b d d d').save()
AddToRawDec('= 0.5 c d d d').save()
AddToRawDec('< 0.2 c d d d d').save()

for p in Particle.objects.order_by('mass'):
    print 'Particle  ' + p.name
    dec = Decay(father=p, rate=1, known=True, fname=p.name, fstate=[p.name])
    SaveDec(dec)
    for rdec in RawDecay.objects.__call__(father=p.name):
        dec = Decay()
        dec.rate = rdec.rate
        dec.known = rdec.known
        dec.father = p
        dec.fname = p.name
        n = len(rdec.daughters)
        lst = []
        fst = []
        DO = []
        for i in range(0, n):
            lst += 'a'
            DO += 'a'
            fst.insert(i, rdec.daughters[i])
        dec.fstate = fst
        for i in range(0, n):
            DO[i] = Decay.objects().__call__(fname=rdec.daughters[i])
        dec.daughters = lst
        #print len(dec.daughters)
        print 'AddToDec start'
        LOD2 = AddToDec(n, rdec, dec, DO)
        print 'AddToDec finish'
"""
