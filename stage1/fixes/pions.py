def pipi(decay_str):
    """
    Assuming that pi pi is pi+ pi- everywhere.
    """

    if decay_str.count("pi") == 2:
        decay_str = decay_str.replace("pi pi", "pi+ pi-")

    return decay_str