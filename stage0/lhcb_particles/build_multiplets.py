

{'Name': 'anti-d', 'MaxWidth': '0', 'PdgID': '-1', 'Q': '+1/3', 'Antiparticle': 'd', 'Mass': '9.9 MeV', 
'EvtGen': 'anti-d', 'PythiaID': '-1', '(c*)Tau/Gamma': '0 ns'}

def convert_to_GeV(v):
    " 'X [TeV/GeV/MeV/eV]' -> Y [GeV] "

    value, dim = v.split(' ')
    multipliers = {
        'eV' : 1.0E-9,
        'MeV': 1.0E-3,
        'GeV': 1.0,
        'TeV': 1.0E+3
    }

    return float(value) * multipliers[dim]


def make_it_beauty(p):
    "Makes particle json nice"
    p['MaxWidth'] = float(p['MaxWidth'])
    p['Q']        = float(p['Q'].replace('1/3', '0.333').replace('2/3', '0.666'))

    p['PdgID']    = int(p['PdgID'])
    p['PythiaID'] = int(p['PythiaID'])
    
    p['lifetime'] = p['(c*)Tau/Gamma']
    del p['(c*)Tau/Gamma']

    p['Mass'] = convert_to_GeV(p['Mass'])

    return p


def intersection(str1, str2):
    """
    Return common part of the two strings
    """
    str1 = str1.replace('anti-', '')
    str2 = str2.replace('anti-', '')

    return ''.join([_[1] for _ in sorted(list(set([c for c in enumerate(str1)]).intersection(set([c for c in enumerate(str2)]))), key=lambda x: x[0])])

def add_multiplet(p, multiplets):
    if p['Antiparticle'] == '-' or p['Antiparticle'] in multiplets.keys():
        return

    m = [p['Name']]

    if p['Antiparticle'] != "self-cc":
        m.append(p['Antiparticle'])
        multiplet_name = intersection(p['Name'], p['Antiparticle'])
    else:
        multiplet_name = p['Name']

    multiplets[multiplet_name] = m

if __name__ == "__main__":
    with open('particles.txt') as f:
        columns = [_.strip() for _ in f.readline()[1:-2].split('|')]
        
        particles = {}
        multiplets = {}

        for l in f.read().splitlines():
            properties = [_.strip() for _ in l[1:-1].split('|')]

            particle = make_it_beauty( {columns[index] : v for index, v in enumerate(properties)} )
            name = properties[0]

            particles[name] = particle

            add_multiplet(particle, multiplets)

        print multiplets
