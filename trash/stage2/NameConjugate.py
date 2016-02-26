import re


def BaryonNameConjugate(name):
    """
        Rule to conjugate Baryon names
    """

    def repl(m):
        return m.group(1) + "bar" + m.group(2)

    prog = re.compile(r'([a-zA-Z].*?)([^a-zA-Z].*|\b)')

    if 'bar' in name:
        new_name = name.replace('bar', '')
    else:
        new_name = re.sub(prog, repl, name)

    if '+' in new_name:
        new_name=new_name.replace('+', '-')
    elif '-' in new_name:
        new_name=new_name.replace('-', '+')

    return new_name

def NormalNameConjugate(name):
    """
        Rule to conjugate non-Baryon names
    """

    def repl(m):
        return m.group(1) + "bar" + m.group(2)

    prog = re.compile(r'([a-zA-Z].*?)([^a-zA-Z].*|\b)')

    new_name = name

    if '+' in new_name:
        new_name=new_name.replace('+', '-')
    elif '-' in new_name:
        new_name=new_name.replace('-', '+')
    if not ('+' in new_name or '-' in new_name):
        if 'bar' in name:
            new_name = name.replace('bar', '')
        else:
            new_name = re.sub(prog, repl, name)       

    return new_name
