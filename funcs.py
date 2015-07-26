from operator import itemgetter

def calcTot(Cobj, Jval):
    Jval['current']['total'] = Jval['H'] * Cobj[Jval['current']['assignment']]['H'] + \
                               Jval['E'] * Cobj[Jval['current']['assignment']]['E'] + \
                               Jval['P'] * Cobj[Jval['current']['assignment']]['P']

def excess (Cobj, Jobj, Clist, num, jOut):
    Clist.sort(key=itemgetter(0), reverse = True)
        #reassign excess
    ties = sum(x.count(Clist[-1][0]) for x in Clist)
    #find tie with highest inPos index
    tInd = ties * -1
    tieList = Clist[tInd::]
    tieList.sort(key=itemgetter(2))
    last = tieList.pop()
    extraJug = Clist.pop(Clist.index(last))[1]
    assign(Cobj, Jobj, extraJug, jOut, num)

def assign(circs, jugs, key, out, num):
    if jugs[key]['picks'] == []:
        #out of picks
        out.append(key)
    else:
        jugs[key]['current']['assignment']=jugs[key]['picks'].pop(0)
        calcTot(circs, jugs[key])
        inPos = len(circs[jugs[key]['current']['assignment']]['assigned'])        
        tup = [jugs[key]['current']['total'], key, inPos]
        circs[jugs[key]['current']['assignment']]['assigned'].append(tup)

        if inPos == num:
            excess(circs, jugs, circs[jugs[key]['current']['assignment']]['assigned'], num, out)


def createLine(k, v, jugs, num):
    #C2 J6 C2:128 C1:31 C0:188, J3 C2:120 C0:171 C1:31, J10 C0:120 C2:86 C1:21, J0 C2:83 C0:104 C1:17
    line = ''
    line = line + 'C' + str(k)
    first = True
    for item in v['assigned']:
        if  not first:
            line = line + ','
        else:
            first = False
        line = line + ' J' + str(item[1])
        for x in range(0, num):
            line = line + ' ' + jugs[item[1]]['opicks'][x][0] + ':' + str(jugs[item[1]]['opicks'][x][1])                
    return line
