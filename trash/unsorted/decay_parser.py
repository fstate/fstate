"""
 pi^0  ->  nu_tau anti-nu_tau
 pi^0  ->  nu_tau anti-nu_tau
 pi^0  ->  gamma  nu anti-nu
 pi^0  ->  gamma  nu anti-nu
 pi^0  ->  gamma  nu anti-nu

= 0.5 u'a' u'b' u'c'
= 0.3 u'a' u'c' u'c'
< 0.2 u'a' u'c' u'c' u'd'
= 0.5 u'b' u'c' u'c'
= 0.2 u'b' u'd' u'd'
< 0.1 u'b' u'd' u'd' u'd'
= 0.5 u'c' u'd' u'd' u'd'
< 0.2 u'c' u'd' u'd' u'd' u'd'

u'b' 70
u'c' 25
u'd' 10
"""


def parse_decay(decay):
    preface = decay.split('->')

    father = preface[0]

    daughters = preface[1]
    daughters = daughters.split(' ')
    daughters = filter(lambda x: x != '', daughters)

    if not daughters or not father:
        return
    if len(daughters) < 1:
        return

    for d in daughters[:]:
        if d.isdigit():
            p = daughters.index(d)
            particle = daughters[p + 1]

            for t in xrange(int(d) - 1):
                daughters.insert(p, particle)

            daughters.remove(d)

    
    return father, daughters
    
