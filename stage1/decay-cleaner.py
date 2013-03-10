# First, let's create set of all available particles.

# We can use particles with masses as known particles
# particles = set([x[1:-2].split(',')[2].strip() for x in open('../data/masses-fin.txt').readlines()])

# Or better, particles with decay modes:
import re

pattern = r'\((.*),(.*)\)(.*)-->'
particles = set([re.match(r'\((.*),(.*)\)(.*)', x).group(2).strip() for x in open('../data/masses-fin.txt').readlines()])
particles.add('-->')
particles.add('gamma')

# Now let's print BAD decays.
# Conditions when decay is BAD:
# 1. Two `-->`
# 2. Particle not in set  defined above
from fixes import fixlist, multiplexers

decays = [re.sub(r'\([0-9.e-]*, [0-9.e-]*\)', '', x).rstrip() 
            for x in open('../data/decays.txt').readlines()] # list is needed for line numbers

GOOD, BADN, TOTAL = 0, 0, 0



def process(decay):
    global BADN, GOOD, TOTAL, particles

    TOTAL += 1
    
    parts = decay.split(' ')
    
    BAD = False
    BAD_PARTICLES = []

    for particle in parts:
        if (not particle in particles) and (particle != ''):
            BAD = True
            BAD_PARTICLES.append(particle)


    if BAD:
        print "BAD: " + str(line), " @ " + str(BAD_PARTICLES)
        BADN += 1
    else:
        GOOD += 1


for line, decay in enumerate(decays):
    # First we need to multiplex everything
    
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
        process(dec)



print "GOOD: ", str(GOOD)
print "BAD: ", str(BADN)
print "TOTAL: ", str(TOTAL)
