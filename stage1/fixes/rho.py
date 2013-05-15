def rho (decay_str):
    if ' rho ' in decay_str:
        decay_str = decay_str.replace(" rho ", " rho(770) ")
    if decay_str[-4:] == ' rho':
        decay_str = decay_str.replace(" rho", " rho(770)")
    if ' rho0 ' in decay_str:
        decay_str = decay_str.replace(" rho0 ", " rho(770) ")
    if decay_str[-5:] == ' rho0':
        decay_str = decay_str.replace(" rho0", " rho(770)")
    return decay_str