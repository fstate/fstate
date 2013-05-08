def mumu(decay_str):
    """
    Assuming that mu mu(once) is mu+ mu- everywhere.
    """

    if decay_str.count("mu") == 2:
        decay_str = decay_str.replace("mu mu", "mu+ mu-")

    return decay_str