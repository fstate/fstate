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
particles.add('pi')
for k in ['a_1(1260)-', 'K^*(892)-', 'K_2^*(1430)-']:
    particles.add(k)

for x in open('../stage0/decays.txt').readlines():
    if x.count('-->') > 1:
        continue
    particles.add(re.match(r'.*\|\|.*\|\|(.*)-->', x)
                  .group(1).split('-->')[0].strip())

# Now let's print BAD decays.
# Conditions when decay is BAD:
# 1. Two `-->`
# 2. Particle not in set  defined above
from fixes import fixlist, multiplexers

decays = []
decfile = open('../stage0/decays.txt')
for line in decfile.readlines():
    status, br, decay = [x.strip() for x in line.rstrip().split("||")]

    if status != "OK":
        continue

    decays.append((br, decay))

GOOD, BAD, TOTAL = 0, 0, 0


def check_good(br, decay):
    global BAD, GOOD, TOTAL, particles

    TOTAL += 1

    checks = [
        lambda br, dec: br > 1e-10,
        lambda br, dec: ',' not in dec,
    ]

    good = all([c(br, decay) for c in checks])
    if good:
        GOOD += 1
        return True
    else:
        BAD += 1
        return False



def main():
    for branching, decay in decays:
        # Apply fixes:
        for fix in fixlist:
            decay = fix(decay)

        # Apply multiplexers
        to_process = [decay]
        for m in multiplexers:
            step = []
            for d in to_process:
                multiplexed = m(d)

                step += [multiplexed] if isinstance(multiplexed, str) else multiplexed

            to_process = step

        for dec in to_process:
            if check_good(float(branching), decay):
                print branching + "|" + dec


if __name__ == "__main__":
    main()
    print "GOOD: ", str(GOOD)
    print "BAD: ", str(BAD)
    print "TOTAL: ", str(TOTAL)
