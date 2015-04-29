import random
import bpy
import collections
## Random Gabriel Graph generator
## In this case applying methods similar to voronoi graph generator, or if
## you like you could use Delaunay Triangulation to search out the
## Circumcircles of this graph to generate the corresponding voronoi graph.
## I implement a method used in regularizing the points on inside a node grid.

## So basically inside a given cell (similar to the prims random maze generator)
## of a user specified spatial size alotment, a randomly positioned
## node is generated, and this procedure is reiterated over the set of nodes.
## While we are doing this and appending the node data we can also compute
## the disk between nearest neighbor nodes in all adjacent cells (adjacency
## is given by 8 cells...3 top 3 bottom and 1 center left and 1 center right).
## The disk is computed by computing the diameter and centroid of the disk
## where both nodes are represented at opposite ends of the disk forming
## such disk diameter.  The centroid is then given a 1/2d  where d is the
## is the diameter of the disk on the edge forming such disk.  From this
## this centroid we compute distances to all other neighbors (8 different
## cell nodes) to verify if any lay inside such disk, if not, then graph
## edge is constructed between both such nodes.

##  Random Node Generator and more
nodes = {}
global dimx
global dimy
dimx = 20
dimy = 20
cellsize = 1
## building a distance checking hash map
## this is used in the disk check algorithm
## basically the idea here is given a two node check
## we check all necessary neighboring cells to see if
## any node in such neighboring cell intercepts the disk
## defined between two node points.  This check is articulated
## by the direction from our starting node to the end point node
## defining such disk.  There is a maximum of 10 cells that need
## be checked in the case of diagonal directions, and 4 cells
## for horizontal and vertical directions.  
dchecks = {}
dchecks['ne'] = {'n':(0,1),'nen':(1,2),
                 'nn':(0,2),'nw':(-1,1),
                 'w':(-1,0), 's':(0,-1),
                 'se':(1,-1), 'e': (1,0),
                 'ee':(2,0), 'nee':(2,1)}
dchecks['nw'] = {'n':(0,1),'ne':(1,1),
                 'nn':(0,2),'nwn':(-1,2),
                 'w':(-1,0), 's':(0,-1),
                 'sw':(-1,-1), 'e': (1,0),
                 'ww':(-2,0), 'nww':(-2,1)}
dchecks['sw'] = {'n':(0,1),'nw':(-1,1),
                 'ss':(0,-2),'sws':(-1,-2),
                 'w':(-1,0), 's':(0,-1),
                 'se':(1,-1), 'e': (1,0),
                 'ww':(-2,0), 'sww':(-2,-1)}
dchecks['se'] = {'n':(0,1),'ne':(1,1),
                 'ss':(0,-2),'ses':(1,-2),
                 'w':(-1,0), 's':(0,-1),
                 'sw':(-1,-1), 'e': (1,0),
                 'ee':(2,0), 'see':(2,-1)}
dchecks['e'] = {'n':(0,1), 'ne': (1,1), 's':(0,-1),
                'se':(1,-1)}
dchecks['w'] = {'n':(0,1), 'nw': (-1,1), 's':(0,-1),
                'sw':(-1,-1)}
dchecks['n'] = {'e':(1,0), 'ne': (1,1), 'w':(-1,0),
                'nw':(-1,1)}
dchecks['s'] = {'e':(1,0), 'se': (1,-1), 'w':(-1,0),
                'sw':(-1,-1)}
dirtopos ={'n':(0,1),'nw':(-1,1),'ne':(1,1),'e':(1,0),
           'w':(-1,0),'s':(0,-1),'se':(1,-1),'sw':(-1,-1)}

def checkNeighbor(nodes,direction, cpos, dchecks, dirtopos):
    def distance(pos,pos2):
        posx,posy = pos
        pos2x,pos2y = pos2
        return ((float(posx-pos2x))**2 + (float(posy-pos2y))**2)**.5
    def midpoint(pos,pos2):
        posx,posy = pos
        pos2x,pos2y = pos2
        return (float(posx+pos2x)/2.0, float(posy+pos2y)/2.0)
    
    cposx, cposy = cpos
    nodepos = nodes[cpos]['position']
    nposx, nposy = nodepos
    c2pos = (cposx + dirtopos[direction][0],
             cposy + dirtopos[direction][1])
    if c2pos in nodes:
        n2pos = nodes[c2pos]['position']
        rdistance = distance(nodepos,n2pos)/2.0
        diskpos = midpoint(nodepos,n2pos)
        dcheckset = dchecks[direction]
        for dirch in dcheckset:
            cellpostr = dcheckset[dirch]
            ##cellpostr is the translation to cell coordinate to be
            ## checked
            checkcellpos = (cposx+cellpostr[0],cposy + cellpostr[1])
            if checkcellpos in nodes:
                checknodepos = nodes[checkcellpos]['position']
                checkdist = distance(checknodepos,diskpos)
                if checkdist <= rdistance:
                    return False
        return True
    else:
        return False
    ##pchecks is a position translation hash that basically sets
    ## the node directions necessary for checking based upon a
    ## a given direction. A direction is given in one of the 8 different
    ##adjacency directions mentioned above.
    ## north
def distance(pos,pos2):
    posx,posy = pos
    pos2x,pos2y = pos2
    return ((float(posx-pos2x))**2 + (float(posy-pos2y))**2)**.5

i = 0
vertices = []
for x in range(0,dimx):
    rowi = i
    for y in range(0,dimy):
        attr = {}
        localx = random.random()
        localy = random.random()
        posx = cellsize*localx+x*cellsize
        posy = cellsize*localy+y*cellsize
        attr = {'position':(posx,posy)}
        attr['vertindex'] = i
##        attr['ne'] = None
##        attr['n'] = None
##        attr['nw'] = None
##        attr['w'] = None
##        attr['e'] = None
##        attr['se'] = None
##        attr['sw'] = None
##        attr['s'] = None
        attr['neighbors'] = []
        nodes[(x,y)] = attr
        i += 1
    for y in range(0,dimy):
        attr = nodes[(x,y)]
        posx,posy = attr['position']
        for direct in dirtopos:
            if checkNeighbor(nodes,direct, (x,y), dchecks, dirtopos):
                nattr = {}
                c2pos = (x + dirtopos[direct][0],
                         y + dirtopos[direct][1])
                nattr['cellposition'] = c2pos
                nattr['position'] = nodes[c2pos]['position']
                nattr['distance'] = distance(nattr['position'],(posx,posy))
                attr['neighbors'].append(nattr)
                currentattr = {}
                currentattr['cellposition'] = (x,y)
                currentattr['position'] = (posx,posy)
                currentattr['distance'] = nattr['distance']
                nodes[c2pos]['neighbors'].append(currentattr)
        nodes[(x,y)] = attr
        vertices.append((posx,posy, 0.0))

## now we need to path trace from to and from a starting vertex without
## the trivial path that is from start to second vertex back to start
## That is we need build faces.  This gets trickier since we can span in
## many different directions on the node neighbor tree.  
## we also need a minimally spanning distance set.
## In this case, we can do see by examining a family of paths,
## the smallest set in such family yields the minimal spanning path.
## maybe more efficient methods exist here...maybe a weighting method for
## recusion searching a path?
## A path loop that we are looking for, however,
## does have an intersting property.  Namely, at any given node if we were
## to draw a line from one node back to the start, the edge given
## should neither intersect with any other edge and remain interior to
## our given polygon.  Thus we may be able to formulate an intersection test.
## Where in our recursion process we test to see that an intersection is
## is formed by regional neighboring edges in a given vicinity.  If so then,
## we end the recursion search.  We may be able to also more readily rely on
## this method given node distribution since there are likely to be simple
##polygons.  I have seen a right turn rule being applied, but this seems
## to suggest directionality on otherwise undirected graph.
##   Another method uses distances weighting of a such that a minimum
## distance is maintained in a given path tree search of a destination
## node relative to a node or nodes in a given path.  In this case,
## a modified form of  Dijkstra's algorithm may be a good choice.

##Let the node at which we are starting be called the initial node.
##Let the distance of node Y be the distance from the initial node to Y.
##Dijkstra's algorithm will assign some initial distance values and
##will try to improve them step by step.
##
##Assign to every node a tentative distance value:
##set it to zero for our initial node and to infinity for all other nodes.
##Set the initial node as current. Mark all other nodes unvisited.
##Create a set of all the unvisited nodes called the unvisited set.
##Step 3. For the current node, consider all of its unvisited neighbors
##and calculate their tentative distances. Compare the newly calculated
##tentative distance to the current assigned value and assign the
##smaller one. For example, if the current node A is marked
##with a distance of 6, and the edge connecting it with a neighbor B
##has length 2, then the distance to B (through A) will be 6 + 2 = 8.
##If B was previously marked with a distance greater than 8 then
##change it to 8. Otherwise, keep the current value.
##When we are done considering all of the neighbors of the current node,
##mark the current node as visited and remove it from the unvisited set.
##A visited node will never be checked again.
##If the destination node has been marked visited (when planning a route
##between two specific nodes) or if the smallest tentative distance among
##the nodes in the unvisited set is infinity (when planning a complete
##traversal; occurs when there is no connection between the initial node
##and remaining unvisited nodes), then stop. The algorithm has finished.
##Select the unvisited node that is marked with the smallest tentative
##distance, and set it as the new "current node" then go back to step 3.

## The modified form of this algorithm must consider reaching the
## the destination node which is actually already visited.  Other
## rules still apply.   It seems the problem is handled,
## if tossing the trivial solution a-n and then working n to a for a 2nd
## or 1rst shortest solution.  Another modification to the algorithm puts
## another weight decision bias which also tests increasing distance relative
## to an initial start node.

## Revision: sweep the set of nodes of the graph generating a distance
## trace map (indicated as prev in algorithm), this is basically by the way
## creating with Dijkstra algorithm a directed graph.
## I will refer to a cycle (or polygon) in this context as a ring.
## We can tell that a node point forms the bridge of a ring, where
## bridge is defined as node with allocated distance relative to both
## a source and another common node point, and there are two such
## bridge points that complete the ring of a polygon.
## A bridge node is referenced by its node distance addressing (or
## minimum tentative distance), Two brige nodes occur where
## sequentially the distance between two shared bridge node pairs (having
## an edge between the two) do not add to the other bridges
## allocated distance address, (using t-distance as tentative distance)
## and that one bridge node t-distance is equal to or less in terms of its
## distance allocation relative the other bridge + the distance between
## both such nodes.  From both such bridge points we can trace 3 distinct
## paths back along the
## path of the polygon back to the root of the ring (or a common node).
## A modified form of the function below marks the bridge nodes.
## This occurs for instance, at the control instance of the function checking
## to verify alt < vdist (as shown below).  Whenever a non-infinity reassignment
## is done then we know that a node neighbor's previous allocation is
## a bridge, for instance, relative the other.  We'd also need consider
## the opposite case, on the else exception again for a non-infinity
## failed assignment change.
print(nodes[(0,0)])
def Dijkstramodified(Graph, source, target, exclusion):
    def addlistval(currentnode, nextnode, Paths):
##        if currentnode in Paths:
        for path in Paths[currentnode]:
            newpath = path[0:len(path)]
            newpath.append(nextnode)
            if nextnode in Paths:
                if not newpath in Paths[nextnode]:
                    Paths[nextnode].append(newpath)
            else:
                Paths[nextnode] = [newpath]
##        else:
##            newpath = [currentnode]
##            Paths[currentnode] = [newpath]

    def checkminCycle(nextnode, Paths):
        cycle = {}
        found = False
        if len(Paths[nextnode]) <= 1:
            return False, None
        else:
            minval = float('inf')
            i = 0
            for path in Paths[nextnode]:
                setpath = path[0:len(path)]
                setpath.sort(reverse = True)
                copypaths = Paths[nextnode][0:len(Paths[nextnode])]
                del copypaths[i]
                for path2 in copypaths:
                    path2copy = path2[0:len(path2)]
                    path2copy.sort(reverse = True)
                    j = 0
                    for pathval in path2copy:
                        if j == 0:
                            continue
                        if pathval in setpath:
                            if setpath.index(pathval) < minval:
                                minval = setpath.index(pathval)
                                minval2 = path2copy.index(pathval)
                                cycle = {(minval, minval2):[tuple(setpath),
                                                            tuple(path2copy)]}
                                found = True
                                break
                        j += 1
                i += 1
            if found:
                return True, cycle
            else:
                return False, None
    ## we modify target so that the solution
    ## source -target path is disallowed 
    ##dist = {source: {'distance':0, 'index':0}}
    dist = [(source,0)]
    distmap = {source:0}
    prev = [(source,None)]
    prevmap = {source:None}
    Bridgepairs = [] ## celladdressing pair tuple
    Paths = {}
    Paths[source] = [[source]]
    Cycles = {}
    Q = []
    tposx, tposy = Graph[target]['position']
    sposx, sposy = Graph[source]['position']
    for cell in Graph:
        cellposx,cellposy = Graph[cell]['position']
        
        if cell != source:
            distmap[cell] = float('inf')
            dist.append((cell,float('inf')))
            prevmap[cell] = None
            prev.append((cell, None))
        t1 = tposx <= sposx
        if t1:
            if cellposx <= tposx:
                t1 = cell != source
                t2 = cell != target
                if t1 and t2:
                    continue
##            elif cell[0] > target[0] and cell[0] <= source[0]:
##                t3 = cell[1] < source[1]
##                if t3:
##                    continue
        else:
            if cellposx < sposx:
                t1 = cell != source
                t2 = cell != target
                if t1 and t2:
                    continue
##            elif cell[0] >= source[0] and cell[0] <= target[0]:
##                t3 = cell[1] > source[1]
##                if t3:
##                    continue
        if cell in exclusion:
            continue
        
        Q.append(cell)
    previouscell = None
    skip = None
##    print(Q)
##    print('source: ', source)
##    print('target: ', target)
    while len(Q) > 0:
        dist.sort(key=lambda tup: tup[1])
        mindist = 0
        i = 0      
        for d in dist:
            if d[0] in Q and skip != d[0]:
                mindist = i
                break
            i += 1
        u = dist[mindist]
        ##print(u[0])
        if not u[0] in Q:
            break
        uind = Q.index(u[0])
        t1 = u[0] == target
        t2 = prevmap[u[0]] != None
        if t1 and t2:
            break
        elif t1 and not t2:
            skip = target
            continue
        del Q[uind]

        for neighborv in Graph[u[0]]['neighbors']:
            alt = u[1] + neighborv['distance']
            vcellpos = neighborv['cellposition']
            if not vcellpos in Q:
                continue
            t1 = u[0] == source
            t2 = vcellpos == target
            ##print('u[0]', u[0])
            ##print('vcellpos:', vcellpos)
            if t1 and t2:
                continue
            if not t1 and t2:
                if skip == target:
                    skip = None
            vdist = distmap[vcellpos]
            vdistind = dist.index((vcellpos,vdist))
            pu = prevmap[vcellpos]
            vprevind = prev.index((vcellpos,pu))
            ##cyclecheck, cycle = checkminCycle(vcellpos, Paths)

            if alt < vdist:
                if vdist != float('inf'):
                    Bridgepairs.append((vcellpos,u[0]))
                dist[vdistind] = (vcellpos,alt)
                distmap[vcellpos] = alt
                prev[vprevind] = (vcellpos,u)
                prevmap[vcellpos] = u
##                addlistval(u[0], vcellpos, Paths)
##                cyclecheck, cycle = checkminCycle(vcellpos, Paths)
##                if cyclecheck:
##                    for c in cycle:
##                        Cycles[tuple(cycle[c])] = c
            elif alt > vdist:
                if vdist != float('inf'):
                    Bridgepairs.append((vcellpos,u[0]))
        previouscell = u[0]
                    
    return dist, distmap, prev, prevmap

##dist, distmap, prev, prevmap, Bridgepairs, Cycles, Paths = Dijkstramodified(nodes,(0,0))
def addexclusions(nodepair, exclusions, Graph, cycle, edgfacecount):
    ##assumed nodepair provided in proper source target ordering
    currentcell = nodepair[1]
    cposx, cposy = Graph[currentcell]['position']
    for cell in cycle:
        cellx,celly = Graph[cell]['position']
        if cposy > celly:
            order = (cell, currentcell)
        else:
            order = (currentcell, cell)
        ## order cell, currentcell
        cellind = cycle.index(cell)
##        if cellind != 0:
        for cell2 in cycle:
##        npos = cycle[cellind-1]
            npos = cell2
            nposx,nposy = Graph[npos]['position']
##            if nposx >= cposx and nposx <= cellx:
            if order in exclusions:
                if not npos in list(order):
                    exclusions[order].append(npos)
            else:
                if not npos in list(order):
                    exclusions[order] = [npos]
        if order in edgfacecount:
            edgfacecount[order] += 1
        else:
            edgfacecount[order] = 1
        currentcell = cell
    cellx,celly = Graph[cycle[0]]['position']
    if cposy > celly:
        order = (cell, currentcell)
    else:
        order = (currentcell, cell)    
    for cell2 in cycle:
##        npos = cycle[cellind-1]
        npos = cell2
        nposx,nposy = Graph[npos]['position']
##            if nposx >= cposx and nposx <= cellx:
        if order in exclusions:
            if not npos in list(order):
                exclusions[order].append(npos)
        else:
            if not npos in list(order):
                exclusions[order] = [npos]
    if order in edgfacecount:
        edgfacecount[order] += 1
    else:
        edgfacecount[order] = 1
    

def getexclusions(nodepair, exclusions):
    if nodepair in exclusions:
        return exclusions[nodepair]
    else:
        return None

def ordervertices(cycle):
    ## find minimum cycle
    cycles2 = cycle[0:len(cycle)]
    cycles2.sort(key = lambda tup:tup[0])
    mincell = cycles2[0]
    for cell in cycles2[1:len(cycles2)]:
        mincellx, mincelly = mincell
        cellx,celly = cell
        if cellx == mincellx:
            if celly < mincelly:
                mincell = cell
##    minx = float('inf')
##    miny = float('inf')
##    mincell = None
##    for cell in cycle:
##        cellx, celly = cell
##        if cellx <= minx:
##        ##and celly <= miny:
##            mincell = cell
##            minx = cellx
##            miny = celly
    mincelli = cycle.index(mincell)
    rotateval = -mincelli
    dcycle = collections.deque(cycle)
    dcycle.rotate(rotateval)
    print(list(dcycle))
    return list(dcycle)

def getrevorder(cycle):
    ## reverse the order of the cycle
    pos1 = cycle[0]
    cycle2 = cycle[1:len(cycle)]
    ## reverse list funny command oldlist[::-1] does this
    return [pos1] + cycle2[::-1]

exclusions = {}    
Cycles = {}
faceindexing = []
edgfacecount = {}
for x in range(0,dimx):
    for y in range(0,dimy):
        maxx = 0
        maxy = 0
        nextnode = None
        nposlist = []
        for neighbor in nodes[(x,y)]['neighbors']:
            npos = neighbor['cellposition']
            nposlist.append(npos)
        nposlist.sort(key = lambda tup:tup[1], reverse=True)
        nposlist2 = []##[nposlist[0]]
        ymax = nposlist[0][1]
        nposlist = nposlist[0:len(nposlist)]
        cposx, cposy = nodes[(x,y)]['position']
        for npos in nposlist:
            nposx, nposy = nodes[npos]['position']
            if nposy >= cposy:
                nposlist2.append(npos)
        if len(nposlist2) == 0:
            continue
        nposlist2.sort(key = lambda tup:tup[0])
        # choosing the ymax and xmin neighbor node
        for nextnode in nposlist2:
            nposx, nposy = nodes[nextnode]['position']
        ##nextnode = nposlist2[0]
            if cposy <= nposy:
                order = ((x,y),nextnode)
            else:
                order = (nextnode, (x,y))
            if order in edgfacecount:
                if edgfacecount[order] >= 2:
                    continue
            excs = getexclusions(order, exclusions)
            if excs == None:
                excs = []
            dist, distmap, prev, prevmap = Dijkstramodified(nodes,(x,y),
                                                            nextnode, excs)
            newNode = None
            currentNode = nextnode
            cycle = []
            while newNode != (x,y):
                if prevmap[currentNode] == None:
                    break
                cycle.append(prevmap[currentNode][0])
                newNode = prevmap[currentNode][0]
                if newNode == currentNode:
                    break

                ##print(newNode)
                ##print(currentNode)
                currentNode = newNode
            if len(cycle) != 0:
                newcycle = [order[1]]
                newcycle = newcycle + cycle
                cycle = ordervertices(newcycle)
                revcycle = getrevorder(cycle)
                t1 = tuple(cycle) in faceindexing
                t2 = tuple(revcycle) in faceindexing
                if not t1 and not t2: 
                    addexclusions(order, exclusions, nodes, cycle, edgfacecount)
                    Cycles[order] = cycle
                    faceindexing.append(tuple(cycle))

##                else:
##                    print('hit')

faces = []
for stpair in Cycles:
    verts = []
    ##verts.append(nodes[stpair[1]]['vertindex'])
    for cell in Cycles[stpair]:
        verts.append(nodes[cell]['vertindex'])
    faces.append(verts)

meshName = "GabrielGraph"
obName = "GabrielGraphObj"
me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)
ob.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(ob)
me.from_pydata(vertices,[],faces)      
me.update(calc_edges=True)   
## now to build polygons
##commonnode = False
##faces = []
##for bridgepair in Bridgepairs:
##    commonnode = False
##    face = [bridgepair[0], bridgepair[1]]
##    currentnode1 = bridgepair[0]
##    currentnode2 = bridgepair[1]
##    while not commonnode:
##        ## move current currentnode1 back 1 step in path iteration
##        nextnode1 = None
##        nextnode2 = None
##        if prevmap[currentnode1] != None:
##            nextnode1 = prevmap[currentnode1][0]
##            if not nextnode1 in face:
##                face.append(nextnode1)
##            else:
##                commonnode = True
##            currentnode1 = nextnode1
##        else:
##            currentnode1 = currentnode1
##            commonnode = True
##        if prevmap[currentnode1] != None:    
##            nextnode2 = prevmap[currentnode2][0]
##            if not nextnode2 in face:
##                face.append(nextnode2)
##            else:
##                commonnode = True
##            currentnode2 = nextnode2
##        else:
##            currentnode2 = currentnode2
##        potentialbr1 = (nextnode1, nextnode2)
##        potentialbr2 = (nextnode2, nextnode1)
##        t1 = potentialbr1 in Bridgepairs
##        t2 = potentialbr2 in Bridgepairs
##        if t1 or t2:
##            commonnode = True
##        ##print(face)    
##    faces.append(face)


## Technically incorrect results.  It would appear this method doesn't work
## well for large scale general graph.  The reason being I suspect is
##that directed
## paths are given in non cyclic orientations excepting more likely intersecting
## occurence around a given source point.  Consider the example of
## two quasi semi linear lines that never technically meet expanding out
## from a given source node.  In between we should find potentially on such
## graph possible intersecting lines that complete rings/cycles on the graph,
## but one source point from directed path construction is not enough in
## finding these.
##This may work, however, for subgraphs,
## or subset definted Q supplied to the method.

##At the moment added several methods to the Dijkstra method, one to check
## trace node paths in reverse, but similar issue as in above, and secondly
## given directionality of a source node influencing the outcome of minimal
##spanning tree, it is not always a given that a node to source path, has
## at a given node a cycle in the path history.  Deviation in roots, for
##instance, with horizontal banding paths are not garuanteed to yield
##cycles (with quasi linear paths).  Same problem as above.
## So I've attempted another method which includes a target intercept, and
##then having used a source target where both such nodes are neighbors,
##but disallowing path tracing including this minimal spanning path.  Instead
## I look for the next source to target spanning path on such neighbors, which
## should yield a cycle.  Now technically for such edge defined by source
##target there should be possibly two such alternate minimal spanning paths, where
## one is ranked less minimal relative the other.  To solve this problem,
## then having solved the first order rank, means adjusting Q in not allowing
## the 1rst cycle set.  So each source target set should be run at least twice,
## including a compliment of G intersect 1rst cycle set.  Added to this to
##prevent reiterations, one includes all previously computed cycles, when
## updating to new source target node set.  Preliminary testing seems to
## to indicate the Dijkstra method works above with source target combination
## I haven't adjusted this with a modified cycles set inclusions
## for a compliment on the graph.
## For a source target test whether or not we run two or one iteration, we
## run a neighbor test on both source and target, if there is a two branch
##split on either node then we run a two iteration source target run, otherwise
## a single run is sufficient on such edge.  To ensure that given branching
## at a given node where at least 2 nodes are to share more than 1 cycle,
## that one generates all cycles for an edge, as stated requires limiting the
##set Q so as neither to traverse a previous path set.  The problem, however,
## it seems with using a source target pattern where a source is also minimimal
## to a given target using an exclusion set on Q means that path traversal
## will take a counter clockwise rotation.  Optimally there should be some point
## on the cycle, however, that generates the cycle even if incrementally
## picking other source target pairs on the same cycle that are not going
## to generate the cycle (why is this?  Lets say the cycle has already been
## generated, then an exclusion set including previous nodes on this set,
## ensures no path trace solution.  In other words, the path on such cycle
## is traced at the outset of encountering the cycle but the cycle can't
## be generated once nodes have been excepted into an exclusion set limiting
## Q to generate the remainder for path completion.
