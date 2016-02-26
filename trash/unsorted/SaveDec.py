from models import *


def SaveDec(dec):
    """THIS FUNCTION SAVE DECAY OBJECT"""
    Decay ( fname     = dec.fname,
            father    = dec.father,
            daughters = dec.daughters,
            rate      = dec.rate,
            known     = dec.known,
            fstate    = dec.fstate).save()
    return
