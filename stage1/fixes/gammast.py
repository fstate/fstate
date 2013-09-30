def gammast (decay_str):

    gammas = ["gamma^*","gamma(DE)"]

    while True:
        for g in gammas:
            if g in decay_str:
                decay_str = decay_str.replace(g, "gamma")
        count = 0
        for g in gammas:
            if decay_str.find(g) != -1:
                count +=1
        if count == 0:
            break

    return decay_str