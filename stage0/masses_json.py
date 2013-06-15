import json

masses = {}

f = open('../data/masses-fin.txt')
for line in f.readlines():
    mass, error, name = [x.strip() for x in line[1:-2].split(',')]
    masses[name] = [mass, error]

print json.dumps(masses)

