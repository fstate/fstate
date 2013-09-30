import re
from copy import deepcopy

def plus1(decay_str):
    #if re.match(r'(.*?)(\(\s)(.*?)(\s\+\s)(.*?)(\s\))(.*?)',decay_str):
    #    print 'Catch!'
    """
    Fix A-> ( B + C )( D + E )
    """
    def mlt(l):
        def repl1(m):
            return m.group(1) + " " +  m.group(3) + " " +  m.group(7)
        def repl2(m):
            return m.group(1) + " " +  m.group(5) + " " +  m.group(7)
        return [
                re.sub(r'(.*?)(\(\s)(.*?)(\s\+\s)(.*?)(\s\))(.*?)',repl1,l),  
                re.sub(r'(.*?)(\(\s)(.*?)(\s\+\s)(.*?)(\s\))(.*?)',repl2,l)            
                ] 

    lst = []
    if type(decay_str) == type(lst):
        lst = decay_str
    else:
        lst.append(decay_str)

    lst2 = []
    for s in lst:
        if re.match(r'(.*?)(\(\s)(.*?)(\s\+\s)(.*?)(\s\))(.*?)',s):
            subs = mlt(s)
            for k in subs:
                lst2.append(k)
        else:
            lst2.append(s)
    
    lst = deepcopy(lst2)

    for d in lst:
        if re.match(r'(.*?)(\(\s)(.*?)(\s\+\s)(.*?)(\s\))(.*?)',d):
            plus1(lst)

    return lst

def plus2(decay_str):
    #if re.match(r'(.*?)(\(\s)(.*?)(\s\+\s)(.*?)(\s\))(.*?)',decay_str):
    #    print 'Catch!'
    """
    Fix A-> B  E + C D
    """
    def repl1(m):
        return m.group(1) + " " +  m.group(2) + " "
    def repl2(m):
        return m.group(1) + " " +  m.group(4) + " "
    if re.match(r'(.*?\-\-\>\s)(.*?)(\s\+\s)(.*?)',decay_str):
        return [
                re.sub(r'(.*?\-\-\>\s)(.*?)(\s\+\s)(.*?)',repl1,decay_str),  
                re.sub(r'(.*?\-\-\>\s)(.*?)(\s\+\s)(.*?)',repl2,decay_str)            
                ] 
    else:
        return decay_str
