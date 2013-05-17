def rho (decay_str):
    while True:
        if ' rho ' in decay_str:
            decay_str = decay_str.replace(" rho ", " rho(770) ")
        if ' rho0 ' in decay_str:
            decay_str = decay_str.replace(" rho0 ", " rho(770) ")
        if decay_str.find(" rho ") == -1:
        	if decay_str.find(" rho0 ") == -1:
        		break
    return decay_str