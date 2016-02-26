#This function transform output of parser to RawDec file.
from models import *


#This function create RawDecay object
#This function takes line from parsed PDF
#which looks like
#'(=|<)_BrachingRatio_FatherName_Daughter1_Daugter2_...'
#(_==SPACE)
#On first position '=' means known Braching, '<' - limit
def AddToRawDec(x):
    i = 2
    dec = RawDecay()
    dgt = ''
    if len(x.split(')')) < 2:
        print 'ERROR DURING CREATION OF RAWDEC'
        print x
        return
    help = x.split(")", 1)
    br = help[0][1:]
    br = br.split(", ")
    dec.rate = float(br[0])
    decay = help[1].split(' --> ')
    dec.father = decay[0]
    dgts = decay[1].split(" ")

    #this part is to avoid 4gamma stuf
    t = 0
    st = '1234567890'
    for i in dgts:
        #print "start dgt"
        for j in st:
            #print i[:1]
            #print j.q
            if i[:1] == j:
                dgts[t] = i[1:]
                for k in range(1, int(j)):
                    dgts.append(i[1:])
    dec.daughters = dgts
    dec.known = True
    return dec
