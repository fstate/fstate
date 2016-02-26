from models import *
from SaveDec import *


def AddToDec(n, rdec, dec, DO):
    if n == 0:
        dec.fstate = []
        dec.known = rdec.known
        #this cycle create correct fstate:
        for i in range(0, len(dec.daughters)):
            dec.known = bool(dec.known * dec.daughters[i].known)
            for j in range(0, len(dec.daughters[i].fstate)):
                dec.fstate.insert(len(dec.fstate), dec.daughters[i].fstate[j])
        #this is just for check
        #if dec.fname == u'b':
        #    print dec.fstate
        SaveDec(dec)
        return

    n -= 1
    for dgt in DO[len(rdec.daughters) - n - 1]:
        dec.daughters[len(rdec.daughters) - n - 1] = dgt
        AddToDec(n, rdec, dec, DO)
