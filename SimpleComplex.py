import math
import random

DimX = 9
DimY = 9
global VARIANCE
VARIANCE = .3
ComplexSize = 20  ## number of Base Complexes to form a composite Union
MaxBaseSize = 7 ## Max n-Gon size
CenterBase = 5 ## The median Base Complex for a Random Base Complex generation
               ## set.  Should always be less than or equal to MaxBaseSize.
               ##  3 <= CenterBase <= MaxBaseSize where CenterBase is an int.
BVariance = 1.0  ## values range from 0 to 1.0 (full)  This means the
                ## a standard deviation from Center Base for all possible
                ## Base Complexes in a given random Base Complex set.

## Computing the Random Base Complex Set
dev1 = MaxBaseSize - CenterBase
dev2 = CenterBase - 3
dev = min(dev1,dev2)
dev *= BVariance
dev = int(dev)  ## floored no roundup
RandomBase = range(CenterBase-dev,CenterBase+dev+1)

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
def ngonc(interior,exterior,olabel, ident,size):
    olabel[1] = {'type':'i'}
    olabel[1]['identifier'] = ident
##    interior[1] = [2,3,4,5,6]
    interior[1] = range(2,size)
    olabel[1]['neighbors'] = range(2,size)
    varshift = 1.0-VARIANCE
    for i in range(2,size):
        rvar = VARIANCE*random.random()
        exterior[i] = varshift+rvar
        olabel[i] = {'type':'e'}
        if i == 2:
            olabel[i]['neighbors'] = [3,1,size-1]
        elif i == size-1:
            olabel[i]['neighbors'] = [2,1,size-2]
        else:
            olabel[i]['neighbors'] = [i+1,1,i-1]
        olabel[i]['identifier'] = ident
                            
def pentc(interior,exterior,olabel,ident):
    olabel[1] = {'type':'i'}
    olabel[1]['identifier'] = ident
    interior[1] = [2,3,4,5,6]
    olabel[1]['neighbors'] = [2,3,4,5,6]
    varshift = 1.0-VARIANCE
    for i in range(2,7):
        rvar = VARIANCE*random.random()
        exterior[i] = varshift+rvar
        olabel[i] = {'type':'e'}
        if i == 2:
            olabel[i]['neighbors'] = [3,1,6]
        elif i == 6:
            olabel[i]['neighbors'] = [2,1,5]
        else:
            olabel[i]['neighbors'] = [i+1,1,i-1]
        olabel[i]['identifier'] = ident

def hexc(interior,exterior,olabel,ident):
    olabel[1] = {'type':'i'}
    olabel[1]['identifier'] = ident
    interior[1] = [2,3,4,5,6,7]
    olabel[1]['neighbors'] = [2,3,4,5,6,7]
    varshift = 1.0-VARIANCE
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
def shiftplabel(interior, exterior,olabel, index = None):
    cinterior = {}
    cexterior = {}
    colabel = {}
    olen = None
    if index == None:  
        olen = len(olabel)
    else:
        olen = index
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

## ******INTERNAL****************

def checkcyclewalk(index, label):
    ## true if complete cycle false if not complete
    neighbors = label[index]['neighbors']
    start = neighbors[0]
    end = neighbors[len(neighbors)-1]
    if start in label[end]['neighbors']:
        return True
    else:
        return False
## *****************************
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
            
## ******INTERNAL****************
def getnnode(node, nnode, olabel):
    neighbors = olabel[node]['neighbors']
    nlen = len(neighbors)
    if nnode == neighbors[0]:
        return neighbors[nlen-1]
    else:
        return neighbors[0]
## ****************************
    
def getbonds(pack1,pack2):
    
    interior1,exterior1,olabel1 = pack1
    interior2,exterior2,olabel2 = pack2
    rmap = {}
    ## generate random bond type
    if random.random() >= .5:
        border = 2
    else:
        border = 3
    ## pick a position around complex1
    p1ekeys = list(exterior1.keys())
    p1ekeysn = len(p1ekeys)-1
    posi = random.randint(0,p1ekeysn)
    enode1 = p1ekeys[posi]

    ## pick a position around complex2
    p2ekeys = list(exterior2.keys())
    p2ekeysn = len(p2ekeys)-1
    pos2i = random.randint(0,p2ekeysn)
    enode2 = p2ekeys[pos2i]
    first = True
    if random.random() >= .5:
        first = True
    else:
        first = False
    ## if the bond type is double then we check for a triple bond
    ## requirement (namely, that a position isn't an inter primitive
    ## bond order node).
    if border == 2:
        nnode1 = None
        if first:
            nnode1 = olabel1[enode1]['neighbors'][0]
        else:
            nnodes1 = olabel1[enode1]['neighbors']
            nnodes1len = len(nnodes1)
            nnode1 = nnodes1[nnodes1len-1]
        nnode2 = None
        if first:
            nnode2 = olabel2[enode2]['neighbors'][0]
        else:
            nnodes2 = olabel2[enode2]['neighbors']
            print(nnodes2)
            nnodes2len = len(nnodes2)
            nnode2 = nnodes2[nnodes2len-1]
        t1 = olabel1[enode1]['identifier'] == 0
        t2 = olabel1[nnode1]['identifier'] == 0
        t3 = olabel2[enode2]['identifier'] == 0
        t4 = olabel2[enode2]['identifier'] == 0
        rmap[enode1] = enode2
        rmap[nnode1] = nnode2
        if t1 or t2 or t3 or t4:
            ## require a triple bond order
            ## enode1 is mapped to enode2
            ## nnode1 is mapped to nnode2
            ## prioritize t1 or t3 bonds firstly
            if t1 or t3:
                nnode3 = getnnode(enode1, nnode1, olabel1)
                nnode4 = getnnode(enode2, nnode2, olabel2)
                rmap[nnode3] = nnode4
            else:
                nnode3 = getnnode(nnode1, enode1, olabel1)
                nnode4 = getnnode(nnode2, enode2, olabel2)
                rmap[nnode3] = nnode4                
    else:
        ## we still check the bond order of the end nodes in either direction
        ## to ensure that we don't have inter primitive bond order node
        ## we can have either a 4 or 5 order bond type
        ## required here.  
        nnode1 = olabel1[enode1]['neighbors'][0]
        nnode2 = getnnode(enode1, nnode1, olabel1)
        nnode3 = olabel2[enode2]['neighbors'][0]
        nnode4 = getnnode(enode2, nnode2, olabel2)
        rmap[enode1] = enode2
        rmap[nnode1] = nnode3
        rmap[nnode2] = nnode4
        t1 = olabel1[nnode1]['identifier'] == 0
        t2 = olabel1[nnode2]['identifier'] == 0
        t3 = olabel2[nnode3]['identifier'] == 0
        t4 = olabel2[nnode4]['identifier'] == 0
        if t1 or t3:
            nnode5 = getnnode(nnode1, enode1, olabel1)
            nnode6 = getnnode(nnode3, enode2, olabel2)
            rmap[nnode5] = nnode6
        if t2 or t4:
            nnode7 = getnnode(nnode2, enode1, olabel1)
            nnode8 = getnnode(nnode4, enode2, olabel2)
            rmap[nnode7] = nnode8            
    return rmap       
        
interior1, exterior1,olabel1 = {},{},{}
interior2, exterior2,olabel2 = {},{},{}

##hex2c(interior1,exterior1,olabel1)
##hex2c(interior2,exterior2,olabel2)
#### shift pack2 labeling, so as not to conflict with pack1
##interior2,exterior2,olabel2 = hexshiftplabel(interior2, exterior2,olabel2)
##pack1 = (interior1,exterior1,olabel1)
##pack2 = (interior2,exterior2,olabel2)
##
#### In this case, bottom of pack1 is indexed as 7,6,13,12
#### top of pack2 is indexed originally 4,5,9,10 or with reindexing + 13 units
#### 17,18,22,23
##igroup = {7:17,6:18,13:22,12:23}
#### connect packs
##connect(pack1,pack2,igroup)
## connected packs are assigned to pack1 so done


hexc(interior1,exterior1,olabel1,1)
hexc(interior2,exterior2,olabel2,2)
interior2,exterior2,olabel2 = shiftplabel(interior2, exterior2,olabel2)
pack1 = (interior1,exterior1,olabel1)
pack2 = (interior2,exterior2,olabel2)
igroup = getbonds(pack1,pack2)
connect(pack1,pack2,igroup)

##***********************************
interior1, exterior1, olabel1 = {},{},{}
packs = []
for i in range(ComplexSize):
    pack = [interior1.copy(),exterior1.copy(),olabel1.copy()]
    packs.append(pack)
prevlen = 0
for i in range(ComplexSize):
    basei = random.randint(0,len(RandomBase)-1)
    rbase = RandomBase[basei]
    interior,exterior,olabel = packs[i]
    ngonc(interior,exterior,olabel, i+1,rbase)
    if i != 0:
        binterior, bexterior, bolabel = packs[0]
        interior,exterior,olabel = shiftplabel(interior, exterior,
                                               olabel,prevlen)
        igroup = getbonds(packs[0],packs[i])
        connect(packs[0],packs[i],igroup)
        prevlen = len(packs[0])
    
        
