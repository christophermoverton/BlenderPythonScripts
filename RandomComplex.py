## Generate Random Complex K (for circle packing algorithm)
import random
import bpy
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
PolygonSize = 20  ## must be 3 or higher

def generateRandomVertex():
    return (random.random()*MaxSize, random.random()*MaxSize)

def generateRandomVertexMM(minX,maxX,minY,maxY):
    return (random.uniform(minX,maxX),random.uniform(minY,maxY))

def cubicInterpolate (p, x):
    return p[1] + 0.5 * x*(p[2] - p[0] + x*(2.0*p[0] - 5.0*p[1] + 4.0*p[2] - p[3] + x*(3.0*(p[1] - p[2]) + p[3] - p[0])))

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

def getXScale(minx,maxx):
    return 1.0/abs(maxx-minx)

def scale(scale, points):
    rpoints = []
    for point in points:
        rpoints.append((scale*point[0], scale*point[1]))
    return rpoints

def translateX(tr, points):
    rpoints = []
    for point in points:
        rpoints.append((tr + point[0], point[1]))
    return rpoints

def slope(edge):
    a, b = edge
    ax,ay = a
    bx,by = b
    return (by - ay)/(bx - ax)

def getY(point, slope, x):
    return slope*(x - point[0]) + point[1]

def getneighborverts(edge,vedges):
    a,b = edge
    n1 = None
    n2 = None
    ne1 = None
    ne2 = None
    for nedge in vedges[a]:
        if edge != nedge:
            na,nb = nedge
            ne1 = nedge
            if na == a:
                n1 = nb
            else:
                n1 = na
    for nedge in vedges[b]:
        if edge != nedge:
            na,nb = nedge
            ne2 = nedge
            if na == b:
                n2 = nb
            else:
                n2 = na
    return n1,n2,ne1,ne2
    

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
##    print(edge)
##    print(vedges)
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
       edgekeys = list(dedge.keys())
       edgekeys.sort(reverse = True)
       Q = edgekeys
    qedges = dedge[Q[0]][0:len(dedge[Q[0]])]   
    pedge = dedge[Q[0]][edgec]
    minx,maxx,miny,maxy = getMinMax(pedge)
    ##nvert = generateRandomVertexMM(minx,maxx,miny,maxy)
    x = (maxx-minx)/2.0 + minx
    n1,n2,ne1,ne2 = getneighborverts(pedge,vedges)
    a,b = pedge
    xscale = getXScale(minx,maxx)
##    print('n1:',n1)
##    print('n2:', n2)
##    print('ne1:', ne1)
##    print('ne2:', ne2)

    p = [n1,a,b,n2]
    ## we need to set up interpolation which means scaling
    ## and translating positions to end up on interval [0,1]
    ## for p1 and p2, will also need to compute position x =-1
    ## for p0 at y.
    p = scale(xscale, p)
    tr = -minx*xscale
    sxt = xscale*x+tr
    p = translateX(tr, p)
    if p[1][0] != 0.0:
        p = [p[3],p[2],p[1],p[0]]
    ne1 = (p[0],p[1])
    ne2 = (p[2],p[3])
    sne1 = slope(ne1)
    sne2 = slope(ne2)
    ny1 = getY(p[0], sne1, -1)
    ny2 = getY(p[3], sne2, 2)
    print('ny1:', ny1)
    print('ny2:', ny2)
    print('p:',p)
    py = [ny1,p[1][1],p[2][1],ny2]
    syt = cubicInterpolate (py, sxt)
    ##rescale y back to original coordinate
    ## note: we don't worry about retranslating since this isn't an xcoordinate
    y = syt*1/xscale
    vertices.append((x,y))
    nvert = (x,y)
    updateEdges(pedge[0],nvert,edges,dedge,vedges)
    updateEdges(pedge[1],nvert,edges,dedge,vedges)

    deleteEdge(pedge,edges,dedge,vedges)

    edgecount += 1
##    print('Q[0]', Q[0])
##    print('qedges', qedges)
##    print('length qedges - 1: ',len(qedges)-1)
    if edgec == len(qedges)-1:
        del Q[0]
        edgec = 0
    else:    
        edgec += 1

def polygonwalk(vert,last,target,vedges, walk):
    for edge in vedges[vert]:
        va, vb = edge
        prev = vert
        nextv = None
        if va == vert:
            if vb != last:
                walk.append(vb)
                if vb != target:
                    nextv = vb
                    polygonwalk(nextv,prev,target,vedges,walk)

        else:
            if va != last:
                walk.append(va)
                if va != target:
                    nextv = va
                    polygonwalk(nextv,prev,target,vedges,walk)


verts = list(vedges.keys())
print(vedges)
a = verts[0]
print('a',a)
tedge = vedges[a][0]
last = None
target = None
walk = [a]
print('walk:', walk)
for vert in tedge:
    if vert != a:
        target = vert
        last = vert
polygonwalk(a,last,target,vedges,walk)
face = []
for vert in walk:
    face.append(vertices.index(vert))
bvertices = []
for vert in vertices:
    x,y = vert
    bvertices.append((x,y,0.0))
faces = []
faces.append(tuple(face))
meshName = "Polygon"
obName = "PolygonObj"
me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)
ob.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(ob)
me.from_pydata(bvertices,[],faces)      
me.update(calc_edges=True) 
