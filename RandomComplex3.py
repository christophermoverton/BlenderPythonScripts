## Generate Random Complex K (for circle packing algorithm)
import random
import bpy
import math
## 1rst Generating Random polygon 
##   
## Starting by generating point maxima and minima.
##  In this method, for n>=3, iteratively start by generating 3 points.

## Iterated point procedures randomly chooses an edge, then with minima,
## and maxima constraints picks a point randomly between edge minima and
## maxima, forming a new edge.
## A limit can be placed on subdivisions such that no further subdivision
## of any newly formed edge can take place without the subdivision
## of any older higher Queue priority edges in the randomization process.

## This modification of RandomComplex.py instead uses the computed circumcircle
## of the 3 gon base, and then prescribes boundary points along
## the circumcircle in determining edge subdivisions.

## Alternately one can generate the random circle and then three random points
## given to a distance conformal mapping to the circle's radial arc.

## For instance, one way to do this is in polar coordinates randomly choosing
## an angle and then with a known radius computing x, y coordinates
## from polar ones.



Triangulated = True
MaxSize = 10
PolygonSize = 30 ## must be 3 or higher
MaxScaleIterations = 30
Scale = .95
EarlyRandom = True  ## leads to greater probability of less convex polygon,
                     ##more jagged
AllConvex = True ## yields Completely convex polygon


def det2(a11,a21,a12,a22):
    return a11*a22-a21*a12

def cofactmatrix(matA,element,i,j):
    ## exclude row and column of element
    ## where i and j represent the row and column index respectively
    matB = []
    ##print('i: ', i)
    ##print('j: ', j)
    l = 0
    for row in matA:
        rowvec = []
        if l != i:
            ##print(row)
            k = 0
            for col in row:
                if k != j:
                    rowvec.append(col)
                k += 1
            matB.append(rowvec)
        l += 1
    ##print(matB)
    return matB

def computedet(matA):
    ## find the cofactors and determine that the matrix is
    ## in a given 2x2 base if not repeat the procedure.
    ## assumed matrix provided is square
    i = 0
    j = 0
    if len(matA) > 2:
        cdetsum = 0
        for row in matA:
            j = 0
            if  i > 0:
                break
            for col in matA[i]:
                s = i+j % 2 
                if s == 0:
                    s = 1
                else:
                    s = -1
                matB = cofactmatrix(matA,col,i,j)
                det = None
                if len(matB) >= 2:
                    det = computedet(matB)
                cdetsum += s*col*det
                j += 1
            i += 1
        return cdetsum 
    else:
        ##print(matA)
        return det2(matA[0][0],matA[0][1],matA[1][0],matA[1][1])

## sources from http://mathworld.wolfram.com/Circumcircle.html
# x0 = - bx/2a y0 = -by/2a
## r = (bx^2+by^2 - 4ac)^1/2 /2|a|

## a = det([[x1,y1,1],[x2,y2,1],[x3,y3,1]])
## bx = -1* det([[x1^2+y1^2, y1, 1],[x2^2+y2^2,y2,1],[x3^2+y3^2,y3,1]])
## by = det([[x1^2+y1^2, x1, 1],[x2^2+y2^2,x2,1],[x3^2+y3^2,x3,1]])
## c = -1*det([[x1^2+y1^2, x1, y1],[x2^2+y2^2,x2,y2],[x3^2+y3^2,x3,y3]])

def circumcircle(p1,p2,p3):
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    a = computedet([[x1,y1,1],[x2,y2,1],[x3,y3,1]])
    bx = -1* computedet([[abs(x1**2)+abs(y1**2), y1, 1],
                         [abs(x2**2)+abs(y2**2), y2, 1],
                         [abs(x3**2)+abs(y3**2), y3, 1]])
    by = computedet([[abs(x1**2)+abs(y1**2), x1, 1],
                     [abs(x2**2)+abs(y2**2), x2, 1],
                     [abs(x3**2)+abs(y3**2), x3, 1]])
    c = -1*computedet([[abs(x1**2)+abs(y1**2), x1, y1],
                       [abs(x2**2)+abs(y2**2), x2, y2],
                       [abs(x3**2)+abs(y3**2), x3, y3]])
    x0 = -bx/(2*a)
    y0 = -by/(2*a)
    r = (abs(bx**2)+abs(by**2) - 4*a*c)**.5/ (2*abs(a))
    return (x0,y0,r)
    
def clockwisewalktest(walk):
    ## works with nonconvex polygons should be safe
    ## I believe for the primitive polygon type (3 vertices)
    ## constructed in this algorithm.
    prev = None
    samt = 0.0
    newwalk = walk[0:len(walk)]
    newwalk.append(walk[0])
    for vert in newwalk:
        if prev == None:
            prev = vert
            continue
##        samt += (vert[0]-prev[0])*(vert[1]+prev[1])
        samt += (prev[0]*vert[1]-prev[1]*vert[0])
##        if walk.index(vert) == len(walk)-1:
##            samt += (walk[0][0] - vert[0])*(walk[0][1]+vert[1])
        prev = vert
    print('samt: ', samt)
    if samt < 0:
        print('original walk is clockwise')
        return True
    else:
        print('original walk is counter clockwise')
        return False

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
def convextest(v1,v2,v3,v4):
    def crossproduct(p1,p2):
        return (p1[0]*p2[1] - p1[1]*p2[0])
    ## assumed v1,v2,v3,v4 are sequentially ordered on the
    ##polygon walk
    ## this is cross product comparison
    t1 = crossproduct(v1,v2) == crossproduct(v2,v3)
    t2 = crossproduct(v3,v4) == crossproduct(v1,v2)
    if t1 and t2:
        return True
    else:
        return False
    

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

def angle(slope):
    return math.atan(slope)

def rotatecoord(coord, theta):
    x,y = coord
    return (x*math.cos(theta) - y*math.sin(theta),
            x*math.sin(theta) + y*math.cos(theta))

def midpoint(edge):
    a,b = edge
    return ((a[0]+b[0])/2,(a[1]+b[1])/2)

def slopenormal(edgeslope):
    return - 1/edgeslope

def testdirection(edge1, edge2):
    #assumed edge1 = (a,b) and edge2 = (b,c)
    # where b intersect edge 1 and 2
    a,b = edge1
    b,c = edge2
    if c > b:
        if a > b:
            return False
        else:
            return True
    else:
        if a > b:
            return True
        else:
            return False

def setRotation(edge, rotheir):
    ## closest distance to walk pair root determines
    ## direction of the vector
    root = rotheir[edge]
    ra, rb = root
    rbx, rby = rb
    rax, ray = ra
    vec = [rbx-rax, rby-ray]
##    a,b = edge
##    ax,ay = a
##    bx,by = b
##    ## find which vertex is closest to root a
##    dara = distance(a,ra)
##    dbra = distance(b,ra)
##    if dara < dbra:
##    vec = [bx-ax, by-ay]
##    else:
##    vec = [ax-bx, ay-by]
    ## 90 degree rotation
    print('ab vector: ', vec)
    vec = [-vec[1], vec[0]]
    print('rotation edge: ', edge)
    print('rotation vector: ', vec)
    return vec

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

def norm(vec):
    ##2d norm
    vx, vy = vec
    d = (abs(vx**2)+abs(vy**2))**.5
    vx = vx/d
    vy = vy/d
    return [vx,vy]
    
def updateEdges(a,b,edges,dedge,vedges):
    edges.append((a,b))
    d = distance(a,b)
    if d in dedge:
        if (a,b) in dedge[d]:
            print('duplicate edge FOUND!')
            print('dup edge: ', (a,b))
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

def updateRotatheir(edge, parent, rotheir):
    ## assumed under midpoint subdivision a new edge
    ## will have at least one but not more than one
    ## matching vertex to the root edge
    root = rotheir[parent]
    ra, rb = root
    a,b = edge
    ax,ay = a
    bx,by = b
    ## find which vertex is closest to root a
##    dara = distance(a,ra)
##    dbra = distance(b,ra)
##    if dara < dbra:
##        rotheir[edge] = (a,b)
##    else:
##        rotheir[edge] = (b,a)
    if a == ra or a == rb:
        if a == rb:
            rotheir[edge] = (b,a)
        else:
            rotheir[edge] = (a,b)
    if b == ra or b == rb:
        if b == rb:
            rotheir[edge] = (a,b)
        else:
            rotheir[edge] = (b,a)

def deleteEdge(edge,edges,dedge,vedges):
    a,b = edge
    d = distance(a,b)
    edges.remove(edge)
    print('removing from dedge: ', dedge[d])
    print('edge: ', edge)
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
rotheir = {}
for i in range(0,3):
    vertices.append(generateRandomVertex())
    if len(vertices) > 0 and len(vertices) != 1:
        a = vertices[0]
        b = vertices[len(vertices)-1]
        updateEdges(a,b,edges,dedge,vedges)
        rotheir[(a,b)] = (a,b)

    edgecount += 1
a = vertices[2]
b = vertices[1]
c = vertices[0]
centerx,centery,circler = circumcircle(c,b,a)
print('centerx, centery, circler ', (centerx,centery,circler))
updateEdges(a,b,edges,dedge,vedges)
rotheir[(a,b)] = (a,b)
edgecount += 1

## create walk order used in determining rotations
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

print('original walk: ', walk)
newwalk = []
if not clockwisewalktest(walk):
    walk0 = walk[0]
    walk1 = walk[1:len(walk)]
    walk1 = walk1[::-1]  ## reverse the order for clockwise
    newwalk.append(walk0)
    newwalk += walk1
    walk = newwalk
    
print('rotation order walk: ', walk)

def setrotatheirorder(walk, rotheir):
    prev = None
    for vert in walk:
        if prev == None:
            prev = vert
            continue
        print('vert,prev pair: ', (vert,prev))
        if (vert, prev) in rotheir:
            print('found rev order rotheir key')
            print('vert,prev pair: ', (vert,prev))
            rotheir[(vert,prev)] = (prev,vert)
        if walk.index(vert) == len(walk)-1:
            if (walk[0], vert) in rotheir:
                rotheir[(walk[0],vert)] = (vert,walk[0])
        prev = vert

def computeNormtoArc(edge, mpoint, norm, r, C):
    ## as per wiki using solution indicated.
    ## s = r - (r*r-l*l)**.5
    a,b = edge
    l2 = distance(a,b)
    l = l2/2.0
    s = r - (r*r-l*l)**.5
    print('s: ', s)
    x,y = mpoint
    dnx,dny = [s*norm[0], s*norm[1]]
    px,py = [x+dnx,y+dny]
    d = distance(mpoint,(px,py))
    ## check to see that this point relative to norm lies on
    ## the circle, if not then we recompute the point using -norm
    ## we then have to find the distance in the direction of the norm
    ## which is r+ distance(c-mp) where c is the center of the circle,
    ## and mp is the midpoint.
    dist = distance(C,(px,py))
    print('radius: ', r)
    print('distance between C and px,py: ', distance(C,(px,py)))
    
    if dist < r or dist > r:
        normi = [-norm[0],-norm[1]]
        dnxi,dnyi = [s*normi[0], s*normi[1]]
        pxi,pyi = [x+dnxi,y+dnyi]
        dcmp = 2*r-distance(mpoint,(pxi,pyi))
        d = dcmp
        dnx,dny = [dcmp*norm[0], dcmp*norm[1]]
        px,py = [x+dnx,y+dny]
        dist = distance(C,(px,py))
        print('new distance between C and px,py', dist)
    return ((px,py),d)
        
def computeNormtoArc2(edge, point, norm, r, C):
    ## generalized solution for any given point on the secant
    ## different method per wiki
    a,b = edge
    ax,ay = a
    bx,by = b
    px, py = point
    Cx,Cy = C
    ## translate point and edge
    atrx,atry = [ax-Cx,ay-Cy]
    btrx,btry = [bx-Cx,by-Cy]
    ptrx,ptry = [px-Cx,py-Cy]
    at = (atrx,atry)
    bt = (btrx,btry)
    ##compute angle of secant
    sedge = slope((at,bt)) ## invariant under translation
    theta = math.atan(sedge)
    ptrrtx, ptrrty = rotatecoord((ptrx,ptry), theta)
    ## also find rotated coordinates of the norm
    ## since we will compare solution values to the norm
    nrtx, nrty = rotatecoord(norm, theta)
    ## compute y'
    yp = ((r*r-ptrrtx*ptrrtx))**.5
    ## check +/- solution of yp
    ## this is whether or not the direction of ptrrty to + point on the arc
    ## is in the desired norm direction.  If not then we use the -yp
    ## solution.
    direcyp = yp - ptrrty
    ##t1 = math.copysign(1,ptrrtx) == math.copysign(1,nrtx)
    t2 = math.copysign(1,direcyp) == math.copysign(1,nrty)
    if not t2:
        yp = -yp
    ## convert to previous pre rotated coordinate system
    strx, stry = rotatecoord((ptrrtx,yp), -theta)
    return ((strx+Cx,stry+Cy), distance((strx+Cx,stry+Cy),point))

def Centroid(walk):
    ## Compute A  for a non self intersecting closed polygon
    A = 0
    i = 0
    for vert in walk:
        x,y = vert
        if i == len(walk)-1:
            xp1,yp1 = walk[0]
        else:
            xp1,yp1 = walk[walk.index(vert)+1]
        A += x*yp1-xp1*y
    A*=.5
    Cx = 0
    Cy = 0
    for vert in walk:
        x,y = vert
        if i == len(walk)-1:
            xp1,yp1 = walk[0]
        else:
            xp1,yp1 = walk[walk.index(vert)+1]
        Cx += (x+xp1)*(x*yp1-xp1*y)
        Cy += (y+yp1)*(x*yp1-xp1*y)
    Cx *= 1/(6*A)
    Cy *= 1/(6*A)
    return Cx,Cy


        
setrotatheirorder(walk,rotheir)
print('rotheir: ', rotheir)

Q = []
edgec = 0
print(dedge)
qedges = None
pedge = None
parents = []
i = 0
circmax = random.randint(3,12)
if AllConvex:
    circmax = PolygonSize+1
while (edgecount < PolygonSize+1):
    if len(Q) == 0:
       ##fill Q
       ##edgescopy = edges[0:len(edges)]
       ##random.shuffle(edgescopy)
       edgekeys = list(dedge.keys())
       edgekeys.sort(reverse = True)
       Q = edgekeys[0:1]
##       avgQ = sum(Q)/float(len(Q))
##       for dist in Q:
##           if dist/avgQ < .1:
##               Q.remove(dist)
##               print('removing dist: ', dist)
       print('Q :', Q)
       i += 1
    if edgec == 0:
        print('new qedges: ', dedge[Q[0]])
        qedges = dedge[Q[0]][0:len(dedge[Q[0]])]
        pedge = dedge[Q[0]][edgec]
    else:
        pedge = qedges[edgec]
    minx,maxx,miny,maxy = getMinMax(pedge)
    x = None
    y = None
    ##nvert = generateRandomVertexMM(minx,maxx,miny,maxy)
    x = (maxx+minx)/2.0
    n1,n2,ne1,ne2 = getneighborverts(pedge,vedges)
##    if testdirection(ne1,pedge) and testdirection(pedge,ne2):
    if edgecount > circmax:
        a,b = pedge
    ##    print('n1:',n1)
    ##    print('n2:', n2)
    ##    print('ne1:', ne1)
    ##    print('ne2:', ne2)
##        if testdirection(ne1,pedge) and testdirection(pedge,ne2):
##            p = [n1,a,b,n2]
##            n1n2slope = slope((n1,n2))
##            theta = angle(n1n2slope)
##            thetai = -theta
##            n1 = rotatecoord(n1, theta)
##            a = rotatecoord(a, theta)
##            b = rotatecoord(b, theta)
##            minx,maxx,miny,maxy = getMinMax((a,b))
##            xscale = getXScale(minx,maxx)
##            n2 = rotatecoord(n2, theta)
##            abslope = slope(pedge)
##            midy = getY(pedge[0],abslope,x)
##            xr,yr = rotatecoord((x,midy), theta)
##            print('xr, yr:', (xr,yr))
##            print('x, y: ', (x, midy))
##            print('check x, y: ', rotatecoord((xr,yr), thetai))
##            p = [n1,a,b,n2]
##            ## we need to set up interpolation which means scaling
##            ## and translating positions to end up on interval [0,1]
##            ## for p1 and p2, will also need to compute position x =-1
##            ## for p0 at y.
##            p = scale(xscale, p)
##            tr = -minx*xscale
##            sxt = xscale*xr+tr
##            p = translateX(tr, p)
##            if p[1][0] != 0.0:
##                p = [p[3],p[2],p[1],p[0]]
##            ne1 = (p[0],p[1])
##            ne2 = (p[2],p[3])
##            sne1 = slope(ne1)
##            sne2 = slope(ne2)
##            ny1 = getY(p[0], sne1, -1)
##            ny2 = getY(p[3], sne2, 2)
##            print('ny1:', ny1)
##            print('ny2:', ny2)
##            print('p:',p)
##            print('sxt: ', sxt)
##            py = [ny1,p[1][1],p[2][1],ny2]
##            
##            syt = cubicInterpolate (py, sxt)
##            ##rescale y back to original coordinate
##            ## note: we don't worry about retranslating since this isn't an xcoordinate
##            y = syt*1/xscale
##            xpt = (sxt-tr)*1/xscale
##            x,y = rotatecoord((xpt,y),thetai)
##        else:
##            a,b = pedge
##            xscale = getXScale(minx,maxx)
##        ##    print('n1:',n1)
##        ##    print('n2:', n2)
##        ##    print('ne1:', ne1)
##        ##    print('ne2:', ne2)
##
##            p = [n1,a,b,n2]
##            ## we need to set up interpolation which means scaling
##            ## and translating positions to end up on interval [0,1]
##            ## for p1 and p2, will also need to compute position x =-1
##            ## for p0 at y.
##            p = scale(xscale, p)
##            tr = -minx*xscale
##            sxt = xscale*x+tr
##            p = translateX(tr, p)
##            if p[1][0] != 0.0:
##                p = [p[3],p[2],p[1],p[0]]
##            ne1 = (p[0],p[1])
##            ne2 = (p[2],p[3])
##            sne1 = slope(ne1)
##            sne2 = slope(ne2)
##            ny1 = getY(p[0], sne1, -1)
##            ny2 = getY(p[3], sne2, 2)
##            print('ny1:', ny1)
##            print('ny2:', ny2)
##            print('p:',p)
##            py = [ny1,p[1][1],p[2][1],ny2]
##            syt = cubicInterpolate (py, sxt)
##            ##rescale y back to original coordinate
##            ## note: we don't worry about retranslating since this isn't an xcoordinate
##            y = syt*1/xscale
        mpoint = midpoint(pedge)
##        pslope = slope(pedge)
##        nslope = slopenormal(pslope)
        rvec = setRotation(pedge, rotheir)
##        y = getY(pedge[0], pslope, x)
        x, y = mpoint
        sc = random.randint(1,8)
        print('y at midpoint: ', y)
        x = x + rvec[0]/(4*sc ) ##+ i)
        y = y + rvec[1]/(4*sc)##+ i)
        
    else:
        mpoint = midpoint(pedge)
##        pslope = slope(pedge)
##        nslope = slopenormal(pslope)
        rvec = setRotation(pedge, rotheir)
##        y = getY(pedge[0], pslope, x)
##        rvec = [mpoint[0]-centerx, mpoint[1]-centery]
        x, y = mpoint
        print('y at midpoint: ', y)
        dmidcent = distance((centerx,centery),mpoint)
##        vlen = circler - dmidcent
        rvec = norm(rvec)
##        rvec = (rvec[0]*vlen, rvec[1]*vlen)
        if EarlyRandom:
            rval = random.random()
            rvec = (rvec[0]*rval*circler, rvec[1]*rval*circler)
        else:
            rvec = (rvec[0]*circler, rvec[1]*circler)
##        x = x + rvec[0] ##+ i)
##        y = y + rvec[1] ##+ i)
        print('rvec: ', rvec)
        C = [centerx,centery]
##        p,d = computeNormtoArc(pedge, mpoint, rvec, circler, C)
##        p,d = computeNormtoArc2(pedge, mpoint, rvec, circler, C)
##        if EarlyRandom:
##            rval = random.random()
##            x,y = [x+rval*d*rvec[0],y+rval*d*rvec[1]]
##        else:
##            x,y = p
        x = centerx + rvec[0]
        y = centery + rvec[1]
    vertices.append((x,y))
    nvert = (x,y)
    updateEdges(pedge[0],nvert,edges,dedge,vedges)
    updateEdges(pedge[1],nvert,edges,dedge,vedges)
    print('new vertex: ', nvert)
    deleteEdge(pedge,edges,dedge,vedges)
    nedge1 = (pedge[0],nvert)
    nedge2 = (pedge[1],nvert)
    updateRotatheir(nedge1, pedge, rotheir)
    updateRotatheir(nedge2, pedge, rotheir)
    del rotheir[pedge]
    edgecount += 1
    print('pedge: ', pedge)
    print('Q[0]', Q[0])
    print('qedges', qedges)
    print('length qedges - 1: ',len(qedges)-1)
    if edgec == len(qedges)-1:
        del Q[0]
        edgec = 0
    else:    
        edgec += 1




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
normneighbors = {}
prevvertices = vertices[0:len(vertices)]
i = 1
bvertices = []
##bvertices += vertices
for vert in vertices:
    x,y = vert
    bvertices.append((x,y,0.0))
faces = []
height = 0
while i < MaxScaleIterations:
    index = len(walk)*i
    indexmn1 = len(walk)*(i-1)
    nvertices = []
    nvertices2 = []
    height += random.random()*.1
    for vert in walk:
        verti = vertices.index(vert)
        vert1 = verti+indexmn1
        vert2 = verti+index
        vindex = walk.index(vert)     
        vindexn = None
        if vindex == 0:
            vindexn = len(walk)-1
        else:
            vindexn = vindex-1
        vnc = walk[vindexn]
        vni = vertices.index(vnc)
        vert3 = vni + index
        vert4 = vni + indexmn1
        if Triangulated:
            face = (vert1,vert2,vert4)
            faces.append(face)
            face = (vert4,vert2,vert3)
            faces.append(face)
        else:
            face = (vert1,vert2,vert3,vert4)
            faces.append(face)
    for vert in prevvertices:
        x,y = vert
        ## translate coordinates
        xtr = x - centerx
        ytr = y - centery
        xs = xtr*Scale
        ys = ytr*Scale
        xs += centerx
        ys += centery
        nvertices2.append((xs,ys))
        nvertices.append((xs, ys, height))
    prevvertices = nvertices2[0:len(nvertices2)]
    bvertices += nvertices
    i+= 1

height += random.random()*.1
bvertices.append((centerx,centery,height))
## Final face/vertex pass
vert3 = len(bvertices)-1
for vert in walk:
    verti = vertices.index(vert)
    vert1 = verti+index
    vindex = walk.index(vert)     
    vindexn = None
    if vindex == 0:
        vindexn = len(walk)-1
    else:
        vindexn = vindex-1
    vnc = walk[vindexn]
    vni = vertices.index(vnc)
    vert2 = vni + index
    face = (vert1,vert3,vert2)
    faces.append(face)
    
## to solve the problem of nested scaling of a polygon to a common
## centroid, one need translate coordinates of the original polygon
## so that the centroid is the origin, scale all vertices, then
## retranslate these coordinates back to the original coordinate
## system.
##for vert in walk:    
##    face.append(vertices.index(vert))
##bvertices = []
##for vert in vertices:
##    x,y = vert
##    bvertices.append((x,y,0.0))
##faces = []
##faces.append(tuple(face))
meshName = "Polygon"
obName = "PolygonObj"
me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)
ob.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(ob)
me.from_pydata(bvertices,[],faces)      
me.update(calc_edges=True) 
