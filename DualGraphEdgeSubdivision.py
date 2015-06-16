import random
##import bpy
import math

Subdivisions = 2

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


dvertices = vertices[0:len(vertices)]
dfaces = faces[0:len(faces)]
edges = {}
completededges = []
edgetonewside = {}
i = 0
for findex, face in enumerate(dfaces):
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

meshName = "DualGraphSubdividePolygon"
obName = "DualGraphSubdividePolygonObj"
me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)
ob.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(ob)
me.from_pydata(dvertices,[],dfaces)      
me.update(calc_edges=True)             
