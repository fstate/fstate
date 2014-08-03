"""
This script form particle list which will be used in future absing on LHCb DaVinvi output.
Format:
|        Name       |     PdgID    |   Q  |     Mass    |  Anti-Paticle name |  Aliases  |   Group aliases  |
Alisaes should be unique (for ex. "K*(890)" for K*(890)0), group aliases may be tha same for different paticles (for ex. "pi" for pi+ and pi-)
"""

def analyze(lines):
    masses = open('LHCb_particles.txt', 'w')

    done, total = 0, len(lines)
    
    lines = lines[1:] #Skip table header

    for line in lines:
        info = line.split("|")
        if "self-cc" in info[9]:
            ap = info[1]
        else:
            ap = info[9]
        if "unknown" in info[7]:
            alias = info[1]
        else:
            alias = info[1]+"$"+info[7]
        group_alias = info[1].replace("+","").replace("-","").replace("~","")
        if group_alias == info[1]:
            group_alias = ""
        corr_line = "|" + info[1] + "|" + info[2] + "|" + info[3] + "|" + info[4] + "|" + ap + "|" + alias + "|" + group_alias + "|\n"

        masses.write(corr_line)

    masses.close()


def main():
    with open('lhcb_particles/particles.txt') as f:
        lines = f.readlines()
        analyze(lines)


if __name__ == '__main__':
    main()
