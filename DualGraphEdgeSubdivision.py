import random
##import bpy
import math

Subdivisions = 2
Height = .3
MaxScaleIterations = 3
Terrace = False
Triangulated = False
Peak = True
Scale = .7
if Terrace:
    MaxScaleIterations *= 2
## This algorithm is an extension of CirclePackDualGraph2.py
## should have run this and previous prerequisites before running this
## script.

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



dvertices = vertices[0:len(vertices)]
bvertices = []
dfaces = faces[0:len(faces)]
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
                    x = x + posit*rvec[0]/(4*sc ) ##+ i)
                    y = y + posit*rvec[1]/(4*sc)##+ i)
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
    
        if Terrace:
            if i % 2 == 0:
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
                    xs = xtr*Scale
                    ys = ytr*Scale
                else:
                    xs = xtr
                    ys = ytr
            else:
                xs = xtr*Scale
                ys = ytr*Scale
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
me.from_pydata(dvertices,[],efaces)      
me.update(calc_edges=True)             

