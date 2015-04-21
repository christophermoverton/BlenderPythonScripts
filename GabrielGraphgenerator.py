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
                attr['neighbors'].append(nattr)
                currentattr = {}
                currentattr['cellposition'] = (x,y)
                currentattr['position'] = (posx,posy)
                nodes[c2pos]['neighbors'].append(currentattr)
        nodes[(x,y)] = attr

## now we need to path trace from to and from a starting vertex without
## the trivial path that is from start to second vertex back to start
## That is we need build faces.  This gets trickier since we can span in
## many different directions on the node neighbor tree.  To solve this
## problem we might want to put a cap on the absolute distance from the
## originating starting cell position...say maybe no more than +/- 7 units
## on either axis or otherwise we kill the recursion search?
## we also need a minimally spanning distance set.
## In this case, we can do see by examining a family of paths,
## the smallest set in such family yields the minimal spanning path.
## maybe more efficient methods exist here...maybe a weighting method for
## recusion searching a path?
