def nice_name(name):
    if name =="J/psi(1S)":
        return "$J/\\psi(1S)$"
    parsed_name={"main":"", "sub":"","sup":"", "mass":"", "macron":False, "suffix":"", "helicity":""}
    for x in ["~","anti-"]:
        if x in name:
            parsed_name["macron"]=True
            name = name.replace(x, "")

    if "_0" in name:
        parsed_name["sub"]+="0"
        name = name.replace("_0","")

    for x in ["++","--"]:
        if x in name:
            parsed_name["sup"]+=x
            name = name.replace(x, "")
            break
    for x in ["H","L"]:
        if name[-1]==x:
            parsed_name["helicity"]+=x
            name = name[:-1]
            break

    for x in ["+", "-", "0"]:
        if name[-1]==x:
            parsed_name["sup"]+=x
            name = name[:-1]
            break
    for x in ["S","L"]:
        if name[-1]==x:
            parsed_name["helicity"]+=x
            name = name[:-1]
            break
    for x in ["(H)","(L)"]:
        if x in name:
            parsed_name["helicity"]+=x.replace("(","").replace(")","")
            name = name.replace(x, "")
            break
    if "_prime" in name:
        parsed_name["suffix"]+="'"
        name = name.replace("_prime","")
    for x in ["*","''","'"]:
        if x in name:
            parsed_name["suffix"]+="'"
            name = name.replace(x, "")
            break
    if "_" in name:
        if "(" in name:
            parsed_name["main"]=name.split("_")[0]
            parsed_name["sub"]+=name.split("_")[1].split("(")[0]
            parsed_name["mass"]="("+name.split("(")[1].split(")")[0]+")"
        else:
            parsed_name["main"]=name.split("_")[0]
            parsed_name["sub"]+=name.split("_")[1]
    elif "(" in name:
        parsed_name["main"]=name.split("(")[0]
        parsed_name["mass"]="("+name.split("(")[1].split(")")[0]+")"
    else:
        parsed_name["main"]=name
    if parsed_name["sub"] in ["tau", "mu"]:
        parsed_name["sub"]="\\"+parsed_name["sub"]
    if not len(parsed_name["main"])==1:
        if parsed_name["main"] not in ["Graviton","opticalphoton","Xsu","Xsd","Xss"]:
            parsed_name["main"]="\\"+parsed_name["main"]
    if parsed_name["macron"]:
        return "$\\bar{"+parsed_name["main"]+"}"+parsed_name["suffix"]+"^{"+parsed_name["sup"]+"}"+"_{"+parsed_name["sub"]+"}"+parsed_name["mass"]+parsed_name["helicity"]+"$"
    else:
        return "$"+parsed_name["main"]+parsed_name["suffix"]+"^{"+parsed_name["sup"]+"}"+"_{"+parsed_name["sub"]+"}"+parsed_name["mass"]+parsed_name["helicity"]+"$"
