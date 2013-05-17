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
for k in ['a_1(1260)-', 'K^*(892)-', 'Kbar^*(892)-', 'K_2^*(1430)-', 'K_1(1270)-', 'K_1(1400)-', 'K_0^*(1430)-', 'K_0^*(1430)+', 'pi(1300)-',
          'K^*(1410)-', 'Lambdabar', 'a_1(1260)+', 'a_2(1320)+', 'Nbar', 'rho(1450)0', 'K^*(892)+', 'Sigma_c(2455)++', 'Sigma_c(2455)0', 'Xi(1690)0', 'Sigma(1385)+', 'Sigma_c(2455)0**', 'Sigma_c(2455)++',
          'Sigma_c(2520)0**', 'Sigma_c(2520)++', 'Sigma(1385)-', 'Delta(1232)++', 'Xi(1530)0']:
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
        if particle in set(["u", "d", "c", "s", "b", "g", "q", "anything", "h+", "h-", "particles", "boson", "dummy", "other", "modes", "X-", "invisible", "neutrals", "tracks", "c.c.", "fit", "except", "prongs", "total"]):
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
