import sys
import re
import requests

def parse_branching_line(line):
    """
    Upper limit
    <$6.6$ $ \times 10^{-5}$

    Normal
    ($1.075$ $\pm.013$) $ \times 10^{-1}$
    $.489$ $\pm.005$

    Assymetric error
    ($.031$ $^{+.013}_{-.011}$) $ \times 10^{1}$

    Seen
    seen
    """

    line = line.split("<td>")[1]
    line = line.split("</td>")[0]

    if "seen" in line:
        return line+" || "


    line = line.replace("$","")
    line = line.replace("}_{","} _{")
    line = line.replace("\\pm","")
    line = line.replace("\\times 10^","e")
    line = line.replace("{","")
    line = line.replace("}","")
    line = line.replace(")","")
    line = line.replace("(","")
    line = line.replace("\\approx","~")
    line = line.replace("\\%","e-2")


    nl = ""
    if "e" in line:
        p = line.split("e")[1]
        line = line.split("e")[0]
        for l in line.split(" "):
            if l!="":
                nl += l + "e" + p + " "
        line = nl
    if line == "":
        line += "Branchning not found"
    return line+" || "


def get_branching(html_big, i):
    #url = "http://pdglive.lbl.gov/RPPdecinfo.brl?parcode=%s&designator=%s"
    #url = "http://pdg8.lbl.gov/rpp2013v2/pdgLive/Particle.action?node=%s#decays"

    data = i.split(':Desig=')

    """
    #Upper limit
    data[0]="S086"
    data[1]="38"
    """

    """
    #No power
    data[0]="M004"
    data[1]="1"
    """

    """
    #Seen
    data[0]="M050"
    data[1]="1"
    """

    #html_big = requests.get(url % data[0]).text

    try:
        line = html_big.split("desig=%s" % data[1])[1].split("\n")[3]
        return parse_branching_line(line)
    except IndexError:
        return  parse_branching_line("not found in PDG")
        pass
    #print data
    #print line

    """
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
    """

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

    archive = {}
    for line in lines:
        if ':Desig=' in line:
            s = line.split(' ')
            ident = s[0]
            parCode = ident.split(":Desig=")[0]
            if not parCode in archive:
                archive[parCode] = requests.get("http://pdg8.lbl.gov/rpp2013v2/pdgLive/Particle.action?node=%s&_eventName=showAllDecays&showAllDecays=true" % parCode).text

            try:
                b = get_branching(archive[parCode], ident)
                #print ident + " " + b
            except IndexError:
                pass # Got shit, need to flag it

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

        #url = 'http://pdg.lbl.gov/2012/pdgid/PDGIdentifiers-2012v1.txt'
        url = 'http://pdg.lbl.gov/2013/pdgid/PDGIdentifiers-current.txt'
        text = requests.get(url).text

        f = open('data.txt', 'w')
        f.write(text)
        f.close()

        analyze([l + "\n" for l in text.split("\n")])

if __name__ == '__main__':
    main()
