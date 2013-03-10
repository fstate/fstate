import sys
import re
import requests


def get_branching(i):
    url = "http://pdglive.lbl.gov/RPPdecinfo.brl?parcode=%s&designator=%s"
    data = i.split(':Desig=')
    html = requests.get(url % (data[0], data[1])).text

    mass1 = re.compile(
        r'Summary:(.*?)(\d+)\.(\d+)(.*?)(\d+)\.(\d+)(.*?)10(.*?)(\d+)',
        flags=re.DOTALL)

    found = mass1.findall(html)[0]

    if not found:
        raise ''

    branching = float(found[1] + '.' + found[2] + 'E-' + found[8])
    error = float(found[4] + "." + found[5] + 'E-' + found[8])

    return (branching, error)
    #print url % (data[0], data[1]), requ.text


def analyze(lines):
    decays = open('decays.txt', 'w')
    masses = open('masses.txt', 'w')

    decays_done, decays_total = 0, 0

    for line in lines:
        if ':Desig=' in line:
            decays_total += 1
        if line[4:6] == "M ":
            masses.write(line)

    masses.close()

    print 'Total decays: ', decays_total

    for line in lines:
        if ':Desig=' in line:
            s = line.split(' ')
            ident = s[0]

            try:
                b = get_branching(ident)
                #print b
            except IndexError:
                pass  # Got shit, need to flag it

            decays.write(
                str(b) + ' '.join([x for x in s[1:] if x != '']))

            decays_done += 1
            p = 100.0 * decays_done / decays_total

            sys.stdout.flush()

            sys.stdout.write("\rDone: ")
            sys.stdout.write(str(int(p)))
            sys.stdout.write("% (" + str(decays_done) + ")")

    decays.close()


def main():
    try:
        with open('data.txt') as f:
            lines = f.readlines()
            analyze(lines)

    except IOError as e:
        import requests

        url = 'http://pdg.lbl.gov/2012/pdgid/PDGIdentifiers-2012v1.txt'
        text = requests.get(url).text

        f = open('data.txt', 'w')
        f.write(text)
        f.close()

        analyze([l + "\n" for l in text.split("\n")])

if __name__ == '__main__':
    main()
