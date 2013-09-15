import json
multiplets = json.loads(open("multiplets.json").read())

def intersection(str1, str2):
    """
    Return common part of the two strings
    """
    str1 = str1.replace('anti-', '')
    str2 = str2.replace('anti-', '')
    return ''.join([_[1] for _ in sorted(list(set([c for c in enumerate(str1)]).intersection(set([c for c in enumerate(str2)]))), key=lambda x: x[0])])


def list_intersection(list):
    if len(list)<1:
        return list[0]
    else:
        i = list[0]
        for p in list:
            i = intersection(i, p)
    return p

def merge_multiplet(list_of_multiplets):
    """
        Merge all multiplets from the list.
        Creae new multiplet with given name.
        Don't forget to remove these old multiplets from the list of the multipets.
    """
    particle_list = []
    for m in list_of_multiplets:
        if not m in multiplets:
            continue
        for p in multiplets[m]["particles"]:
            particle_list.append(p)
        del multiplets[m]
    mlt = {"particles":particle_list,"antimultiplet":list_intersection(list_of_multiplets)}
    multiplets[list_intersection(list_of_multiplets)]=mlt

def merge():
    mc = multiplets.copy()
    for name1, m1 in mc.iteritems():
        if not m1["antimultiplet"] == name1:
            continue
        for name2, m2 in mc.iteritems():
            if not m2["antimultiplet"] == name2:
                continue


            if len(m1['particles']) + len(m2['particles'])==3:
                if ( name1 + "0" == name2) or (name2 + "0" == name1):
                    listm=[name1, name2]
                    merge_multiplet(listm)

merge()
print multiplets