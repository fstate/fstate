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
        for p in multiplets[m]:
            particle_list.append(p)
        del multiplets[m]
    multiplets[list_intersection(list_of_multiplets)]=particle_list
