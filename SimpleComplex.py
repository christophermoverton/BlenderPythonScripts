import math
import random

DimX = 9
DimY = 9
global VARIANCE
VARIANCE = .3
interior = {}
exterior = {}
c = 0
verttoc = {}
for i in range(DimX):
    for j in range(DimY):
        verttoc[(i,j)] = c
        c += 1
t9 = DimX % 3 == 0
t10 = DimY % 3 == 0
for i in range(DimX):
    for j in range(DimY):
        t1 = i == 0 or i == DimX-1
        t2 = j == 0 or j == DimY-1
        if t1 or t2:
            c = verttoc[(i,j)]
            if i == 0 and j == 0 or i == DimX-1 and j == DimY-1:
                exterior[c] = .05
            else:
                exterior[c] = .1*random.random()
        else:
            t3 = i == DimX-2
            t4 = i == 1
            t5 = j == DimY-2
            t6 = j == 1
            t7 = i % 2 != 0
            t8 = j % 2 != 0
            c = verttoc[(i,j)]
            n = verttoc[(i,j+1)]
            ne = verttoc[(i+1,j+1)]
            nw = verttoc[(i-1,j+1)]
            e = verttoc[(i+1,j)]
            w = verttoc[(i-1,j)]
            s = verttoc[(i,j-1)]
            se = verttoc[(i+1,j-1)]
            sw = verttoc[(i-1,j-1)]
            ##interior[c] = [n,ne,e,se,s,sw,w,nw]
            if t4 and t6:
                interior[c] = [n,ne,e,se,s,sw,w,nw]
            else:
                if t9 and t10:
                    if t7 and t8:
                        interior[c] = [n,ne,e,se,s,sw,w,nw]
                    elif not t7 and t8:
                        interior[c] = [n,e,s,w]
                    elif t7 and not t8:
                        interior[c] = [n,e,s,w]
                    elif not t7 and not t8:
                        interior[c] = [n,ne,e,se,s,sw,w,nw]
                elif not t9 and t10:
                    if t7 and t8:
                        interior[c] = [n,ne,e,se,s,sw,w,nw]
                    elif t7 and not t8:
                        if t3:
                            interior[c] = [n,ne,e,se,s,w]
                        else:
                            interior[c] = [n,e,s,w]
                    elif not t7 and t8:
                        ##even column odd row
                        if t3:
                            interior[c] = [n,ne,e,se,s,w]
                        else:
                            interior[c] = [n,e,s,w]
##            interior[c] = [n,e,s,sw,w,nw]

## To define a convex versus non convex node to node relation
## That is important since a non convex node to node relation
## indicate where polyhedra (of the same type order) should have
## different bond configurations relative to convex types.
##  What this means is that an outwardly convex node to node
## type means that even bond orders are (e.g., a double bond) would
## not have a odd 3 bond relation.  For instance, consider
## a double bond hex complex.  Now there are precisely two points in such
## complex where a single or double bond means that we should have
## a triple bond configuration and not a double bond.  These are
## the non convex node positions in the complex, or inter primitive
## complex positions.  If we track for a given complex its structure
## in terms of primitives (that is, a base complex that is smaller
## and fundamental to such structure), then we can discern the bond
## bond order type.
## An inter primitives bond order node has a reserved identifier 0.
def hexc(interior,exterior,olabel,ident):
    olabel[1] = {'type':'i'}
    olabel[1]['identifier'] = ident
    interior[1] = [2,3,4,5,6,7]
    olabel[1]['neighbors'] = [2,3,4,5,6,7]
    for i in range(2,8):
        rvar = VARIANCE*random.random()
        exterior[i] = varshift+rvar
        olabel[i] = {'type':'e'}
        if i == 2:
            olabel[i]['neighbors'] = [3,1,7]
        elif i == 7:
            olabel[i]['neighbors'] = [2,1,6]
        else:
            olabel[i]['neighbors'] = [i+1,1,i-1]
        olabel[i]['identifier'] = ident

def hex2c(interior,exterior,olabel, ident):
    for i in range(1,4):
        olabel[i] = {'type':'i'}
        olabel[i]['identifier'] = ident
    interior[1] =[4,5,2,6,7,8]
    olabel[1]['neighbors'] = [4,5,2,6,7,8]
    interior[2] =[5,9,3,13,6,1]
    olabel[2]['neighbors'] = [5,9,3,13,6,1]
    interior[3] =[9,10,11,12,13,3]
    olabel[3]['neighbors'] = [9,10,11,12,13,3]
    varshift = 1.0-VARIANCE
    for i in range(4,14):
        rvar = VARIANCE*random.random()
        exterior[i] = varshift+rvar
        olabel[i] = {'type':'e'}
        olabel[i]['identifier'] = ident
    olabel[4]['neighbors'] = [5,1,8]
    olabel[5]['neighbors'] = [9,2,1,4]
    olabel[6]['neighbors'] = [7,1,2,13]
    olabel[7]['neighbors'] = [8,1,6]
    olabel[8]['neighbors'] = [4,1,7]
    olabel[9]['neighbors'] = [10,3,2,5]
    olabel[10]['neighbors'] = [11,3,9]
    olabel[11]['neighbors'] = [12,3,10]
    olabel[12]['neighbors'] = [13,3,11]
    olabel[13]['neighbors'] = [6,2,3,12]

def hexshiftplabel(interior, exterior,olabel):
    cinterior = {}
    cexterior = {}
    colabel = {}
    olen = len(olabel)
    olist = list(olabel.keys())
    olist.sort()
    for i in range(0,3):
        colabel[olist[i]+olen] = olabel[olist[i]].copy()
    for i in range(3,13):
        colabel[olist[i]+olen] = olabel[olist[i]].copy()
##    for o in olist:
##        if olabel[o]['type'] == 'e':
##            cexterior[o] = .1
##        else:
##            cycle = []
##            for cval in interior[o-olen]:
##                cycle.append(cval+olen)
##            cinterior[o] = cycle
    ## adjust colabel neighbor indexing
    for o in colabel:
        cycle = []
        for n in colabel[o]['neighbors']:
            n+=olen
            cycle.append(n)
        colabel[o]['neighbors'] = cycle
    for o in colabel:
        if colabel[o]['type'] == 'e':
            cexterior[o] = exterior[o-olen]
        else:
            neighs = colabel[o]['neighbors']
            cinterior[o] = neighs[0:len(neighs)]
    return cinterior,cexterior,colabel

## abstracted plabel shift process
def shiftplabel(interior, exterior,olabel):
    cinterior = {}
    cexterior = {}
    colabel = {}
    olen = len(olabel)
    olist = list(olabel.keys())
    olist.sort()
    ## 
    for i in range(olen):
        colabel[olist[i]+olen] = olabel[olist[i]].copy()

    ## adjust colabel neighbor indexing
    for o in colabel:
        cycle = []
        for n in colabel[o]['neighbors']:
            n+=olen
            cycle.append(n)
        colabel[o]['neighbors'] = cycle
    for o in colabel:
        if colabel[o]['type'] == 'e':
            cexterior[o] = exterior[o-olen]
        else:
            neighs = colabel[o]['neighbors']
            cinterior[o] = neighs[0:len(neighs)]
    return cinterior,cexterior,colabel

def checkcyclewalk(index, label):
    ## true if complete cycle false if not complete
    neighbors = label[index]['neighbors']
    start = neighbors[0]
    end = neighbors[len(neighbors)-1]
    if start in label[end]['neighbors']:
        return True
    else:
        return False

##def order

def connect(pack1,pack2,igroup):
    interior1,exterior1,olabel1 = pack1
    interior2,exterior2,olabel2 = pack2
    # igroup is an index correspondence for interpack connections
    ## igroup is mapped from pack1 to pack2
    ## we check pack1 connectors, connections are combined and connections
    ## are reindexed to pack1 connectors, i.e., pack2 connectors are dropped.
    ## defintion of interior point.  An interior point is formed by a complete
    ## cycle, that is, where all points of the cycle are directly
    ## interconnected.  Exterior points are formed by incomplete cycles, or
    ## non closed sub arcs.
    ## rebuild cycles on pack1.  Assumed that when checking a cycle,
    ## that all intermediate points in the cycle are interconnected.
    igvalues = list(igroup.values())
    igrouprev = {}
    for i in igroup:
        igrouprev[igroup[i]] = i
    ## now add  pack2 nodes (except connectors), need also update labels
    for i in olabel2:
        rdict = {}
        update = []
        if not i in igvalues:
            rdict['type'] = olabel2[i]['type']
            cycle = olabel2[i]['neighbors']
            cyclec = cycle[0:len(cycle)]
            for j in igvalues:
                if j in cyclec:
                    jindex = cyclec.index(j)
                    cyclec[jindex] = igrouprev[j]
            rdict['neighbors'] = cyclec
            rdict['identifier'] = olabel2[i]['identifier']
            olabel1[i] = rdict
            update.append(i)
            if olabel2[i]['type'] == 'e':
                exterior1[i] = exterior2[i]
            else:
                interior1[i] = olabel1[i]['neighbors']
    for i in igroup:
        appen = None
        remove = []
        for n in olabel2[igroup[i]]['neighbors']:
            if n in igvalues:  
                if appen == None:
                    if olabel1[i]['neighbors'].index(igrouprev[n]) == 0:
                        appen = False
                    else:
                        appen = True
                remove.append(n)
        n2list = olabel2[igroup[i]]['neighbors']
        n2listc = n2list[0:len(n2list)]
        for r in remove:
            n2listc.remove(r)
        if appen:
            olabel1[i]['neighbors']+= n2listc
        else:
            n2listc += olabel1[i]['neighbors']
            olabel1[i]['neighbors'] = n2listc
        ## check for complete cycles
        if checkcyclewalk(i, olabel1):
            interior1[i]= olabel1[i]['neighbors']
            olabel1[i]['type'] = 'i'
            del exterior1[i]
        else:
            olabel1[i]['identifier'] = 0
                
    igroupkeys = list(igroup.keys())

    ## now update pack1 exterior and interior dicts
    for i in update:
        if olabel1[i]['type'] == 'e':
            exterior1[i] = exterior2[i]
        else:
            interior1[i] = olabel1[i]['neighbors']

## test build 2 triple bond hex, shift the labels of one set, and then
## connect on a node boundary appropriately

## build random connections but need a test to confirm bond type
def getbonds(pack1,pack2):
    interior1,exterior1,olabel1 = pack1
    interior2,exterior2,olabel2 = pack2
    ## generate random bond type
    if random.random() >= .5:
        border = 2
    else:
        border = 1
    ## pick a position around complex1
    p1ekeys = list(exterior1.keys())
    p1ekeysn = len(p1ekeys)
    posi = random.randint(0,p1ekeysn)
    enode1 = p1ekeys[posi]

    ## pick a position around complex2
    p1ekeys = list(exterior1.keys())
    p1ekeysn = len(p1ekeys)
    posi = random.randint(0,p1ekeysn)
    enode1 = p1ekeys[posi]
    
interior1, exterior1,olabel1 = {},{},{}
interior2, exterior2,olabel2 = {},{},{}

hex2c(interior1,exterior1,olabel1)
hex2c(interior2,exterior2,olabel2)
## shift pack2 labeling, so as not to conflict with pack1
interior2,exterior2,olabel2 = hexshiftplabel(interior2, exterior2,olabel2)
pack1 = (interior1,exterior1,olabel1)
pack2 = (interior2,exterior2,olabel2)

## In this case, bottom of pack1 is indexed as 7,6,13,12
## top of pack2 is indexed originally 4,5,9,10 or with reindexing + 13 units
## 17,18,22,23
igroup = {7:17,6:18,13:22,12:23}
## connect packs
connect(pack1,pack2,igroup)
## connected packs are assigned to pack1 so done
