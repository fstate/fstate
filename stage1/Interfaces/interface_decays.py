def add_decay_alias (original_decay, alias_decay):
    """
    Add decay alias for decay to the list of aliases (stage1/data/Decay_Aliases.txt). Alias may be not unique. 
    Format:
    $decay$alias$
    Both decay and alias should be in Format
    status || branching || decay line
    """
    return True

def check_decay_line (decay_line):
    """
    Check given decay line. return true or false.
    In order to pass, decay should consist of recognized particles only, and should not have any extra elements.
    """
    return True

def add_to_black_list(decay):
    """
    Add given decay to the black list (stage1/data/Black_List.txt)
    """
    return True

def add_to_white_list(decay):
    """
    Add given decay to the white list (stage1/data/White_List.txt)
    """
    return True

def has_aliases(decay):
    """
    Check if decay has aliases
    """
    return True

def read_decay_alias(decay):
    """
    Return aliases for given decay
    """
    return True
