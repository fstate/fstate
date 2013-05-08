# First, let's create set of all available particles.

# We can use particles with masses as known particles
# particles = set([x[1:-2].split(',')[2].strip() for x in open('../data/masses-fin.txt').readlines()])

# Or better, particles with decay modes:
import re

pattern = r'\((.*),(.*)\)(.*)-->'
particles = set([re.match(r'\((.*),(.*)\)(.*)', x).group(2).strip() for x in open('../data/masses-fin.txt').readlines()])
particles.add('-->')
particles.add('gamma')
particles.add('pi')


for x in open('../data/decays.txt').readlines():
    particles.add(re.match(r'\([0-9.e-]*, [0-9.e-]*\)(.*)-->', x).group(1).split('-->')[0].strip())

# Now let's print BAD decays.
# Conditions when decay is BAD:
# 1. Two `-->`
# 2. Particle not in set  defined above
from fixes import fixlist, multiplexers



decays = [re.sub(r'(\([0-9.e-]*, [0-9.e-]*\))', r'\1|', x).rstrip() 
    for x in open('../data/decays.txt').readlines() 
    if float(x[1:].split(',')[0]) > 1E-9] # branching check


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
    
    BAD = False
    BAD_PARTICLES = []

    for particle in parts:
        if (not particle in particles) and (particle != ''):
            BAD = True
            BAD_PARTICLES.append(particle)

    for particle in parts:
        if particle == "anything":
            BAD = True

    for particle in parts:
        if particle == "X":
            BAD = True


    if BAD or decay.count('-->') != 1:
        #print "BAD:\t", decay , "\t", str(BAD_PARTICLES)
        BADN += 1
        return False
    else:
        GOOD += 1
        return True


for line, decay in enumerate(decays):
    #full_decay = decay
    #decay = re.sub(r'\([0-9.e-]*, [0-9.e-]*\)', '', decay).rstrip()
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
        if process(dec, line+1):
            parts = dec.split(" ")
            if mass(parts[0])>0:                
                m = 0
                for p in parts[1:]:
                    m += mass(p)
                if m >= mass(parts[0]):
                    continue
            print branching + "|" + dec 
            continue



#print "GOOD: ", str(GOOD)
#print "BAD: ", str(BADN)
#print "TOTAL: ", str(TOTAL)
