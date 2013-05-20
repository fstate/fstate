def gammast (decay_str):
    while True:
        if 'gamma^*' in decay_str:
            decay_str = decay_str.replace("gamma^*", "gamma")
        if decay_str.find("gamma^*") == -1:
        	break
    return decay_str