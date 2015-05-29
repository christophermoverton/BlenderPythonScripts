import bpy
import math
##import RandomComplex4
CirclePoints = 12
#Construct Circle points

thetainc = 2*math.pi/float(CirclePoints)
cpositions = []
theta = 0.0
faces = []
for i in range(CirclePoints):
    pos = (math.cos(theta),math.sin(theta))
    cpositions.append(pos)
    theta += thetainc
##    if i == CirclePoints-1:
##        face = (i,0,CirclePoints)
##        faces.append(face)
##    else:
##        face = (i,i+1,CirclePoints)
##        faces.append(face)

## expects already named object cpack
## that is a circle packing dictionary object
cpvertices = []
cpfaces = []
i = 0
for c in cpack:
    center, radius = cpack[c]
    cx = center.real
    cy = center.imag
    MaxScaleIterations = random.randint(2,10)
    PolygonSize = random.randint(4,20)
    verts,faces = generatePolygon((cx,cy),radius, MaxScaleIterations,
                                  PolygonSize)
    vertsind = len(cpvertices)
    nfaces = []
    for face in faces:
        face = list(face)
        for index, vert in enumerate(face):
            face[index] += vertsind
        nfaces.append(tuple(face))
    cpvertices += verts
    cpfaces += nfaces
##    circiter = (CirclePoints+1)*i
##    centerposi = (CirclePoints+1)*(i+1)-1
##    j = 0
##    for pos in cpositions:
##        cpvertices.append((pos[0]*radius+cx,pos[1]*radius+cy, 0.0))
##        if j == CirclePoints-1:
##            
##            face = (circiter+j,circiter,centerposi)
##            cpfaces.append(face)
##        else:
##            face = (circiter+j,circiter+j+1,centerposi)
##            cpfaces.append(face)
##        j += 1
##    cpvertices.append((cx,cy,0.0))
    i += 1
        
meshName = "CirclePacking"
obName = "CirclePackingObj"
me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)
ob.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(ob)
me.from_pydata(cpvertices,[],cpfaces)      
me.update(calc_edges=True) 
