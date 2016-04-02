from random import shuffle

def min_index(values):
    return min(xrange(len(values)), key=values.__getitem__)


def get_jobs(procs):
    data = [x.split() for x in open('max.log').readlines()]

    for x in data:
        h, m, s = [float(y) for y in x[1].split(':')]
        x[1] = h * 3600 + m * 60 + s

    data = sorted(data, key=lambda x: -x[1])


    work = [[] for _ in range(procs)]
    time = [0 for _ in range(procs)]

    for x in data:
        father, t = x
        i = min_index(time)

        time[i] += t
        work[i].append(father)

    for x in work:
        shuffle(x) # Otherwise output will be dummy at start.

    return work
