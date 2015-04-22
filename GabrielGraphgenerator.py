import random
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
dimx = 10
dimy = 10
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

for x in range(0,dimx):
    for y in range(0,dimy):
        attr = {}
        localx = random.random()
        localy = random.random()
        posx = cellsize*localx+x*cellsize
        posy = cellsize*localy+y*cellsize
        attr = {'position':(posx,posy)}
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
def Dijkstramodified(Graph, source):
    ## we modify target so that the solution
    ## source -target path is disallowed 
    ##dist = {source: {'distance':0, 'index':0}}
    dist = [(source,0)]
    distmap = {source:0}
    prev = [(source,None)]
    prevmap = {source:None}
    Bridgepairs = [] ## celladdressing pair tuple
    Q = []
    for cell in Graph:
        if cell != source:
            distmap[cell] = float('inf')
            dist.append((cell,float('inf')))
            prevmap[cell] = None
            prev.append((cell, None))
        Q.append(cell)
    while len(Q) > 0:
        dist.sort(key=lambda tup: tup[1])
        mindist = 0
        i = 0
        for d in dist:
            if d[0] in Q:
                mindist = i
                break
            i += 1
        u = dist[mindist]
        
        uind = Q.index(u[0])
        del Q[uind]

        for neighborv in Graph[u[0]]['neighbors']:
            alt = u[1] + neighborv['distance']
            vcellpos = neighborv['cellposition']
            vdist = distmap[vcellpos]
            vdistind = dist.index((vcellpos,vdist))
            pu = prevmap[vcellpos]
            vprevind = prev.index((vcellpos,pu))
            if alt < vdist:
                if vdist != float('inf'):
                    Bridgepairs.append((vcellpos,u[0]))
                dist[vdistind] = (vcellpos,alt)
                distmap[vcellpos] = alt
                prev[vprevind] = (vcellpos,u)
                prevmap[vcellpos] = u
            elif alt > vdist:
                if vdist != float('inf'):
                    Bridgepairs.append((vcellpos,u[0]))                
    return dist, distmap, prev, prevmap, Bridgepairs

dist, distmap, prev, prevmap, Bridgepairs = Dijkstramodified(nodes, (0,0))
