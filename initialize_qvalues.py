import json
from itertools import chain

# Script to create Q-Value JSON file, initilazing with zeros

qval = {}
en_warmup = True;

# player velocity, max velocity, downward accleration, accleration on flap
playerMaxVelY =  10   # max vel along Y, max descend speed
playerMinVelY =  -8   # min vel along Y, max ascend speed
playerAccY    =   1   # players downward accleration
playerFlapAcc =  -9   # players speed on flapping

PIPEGAPSIZE  = 100 # gap between upper and lower part of pipe
if en_warmup :
    FacUp = 1.2
    FacBot = 1.5
else:
    FacUp= 1000
    FacBot = 1000

# X -> [-40,-30...120] U [140, 210 ... 490]
# Y -> [-300, -290 ... 160] U [180, 240 ... 420]
for x in chain(list(range(-40,140,10)), list(range(140,421,70))):
    for y in chain(list(range(-300,180,10)), list(range(180,421,60))):
        for v in range(-10,11):
            if y > FacUp*PIPEGAPSIZE:
                qval[str(x)+'_'+str(y)+'_'+str(v)] = [500, 0]
            elif y < PIPEGAPSIZE - FacBot*abs(playerFlapAcc)**2/2/abs(playerAccY):
                qval[str(x) + '_' + str(y) + '_' + str(v)] = [0, 500]
            else:
                qval[str(x) + '_' + str(y) + '_' + str(v)] = [0, 0]

fd = open('qvalues.json', 'w')
json.dump(qval, fd)
fd.close()
