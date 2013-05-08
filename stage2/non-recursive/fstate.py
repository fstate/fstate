from itertools import izip, product

def get_fstates(products, db):
    if len(products) == 1 and type(products) == list:
        products = products[0]
    
    if type(products) != list:
        if products in db:
            return [products] + [x for x in db[products]]
        else:
            return [products] 
    else:
        a = get_fstates(products[:-1], db)
        b = get_fstates(products[-1], db)
        
        fstates = []

        for x in a:
            for y in b:
                if type(x) != list:
                    x = [x]
                if type(y) != list:
                    y = [y]

                fstates.append(x + y)

        return fstates