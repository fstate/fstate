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
        for p in multiplets[m]["particles"]:
            particle_list.append(p)
        del multiplets[m]
    mlt = {"particles":particle_list,"antimultiplet":list_intersection(list_of_multiplets)}
    multiplets[list_intersection(list_of_multiplets)]=mlt

def merge():
    for name1, m1 in multiplets.iteritems():
        for name2, m2 in multiplets.iteritems():
            if m1["antimultiplet"] == name1:
                if m2["antimultiplet"] == name2:
                    if len(m1)+len(m2)==3:
                        if ( m1 + "0" == m2) or (m2 + "0" == m1):
                            list=[name1, name2]
                            merge_multiplet(name1, name2)
