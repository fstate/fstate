from Interfaces import *
"""
This script should create list of valid decays (stage1/deta/valid.txt) from the list of decays obtained from PDG (stage0/decays.txt)
and from the list of particles, obained from LHCb software (stage0/LHCb_particles.txt)
"""

def Remove_Shotcuts(decay):
    """
    Remove known shotcuts like pi+- K-+ and other. This function should return a list of unshortcuted decays
    """
    return True

def Apply_Known_Exceptions(decay):
    """
    Apply known exceptions which can not be classified. For example, information about intermediate states or spin waves.
    """
    return True

def Apply_Particle_Aliaces(decay):
    """
    Check if unrecoginzed particles can be recoginzed using list of aliases
    """
    return True

def Apply_Group_Particle_Aliaces(decay):
    """
    Check if unrecoginzed particles can be recoginzed using list of group aliases
    """
    return True


def fix_decay(decay):

    #First, lets check if decay has already have alias
    if has_aliases(decay):
        #If so, lets return all aliases
        return read_decay_alias(decay)
    else:
        #If this decay was not checked yet, we should apply known checks step by step
        d = decay
        #Remove shortcuts like pi+- K-+ and other
        d = Remove_Shotcuts(d)
        #Work known exceptions like wave information and caskades
        #We can ignore this extra information, but status should be put to "untrusted"
        d = Apply_Known_Exceptions(d)
        #Check if instead of name of a particle decay contain it alias
        d = Apply_Particle_Aliaces(d)
        #Or, even, group alias
        d = Apply_Group_Particle_Aliaces(d)
        #In result we can have a set of automatically-recontructed decays 
        #And some of them can break charge or energy conservation laws
        #This should be checked later.
        return d


def main():

    #Create a list of all decays from data
    decays = []
    #decays : [[status, br, decay_line],...]
    decfile = open('../stage0/decays.txt')
    for line in decfile.readlines():
        status, br, decay = [x.strip() for x in line.rstrip().split("||")]
        decays.append([status,br, decay])

    #Create a list of all particles from data
    particles = []
    #particles: [[name, PDGID, Q, M, antiparticle_name, [alias1,...], [group alias1,...]],...]
    pfile = open('../stage0/LHCb_particles.txt')
    for line in pfile.readlines():
        Name = line.split("|")[1].replace(" ","")
        PdgID = line.split("|")[2].replace(" ","")
        Q = line.split("|")[3].replace(" ","")
        Mass = line.split("|")[4].replace(" ","")
        AntiName = line.split("|")[5].replace(" ","")
        Aliases = line.split("|")[6].split("$").replace(" ","")
        GroupAliases = line.split("|")[7].split("$").replace(" ","")
        particles.append([Name,PdgID,Q,Mass,AntiName,Aliases,GroupAliases])


    for d in decays:
        #First, check if line in readable bby itself
        if check_decay_line(d[2]):
            #If so, we can add it to the white list
            add_to_white_list(d)
        else:
            fixed_successfully = False
            #else, we should try to fix it
            for fd in fix_decay(d):
                #During the fix procedure we can obtain multiple decays
                #So now we check all of the fixed decays
                if check_decay_line(fd[2]):
                    #if we fixed decay successfully, we create alias
                    add_decay_alias(d,fd)
                    #and add it to the white list
                    add_to_white_list(fd)
                    #Plus, we should flag that our fixes worked fine
                    fixed_successfully = True
            if not fixed_successfully:
                #If we failed to fix decay, we add it to the black list for manual check
                add_to_black_list(d)

    return True

if __name__ == "__main__":
    main()
