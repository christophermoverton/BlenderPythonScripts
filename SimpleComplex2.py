import math
import random
##import CirclePack
## Modified version of SimpleComplex that includes distance from center
## metric so that the Complex is evenly expanded from exterior nodes

DimX = 9
DimY = 9
global VARIANCE
VARIANCE = .5
ComplexSize = 25 ## number of Base Complexes to form a composite Union
MaxBaseSize = 6 ## Max n-Gon size
CenterBase = 6 ## The median Base Complex for a Random Base Complex generation
               ## set.  Should always be less than or equal to MaxBaseSize.
               ##  3 <= CenterBase <= MaxBaseSize where CenterBase is an int.
BVariance = 0.0  ## values range from 0 to 1.0 (full)  This means the
                ## a standard deviation from Center Base for all possible
                ## Base Complexes in a given random Base Complex set.

## Computing the Random Base Complex Set
dev1 = MaxBaseSize - CenterBase
dev2 = CenterBase - 4
dev = min(dev1,dev2)
dev *= BVariance
dev = int(dev)  ## floored no roundup
RandomBase = list(range(CenterBase-dev,CenterBase+dev+1))

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
    interior[1] = list(range(2,size+1))
    olabel[1]['neighbors'] = list(range(2,size+1))
    varshift = 1.0-VARIANCE
    for i in range(2,size+1):
        rvar = VARIANCE*random.random()
        exterior[i] = varshift+rvar
        olabel[i] = {'type':'e'}
        if i == 2:
            olabel[i]['neighbors'] = [3,1,size]
        elif i == size:
            olabel[i]['neighbors'] = [2,1,size-1]
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
    if index == None:
        for i in range(olen):
            colabel[olist[i]+olen] = olabel[olist[i]].copy()
    else:
        for i in range(len(olist)):
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
## ******INTERNAL****************
def getnnode(node, nnode, olabel):
    neighbors = olabel[node]['neighbors']
    if nnode == neighbors[0]:
        return neighbors[-1]
    else:
        return neighbors[0]

def exteriorcheck(node,olabel):
    if olabel[node]['type'] == 'e':
        return True
    else:
        return False

def getrandomexterior(exterior):
    p1ekeys = list(exterior.keys())
    p1ekeysn = len(p1ekeys)-1
    posi = random.randint(0,p1ekeysn)
    return p1ekeys[posi]

def extintconvpass(exterior,interior,olabel):
    exteriorkeys = list(exterior.keys())
    for node in exteriorkeys:
        n1 = olabel[node]['neighbors'][0]
        n2 = olabel[node]['neighbors'][-1]
        t1 = exteriorcheck(n1,olabel)
        t2 = exteriorcheck(n2,olabel)
        if not t1 and not t2:
            olabel[node]['type'] = 'i'
            del exterior[node]
            interior[node] = olabel[node]['neighbors']
def zeronodecheck(node,olabel):
    if olabel[node]['identifier'] == 0:
        return True
    else:
        return False

def updatexteriordist(extdistpack,dist,ext):
    extdist,extdistr = extdistpack
    if dist in extdist:
        extdist[dist].append(ext)
    else:
        extdist[dist] = [ext]
    extdistr[ext] = dist
##    extdistpack = (extdist,extdistr)

def removexteriordist(extdistpack,dist,ext):
    extdist,extdistr = extdistpack
    if dist in extdist:
        exts = extdist[dist]
        if ext in exts:
            exts.remove(ext)
            extdist[dist] = exts
        if len(extdist[dist])==0:
            del extdist[dist]
    if ext in extdistr:
        del extdistr[ext]
##    extdistpack = (extdist,extdistr)

def getminext(extdist):
    dists = list(extdist.keys())
    dists.sort()
    mindist = dists[0]
    return (mindist,extdist[mindist])

def getminextdict(minexts,exterior):
    extdict = {}
    for minext in minexts:
        extdict[minext] = exterior[minext]
    return extdict
            
## ****************************

def connect(pack1,pack2,igroup, border = None, extdistpack = None):
    interior1,exterior1,olabel1 = pack1
    interior2,exterior2,olabel2 = pack2
    extdist,extdistr = extdistpack
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
    dists = []
    for i in igroup:
        igrouprev[igroup[i]] = i
        ## get distances to pack2 interior center node
        dists.append(extdistr[i])
    ## find minimum distance on dists set this indicates distance
    ## indexing on the newly added complex set.  Since 
    ## a triple bond yields all points being +1 from center or
    ## +0 or -1 from center.
    cdist = min(dists) + 1
    ## now add  pack2 nodes (except connectors), need also update labels
    remove2 = []
    appendict = {}
    appendictrev = []
    for i in border:
        ## check for triple bond non zero center node
        ## That is only where center node is shared all other nodes
        ## in such bond are independent.  Important to check this
        ## since a triple bond non zero center node leads to
        ## special appending or inserting of nodes in such bonding
        ## from pack1 to pack2.  Usually for all other bonds we
        ## transfer pack2 to pack1 or append insert nodes from
        ## pack2 to pack1 but not to nodes specifically in pack2 from pack1
        if len(border[i]) == 3:
            bl,bc,br = border[i]
            if olabel1[i]['identifier'] != 0:
                appendict[igroup[bl]] = None
                appendict[igroup[br]] = None
                appendictrev += [bl,br]
    for i in igroup:
        appen = None
        remove = []
        if border == None:
            for n in olabel2[igroup[i]]['neighbors']:
                if n in igvalues:  
                    if appen == None:
                        ##print('i from igroup: ', i)
                        ##print('olabel1[i]neighbors: ', olabel1[i]['neighbors'])
                        if olabel1[i]['neighbors'].index(igrouprev[n]) == 0:
                            appen = False
                        else:
                            appen = True
                    remove.append(n)
        else:
            bset = border[i] ## bond set
            if len(bset) == 3:
                ## triple bond i is always center
                ## technically either append or insert fine
                appen = True
                ## check that primary bond node i isn't a base zero order bond
                ## if it is then we remove neighbor 2 nodes on the bset
                ## else we don't...that is a distinction between the triple
                ## bond set.  When it is a triple bond formed on the a non
                ## inter composite complex node, then the neighboring nodes
                ## are not shared to common nodes for the triple bond.
                ## When the are foremd on a inter composite complex node, then
                ## they are shared.  For example, A triple bond formed
                ## with only one shared node (the center of the triple) versus
                ## a triple bond with all three nodes in the bond shared.
                bl,bc,br = bset
                if olabel1[i]['identifier'] == 0:
                    if not igroup[bl] in remove2:
                        remove2.append(igroup[bl])
                    if not igroup[br] in remove2:
                        remove2.append(igroup[br])
                    if not igroup[bc] in remove2:
                        remove2.append(igroup[bc])
                else:
                    if not igroup[bc] in remove2:
                        remove2.append(igroup[bc])
            else:
                bl,br = bset
                if br == i:
                    appen = True
                else:
                    appen = False
                t2 = igroup[bl] in appendict
                t3 = igroup[br] in appendict
                if not igroup[bl] in remove2 and not t2:
                    remove2.append(igroup[bl])
                if not igroup[br] in remove2 and not t3:
                    remove2.append(igroup[br])
                if igroup[bl] in appendict:
                    appendict[igroup[bl]] = not appen
                if igroup[br] in appendict:
                    appendict[igroup[br]] = not appen
        
    for i in olabel2:
        rdict = {}
        update = []
        
        if not i in remove2: ## originally igvalues:
            rdict['type'] = olabel2[i]['type']
            cycle = olabel2[i]['neighbors']
            cyclec = cycle[0:len(cycle)]
##            for j in igvalues:
##                if j in cyclec:
            for j in remove2:
                if j in cyclec:
            
                    jindex = cyclec.index(j)
##                    ##print('cyclec: ', cyclec)
##                    ##print(type(cyclec))
                    cyclec[jindex] = igrouprev[j]
            if i in appendict:
                if appendict[i]:
                    cyclec.append(igrouprev[i])
                else:
                    ncyclec = [igrouprev[i]]
                    ncyclec += cyclec
                    cyclec = ncyclec
                ## connecting node distance center dist for this
                ## type 3 bond
                updatexteriordist(extdistpack,cdist,i)
            else:
                if olabel2[i]['type'] == 'e':
                    updatexteriordist(extdistpack,cdist+1,i)
                
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
        if border == None:
            for n in olabel2[igroup[i]]['neighbors']:
                if n in igvalues:  
                    if appen == None:
                        ##print('i from igroup: ', i)
                        ##print('olabel1[i]neighbors: ', olabel1[i]['neighbors'])
                        if olabel1[i]['neighbors'].index(igrouprev[n]) == 0:
                            appen = False
                        else:
                            appen = True
                    remove.append(n)
        else:
            bset = border[i] ## bond set
            if len(bset) == 3:
                ## triple bond i is always center
                ## technically either append or insert fine
                appen = True
                ## check that primary bond node i isn't a base zero order bond
                ## if it is then we remove neighbor 2 nodes on the bset
                ## else we don't...that is a distinction between the triple
                ## bond set.  When it is a triple bond formed on the a non
                ## inter composite complex node, then the neighboring nodes
                ## are not shared to common nodes for the triple bond.
                ## When the are foremd on a inter composite complex node, then
                ## they are shared.  For example, A triple bond formed
                ## with only one shared node (the center of the triple) versus
                ## a triple bond with all three nodes in the bond shared.
                bl,bc,br = bset
                if olabel1[i]['identifier'] == 0:
                    remove.append(igroup[bl])
                    remove.append(igroup[br])
                    remove.append(igroup[bc])
                else:
                    remove.append(igroup[bc])
            else:
                bl,br = bset
                if br == i:
                    appen = True
                else:
                    appen = False
                remove.append(igroup[bl])
                remove.append(igroup[br])
        n2list = olabel2[igroup[i]]['neighbors']
        n2listc = n2list[0:len(n2list)]
        
        for r in remove2:
            if r in n2listc:
                ##print('n2listc (prior to r removal): ', n2listc)
                n2listc.remove(r)
                ##print('n2listc (after r removal): ', n2listc)
                ##print('igroup i: ', i)
                ##print('appendict: ', appendict)
        if appen:
            ## distinction is needed here for shared versus non shared nodes
            ## in the special triple bond case (mentioned above)
            if i in appendictrev:
                olabel1[i]['neighbors'] += [igroup[i]]
            else:
                olabel1[i]['neighbors']+= n2listc
        else:
            if i in appendictrev:
                ncycle = [igroup[i]]
                ncycle += olabel1[i]['neighbors']
                olabel1[i]['neighbors'] = ncycle
            else:
                n2listc += olabel1[i]['neighbors']
                olabel1[i]['neighbors'] = n2listc

        ##print(remove2)
        ## check for complete cycles
        if checkcyclewalk(i, olabel1):
            interior1[i]= olabel1[i]['neighbors']
            ##print('complete cycle')
            ##print(olabel1[i]['type'])
            ##print(i)
            olabel1[i]['type'] = 'i'
            del exterior1[i]
            rdist = extdistr[i]
            removexteriordist(extdistpack,rdist,i)
        else:
            olabel1[i]['identifier'] = 0
                
    igroupkeys = list(igroup.keys())

    ## now update pack1 exterior and interior dicts
    for i in update:
        if olabel1[i]['type'] == 'e':
            exterior1[i] = exterior2[i]
        else:
            interior1[i] = olabel1[i]['neighbors']
    ## a final pass on the exterior nodes to account for nodes
    ## that are isolated (between interior nodes) but are also
    ## classified exterior.  These are converted to interior nodes
    ##extintconvpass(exterior1,interior1,olabel1)

## test build 2 triple bond hex, shift the labels of one set, and then
## connect on a node boundary appropriately

## build random connections but need a test to confirm bond type
def getrandomexteriors(pack1,pack2,extdist):
    interior1,exterior1,olabel1 = pack1
    interior2,exterior2,olabel2 = pack2
    ##exterior1c = exterior1.copy()
    exterior2c = exterior2.copy()
    extdistc = extdist.copy()
    maincheck = True
    if random.random() >= .5:
        border = 2
    else:
        border = 3
##    if random.random() >= .5:
##        first = True
##    else:
##        first = False
    first = True
    border = 3  ## checking doubles only
    enode2 = getrandomexterior(exterior2)
    
    nnode2f = olabel2[enode2]['neighbors'][-1]
    
    nnode2l = olabel2[enode2]['neighbors'][0]
    nnode4f = getnnode(enode2, nnode2f, olabel2)
    nnode4l = getnnode(enode2, nnode2l, olabel2)

    mindist, mexteriors = getminext(extdistc)
    exterior1c = getminextdict(mexteriors,exterior1)
    while maincheck:
        enode1 = getrandomexterior(exterior1c)
        
        nnode1f = olabel1[enode1]['neighbors'][0]
        
        nnode1l = olabel1[enode1]['neighbors'][-1]
        nnode3f = getnnode(enode1, nnode1f, olabel1)
        nnode3l = getnnode(enode1, nnode1l, olabel1)
        if border == 2:
            t1 = exteriorcheck(nnode1f,olabel1)
            t2 = exteriorcheck(nnode1l,olabel1)
            if  t1:
                return (2,first,[[enode1,nnode1f],[enode2,nnode2f]])
            elif t2:
                return (2,not first,[[enode1,nnode1l],[enode2,nnode2l]])
        else:
            t1 = exteriorcheck(nnode1f,olabel1)
            t2 = exteriorcheck(nnode1l,olabel1)
            t3 = exteriorcheck(nnode3f,olabel1)
            t4 = exteriorcheck(nnode3l,olabel1)
            if t1 and t3:
                return (3,first,[[enode1,nnode1f, nnode3f],
                                 [enode2,nnode2f, nnode4f]])
            elif t2 and t4:
                return (3,not first,[[enode1,nnode1l, nnode3l],
                                 [enode2,nnode2l, nnode4l]])
            if t1:
                return (2,first,[[enode1,nnode1f],[enode2,nnode2f]])
            elif t2:
                return (2,not first,[[enode1,nnode1l],[enode2,nnode2l]])
        del exterior1c[enode1]
        ##print('exterior: ', exterior1)
        if len(exterior1c) == 0:
            del extdistc[mindist]
            if len(extdistc) == 0:
                return (None,None,None)
            mindist, mexteriors = getminext(extdistc)
            exterior1c = getminextdict(mexteriors,exterior1)
            
    
def getbonds(pack1,pack2,extdist):
    
    interior1,exterior1,olabel1 = pack1
    interior2,exterior2,olabel2 = pack2
    rmap = {}
    bordermap = {}  ## on the primary pack1 
##    ## generate random bond type
##    if random.random() >= .5:
##        border = 2
##    else:
##        border = 3
##    ## pick a position around complex1
##    p1ekeys = list(exterior1.keys())
##    p1ekeysn = len(p1ekeys)-1
##    posi = random.randint(0,p1ekeysn)
##    enode1 = p1ekeys[posi]
##
##    ## pick a position around complex2
##    p2ekeys = list(exterior2.keys())
##    p2ekeysn = len(p2ekeys)-1
##    pos2i = random.randint(0,p2ekeysn)
##    enode2 = p2ekeys[pos2i]
##    first = True
##    if random.random() >= .5:
##        first = True
##    else:
##        first = False
    border, first, rnodes = getrandomexteriors(pack1,pack2,extdist)
    enode1 = rnodes[0][0]
    enode2 = rnodes[1][0]
    ## if the bond type is double then we check for a triple bond
    ## requirement (namely, that a position isn't an inter primitive
    ## bond order node).
    if border == 2:
        nnode1 = None
        ##print('hit border2')
        if first:
            nnode1 = olabel1[enode1]['neighbors'][0]
            bordermap[nnode1] = [enode1,nnode1]
            bordermap[enode1] = [enode1,nnode1]
        else:
            nnode1 = olabel1[enode1]['neighbors'][-1]
            bordermap[nnode1] = [nnode1,enode1]
            bordermap[enode1] = [nnode1,enode1]
        nnode2 = None
        if first:
            nnode2 = olabel2[enode2]['neighbors'][-1]
        else:
            nnode2 = olabel2[enode2]['neighbors'][0]

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
                ## make sure nnode3 is exterior
                t5 = exteriorcheck(nnode3,olabel1)
                if first and t5:
                    bordermap[nnode1] = [enode1,nnode1]
                    bordermap[enode1] = [nnode3,enode1,nnode1]
                    bordermap[nnode3] = [nnode3,enode1]
                elif not first and t5:
                    bordermap[nnode1] = [nnode1,enode1]
                    bordermap[enode1] = [nnode1,enode1,nnode3]
                    bordermap[nnode3] = [enode1,nnode3]
                if t5:
                    nnode4 = getnnode(enode2, nnode2, olabel2)
                    rmap[nnode3] = nnode4
            else:
                nnode3 = getnnode(nnode1, enode1, olabel1)
                t5 = exteriorcheck(nnode3,olabel1)
                if first and t5:
                    bordermap[nnode1] = [enode1,nnode1,nnode3]
                    bordermap[enode1] = [enode1,nnode1]
                    bordermap[nnode3] = [nnode1,nnode3]
                elif not first and t5:
                    bordermap[nnode1] = [nnode3,nnode1,enode1]
                    bordermap[enode1] = [nnode1,enode1]
                    bordermap[nnode3] = [nnode3,nnode1]
                if t5:
                    nnode4 = getnnode(nnode2, enode2, olabel2)
                    rmap[nnode3] = nnode4                
    else:
        ## we still check the bond order of the end nodes in either direction
        ## to ensure that we don't have inter primitive bond order node
        ## we can have either a 4 or 5 order bond type
        ## required here.
        ##print('hit border3')
        if first:
            nnode1 = olabel1[enode1]['neighbors'][0]
            nnode2 = getnnode(enode1, nnode1, olabel1)
            nnode3 = olabel2[enode2]['neighbors'][-1]
            nnode4 = getnnode(enode2, nnode3, olabel2)
        else:
            nnode1 = olabel1[enode1]['neighbors'][-1]
            nnode2 = getnnode(enode1, nnode1, olabel1)
            nnode3 = olabel2[enode2]['neighbors'][0]
            nnode4 = getnnode(enode2, nnode3, olabel2)            
        rmap[enode1] = enode2
        rmap[nnode1] = nnode3
        rmap[nnode2] = nnode4
        t1 = olabel1[nnode1]['identifier'] == 0
        t2 = olabel1[nnode2]['identifier'] == 0
        t3 = olabel2[nnode3]['identifier'] == 0
        t4 = olabel2[nnode4]['identifier'] == 0
        t5 = len(olabel2) > 4
        t6 = len(olabel2) > 5
        if first:
            bordermap[nnode1] = [enode1,nnode1]
            bordermap[enode1] = [nnode2,enode1,nnode1]
            bordermap[nnode2] = [nnode2,enode1]
        else:
            bordermap[nnode1] = [nnode1,enode1]
            bordermap[enode1] = [nnode1,enode1,nnode2]
            bordermap[nnode2] = [enode1,nnode2]
##        if (t1 or t3) and t5:
##            nnode5 = getnnode(nnode1, enode1, olabel1)
##            t7 = exteriorcheck(nnode5,olabel1)
##            if first and t7:
##                bordermap[nnode1] = [enode1,nnode1,nnode5]
##                bordermap[nnode5] = [nnode1,nnode5]
####                bordermap[enode1] = (nnode1,enode1,nnode2)
####                bordermap[enode2] = (enode1,nnode2)
##            elif not first and t7:
##                bordermap[nnode1] = [nnode5,nnode1,enode1]
##                bordermap[nnode5] = [nnode5,nnode1]
####                bordermap[enode1] = (nnode2,enode1,nnode1)
####                bordermap[enode2] = (nnode2,enode1)
##            if t7:
##                nnode6 = getnnode(nnode3, enode2, olabel2)
##                rmap[nnode5] = nnode6
##        if len(rmap) > 3:
##            t7 = t6
##        else:
##            t7 = t5
##        if (t2 or t4) and t5:
##            nnode7 = getnnode(nnode2, enode1, olabel1)
##            t7 = exteriorcheck(nnode7,olabel1)
##            if first and t7:
####                bordermap[nnode1] = (nnode1,enode1)
####                bordermap[enode1] = (nnode1,enode1,nnode2)
##                bordermap[nnode2] = [nnode7,nnode2,enode1]
##                bordermap[nnode7] = [nnode7,nnode2]
##            elif not first and t7:
####                bordermap[nnode1] = (enode1,nnode1)
####                bordermap[enode1] = (nnode2,enode1,nnode1)
##                bordermap[nnode2] = [enode1,nnode2,nnode7]
##                bordermap[nnode7] = [nnode2,nnode7]
##            if t7:
##                nnode8 = getnnode(nnode4, enode2, olabel2)
##                rmap[nnode7] = nnode8            
    return (rmap, bordermap)      
        
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


##hexc(interior1,exterior1,olabel1,1)
##hexc(interior2,exterior2,olabel2,2)
##interior2,exterior2,olabel2 = shiftplabel(interior2, exterior2,olabel2)
##pack1 = (interior1,exterior1,olabel1)
##pack2 = (interior2,exterior2,olabel2)
##igroup = getbonds(pack1,pack2)
##connect(pack1,pack2,igroup)

##***********************************
interior1, exterior1, olabel1 = {},{},{}
packs = []
extdist,extdistr = {},{}
extdistpack = (extdist,extdistr)

for i in range(ComplexSize):
    pack = [interior1.copy(),exterior1.copy(),olabel1.copy()]
    packs.append(pack)
prevlen = 0
mbonds = []

    
for i in range(ComplexSize):
    igroup = {}
    basei = random.randint(0,len(RandomBase)-1)
    rbase = RandomBase[basei]
    interior,exterior,olabel = packs[i]
    ngonc(interior,exterior,olabel, i+1,rbase)
    if i != 0:
        binterior, bexterior, bolabel = packs[0]
        interior,exterior,olabel = shiftplabel(interior, exterior,
                                               olabel,prevlen)
        packs[i] = [interior,exterior,olabel]
        bonddat = getbonds(packs[0],packs[i],extdist)
        igroup, border = bonddat
        ##print('Igroup: ', igroup)
        ##print('border: ', border)
        for b in igroup:
            if packs[0][2][b]['type'] == 'i':
                mbonds.append(b)
        extdistpack = (extdist,extdistr)
        ##print('extdistpack: ', extdistpack)
        connect(packs[0],packs[i],igroup, border,extdistpack)
        ##prevlen = len(packs[0])
        prevlen += len(packs[i][2])
    else:
        prevlen = len(packs[0][2])
        ## update extdist dictionary
        for i in exterior:
            updatexteriordist(extdistpack,1,i)
    ##print(packs[0])
    ##print('previous length: ', prevlen)
    
##cpack = CirclePack(interior1,exterior1)        
