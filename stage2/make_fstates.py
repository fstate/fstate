import sys
print "Limit is", sys.getrecursionlimit()
#sys.setrecursionlimit(500000)
particles = dict()
skip = 0
for line in open('decays.txt').readlines():
    branching_str = str()

    for c in line[:]:
        branching_str += c
        line = line[1:]

        if c == ')':
            break

    branching = branching_str[1:-1].split(',')
    branching = [float(x) for x in branching[:]]
    if branching[0] == 0.0:
        skip += 1
        continue

    try:
        father, daughters = line.split('-->')
    except ValueError:
        continue

    father = father.strip()
    daughters = daughters.strip()

    if not father in particles:
        particles[father] = {'decays': list()}

    particles[father]['decays'].append((branching, daughters))
print "Skipped", skip

def get_fstates(br, p, particles):
    br_start = br
    fstates = []

    for decay in particles[p]['decays']:
        """if p == "B_s()0":
            print decay"""

        br = br_start
        br *= decay[0][0] + decay[0][1]
        
        if (br == 0.0 or br < 1E-9) and p == "B_s()0":
            print "Skipping", decay,br
            continue

        if (br == 0.0 or br < 1E-9):
            continue

        daughters = decay[1].split(' ')

        try:
            dec = [lookup(br, p, daughter, particles) for daughter in daughters]
            """if p == "B_s()0" and decay[1] == "J/psi(1S) pi0":
                print "="*40
                print br, dec
                print "="*40"""
            fstates.append([p + ' -> ' + decay[1],br, dec])
        except RuntimeError:
            continue
        
    return fstates


def lookup(br, p, daughters, particles):
    #print "\t Looking up: ", daughters

    #if len(daughters) != 1:
    #    return [lookup(br, p, [daughters[0]], particles), lookup(br, p, daughters[1:], particles)]
    

    p = daughters

    if not p in particles:
        return p
    elif p in ['mu+', "mu-", 'e-', 'e+', 'gamma', 'pi+', 'pi-']:
        return p
    elif 'gamma' in p:
        return p
    else:
        return get_fstates(br, p, particles)


"""particles = {
    'B'   : {'decays': [(5,'Jpsi gamma'), (6, 'Jpsi pi0')]},
    'Jpsi': {'decays' : [(1,'mu- mu-')]},
    'pi0' : {'decays' : [(1,'gamma gamma')]},
        }"""
l = get_fstates(1.0, 'B_s()0', particles)
for i in l:
    print i
    raw_input()
