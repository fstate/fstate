from mongoengine import *
from models import *
from test import *


def CreateList(n, ListOfDgt, rawdec, Decay):
    if not n:
        return ListOfDgt
    for dgt in Decay.objects:
        if dgt.father.name == rawdec.daughters[len(rawdec.daughters) - n]:
            n -= 1
            ListOfDgt[len(rawdec.daughters) - n] = dgt
            CreateList(n, ListOfDgt, rawdec)
