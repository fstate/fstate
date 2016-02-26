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

prt = ['-->']
exceptions = {}

def Record(decay, branching):
    if Wrong(decay):
        ManualFix(decay, branching)
    else:
        NormalRecord(decay, branching)
    return

def GetParticles():
    global prt
    d = particles.find()
    for i in range (0, d.count()):
        p = particles.find()[i]
        if p['particle'] == p['antiparticle']:
            prt.append(p['particle'])
        else:
            prt.append(p['particle'])
            prt.append(p['antiparticle'])
    for p in prt:
        print p
    return


def GetExceptions():
    global exceptions
    rawexp = [re.sub(r'(\s replace \s with \s)', r'\1', x).rstrip() for x in open('Exceptions.txt').readlines()] 
    for rex in rawexp:
        #sex = splitted esception
        sex = rex.split(' replace with ')
        if not sex[0] in exceptions:
            exceptions[sex[0]] = [sex[1]]
        else:
            exceptions[sex[0]].append(sex[1])
    print exceptions
    return

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
        new_decay = decay.replace(' K_0^*(1430) ', ' K_0()^*(1430) ')
        Record(new_decay, branching)
        return True    

    if 'D_s1(2460)' in decay:
        new_decay = decay.replace('D_s1(2460)', 'D(s1)(2460)')
        Record(new_decay, branching)
        return True    

    if 'D_s^*()' in decay:
        new_decay = decay.replace('D_s^*()', 'D_s()^*')
        Record(new_decay, branching)
        return True    

    if ' Dbar()0 ' in decay:
        new_decay = decay.replace(' Dbar()0 ', ' Dbar0 ')
        Record(new_decay, branching)
        return True   

    if ' D_s+ ' in decay:
        new_decay = decay.replace(' D_s+ ', ' D_s()+ ')
        Record(new_decay, branching)
        return True    

    if 'D_s0^*(2317)' in decay:
        new_decay = decay.replace('D_s0^*(2317)', 'D(s0)^*(2317)')
        Record(new_decay, branching)
        return True    

    if 'D_sJ' in decay:
        new_decay = decay.replace('D_sJ', 'D(sJ)')
        Record(new_decay, branching)
        return True   

    if 'D_s1(2536)' in decay:
        new_decay = decay.replace('D_s1(2536)', 'D(s1)(2536)')
        Record(new_decay, branching)
        return True   

    if 'D_s2(2573)' in decay:
        new_decay = decay.replace('D_s2(2573)', 'D(s2)(2573)')
        Record(new_decay, branching)
        return True   


    if 'D(s0)^*(2317) ' in decay:
        new_decay = decay.replace('D(s0)^*(2317) ', 'D(s0)^*(2317)+ ')
        Record(new_decay, branching)
        return True    

    if 'D_s^*(2112)' in decay:
        new_decay = decay.replace('D_s^*(2112)', 'D_s()^*')
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
        
    if ' 3pi+ ' in decay:
        new_decay = decay.replace(' 3pi+ ', ' pi+ pi+ pi+ ')
        Record(new_decay, branching)
        return True    

    if ' 2pi- ' in decay:
        new_decay = decay.replace(' 2pi- ', ' pi- pi- ')
        Record(new_decay, branching)
        return True    

    if ' 3pi- ' in decay:
        new_decay = decay.replace(' 3pi- ', ' pi- pi- pi- ')
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

    if 'nu nubar ' in decay:
        new_decay = decay.replace('nu nubar ', 'nu_e nubar_e ')
        Record(new_decay, branching)
        new_decay = decay.replace('nu nubar ', 'nu_mu nubar_mu ')
        Record(new_decay, branching)
        new_decay = decay.replace('nu nubar ', 'nu_tau nubar_tau ')
        Record(new_decay, branching)
        return True    

    if ' e+- mu-+ ' in decay:
        new_decay = decay.replace(' e+- mu-+ ', ' e+ mu- ')
        Record(new_decay, branching)
        new_decay = decay.replace(' e+- mu-+ ', ' e- mu+ ')
        Record(new_decay, branching)
        return True    

    if ' pi pi ' in decay:
        new_decay = decay.replace(' pi pi ', ' pi+ pi- ')
        Record(new_decay, branching)
        new_decay = decay.replace(' pi pi ', ' pi0 pi0 ')
        Record(new_decay, branching)
        return True    

    if ' K pi ' in decay:
        new_decay = decay.replace(' K pi ', ' K+ pi- ')
        Record(new_decay, branching)
        new_decay = decay.replace(' K pi ', ' K- pi+ ')
        Record(new_decay, branching)        
        new_decay = decay.replace(' K pi ', ' K0 pi0 ')
        Record(new_decay, branching)
        return True    

    if ' K rho ' in decay:
        new_decay = decay.replace(' K rho ', ' K+ rho- ')
        Record(new_decay, branching)
        new_decay = decay.replace(' K rho ', ' K- rho+ ')
        Record(new_decay, branching)        
        new_decay = decay.replace(' K rho ', ' K0 rho(770) ')
        Record(new_decay, branching)
        return True   

    if ' K^*(892) pi ' in decay:
        new_decay = decay.replace(' K^*(892) pi ', ' K^*(892)+ pi- ')
        Record(new_decay, branching)
        new_decay = decay.replace(' K^*(892) pi ', ' K^*(892)- pi+ ')
        Record(new_decay, branching)
        new_decay = decay.replace(' K^*(892) pi ', ' K^*(892)0 pi0 ')
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


    if ' lepton+ nu_lepton ' in decay:
        new_decay = decay.replace(' lepton+ nu_lepton ', ' e+ nu_e ')
        Record(new_decay, branching)
        new_decay = decay.replace(' lepton+ nu_lepton ', ' mu+ nu_mu ')
        Record(new_decay, branching)
        new_decay = decay.replace(' lepton+ nu_lepton ', ' tau+ nu_tau ')
        Record(new_decay, branching)
        return True    

    if ' lepton- nubar_lepton ' in decay:
        new_decay = decay.replace(' lepton- nubar_lepton ', ' e+ nu_e ')
        Record(new_decay, branching)
        new_decay = decay.replace(' lepton- nubar_lepton ', ' mu+ nu_mu ')
        Record(new_decay, branching)
        new_decay = decay.replace(' lepton- nubar_lepton ', ' tau+ nu_tau ')        
        Record(new_decay, branching)
        return True    

    if ' lepton+ lepton- ' in decay:
        new_decay = decay.replace(' lepton+ lepton- ', ' e+ e- ')
        Record(new_decay, branching)
        new_decay = decay.replace(' lepton+ lepton- ', ' mu+ mu- ')
        Record(new_decay, branching)
        new_decay = decay.replace(' lepton+ lepton- ', ' tau+ tau- ')
        Record(new_decay, branching)
        return True    

    if 'Delta()' in decay:
        new_decay = decay.replace('Delta()', 'Delta')
        Record(new_decay, branching)
        return True    

    if ' Delta+ ' in decay:
        new_decay = decay.replace(' Delta+ ', ' Delta ')
        Record(new_decay, branching)
        return True    

    if ' Delta++ ' in decay:
        new_decay = decay.replace(' Delta++ ', ' Delta ')
        Record(new_decay, branching)
        return True    

    if ' Delta0 ' in decay:
        new_decay = decay.replace(' Delta0 ', ' Delta ')
        Record(new_decay, branching)
        return True    

    if ' Delta- ' in decay:
        new_decay = decay.replace(' Delta- ', ' Delta ')
        Record(new_decay, branching)
        return True    
    
    if ' Delta ' in decay:
        new_decay = decay.replace(' Delta ', ' Delta(1232) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(1600) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(1620) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(1700) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(1750) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(1900) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(1905) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(1910) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(1920) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(1930) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(1940) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(1950) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(2000) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(2150) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(2200) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(2300) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(2350) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(2390) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(2400) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(2420) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(2750) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(2950) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Delta ', ' Delta(~3000) ')
        Record(new_decay, branching)
        return True  

    if 'Deltabar()' in decay:
        new_decay = decay.replace('Deltabar()', 'Deltabar')
        Record(new_decay, branching)
        return True    

    if ' Deltabar+ ' in decay:
        new_decay = decay.replace(' Deltabar+ ', ' Deltabar ')
        Record(new_decay, branching)
        return True    

    if ' Deltabar-- ' in decay:
        new_decay = decay.replace(' Deltabar-- ', ' Deltabar ')
        Record(new_decay, branching)
        return True    

    if ' Deltabar0 ' in decay:
        new_decay = decay.replace(' Deltabar0 ', ' Deltabar ')
        Record(new_decay, branching)
        return True    

    if ' Deltabar- ' in decay:
        new_decay = decay.replace(' Deltabar- ', ' Deltabar ')
        Record(new_decay, branching)
        return True    
    
    if ' Deltabar ' in decay:
        new_decay = decay.replace(' Deltabar ', ' Deltabar(1232) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(1600) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(1620) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(1700) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(1750) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(1900) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(1905) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(1910) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(1920) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(1930) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(1940) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(1950) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(2000) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(2150) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(2200) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(2300) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(2350) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(2390) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(2400) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(2420) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(2750) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(2950) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Deltabar ', ' Deltabar(~3000) ')
        Record(new_decay, branching)
        return True  

    if 'Sigma_c()' in decay:
        new_decay = decay.replace('Sigma_c()', 'Sigma_c')
        Record(new_decay, branching)
        return True    

    if ' Sigma_c+ ' in decay:
        new_decay = decay.replace(' Sigma_c+ ', ' Sigma_c ')
        Record(new_decay, branching)
        return True    

    if ' Sigma_c++ ' in decay:
        new_decay = decay.replace(' Sigma_c++ ', ' Sigma_c ')
        Record(new_decay, branching)
        return True    

    if ' Sigma_c0 ' in decay:
        new_decay = decay.replace(' Sigma_c0 ', ' Sigma_c ')
        Record(new_decay, branching)
        return True    

    if ' Sigma_c ' in decay:
        new_decay = decay.replace(' Sigma_c ', ' Sigma_c(2455) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Sigma_c ', ' Sigma_c(2520) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Sigma_c ', ' Sigma_c(2800) ')
        Record(new_decay, branching)
        return True  

    if 'Sigmabar_c()' in decay:
        new_decay = decay.replace('Sigmabar_c()', 'Sigmabar_c')
        Record(new_decay, branching)
        return True    

    if ' Sigmabar_c- ' in decay:
        new_decay = decay.replace(' Sigmabar_c- ', ' Sigmabar_c ')
        Record(new_decay, branching)
        return True    

    if ' Sigmabar_c-- ' in decay:
        new_decay = decay.replace(' Sigmabar_c-- ', ' Sigmabar_c ')
        Record(new_decay, branching)
        return True    

    if ' Sigmabar_c0 ' in decay:
        new_decay = decay.replace(' Sigmabar_c0 ', ' Sigmabar_c ')
        Record(new_decay, branching)
        return True       

    if ' Sigmabar_c ' in decay:
        new_decay = decay.replace(' Sigmabar_c ', ' Sigmabar_c(2455) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Sigmabar_c ', ' Sigmabar_c(2520) ')
        Record(new_decay, branching)
        new_decay = decay.replace(' Sigmabar_c ', ' Sigmabar_c(2800) ')
        Record(new_decay, branching)
        return True  

        
    if ' Dbar^*()0 ' in decay:
        new_decay = decay.replace(' Dbar^*()0 ', ' Dbar^*(2007)0 ')
        Record(new_decay, branching)
        return True       

    if ' D^*()0 ' in decay:
        new_decay = decay.replace(' D^*()0 ', ' D^*(2007)0 ')
        Record(new_decay, branching)
        return True       

    if ' D^*()- ' in decay:
        new_decay = decay.replace(' D^*()- ', ' D^*(2010)- ')
        Record(new_decay, branching)
        return True  


    if ' D^*()+ ' in decay:
        new_decay = decay.replace(' D^*()+ ', ' D^*(2010)+ ')
        Record(new_decay, branching)
        return True  

    if ' D_s0(2317)+ ' in decay:
        new_decay = decay.replace(' D_s0(2317)+ ', ' D(s0)^*(2317)+ ')
        Record(new_decay, branching)
        return True   

    if ' Dbar_2^*(2460)0 ' in decay:
        new_decay = decay.replace(' Dbar_2^*(2460)0 ', ' Dbar_2()^*(2460)0 ')
        Record(new_decay, branching)
        return True          

    return False

def Wrong(decay):
    global prt
    #for p in prt:
    #    print p
    parts = decay.split(' ')

    for particle in parts:
        if not (particle in prt) and (particle != ''):
            print "Problem with particle "+particle
            return True
    return False

def AddException(decay, correctdecay):
    with open("Exceptions.txt", "a") as f:
        f.write( decay + " replace with " + correctdecay + '\n')
    return

def KnownException(decay):
    global exceptions
    if decay in exceptions:
        return True
    return False

def AddParticle(particle):
    global baryons, neutrals, prt
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
    GetParticles()
    return

def ManualFix(decay, branching):
    global trash, prt, exceptions
    #exceptions = GetExceptions()
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