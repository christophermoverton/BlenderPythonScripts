## Generate Random Complex K (for circle packing algorithm)
import random

## 1rst Generating Random polygon 
##  Monotone polygon

## Starting by generating point maxima and minima.
##  In this method, for n>=3, iteratively start by generating 3 points.

## Iterated point procedures randomly chooses an edge, then with minima,
## and maxima constraints picks a point randomly between edge minima and
## maxima, forming a new edge.
## A limit can be placed on subdivisions such that no further subdivision
## of any newly formed edge can take place without the subdivision
## of any older higher Queue priority edges in the randomization process.

MaxSize = 10
PolygonSize = 6  ## must be 3 or higher

def generateRandomVertex():
    return (random.random()*MaxSize, random.random()*MaxSize)

def generateRandomVertexMM(minX,maxX,minY,maxY):
    return (random.uniform(minX,maxX),random.uniform(minY,maxY))

def distance(a,b):
    ax,ay = a
    bx,by = b
    return ((ax-bx)**2+(ay-by)**2)**.5

def getMinMax(edge):
    edgex = edge[0:len(edge)]
    edgey = edge[0:len(edge)]
    edgex = list(edgex)
    edgey = list(edgey)
    edgex.sort(key = lambda tup:tup[0])
    edgey.sort(key = lambda tup:tup[1])
    minx = edgex[0][0]
    maxx = edgex[1][0]
    miny = edgey[0][1]
    maxy = edgey[1][1]
    return (minx,maxx,miny,maxy)

def updateEdges(a,b,edges,dedge,vedges):
    edges.append((a,b))
    d = distance(a,b)
    if d in dedge:
        dedge[d].append((a,b))
    else:
        dedge[d] = [(a,b)]
    if a in vedges:
        vedges[a].append((a,b))
    else:
        vedges[a] = [(a,b)]
    if b in vedges:
        vedges[b].append((a,b))
    else:
        vedges[b] = [(a,b)]

def deleteEdge(edge,edges,dedge,vedges):
    a,b = edge
    d = distance(a,b)
    edges.remove(edge)
    dedge[d].remove(edge)
    if len(dedge[d]) == 0:
        del dedge[d]
    print(edge)
    print(vedges)
    vedges[a].remove(edge)
    vedges[b].remove(edge)

edgecount = 0
vertices = []
edges = []
dedge = {}
vedges = {}
edged = {}
for i in range(0,3):
    vertices.append(generateRandomVertex())
    if len(vertices) > 0 and len(vertices) != 1:
        a = vertices[0]
        b = vertices[len(vertices)-1]
        updateEdges(a,b,edges,dedge,vedges)

    edgecount += 1
a = vertices[2]
b = vertices[1]
updateEdges(a,b,edges,dedge,vedges)

edgecount += 1

Q = []
edgec = 0
print(dedge)
while (edgecount < PolygonSize+1):
    if len(Q) == 0:
       ##fill Q
       ##edgescopy = edges[0:len(edges)]
       ##random.shuffle(edgescopy)
       edgekeys = dedge.keys()
       edgekeys.sort()
       Q = edgekeys
    qedges = dedge[Q[0]][0:len(dedge[Q[0]])]   
    pedge = dedge[Q[0]][edgec]
    minx,maxx,miny,maxy = getMinMax(pedge)
    nvert = generateRandomVertexMM(minx,maxx,miny,maxy)
    vertices.append(nvert)
    updateEdges(pedge[0],nvert,edges,dedge,vedges)
    updateEdges(pedge[1],nvert,edges,dedge,vedges)

    deleteEdge(pedge,edges,dedge,vedges)

    edgecount += 1
    print('Q[0]', Q[0])
    print('qedges', qedges)
    print('length qedges - 1: ',len(qedges)-1)
    if edgec == len(qedges)-1:
        del Q[0]
        edgec = 0
    else:    
        edgec += 1
