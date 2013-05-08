def pipi(decay_str):
    """
    Assuming that pi pi(once) is pi+ pi- everywhere.
    """

    if decay_str.count("pi") == 2:
        return [
                    decay_str.replace("pi pi", "pi+ pi-"),
                    decay_str.replace("pi pi", "pi0 pi0")
                ]
    else:
        return decay_str