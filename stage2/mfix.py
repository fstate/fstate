from NameConjugate import *
from database import *

bosons = ['W','Z','gamma']
leptons = ['e','mu','tau','nu_e','nu_mu','nu_tau']
mesons = ['pi','K']
baryons = ['N','Omega', 'Delta', 'Lambda', 'Sigma', 'Xi', 'Chi']
neutrals = ['Z', 'gamma', 'pi', 'b', 'rho', 'a', 'eta', 'h', 'omega', 'phi', 'f', 'X', 'chi', 'psi', 'Y']
trash = ["u", "d", "c", "s", "b", "g", "q", "anything", "3h+", "2h-", "h+", "h-" "particles", "X",
            "dummy", "other", "modes", "X-", "invisible", "neutrals", "tracks",
            "fit", "except", "prongs", "total","hadrons","semitauic","semimuic","semieic","any","noncharmed",'X_u','X_c',
            "charm","charmless","hadron+","hadron-","sbar","cbar","(X)",'virtual']

def Record(decay, branching):
    if Wrong(decay):
        ManualFix(decay, branching)
    else:
        NormalRecord(decay, branching)
    return

def GetParticles():
    prt = ['-->']
    d = particles.find()
    for i in range (0, d.count()):
        p = particles.find()[i]
        if p['particle'] == p['antiparticle']:
            prt.append(p['particle'])
        else:
            prt.append(p['particle'])
            prt.append(p['antiparticle'])
    return prt


def GetExceptions():
    exceptions = {}
    rawexp = [re.sub(r'(\s replace \s with \s)', r'\1', x).rstrip() for x in open('Exceptions.txt').readlines()] 
    for rex in rawexp:
        #sex = splitted esception
        sex = rex.split(' replace with ')
        if not sex[0] in exceptions:
            exceptions[sex[0]] = [sex[1]]
        else:
            exceptions[sex[0]].append(sex[1])
    return exceptions

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
        print 'Dublicate exception!'
        return

def AutomaticFixes(decay, branching):


    if ' K_0^*(1430) ' in decay:
        new_decay = decay.replace(' K_0^*(1430) ', ' K_0()*(1430) ')
        Record(new_decay, branching)
        return True    

    if ' phi ' in decay:
        new_decay = decay.replace(' phi ', ' phi(1020) ')
        Record(new_decay, branching)
        return True       
        
    if ' 2pi+ ' in decay:
        new_decay = decay.replace(' 2pi+ ', ' pi+ pi+ ')
        Record(new_decay, branching)
        return True    

    if ' 2pi- ' in decay:
        new_decay = decay.replace(' 2pi- ', ' pi- pi- ')
        Record(new_decay, branching)
        return True    

    if ' 2pi0 ' in decay:
        new_decay = decay.replace(' 2pi0 ', ' pi0 pi0 ')
        Record(new_decay, branching)
        return True    

    if ' 3pi0 ' in decay:
        new_decay = decay.replace(' 3pi0 ', ' pi0 pi0 pi0 ')
        Record(new_decay, branching)
        return True    

    if ' rho0 ' in decay:
        new_decay = decay.replace(' rho0 ', ' rho(770) ')
        Record(new_decay, branching)
        return True       
 
    if ' f_0(500)' in decay:
        new_decay = decay.replace(' f_0(500)', ' f_0()(500)')
        Record(new_decay, branching)
        return True  

    if ' sigma' in decay:
        new_decay = decay.replace(' sigma', ' f_0()(500)')
        Record(new_decay, branching)
        return True    

    if ' + c.c.' in decay:
        new_decay = decay.replace(' + c.c.', '')
        Record(new_decay, branching)
        return True    

    if 'K Kbar^*(892)' in decay:
        new_decay = decay.replace('K Kbar^*(892)', 'K+ K^*(892)-')
        Record(new_decay, branching)
        new_decay = decay.replace('K Kbar^*(892)', 'K0 Kbar^*(892)0')
        Record(new_decay, branching)
        return True    

    if 'K Kbar ' in decay:
        new_decay = decay.replace('K Kbar', 'K+ K- ')
        Record(new_decay, branching)
        new_decay = decay.replace('K Kbar', 'K0 Kbar0 ')
        Record(new_decay, branching)
        return True    

    if ' pi pi ' in decay:
        new_decay = decay.replace(' pi pi ', ' pi+ pi- ')
        Record(new_decay, branching)
        new_decay = decay.replace(' pi pi ', ' pi0 pi0 ')
        Record(new_decay, branching)
        return True    

    if ' 2pi ' in decay:
        new_decay = decay.replace(' 2pi ', ' pi+ pi- ')
        Record(new_decay, branching)
        new_decay = decay.replace(' 2pi ', ' pi0 pi0 ')
        Record(new_decay, branching)
        return True    

    if ' 3pi ' in decay:
        new_decay = decay.replace(' 3pi ', ' pi+ pi- pi0 ')
        Record(new_decay, branching)
        new_decay = decay.replace(' 3pi ', ' pi0 pi0 pi0 ')
        Record(new_decay, branching)
        return True    

    if ' 3 pi' in decay:
        new_decay = decay.replace(' 3 pi ', ' pi+ pi- pi0 ')
        Record(new_decay, branching)
        new_decay = decay.replace(' 3 pi ', ' pi0 pi0 pi0 ')
        Record(new_decay, branching)
        return True    

    if ' 4pi ' in decay:
        new_decay = decay.replace(' 4pi ', ' pi+ pi- pi+ pi- ')
        Record(new_decay, branching)
        new_decay = decay.replace(' 4pi ', ' pi0 pi0 pi0 pi0 ')
        Record(new_decay, branching)
        new_decay = decay.replace(' 4pi ', ' pi0 pi0 pi+ pi- ')
        Record(new_decay, branching)
        return True    
    return False

def Wrong(decay):
    prt = GetParticles()
    #for p in prt:
    #    print p
    parts = decay.split(' ')

    for particle in parts:
        if (not particle in prt) and (particle != ''):
            print "Problem with particle "+particle
            return True
    return False

def AddException(decay, correctdecay):
    with open("Exceptions.txt", "a") as f:
        f.write( decay + " replace with " + correctdecay + '\n')
    return

def KnownException(decay):
    exceptions = GetExceptions()
    if decay in exceptions:
        return True
    return False

def AddParticle(particle):
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
    global trash
    exceptions = GetExceptions()
    parts = decay.split(' ')
    for particle in parts:
        if particle in trash:
            return
    if not KnownException(decay):
    	if AutomaticFixes(decay, branching):
    		return
        print 'Input this decay correctly '
        print decay
        line = ''
        while True:
            line = raw_input()
            if line.split(' ')[0]=='addparticle':
            	if len(line.split(' '))==3:
                    AddParticle(line.replace('addparticle ',''))
                    if Wrong(decay):
                        print "Sill some problems, add more particles or re-input decay: "
                        continue
                    else:
                        NormalRecord(decay, branching)
                        return
                else:
                	print 'correct comad syntax: > addparticle mass name'
                	continue
            elif line == 'end':
                return
            elif line == 'plist':
                prt = GetParticles()
                for p in prt:
                    print p
            elif line == '':
                continue
            elif line == 'no':
                AddException(decay, 'skip')
                return
            elif line == 'help':
            	print 'You can:'
            	print 'Add decay typing correct decay: > A --> B C'
            	print 'Input is finished by typing > end'
            	print 'Show the list of particles: > plist'
            	print 'Add missing particle: > addparticle mass name'
            	print 'Add skip exception for decay: > no'
            	continue
            else:
                if Wrong(line):
                    print "Wrong line, please re-input: "
                    continue
                else:
                    AddException(decay, line)
                    NormalRecord(line, branching)
    else:
        for e in exceptions[decay]:
            NormalRecord(e, branching)
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
    if decay == 'skip':
        return
    with open("CorrectDecays.txt", "a") as f:
        f.write( branching + "|" + decay + '\n')
    decay = Conjugate(decay)
    with open("CorrectDecays.txt", "a") as f:
        f.write( branching + "|" + decay + '\n')
    return