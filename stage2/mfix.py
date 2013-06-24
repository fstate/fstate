from NameConjugate import *
from database import *

bosons = ['W','Z','gamma']
leptons = ['e','mu','tau','nu_e','nu_mu','nu_tau']
mesons = ['pi','K']
baryons = ['N','Omega', 'Delta', 'Lambda', 'Sigma', 'Xi', 'Chi']

neutrals = ['Z', 'gamma', 'pi', 'b', 'rho', 'a', 'eta', 'h', 'omega', 'phi', 'f', 'X', 'chi', 'psi', 'Y']

prt = ['-->']

d = particles.find()

for i in range (0, d.count()):
    p = particles.find()[i]
    if p['particle'] == p['antiparticle']:
        prt.append(p['particle'])
    else:
        prt.append(p['particle'])
        prt.append(p['antiparticle'])


def ATDB(mass, name, antiname):
    try:
        particles.insert({
                        'mass': mass,
                        'particle': name,
                        'antiparticle': antiname,
                        'keys': [name, antiname]
                        })
        print 'added '+name+' and '+antiname
    except pymongo.errors.DuplicateKeyError:
        print 'Dublicate exceprion!'
        return


def Wrong(decay):
    global prt
    for p in prt:
    	print p
    parts = decay.split(' ')

    for particle in parts:
        if (not particle in prt) and (particle != ''):
            return True
    return False

def AddPaticle(particle):
    global baryons, neutrals
    mass = particle.split(' ')[0]
    name = particle.split(' ')[1]
    line = '('+mass+', '+'0.0, '+name+')\n'
    with open("AdditionalParticles.txt", "a") as f:
        f.write(line)
    baryon = False
    neutral = False
    for b in baryons:
        if b in name:
            baryon = True
    for n in neutrals:
        if n in name:
            neutral = True
    antiname = name
    if baryon:
        antiname = BaryonNameConjugate(name)
    else:
        if not neutral or '+' in name or '-' in name:
            antiname = NormalNameConjugate(name)
    ATDB(mass, name, antiname)
    return

def ManualFix(decay, branching):
    print 'Input this decay correctly '
    print decay
    line = ''
    while True:
        line = raw_input()
        if line.split(' ')[0]=='addparticle':
            AddParticle(line.replace('addparticle ','')) 
        elif line == 'end':
            return
        else:
            NormalRecord(line, branching)
    return

def Conjugate(decay):
    d = particles.find()
    parts = decay.split(' ')
    cdec=''
    for p in parts:
        if p == '-->':
            cdec += '--> '
        else:
            for i in range (0, d.count()):
                j = particles.find()[i]
                if p == j['antiparticle']:
                    cdec = cdec + j['particle'] + ' '
                    continue
                elif p == j['particle']:
                    cdec = cdec + j['antiparticle'] + ' '
                    continue
    return cdec

def NormalRecord(decay, branching):
    with open("CorrectDecays.txt", "a") as f:
        f.write( branching + "|" + decay + '\n')
    decay = Conjugate(decay)
    with open("CorrectDecays.txt", "a") as f:
        f.write( branching + "|" + decay + '\n')
    return