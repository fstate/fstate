import json
from merge_multiplet import *

baryon_names = set(['Delta(1620)~+', 'Delta(1620)-', 'Delta~+', 'Delta-', 'Delta(1905)~+', 'Delta(1905)-', 'Delta(1950)~+', 'Delta(1950)-', 'Delta(1620)~0', 'Delta(1620)0', 'N(1520)~0', 'N(1520)0', 'Delta(1905)~0', 'Delta(1905)0', 'N(2190)~0', 'N(2190)0', 'n~0', 'n0', 'Delta~0', 'Delta0', 'N(1675)~0', 'N(1675)0', 'Delta(1950)~0', 'Delta(1950)0', 'Delta(1620)~-', 'Delta(1620)+', 'N(1520)~-', 'N(1520)+', 'Delta(1905)~-', 'Delta(1905)+', 'N(2190)~-', 'N(2190)+', 'p~-', 'p+', 'Delta~-', 'Delta+', 'N(1675)~-', 'N(1675)+', 'Delta(1950)~-', 'Delta(1950)+', 'Delta(1620)~--', 'Delta(1620)++', 'Delta~--', 'Delta++', 'Delta(1905)~--', 'Delta(1905)++', 'Delta(1950)~--', 'Delta(1950)++', 'Sigma~+', 'Sigma-', 'Sigma*~+', 'Sigma*-', 'Sigma(1775)~+', 'Sigma(1775)-', 'Sigma(2030)~+', 'Sigma(2030)-', 'Lambda~0', 'Lambda0', 'Lambda(1520)~0', 'Lambda(1520)0', 'Lambda(1820)~0', 'Lambda(1820)0', 'Lambda(2100)~0', 'Lambda(2100)0', 'Sigma~0', 'Sigma0', 'Sigma*~0', 'Sigma*0', 'Sigma(1775)~0', 'Sigma(1775)0', 'Sigma(2030)~0', 'Sigma(2030)0', 'Sigma~-', 'Sigma+', 'Sigma*~-', 'Sigma*+', 'Sigma(1775)~-', 'Sigma(1775)+', 'Sigma(2030)~-', 'Sigma(2030)+', 'Xi~+', 'Xi-', 'Xi*~+', 'Xi*-', 'Xi~0', 'Xi0', 'Xi*~0', 'Xi*0', 'Omega~+', 'Omega-', 'Sigma_c~0', 'Sigma_c0', 'Sigma_c*~0', 'Sigma_c*0', 'Lambda_c~-', 'Lambda_c+', 'Xi_c~0', 'Xi_c0', 'Sigma_c~-', 'Sigma_c+', 'Sigma_c*~-', 'Sigma_c*+', 'Sigma_c~--', 'Sigma_c++', 'Sigma_c*~--', 'Sigma_c*++', 'Xi_c~-', 'Xi_c+', "Xi'_c~0", "Xi'_c0", 'Xi_c*~0', 'Xi_c*0', "Xi'_c~-", "Xi'_c+", 'Xi_c*~-', 'Xi_c*+', 'Omega_c~0', 'Omega_c0', 'Omega_c*~0', 'Omega_c*0', 'Xi_cc~-', 'Xi_cc+', 'Xi*_cc~-', 'Xi*_cc+', 'Xi_cc~--', 'Xi_cc++', 'Xi*_cc~--', 'Xi*_cc++', 'Omega_cc~-', 'Omega_cc+', 'Omega*_cc~-', 'Omega*_cc+', 'Omega*_ccc~--', 'Omega*_ccc++', 'Sigma_b~+', 'Sigma_b-', 'Sigma_b*~+', 'Sigma_b*-', 'Lambda_b~0', 'Lambda_b0', 'Lambda_b(5920)~0', 'Lambda_b(5920)0', 'Xi_b~+', 'Xi_b-', 'Xi_bc~0', 'Xi_bc0', 'Sigma_b~0', 'Sigma_b0', 'Sigma_b*~0', 'Sigma_b*0', 'Sigma_b~-', 'Sigma_b+', 'Sigma_b*~-', 'Sigma_b*+', 'Xi_b~0', 'Xi_b0', 'Xi_bc~-', 'Xi_bc+', "Xi'_b~+", "Xi'_b-", 'Xi_b*~+', 'Xi_b*-', "Xi'_b~0", "Xi'_b0", 'Xi_b*~0', 'Xi_b*0', 'Omega_b~+', 'Omega_b-', 'Omega_b*~+', 'Omega_b*-', 'Omega_bc~0', 'Omega_bc0', "Xi'_bc~0", "Xi'_bc0", 'Xi*_bc~0', 'Xi*_bc0', "Xi'_bc~-", "Xi'_bc+", 'Xi*_bc~-', 'Xi*_bc+', "Omega'_bc~0", "Omega'_bc0", 'Omega*_bc~0', 'Omega*_bc0', 'Omega_bcc~-', 'Omega_bcc+', 'Omega*_bcc~-', 'Omega*_bcc+', 'Xi_bb~+', 'Xi_bb-', 'Xi*_bb~+', 'Xi*_bb-', 'Xi_bb~0', 'Xi_bb0', 'Xi*_bb~0', 'Xi*_bb0', 'Omega_bb~+', 'Omega_bb-', 'Omega*_bb~+', 'Omega*_bb-', 'Omega_bbc~0', 'Omega_bbc0', 'Omega*_bbc~0', 'Omega*_bbc0', 'Omega*_bbb~+', 'Omega*_bbb-', 'Delta(1900)~+', 'Delta(1900)-', 'Delta(1700)~+', 'Delta(1700)-', 'Delta(1930)~+', 'Delta(1930)-', 'Delta(1900)~0', 'Delta(1900)0', 'Delta(1930)~0', 'Delta(1930)0', 'N(1440)~0', 'N(1440)0', 'Delta(1700)~0', 'Delta(1700)0', 'N(1680)~0', 'N(1680)0', 'N(1990)~0', 'N(1990)0', 'Delta(1900)~-', 'Delta(1900)+', 'Delta(1930)~-', 'Delta(1930)+', 'N(1440)~-', 'N(1440)+', 'Delta(1700)~-', 'Delta(1700)+', 'N(1680)~-', 'N(1680)+', 'N(1990)~-', 'N(1990)+', 'Delta(1900)~--', 'Delta(1900)++', 'Delta(1700)~--', 'Delta(1700)++', 'Delta(1930)~--', 'Delta(1930)++', 'Sigma(1660)~+', 'Sigma(1660)-', 'Sigma(1670)~+', 'Sigma(1670)-', 'Sigma(1915)~+', 'Sigma(1915)-', 'Lambda(1405)~0', 'Lambda(1405)0', 'Lambda(1690)~0', 'Lambda(1690)0', 'Lambda(1830)~0', 'Lambda(1830)0', 'Sigma(1660)~0', 'Sigma(1660)0', 'Sigma(1670)~0', 'Sigma(1670)0', 'Sigma(1915)~0', 'Sigma(1915)0', 'Sigma(1660)~-', 'Sigma(1660)+', 'Sigma(1670)~-', 'Sigma(1670)+', 'Sigma(1915)~-', 'Sigma(1915)+', 'Xi(1820)~+', 'Xi(1820)-', 'Xi(1820)~0', 'Xi(1820)0', 'Lambda_c(2595)~-', 'Lambda_c(2595)+', 'Lambda_b(5912)~0', 'Lambda_b(5912)0', 'Delta(1910)~+', 'Delta(1910)-', 'Delta(1920)~+', 'Delta(1920)-', 'Delta(1910)~0', 'Delta(1910)0', 'N(1700)~0', 'N(1700)0', 'N(1535)~0', 'N(1535)0', 'Delta(1920)~0', 'Delta(1920)0', 'Delta(1910)~-', 'Delta(1910)+', 'N(1700)~-', 'N(1700)+', 'N(1535)~-', 'N(1535)+', 'Delta(1920)~-', 'Delta(1920)+', 'Delta(1910)~--', 'Delta(1910)++', 'Delta(1920)~--', 'Delta(1920)++', 'Sigma(1750)~+', 'Sigma(1750)-', 'Sigma(1940)~+', 'Sigma(1940)-', 'Lambda(1600)~0', 'Lambda(1600)0', 'Lambda(1890)~0', 'Lambda(1890)0', 'Lambda(2110)~0', 'Lambda(2110)0', 'Sigma(1750)~0', 'Sigma(1750)0', 'Sigma(1940)~0', 'Sigma(1940)0', 'Sigma(1750)~-', 'Sigma(1750)+', 'Sigma(1940)~-', 'Sigma(1940)+', 'Delta(1600)~+', 'Delta(1600)-', 'N(1720)~0', 'N(1720)0', 'N(1650)~0', 'N(1650)0', 'Delta(1600)~0', 'Delta(1600)0', 'N(1720)~-', 'N(1720)+', 'N(1650)~-', 'N(1650)+', 'Delta(1600)~-', 'Delta(1600)+', 'Delta(1600)~--', 'Delta(1600)++', 'Lambda(1670)~0', 'Lambda(1670)0', 'N(1900)~0', 'N(1900)0', 'N(1710)~0', 'N(1710)0', 'N(1900)~-', 'N(1900)+', 'N(1710)~-', 'N(1710)+', 'Lambda(1800)~0', 'Lambda(1800)0', 'N(2090)~0', 'N(2090)0', 'N(2090)~-', 'N(2090)+', 'Lambda(1810)~0', 'Lambda(1810)0', 'Sigma(2250)~+', 'Sigma(2250)-', 'Sigma(2250)~0', 'Sigma(2250)0', 'Sigma(2250)~-', 'Sigma(2250)+', 'Xi(1950)~+', 'Xi(1950)-', 'Xi(1950)~0', 'Xi(1950)0', 'Lambda_c(2625)~-', 'Lambda_c(2625)+', 'Xi_c(2815)~0', 'Xi_c(2815)0', 'Xi_c(2790)~0', 'Xi_c(2790)0', 'Xi_c(2815)~-', 'Xi_c(2815)+', 'Xi_c(2790)~-', 'Xi_c(2790)+', 'Xi(1690)~+', 'Xi(1690)-', 'Xi(2030)~+', 'Xi(2030)-', 'Xi(1690)~0', 'Xi(1690)0', 'Xi(2030)~0', 'Xi(2030)0', 'Omega(2250)~+', 'Omega(2250)-', 'Lambda_c(2880)~-', 'Lambda_c(2880)+', 'Z(4430)-', 'Z(4430)+'])


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

    m = { 'particles': [p['Name']] }

    if p['Antiparticle'] != "self-cc":
        m['particles'].append(p['Antiparticle'])
        multiplet_name = intersection(p['Name'], p['Antiparticle'])
    else:
        multiplet_name = p['Name']

    if p['is_baryon']:
        m['antimultiplet'] = multiplet_name + '~'
    else:
        m['antimultiplet'] = multiplet_name

    if not multiplet_name in multiplets:
        multiplets[multiplet_name] = m
    elif not p['Name'] in multiplets[multiplet_name]['particles']:
        multiplets[multiplet_name]['particles'] += m['particles']

    p['multiplet'] = multiplet_name



with open('particles.txt') as f:
    columns = [_.strip() for _ in f.readline()[1:-2].split('|')]
    
    particles = {}
    multiplets = {}

    for l in f.read().splitlines():
        properties = [_.strip() for _ in l[1:-1].split('|')]

        particle = make_it_beauty( {columns[index] : v for index, v in enumerate(properties)} )
        name = properties[0]

        if name in baryon_names:
            particle['is_baryon'] = True
        else:
            particle['is_baryon'] = False
        
        particles[name] = particle

        add_multiplet(particle, multiplets)

    for k, m in multiplets.copy().iteritems():
        if k != m['antimultiplet']:
            tildas = [p for p in m['particles'] if '~' in p]
            multiplets[m['antimultiplet']] = {'antimultiplet': k, 'particles': tildas}
            
            for t in tildas:
                m['particles'].remove(t)
        else:
            neutrals = [p for p in m['particles'] if p[-1] == '0']
            if len(m['particles']) == 4 and len(neutrals) == 2:
                multiplets[k + '0'] = {'particles': neutrals, 'antimultiplet': k + '0'}
                for n in neutrals:
                    m['particles'].remove(n)

    merge(multiplets)

    data_path = '../../data/'

    open(data_path + 'particles.json', 'w').write(json.dumps(particles))
    open(data_path + 'multiplets.json', 'w').write(json.dumps(multiplets))
