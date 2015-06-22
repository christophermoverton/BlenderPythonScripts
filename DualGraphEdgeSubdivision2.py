import random
##import bpy
import math

Subdivisions = 3
Height = .05
MaxScaleIterations = 10
Terrace = False
Triangulated = False
Peak = True
Scale = .95
SmoothJaggedness = 20  ## Higher factor means less jagged polygon randomization
Flatten = True
Flatteniterations = 1
if Terrace:
    MaxScaleIterations *= 2
## This algorithm is an extension of CirclePackDualGraph.py
## should have run this and previous prerequisites before running this
## script.


## Code extends from a previous version.  This version works to group
## cells into edge subdivision conglomerates where a base contour wraps
## a cellular group with closed contour curves through a series of scaled
## subdivisions.  To do this a grouping procedure need be defined here,
## the conglomerate scaled edge is defined by exterior edges of the cellular
## conglomerate and not by interior shared cellular edges.
## I also intend to define conglormerate interior conglomerates which
## then define another series of scaled subidivisions in the same way.
## Conglomerate decomposition is atomically base at a given cell.
## A conglomerate may be defined as the union of more than neighboring cell.
## A conglomerate may be thought of as an individual face alone.  I will
## use walk interchangably with the cycle of a conglomerate which defines
## in turn the points of the conglomerate in walking order from start to finish
## where the final point of the walk is connected to the first point
## representing the base of a contour edge.

## In order to scale represent the edge of a conglomerate, we do need to
## compute the centroid of it by way of all representing points given by the
## walk/cycle of it.

## 
def midpoint(edge):
    a,b = edge
    return ((a[0]+b[0])/2.0,(a[1]+b[1])/2.0)

def norm(vec):
    ##2d norm
    vx, vy = vec
    d = (abs(vx**2)+abs(vy**2))**.5
    vx = vx/d
    vy = vy/d
    return [vx,vy]

def setRotation(edge):
    ## closest distance to walk pair root determines
    ## direction of the vector
    ra, rb = edge
    rbx, rby = rb
    rax, ray = ra
    vec = [rbx-rax, rby-ray]

    ## 90 degree rotation

    vec = [-vec[1], vec[0]]
    
    vec = norm(vec)
    return vec

def addinteriorcycle(cycle,Interior,vertex, order):
    ##cycle order
    ## This is specific to the order of face indexing
    ## in the method given on scaling iterations

    if order == 2:
        Interior[vertex] = cycle
    elif order == 1:
        cycle += Interior[vertex]
        Interior[vertex] = cycle

    elif order == 5:
        Interior[vertex].insert(3,cycle[0])
        ## only to be found on scaled walk 1 time for exception.
        ## this is where 4th cycle is populated before the first.

    elif order == 7:
        Interior[vertex] += cycle

def Centroid(walk):
    ## Compute A  for a non self intersecting closed polygon
    A = 0
    i = 0
    for ind, vert in enumerate(walk):
        x,y,z = vert
        if ind == len(walk)-1:
            xp1,yp1,zp1 = walk[0]
        else:
            xp1,yp1,zp1 = walk[ind+1]
        A += x*yp1-xp1*y
    A*=.5
    Cx = 0
    Cy = 0
    for ind, vert in enumerate(walk):
        x,y,z = vert
        if ind == len(walk)-1:
            xp1,yp1,zp1 = walk[0]
        else:
            xp1,yp1,zp1 = walk[ind+1]
        Cx += (x+xp1)*(x*yp1-xp1*y)
        Cy += (y+yp1)*(x*yp1-xp1*y)
    Cx *= 1/(6*A)
    Cy *= 1/(6*A)
    return Cx,Cy

def Rescalewalk(walk,faces,vertices, nodetofaceind,
                bedgetoface, iterations):
##    centerx,centery = centroid
    i = 0
    height = 0
    prevedge = (walk[len(walk)-1],walk[0])
    owalk = walk[0:len(walk)]  ## original walk for tracking interedge nodes
    owalkmap = {}
    interFace = []
    ## initialize owalkmap
    prevFace = bedgetoface[prevedge]
    for vi, vert in enumerate(walk):
        if vi == 0:
            nvi = len(walk)-1
        else:
            nvi = vi-1
##        edge = (vert,walk[nvi])
        edge = (walk[nvi],vert)
        if bedgetoface[edge] != prevFace:
            vert1, vert2 = prevedge
            if vert in list(prevedge):
                interFace.append(vert)
            else:
                interFace.append(walk[nvi])
        center,radius = nodetofaceind[bedgetoface[edge]]
        cx = center.real
        cy = center.imag
        owalkmap[(walk[nvi],vert)] = (cx,cy)
        prevFace = bedgetoface[edge]
        prevedge = edge
    print(owalkmap)
    print(interFace)
    while i < iterations:
##        index = len(walk)*i
##        indexmn1 = len(walk)*(i-1)
        passed = False ## switch for interface check
        nvertices = []
        rscale = random.uniform(.6,.9999)
        if Terrace:
            if i % 2 == 0:
                if Flatten:
                    if i > Flatteniterations:
                        height += random.random()*Height
                else:
                    height += random.random()*Height
        else:
            if Flatten:
                if i > Flatteniterations:
                    height += random.random()*Height
            else:
                height += random.random()*Height
        for vi, vert in enumerate(walk):
##            print('passed:', passed)
            if vi == 0:
                nvert = walk[len(walk)-1]
                nvert2 = walk[len(walk)-2]
            else:
                nvert = walk[vi-1]
                if vi-1 == 0:
                    nvert2 = walk[len(walk)-1]
                else:
                    nvert2 = walk[vi-2]
                
            edge = (nvert,vert)
            if owalkmap[edge] == None:
                NextEdge = True
                passed = 2
                continue
            centerx, centery = owalkmap[edge]
            joinVert = None
            vert3 = None
            vert4 = None
            if i == 0:
                ## first walk pass we use inteface set to determine
                ## which vertices need be joined (this is not unlike a polygon
                ## inset method).
                t1 = vert in interFace
                if t1:
##                    print('hit')
                    if not passed:
                        passed = 1
##                        joinVert = nvertices[len(nvertices)-1]
##                    else:
##                        joinVert = nvertices[len(nvertices)-1]
            if passed >= 2:
##                print('hit')
                joinVert = nvertices[len(nvertices)-1]
                
                x,y,z = vertices[nvert]
##                x,y,z = vertices[vert]
                ## translate coordinates
                xtr = x - centerx
                ytr = y - centery
                xs = None
                ys = None
                
                if Terrace:
                    if i % 2 != 0:
                        xs = xtr*Scale*rscale
                        ys = ytr*Scale*rscale
                    else:
                        xs = xtr
                        ys = ytr
                else:
                    xs = xtr*Scale*rscale
                    ys = ytr*Scale*rscale
                xs += centerx
                ys += centery
                vertices.append((xs,ys,height))
                nvertices.append(len(vertices)-1)
                vert3 = len(vertices)-1
            x,y,z = vertices[vert]
            ## translate coordinates
            xtr = x - centerx
            ytr = y - centery
            xs = None
            ys = None
            
            if Terrace:
                if i % 2 != 0:
                    xs = xtr*Scale*rscale
                    ys = ytr*Scale*rscale
                else:
                    xs = xtr
                    ys = ytr
            else:
                xs = xtr*Scale*rscale
                ys = ytr*Scale*rscale
            xs += centerx
            ys += centery
            vertices.append((xs,ys,height))
##            nvertices2.append((xs,ys))
##            nvertices.append((xs, ys, height))
            nvertices.append(len(vertices)-1)
##            if i == 0:
##                continue
            vert2 = len(vertices)-1
##            verti = dvertices.index(vert)
            vert1 = vert
##            vert2 = verti+index
##            vindex = walk.index(vert)     
##            vindexn = None

            if vi == 0:
                ##vindexn = len(walk)-1
                if not passed >= 2:
                    if i == 0:
                        vert3 = len(vertices)-1+len(walk)-1+len(interFace)
                        print('vert3: ', vert3)
                    else:
                        vert3 = len(vertices)-1+len(walk)-1
                
                vert4 = walk[len(walk)-1]
            else:
                if not passed >= 2:
                    vert3 = len(vertices)-2
                vert4 = walk[vi-1]
##            vnc = walk[vindexn]
##            vni = dvertices.index(vnc)
##            vert3 = vni + index
##            vert4 = vni + indexmn1
            owalkmap[(vert3,vert2)] = (centerx,centery)
            if Triangulated:
                face = (vert1,vert2,vert4)
                faces.append(face)
                face = (vert4,vert2,vert3)
                faces.append(face)
                if passed:
                    face = (vert3,joinVert,vert4)
                    passed = False
                    owalkmap[(joinVert,vert3)] = None
                    faces.append(face)
                ## order of operations for a given vertex
                ## A vertex is first encountered in the 2nd
                ## configuration, followed by the 3rd, followed
                ## by the 1rst, followed by the 4th normally
                ## 3rd configuration is not recorded (repetition of writing
                ## vertices).  There should normally by 6 vertices
                ## recorded over the entire sequence for 1 vertex forming a cycle.
                cycle4 = [vert1,vert2,vert3]
    ##            cycle3 = [vert2]
                cycle1 = [vert4]
                cycle2 = [vert4,vert1]
                if i == 1:
                    addinteriorcycle(cycle2,Interior,vert2,2)
                elif i == MaxScaleIterations-1:
                    cycle2 = [vert3,vert4,vert1]
                    cycle3 = [vert2]
                    
                    addinteriorcycle(cycle4,Interior,vert4,1)
                    if walk.index(vert) == len(walk)-1:
                        addinteriorcycle(cycle1,Interior,vert1,5)
                        addinteriorcycle(cycle2,Interior,vert2,7)
                        addinteriorcycle(cycle3,Interior,vert3,1)
                    elif walk.index(vert) == 0:
                        addinteriorcycle(cycle3,Interior,vert3,2)
                        addinteriorcycle(cycle2,Interior,vert2,2)
                        addinteriorcycle(cycle1,Interior,vert1,1)
                    else:
                        addinteriorcycle(cycle1,Interior,vert1,1)
                        addinteriorcycle(cycle3,Interior,vert3,1)
                        addinteriorcycle(cycle2,Interior,vert2,2)
                else:
                    addinteriorcycle(cycle2,Interior,vert2,2)
                    addinteriorcycle(cycle4,Interior,vert4,1)
                    if walk.index(vert) == len(walk)-1:
                        addinteriorcycle(cycle1,Interior,vert1,5)
                    else:
                        addinteriorcycle(cycle1,Interior,vert1,1)
            else:
                face = (vert1,vert2,vert3,vert4)
                faces.append(face)
                if passed >= 2:
                    if i == 0:
                        face = (vert3,joinVert,vert4)
                    else:
                        face = (vert4,vert3,joinVert,nvert2)
                        ##face = (vert3,joinVert,vert4,vert)
                        
                    faces.append(face)
                    if not vert in interFace:
                        passed = False

##                    print('vert3: ', vert3)
##                    print('joinVert: ', joinVert)
##                    print('vert2: ', vert2)
                    owalkmap[(joinVert,vert3)] = None
            if passed:
                passed += 1
##            if vert in interFace:
##                passed = 1
        ##prevwalk = walk[0:len(walk)]
        print(list(owalkmap.keys()))
        print(nvertices)
        walk = nvertices[0:len(nvertices)]


        
        i+= 1    

## Grouping cells.
## Find the base conglomerate cycle.
## Edge tuples are keyed according to face index if any edge tuple
## that is shared (repeat finding), is added to a list interioredge.  Once
## all faces have been traversed, compliment set of interioredge, forms
## the bases of exterior edge of the base conglomerate.  We pick arbitrarily,
## an edge from a given dictionary and use the walk...this should be
## ordered as desired until we have completed the cycle.
bedges = []
bverttoedges = {}
bedgetoface = {}
dvertices = vertices[0:len(vertices)]
dfaces = faces[0:len(faces)]

for findex,face in enumerate(dfaces):
    for ind,vi in enumerate(face):
        nn = None
        if ind == len(face)-1:
            nn = face[0]
        else:
            nn = face[ind +1]
        p1 = (vi,nn)
        p2 = (nn,vi)
        t1 = (vi,nn) in bedges
        t2 = (nn,vi) in bedges
        if t1 or t2:
            if t1:
                bedges.remove(p1)
                bverttoedges[vi].remove(p1)
                bverttoedges[nn].remove(p1)
                del bedgetoface[p1]
            else:
                bedges.remove(p2)
                bverttoedges[vi].remove(p2)
                bverttoedges[nn].remove(p2)
                del bedgetoface[p2]

        else:
            bedges.append((vi,nn))
            bedgetoface[p1] = findex
            if vi in bverttoedges:
                bverttoedges[vi].append((vi,nn))
            else:
                bverttoedges[vi] = [(vi,nn)]
            if nn in bverttoedges:
                bverttoedges[nn].append((vi,nn))
            else:
                bverttoedges[nn] = [(vi,nn)]

## walk the main cycle
startedge = bedges[0]
start,nextv = startedge
## get the end vertex
end = None
for edge in bverttoedges[start]:
    if edge != startedge:
        end, cvert = edge
i = 0  ## iterator to prevent a just in case endless loop for testing
mainwalk = [start,nextv]
cedge = startedge
nextvert = nextv
while nextvert != end and i < 2000:
    for edge in bverttoedges[nextvert]:
        if edge != cedge:
            vert1, vert2 = edge
            if vert1 == nextvert:
                nextvert = vert2
            else:
                nextvert = vert1
            mainwalk.append(nextvert)
            cedge = edge
            break
    i += 1

## compute the centroid of the mainwalk
## compile the vertex positions of the mainwalk
mainwalkpos = []
for vind in mainwalk:
    mainwalkpos.append(dvertices[vind])

##Cx,Cy = Centroid(mainwalkpos)

## let's test rescaling and add new faces to mainwalk
ffaces = []
##centroid = (Cx,Cy)
evertices = dvertices[0:len(dvertices)]
Rescalewalk(mainwalk,ffaces,evertices, nodetofaceind,bedgetoface, 2)

bvertices = []

edges = {}
completededges = []
edgetonewside = {}
efaces = []
i = 0
for findex, face in enumerate(dfaces):
    newface = []
    center, radius = nodetofaceind[findex]
    centerx = center.real
    centery = center.imag
    for ind, vi in enumerate(face):
        
        nn = None
        if ind == len(face)-1:
            nn = face[0]
        else:
            nn = face[ind +1]
        t1 = (vi,nn) in edgetonewside
        if not t1:
            vedge = []
            newedges = [(vi,nn)]
##            print(newedges)
            i = 0
            while i < Subdivisions:
                newedgesr = []
                for edgevind in newedges:
                    
                    ai,bi = edgevind
                    edge = [list(dvertices[ai])[0:2],
                            list(dvertices[bi])[0:2]]  ##expects 2d
                    mpoint = midpoint(edge)
                    rvec = setRotation(edge)
                    x, y = mpoint
                    sc = random.randint(1,8)
                    posit = None
                    if random.random() > .5:
                        posit = 1
                    else:
                        posit = -1
                    ##print('y at midpoint: ', y)
                    x = x + posit*rvec[0]/(2*sc*SmoothJaggedness ) ##+ i)
                    y = y + posit*rvec[1]/(2*sc*SmoothJaggedness )##+ i)
                    dvertices.append((x,y,0.0))
                    nvindex = len(dvertices)-1
                    newedgesr.append((ai,nvindex))
                    newedgesr.append((nvindex,bi))
                newedges = newedgesr[0:len(newedgesr)]
                i += 1
            newside = []  ## for edge to newside
            for edge in newedges:
                ai,bi = edge
                if not ai in newface:
                    newface.append(ai)
                    ##newside.append(ai)
                if not bi in newface:
                    newface.append(bi)
                    ##newside.append(bi)
                if not ai in newside:
                    newside.append(ai)
                if not bi in newside:
                    newside.append(bi)
            edgetonewside[(nn,vi)] = newside[::-1]
        else:
            newside = edgetonewside[(vi,nn)]
            for v in newside:
                if not v in newface:
                    newface.append(v)
    dfaces[findex] = newface[0:len(newface)]
    Interior = {}

    walk = newface[0:len(newface)]
    prevwalk = []
    height = 0
    i = 0 
    while i < MaxScaleIterations:
##        index = len(walk)*i
##        indexmn1 = len(walk)*(i-1)
        nvertices = []
        rscale = random.uniform(.6,.9999)
        if Terrace:
            if i % 2 == 0:
                if Flatten:
                    if i > Flatteniterations:
                        height += random.random()*Height
                else:
                    height += random.random()*Height
        else:
            if Flatten:
                if i > Flatteniterations:
                    height += random.random()*Height
            else:
                height += random.random()*Height
        for vi, vert in enumerate(walk):
 
            x,y,z = dvertices[vert]
            ## translate coordinates
            xtr = x - centerx
            ytr = y - centery
            xs = None
            ys = None
            
            if Terrace:
                if i % 2 != 0:
                    xs = xtr*Scale*rscale
                    ys = ytr*Scale*rscale
                else:
                    xs = xtr
                    ys = ytr
            else:
                xs = xtr*Scale*rscale
                ys = ytr*Scale*rscale
            xs += centerx
            ys += centery
            dvertices.append((xs,ys,height))
##            nvertices2.append((xs,ys))
##            nvertices.append((xs, ys, height))
            nvertices.append(len(dvertices)-1)
##            if i == 0:
##                continue
            vert2 = len(dvertices)-1
##            verti = dvertices.index(vert)
            vert1 = vert
##            vert2 = verti+index
##            vindex = walk.index(vert)     
##            vindexn = None
            vert3 = None
            vert4 = None
            if vi == 0:
                ##vindexn = len(walk)-1
                vert3 = len(dvertices)-1+len(walk)-1
                vert4 = walk[len(walk)-1]
            else:
                vert3 = len(dvertices)-2
                vert4 = walk[vi-1]
##            vnc = walk[vindexn]
##            vni = dvertices.index(vnc)
##            vert3 = vni + index
##            vert4 = vni + indexmn1
            if Triangulated:
                face = (vert1,vert2,vert4)
                efaces.append(face)
                face = (vert4,vert2,vert3)
                efaces.append(face)
                ## order of operations for a given vertex
                ## A vertex is first encountered in the 2nd
                ## configuration, followed by the 3rd, followed
                ## by the 1rst, followed by the 4th normally
                ## 3rd configuration is not recorded (repetition of writing
                ## vertices).  There should normally by 6 vertices
                ## recorded over the entire sequence for 1 vertex forming a cycle.
                cycle4 = [vert1,vert2,vert3]
    ##            cycle3 = [vert2]
                cycle1 = [vert4]
                cycle2 = [vert4,vert1]
                if i == 1:
                    addinteriorcycle(cycle2,Interior,vert2,2)
                elif i == MaxScaleIterations-1:
                    cycle2 = [vert3,vert4,vert1]
                    cycle3 = [vert2]
                    
                    addinteriorcycle(cycle4,Interior,vert4,1)
                    if walk.index(vert) == len(walk)-1:
                        addinteriorcycle(cycle1,Interior,vert1,5)
                        addinteriorcycle(cycle2,Interior,vert2,7)
                        addinteriorcycle(cycle3,Interior,vert3,1)
                    elif walk.index(vert) == 0:
                        addinteriorcycle(cycle3,Interior,vert3,2)
                        addinteriorcycle(cycle2,Interior,vert2,2)
                        addinteriorcycle(cycle1,Interior,vert1,1)
                    else:
                        addinteriorcycle(cycle1,Interior,vert1,1)
                        addinteriorcycle(cycle3,Interior,vert3,1)
                        addinteriorcycle(cycle2,Interior,vert2,2)
                else:
                    addinteriorcycle(cycle2,Interior,vert2,2)
                    addinteriorcycle(cycle4,Interior,vert4,1)
                    if walk.index(vert) == len(walk)-1:
                        addinteriorcycle(cycle1,Interior,vert1,5)
                    else:
                        addinteriorcycle(cycle1,Interior,vert1,1)
            else:
                face = (vert1,vert2,vert3,vert4)
                efaces.append(face)
        ##prevwalk = walk[0:len(walk)]
        walk = nvertices[0:len(nvertices)]

        
        i+= 1
    if Peak:
        height += random.random()*Height
    dvertices.append((centerx,centery,height))
    ## Final face/vertex pass
    vert3 = len(dvertices)-1
    Interior[vert3] = []
    for vi,vert in enumerate(walk):
##        cycle = [vert3]
##        verti = vertices.index(vert)
        vert1 = vert
##        Interior[vert3].append(vert1)
##        cycle += Interior[vert1]
##        Interior[vert1] = cycle
##        vindex = walk.index(vert)     
        vert2 = None
        if vi == 0:
            vert2 = walk[len(walk)-1]
        else:
            vert2 = walk[vi-1]
##        vnc = walk[vindexn]
##        vni = vertices.index(vnc)
##        vert2 = vni + index
        face = (vert1,vert3,vert2)
        efaces.append(face)

meshName = "DualGraphSubdividePolygon"
obName = "DualGraphSubdividePolygonObj"
me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)
ob.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(ob)
me.from_pydata(evertices,[],ffaces)      
me.update(calc_edges=True)             

