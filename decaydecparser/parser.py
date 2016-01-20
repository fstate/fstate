import json

DECAY_DEC_PATH = "../data/DECAY.DEC"
MODELS = set(["PHSP", "PHSP;", "HELAMP", "ISGW2;", "PHOTOS", "SVS", "SVS;", "SVV_HELAMP", "PYTHIA", "HQET2", "HQET2;", "ISGW2;"])


# Global dict to return
result = {
    'Define': {},
    'Alias': {},
    'ChargeConj': {},
    'decays': {}
}

current_particle = None


def read_lines_from_decaydec():
    f = open(DECAY_DEC_PATH)
    lines = f.readlines()
    f.close()
    return lines


def split_line_to_tokens(line):
    # Remove commented part
    line = line.strip().split("#")[0]
    if line == "":
        return None

    # Split line by spaces, remove empty parts
    return [tok for tok in line.split() if tok != ""]


def process_decay(tokens):
    # Example: ['0.000127000', 'anti-Sigma+', 'gamma', 'PHSP;']
    result = {
        "braching": float(tokens[0]),
        "daughters": []
    }
    for d in tokens[1:]:
        if d in MODELS:
            break

        result['daughters'].append(d)

    return result


def process_tokens(tokens):
    global current_particle

    if tokens[0] in set(["Define", "Alias", "ChargeConj"]):
        assert len(tokens) == 3, str(tokens)
        key = tokens[1]
        value = tokens[2]
        result[tokens[0]][key] = value
    elif tokens[0] == "Decay":
        current_particle = tokens[1]
        result["decays"][current_particle] = []
    elif tokens[0] == "Enddecay":
        current_particle = None
    elif current_particle:
        result['decays'][current_particle].append(process_decay(tokens))
    else:
        print "Dont know what to do with:", tokens


def main():
    lines = read_lines_from_decaydec()

    for line in lines:
        tokens = split_line_to_tokens(line)
        if not tokens:
            continue

        process_tokens(tokens)

    print json.dumps(result)


if __name__ == '__main__':
    main()