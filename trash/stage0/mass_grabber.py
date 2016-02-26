import sys
import re
import requests


def get_mass(i):
    url = "http://pdglive.lbl.gov/popupblockdata.brl?nodein=%s"
    data = i.split(' ')
    html = requests.get(url % data[0]).text

    mass = re.compile(r'\<tr  bgcolor=#eeeeee >(.*?)(\d+)(.*?)\&\#177\;(.*?)(\d+)')
    try: 
        found = mass.findall(html)[0]
    except IndexError:
        return str((-1, -1, data[-2]))

    return str((float(found[1]), float(found[4]), data[11]))


def analyze(lines):
    masses = open('masses-parsed.txt', 'w')

    done, total = 0, len(lines)
    
    for line in lines:
        masses.write(get_mass(line) + "\n")
        done += 1
        p = 100.0 * done / total

        sys.stdout.flush()
        sys.stdout.write("\rDone: ")
        sys.stdout.write(str(int(p)))
        sys.stdout.write("% (" + str(done) + "/" + str(total) + ")")

    masses.close()


def main():
    with open('masses.txt') as f:
        lines = f.readlines()
        analyze(lines)


if __name__ == '__main__':
    main()
