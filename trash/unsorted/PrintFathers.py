from models import *
from mongoengine import *
from AddToRawDec import *
from AddToPart import *
from AddToDec import *
from SaveDec import *

connect('DBFORRAWDEC')

lstFromDec = []
lstFromMass = []
lstDiff = []
for i in RawDecay.objects():
	flag = True
	for j in lstFromDec:
		if j == i.father:
			flag = False
	if flag == True:
		lstFromDec.append(i.father)
for i in RawDecay.objects():
	flag = True
	for j in i.daughters:
		for k in lstFromDec:
			if k == j:
				flag = False
		if flag == True:
			lstFromDec.append(j)
for i in Particle.objects():
	flag = True
	for j in lstFromMass:
		if j == i.name:
			flag = False
	if flag == True:
		lstFromMass.append(i.name)
for i in lstFromDec:
	flag = False
	for j in lstFromMass:
		if i == j:
			flag = True
	if flag == False:
		lstDiff.append(i)
		print i