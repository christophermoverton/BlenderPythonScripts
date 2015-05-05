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

edgecount = 0
vertices = []
edges = []
for i in range(0,3):
    vertices.append(generateRandomVertex())
    if len(vertices) > 0 and len(vertices) != 1:
        edges.append((vertices[0],vertices[len(vertices)-1]))
    edgecount += 1

edges.append((vertices[2],vertices[1]))

Q = []
while (edgecount < PolygonSize+1):
    if len(Q) == 0:
       ##fill Q
       edgescopy = edges[0:len(edges)]
       random.shuffle(edgescopy)
       Q = edgescopy
    pedge = Q[0]
    minx,maxx,miny,maxy = getMinMax(pedge)
    nvert = generateRandomVertexMM(minx,maxx,miny,maxy)
    vertices.append(nvert)
    nedge1 = (pedge[0],nvert)
    nedge2 = (pedge[1],nvert)
    pedgei = edges.index(pedge)
    del edges[pedgei]
    edges.append(nedge1)
    edges.append(nedge2)
    del Q[0]
    edgecount += 1
    
    
