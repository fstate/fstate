from mfix import Wrong
from AutomaticFixes import *

def AutomaticFixes(decay, branching):

    if ' phi ' in decay:
        new_decay = decay.replace(' phi ', ' phi(1020) ')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)

    if ' sigma' in decay:
        new_decay = decay.replace(' sigma', ' f_0()(500)')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)

    if ' + c.c.' in decay:
        new_decay = decay.replace(' + c.c.', '')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)

    if 'K Kbar^*(892)' in decay:
        new_decay = decay.replace('K Kbar^*(892)', 'K+ K^*(892)-')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)
        new_decay = decay.replace('K Kbar^*(892)', 'K0 Kbar^*(892)0')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)   

    if 'K Kbar ' in decay:
        new_decay = decay.replace('K Kbar', 'K+ K- ')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)
        new_decay = decay.replace('K Kbar', 'K0 Kbar0 ')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)

    if 'pi pi' in decay:
        new_decay = decay.replace('pi pi', 'pi+ pi-')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)
        new_decay = decay.replace('pi pi', 'pi0 pi0')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)

    if '2pi' in decay:
        new_decay = decay.replace('2pi', 'pi+ pi-')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)
        new_decay = decay.replace('2pi', 'pi0 pi0')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)

    if '3pi' in decay:
        new_decay = decay.replace('3pi', 'pi+ pi- pi0')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)
        new_decay = decay.replace('3pi', 'pi0 pi0 pi0')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)

    if ' 3 pi' in decay:
        new_decay = decay.replace(' 3 pi', ' pi+ pi- pi0')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)
        new_decay = decay.replace(' 3 pi', ' pi0 pi0 pi0')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)

    if '4pi' in decay:
        new_decay = decay.replace('4pi', 'pi+ pi- pi+ pi-')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)
        new_decay = decay.replace('4pi', 'pi0 pi0 pi0 pi0')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)
        new_decay = decay.replace('4pi', 'pi0 pi0 pi+ pi-')
        if Wrong(new_decay):
            ManualFix(new_decay, branching)
        else:
            NormalRecord(new_decay, branching)
    return False