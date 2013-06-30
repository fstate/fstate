import json
import re

masses = {}

with open('../data/masses-fin.txt') as f:
    for line in f.readlines():
        mass, error, name = [x.strip() for x in line[1:-2].split(',')]
        masses[name] = [mass, error]


particles = set()

with open('../data/decays.txt') as f:
    for x in f.readlines():
        particles.add(re.match(r'\([0-9.e-]*, [0-9.e-]*\)(.*)-->', x)
                      .group(1).split('-->')[0].strip())

    for p in particles:
        if '(' in p and ')' in p:
            print p
            mass = p.split('(')[1].split(')')[0]
            if mass.isdigit() and not 'P' in mass and len(mass) > 0:
                mass = float(mass)
            else:
                continue
            if not p in masses.keys():
                masses[p] = [mass, 0]

print json.dumps(masses)
