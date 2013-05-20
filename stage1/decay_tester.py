# First, let's create set of all available particles.

# We can use particles with masses as known particles
# particles = set([x[1:-2].split(',')[2].strip() for x in open('../data/masses-fin.txt').readlines()])

# Or better, particles with decay modes:
import re

pattern = r'\((.*),(.*)\)(.*)-->'
particles = set([re.match(r'\((.*),(.*)\)(.*)', x).group(
    2).strip() for x in open('../data/masses-fin.txt').readlines()])
particles.add('-->')
particles.add('gamma')
for k in ['a_1(1260)-', 'K^*(892)-', 'Kbar^*(892)-', 'K_2^*(1430)-', 
          'K_1(1270)-', 'K_1(1400)-', 'K_0^*(1430)-', 'K_0^*(1430)+', 
          'pi(1300)-','K^*(1410)-', 'Lambdabar', 'a_1(1260)+', 'a_2(1320)+', 
          'Nbar', 'rho(1450)0', 'K^*(892)+', 'Sigma_c(2455)++', 'Sigma_c(2455)0', 
          'Xi(1690)0', 'Sigma(1385)+', 'Sigma_c(2455)0**', 'Sigma_c(2455)++',
          'Sigma_c(2520)0**', 'Sigma_c(2520)++', 'Sigma(1385)-', 'Delta(1232)++', 
          'Xi(1530)0','K^*()0','K^*','Kbar_1(1270)0','Kbar_1(1400)0','Kbar^*(1410)0',
          'Kbar_0^*(1430)0','Kbar^*(1680)0','Kbar_2^*(1430)0','Kbar_0^*(800)0',
          'K_2^*(1430)0','f_0(1790)','Kbar_0^*(800)','a_0(1450)0', 'Kbar_S()0',
          'a_1(1260)0','rho(1700)+','K^*(1680)-','a_0(980)0','a_0(980)+','a_0(980)-',
          'K_1(1270)+','K_1(1400)+','rho(1450)+','rho(1450)-','rho(1700)0','rho(1700)+',
          'rho(1700)-','K_2^*(1430)+','D^*()0','D^*()+','D^*()-','D','Dbar','Dbar0','D^*',
          'Kbar^*(1430)0','K^*(1410)0','K^*(892)0','D_s^*(2112)+','D_s+','D_s0^*(2317)+','D_s1^*(2700)+',
          'D_s1^*(2700)-','D_sJ^*(2860)-','D_sJ(3040)+','Dbar()0','Dbar^*(2007)0','Dbar0',
          'D_s0(2317)+','D_sJ(2457)+','D_s^*()-','Sigmabar','K^*(1680)+','K_3^*(1780)+','K_4^*(2045)+',
          'Deltabar0','Delta++','Deltabar+','Lambdabar_c(2593)-','Lambdabar_c(2625)-','Sigmabar_c(2455)0',
          'Dbar^*(2007)0','D_sJ^*(2860)+','D_sJ(3040)-','Dbar^*(2010)','K_1(1400)0',
          'Sigmabar_c()--','Delta()++','Sigmabar_c()0','Dbar_2^*(2460)0','Dbar_1^*(2420)0','D^**','Lambdabar_c()-',
          'Dbar_1(2420)0','Dbar_2^*(2460)0','D_s^(*)()+','eta_c','K(1270)+','K(1400)+','Sigmabar_c(2455)--','Sigmabar_c(2520)0',
          'Dbar^*(2010)+','Dbar^*','Dbar^*()0','D_sJ(2573)+','Dbar_2^*(2462)0','Dbar_0^*(2400)0',
          'Dbar_1(2421)0','Xi', 'B^*()','Bbar^*()','B()','Bbar()','Bbar','K^*(1680)0', 'K_0^*(1430)0',
          'X(3872)+','Lambdabar(1520)', 'Theta(1710)++','chi_c0()','Dbar^**()0', "Dbar_1^'(2427)0",'f_2(1270)0',
          'f_0(1370)0', 'rho^0(1450)', 'X(4260)0', 'Sigmabar()0','X_0(1550)','K^*()+','X(3915)0','Z(3930)0','Lambda_c()-',
          'Dbar^**0()','Xibar_c()0','Delta_X(1600)++','Delta_X(2420)++','a_1()+','b_1()0','Sigmabar(1385)0','Delta+',
          'K^*()+','D_sJ(2700)+',"Dbar_1^'(2430)0",'Dbar_0^*(2420)0','b_1()+','K^*(1410)+','K_2^*(1770)+','K_2^*(1820)+',
          'Sigmabar_c(2800)0','K^*()+','X(1812)','chi_c2()','X(214)'

          ]:
    particles.add(k)
particles.add('pi')


for x in open('../data/decays.txt').readlines():
    particles.add(re.match(r'\([0-9.e-]*, [0-9.e-]*\)(.*)-->', x)
                  .group(1).split('-->')[0].strip())

# Now let's print BAD decays.
# Conditions when decay is BAD:
# 1. Two `-->`
# 2. Particle not in set  defined above
from fixes import fixlist, multiplexers


decays = [re.sub(r'(\([0-9.e-]*, [0-9.e-]*\))', r'\1|', x).rstrip()
          for x in open('../data/decays.txt').readlines()
          if float(x[1:].split(',')[0]) > 1E-9]  # branching check


GOOD, BADN, TOTAL = 0, 0, 0


def mass(part):
    for x in open('../data/masses-fin.txt').readlines():
        if part == re.match(r'\((.*),(.*)\)(.*)', x).group(2).strip():
            return float(re.match(r'\((.*),(.*)\)(.*)', x).group(1).strip().split(', ')[0])
    return 0


def process(decay, lineno):
    global BADN, GOOD, TOTAL, particles

    TOTAL += 1

    parts = decay.split(' ')

    BAD = ""
    BAD_PARTICLES = []

    for particle in parts:
        if (not particle in particles) and (particle != ''):
            BAD += particle + " not in particles. "
            BAD_PARTICLES.append(particle)

    if decay.count('-->') != 1:
        BAD += "Cascade decay. "

    """
    Pay attention!!! In next line can be exclusion of c.c.!!! You shouldn't use it in final version!!
    """

    for particle in parts:
        if particle in set(["u", "d", "c", "s", "b", "g", "q", "anything", "h+", "h-", "particles", 
            "boson", "dummy", "other", "modes", "X-", "invisible", "neutrals", "tracks", "c.c.", 
            "fit", "except", "prongs", "total","hadrons","pi)(s)","semitauic","semimuic","semieic","any","X_c"]):
            BAD = ""
        if particle.find(">=") > -1:
            BAD = ""
        if particle.find("non-") > -1:
            BAD = ""

    for particle in parts:
        if particle == "X":
            BAD = ""

    if 'ex.' in decay:
        BAD = ""

    bads = set(['pi', 'pi+', 'pi-', 'pi0', 'mu', 'mu+', 'mu-', 'K',
               'K+', 'K-', 'K0', 'W', 'W+', 'W-', 'Z'])

    if parts[0] in bads:
        BAD = ""

    #print "BAD:\t", decay , "\t", str(BAD_PARTICLES)
    if BAD != "":
        BADN += 1
    else:
        GOOD += 1

    return BAD


for line, decay in enumerate(decays):
    #full_decay = decay
    #decay = re.sub(r'\([0-9.e-]*, [0-9.e-]*\)', '', decay).rstrip()
    decay += " "
    branching, decay = decay.split('|')

    # Apply fixes:
    for fix in fixlist:
        decay = fix(decay)

    to_process = [decay]
    for m in multiplexers:
        step = []
        for d in to_process:
            multiplexed = m(d)

            if isinstance(multiplexed, str):
                step += [multiplexed]

            elif isinstance(multiplexed, list):
                step += multiplexed

        to_process = step

    for dec in to_process:
        if process(dec, line + 1) != "":
            print process(dec, line)
            print dec
            print




#print "GOOD: ", str(GOOD)
#print "BAD: ", str(BADN)
#print "TOTAL: ", str(TOTAL)
