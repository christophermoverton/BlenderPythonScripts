import random
##import bpy
import math

Subdivisions = 3
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

def updateRotatheir(edge, parent, rotheir):
    ## assumed under midpoint subdivision a new edge
    ## will have at least one but not more than one
    ## matching vertex to the root edge
    root = rotheir[parent]
    ra, rb = root
    a,b = edge

    ## find which vertex is closest to root a

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

edges = {}
completededges = []
edgetonewside = {}
i = 0
for findex, face in enumerate(faces):
    newface = []
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
                    edge = [list(vertices[ai])[0:2],
                            list(vertices[bi])[0:2]]  ##expects 2d
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
                    vertices.append((x,y,0.0))
                    nvindex = len(vertices)-1
                    newedgesr.append((ai,nvindex))
                    newedgesr.append((nvindex,bi))
                newedges = newedgesr[0:len(newedgesr)]
                i += 1
            newside = []  ## for edge to newside
            for edge in newedges:
                ai,bi = edge
                if not ai in newface:
                    newface.append(ai)
                    newside.append(ai)
                if not bi in newface:
                    newface.append(bi)
                    newside.append(bi)
            edgetonewside[(nn,vi)] = newside[::-1]
        else:
            newside = edgetonewside[(vi,nn)]
            for v in newside:
                if not v in newface:
                    newface.append(v)
    faces[findex] = newface[0:len(newface)]

meshName = "DualGraphSubdividePolygon"
obName = "DualGraphSubdividePolygonObj"
me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)
ob.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(ob)
me.from_pydata(vertices,[],faces)      
me.update(calc_edges=True)             
