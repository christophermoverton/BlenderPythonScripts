import cmath
import math
import bpy

## It is expected that CirclePackDualGraph.py has been run prior to instancing
## this script.  It is also expected that Penrose2.py has been instanced
## that is loaded in console.

triangles = []
pvertices = []
pfaces = []
pselections = []
nextinc = 0
nextincf = 0
Scaleiterations = 2
Scale = .5
def midpoint(edge):
    ## complex form of midpoint
    a,b = edge
    return (a+b)/2

def rescale(A, Center, Scale = Scale):
    A -= Center
    A *= Scale
    A += Center
    return A

for findex, face in enumerate(faces):
    croot,cradius = nodetofaceind[findex]
    ## sample height
    z = vertices[face[0]][2]
    print('face z: ', z)
##    rx,ry = root
##    croot = complex(rx,ry)
    triangles = []
    POLY = float(len(face)*2.0)
    prevface = []
    for index, vert in enumerate(face):
        pvertices.append(vertices[vert])
        prevface.append(len(pvertices)-1)
        nindex = None
        nvert = None
        if index == len(face)-1:
            nindex = 0
        else:
            nindex = index+1
        nvert = face[nindex]
        vcoord = vertices[vert]
        nvcoord = vertices[nvert]
        xv,yv,zv = vcoord
        xnv,ynv,znv = nvcoord
        a = complex(xv,yv)
        b = complex(xnv,ynv)
        mab = midpoint((a,b))
        x = mab.real
        y = mab.imag
        pvertices.append(tuple((x,y,z)))
        prevface.append(len(pvertices)-1)
        
    for i in range(Scaleiterations):
        nwalk = []
        for index, vert in enumerate(prevface):
            nindex = None
            nvert = None
            if index == len(prevface)-1:
                nindex = 0
            else:
                nindex = index+1
            nvert = prevface[nindex]
            vcoord = pvertices[vert]
            nvcoord = pvertices[nvert]
            xv,yv,zv = vcoord
            xnv,ynv,znv = nvcoord
            a = complex(xv,yv)
            b = complex(xnv,ynv)
##            mab = midpoint((a,b))
            a = rescale(a,croot)
            b = rescale(b,croot)
            pvertices.append(tuple((a.real,a.imag,z)))
            av1 = len(pvertices)-1
            nwalk.append(av1)
            ##pvertices.append(tuple(b.real,b.imag, z))
            bv1 = None
            if nindex == 0:
                bv1 = nwalk[0]
            else:
                bv1 = len(pvertices)
            nface = [vert,nvert,bv1,av1]
            pfaces += [nface]
        prevface = nwalk[0:len(nwalk)]
##            triangles.append((0,croot,a,mab))
##            triangles.append((0,croot,mab,b))
    for index, vert in enumerate(prevface):
        nindex = None
        nvert = None
        if index == len(prevface)-1:
            nindex = 0
        else:
            nindex = index+1
        nvert = prevface[nindex]
        vcoord = pvertices[vert]
        nvcoord = pvertices[nvert]
        xv,yv,zv = vcoord
        xnv,ynv,znv = nvcoord
        a = complex(xv,yv)
        b = complex(xnv,ynv)
##        mab = midpoint((a,b))
        
        triangles.append((0,croot,a,b))
##        triangles.append((0,croot,mab,b))
    ##triangles = []
##    for i in range(int(POLY)):
##    ##    if i % 2 == 0:
##        B = cmath.rect(cradius, (2*i - 1) * math.pi / POLY)
##        C = cmath.rect(cradius, (2*i + 1) * math.pi / POLY)
    ##    else:
    ##        B = cmath.rect(0.6180339887498948, (2*i - 1) * math.pi / 10)
    ##        C = cmath.rect(1, (2*i + 1) * math.pi / 10)
##        if i % 2 == 0:
##            B, C = C, B  # Make sure to mirror every second triangle
##        B += croot
##        C += croot
##        triangles.append((0, croot, B, C))
    cv, cf, sv = penrosesubdivde(triangles, subdivide = False)
    nextinc = len(pvertices)
    nextincf = len(pfaces)
    ## reindex vertices and selectionvertices (misnomer faces actually)
    for indf, f in enumerate(cf):
        lf = list(f)
        for indv, v in enumerate(lf):
            lf[indv] += nextinc
        cf[indf] = tuple(lf)
    for indf, f in enumerate(sv):
        sv[indf] += nextincf
    ## concatenate vertices and everything else
    for i, v in enumerate(cv):
        vl = list(v)
        vl[2] = z
        cv[i] = vl
    pvertices += cv
    pfaces += cf
    pselections += sv
        
meshName = "PenroseGraph"
obName = "PenroseGraphObj"
me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)
ob.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(ob)
me.from_pydata(pvertices,[],pfaces)      
me.update(calc_edges=True)


scn = bpy.context.scene
scn.objects.active = ob
ob.select = True
obj = bpy.context.active_object

bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.object.mode_set(mode = 'OBJECT')

cvertices = obj.data.vertices
cfaces = obj.data.polygons        

for sel in pselections:
    cfaces[sel].select = True

bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.object.vertex_group_add()
bpy.ops.object.vertex_group_assign()
bpy.ops.mesh.dissolve_edges()
