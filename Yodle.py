import re
import json
import funcs
from operator import itemgetter
from datetime import datetime
startTime = datetime.now()
infile = open('jugglefest2.txt')

jugglers = {}
circuits = {}
jugsOut = []
delims = [' ', ':', ',', '\n']
def calcPick(circ, jug, cno):
    return jug['H'] * circ[cno]['H'] + jug['E'] * circ[cno]['E'] + jug['P'] * circ[cno]['P']
    
for line in infile:
    keys = []    
    word = ''
    for letter in line:
        if letter in delims:
            keys.append(word)
            word = ''
        else:
            word = word + letter
    if keys[0] == 'J':
        J_No = int(keys[1][1::])
        jugglers[J_No] = {'H':int(keys[3]), 'E':int(keys[5]), 'P':int(keys[7]),
                                       'picks':[int(keys[x+8][1::]) for x in range(len(keys[8:]))],
                                       'opicks':[],
                                       'current':{}}
        for x in range(len(keys[8:])):
            score = (keys[x+8], calcPick(circuits, jugglers[J_No], int(keys[x+8][1::])))
            jugglers[J_No]['opicks'].append(score)
                     
       
    elif keys[0] == 'C':
        circuits[int(keys[1][1::])] = {'H':int(keys[3]), 'E':int(keys[5]),
                                       'P':int(keys[7]), 'assigned':[]}

infile.close()                                                                             
max_assign = len(jugglers)/len(circuits)
picks = len(jugglers[0]['opicks'])
for k in jugglers.keys():
    funcs.assign(circuits, jugglers, k, jugsOut, max_assign)

#check len(assigned) if > num_assign, reverse assigned to allow pop(?), 
#   pop and reassign last place
#print json.dumps(circuits, sort_keys=True, indent=4, separators=(',', ': '))
#print json.dumps(jugglers, sort_keys=True, indent=4, separators=(',', ': '))

def finalize(C_No):
    Jno = jugsOut.pop()
    jugglers[Jno]['picks'].append(C_No)
    funcs.assign(circuits, jugglers, Jno, jugsOut, max_assign)

for k, v in circuits.iteritems():
    filled = len(v['assigned'])
    empty_slots=max_assign - filled
    for x in range(empty_slots):
        finalize(k)
    #pop jugsOut
    #add circuit to picks
    #assign
    
'''
gen = ('%-8s\n' % x if i%10==0 else '%-8s' %x
       for i,x in enumerate(jugsOut,1))
print ''.join(gen)
'''


ofile  = open('assignment.txt', 'w')

for k, v in circuits.iteritems():
    ofile.write(funcs.createLine(k, v, jugglers, picks) + '\n')

print datetime.now() - startTime
#28762
