import math
import cmath
##import cairo
import bpy

#------ Configuration --------
IMAGE_SIZE = (1000, 1000)
NUM_SUBDIVISIONS = 8
POLY = 12
MGOLDENRATIO = True
#-----------------------------


goldenRatio = (1 + math.sqrt(5)) / 2

def subdivide(triangles):
    result = []
    for color, A, B, C in triangles:
        if color == 0:
            # Subdivide red triangle
            P = A + (B - A) / goldenRatio
            result += [(0, C, P, B), (1, P, C, A)]
        else:
            # Subdivide blue triangle
            Q = B + (A - B) / goldenRatio
            R = B + (C - B) / goldenRatio
            result += [(1, R, C, A), (1, Q, R, B), (0, R, Q, A)]
    return result

def measurePhi():
    B = cmath.rect(1,math.pi/2.0)
    C = cmath.rect(1,math.pi/2.0-2.0*math.pi/(POLY/2.0))
    BC = C-B
    sidelen = abs(BC)
    chord = BC.real
    chord *= 2.0
    return chord/sidelen

if MGOLDENRATIO:
    goldenRatio = measurePhi()
    

# Create wheel of red triangles around the origin
triangles = []
for i in range(POLY):
##    if i % 2 == 0:
    B = cmath.rect(1, (2*i - 1) * math.pi / POLY)
    C = cmath.rect(1, (2*i + 1) * math.pi / POLY)
##    else:
##        B = cmath.rect(0.6180339887498948, (2*i - 1) * math.pi / 10)
##        C = cmath.rect(1, (2*i + 1) * math.pi / 10)
    if i % 2 == 0:
        B, C = C, B  # Make sure to mirror every second triangle
    triangles.append((0, 0j, B, C))

# Perform subdivisions
for i in range(NUM_SUBDIVISIONS):
    triangles = subdivide(triangles)

# Prepare cairo surface
##surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMAGE_SIZE[0], IMAGE_SIZE[1])
##cr = cairo.Context(surface)
##cr.translate(IMAGE_SIZE[0] / 2.0, IMAGE_SIZE[1] / 2.0)
##wheelRadius = 1.2 * math.sqrt((IMAGE_SIZE[0] / 2.0) ** 2 + (IMAGE_SIZE[1] / 2.0) ** 2)
##cr.scale(wheelRadius, wheelRadius)
##
### Draw red triangles
##for color, A, B, C in triangles:
##    if color == 0:
##        cr.move_to(A.real, A.imag)
##        cr.line_to(B.real, B.imag)
##        cr.line_to(C.real, C.imag)
##        cr.close_path()
##cr.set_source_rgb(1.0, 0.35, 0.35)
##cr.fill()    
##
### Draw blue triangles
##for color, A, B, C in triangles:
##    if color == 1:
##        cr.move_to(A.real, A.imag)
##        cr.line_to(B.real, B.imag)
##        cr.line_to(C.real, C.imag)
##        cr.close_path()
##cr.set_source_rgb(0.35, 0.35, 1.0)
##cr.fill()
##
### Determine line width from size of first triangle
##color, A, B, C = triangles[0]
##cr.set_line_width(abs(B - A) / 10.0)
##cr.set_line_join(cairo.LINE_JOIN_ROUND)
##
### Draw outlines
##for color, A, B, C in triangles:
##    cr.move_to(C.real, C.imag)
##    cr.line_to(A.real, A.imag)
##    cr.line_to(B.real, B.imag)
##cr.set_source_rgb(0.2, 0.2, 0.2)
##cr.stroke()
##
### Save to PNG
##surface.write_to_png('penrose.png')

vertices = []
faces = []
vertindex = {}
vertsface = {}
## vertsface keyed by triangle double complex pair
## values are tuple paired by face index and color assignment

def connectivity(triangle, vertsface):
    ## check for connectivity
    color,A,B,C = triangle
    if (A,B) in vertsface:
        for V in vertsface[(A,B)]:
            if V != C:
                if color == vertsface[(A,B)][V][1]:
                    return (True, (A,B), C)
    if (B,A) in vertsface:
        for V in vertsface[(B,A)]:
            if V != C:
                if color == vertsface[(B,A)][V][1]:
                    return (True, (B,A), C)
    if (A,C) in vertsface:
        for V in vertsface[(A,C)]:
            if V != B:
                if color == vertsface[(A,C)][V][1]:
                    return (True, (A,C), B)
    if (C,A) in vertsface:
        for V in vertsface[(C,A)]:
            if V != B:
                if color == vertsface[(C,A)][V][1]:
                    return (True, (C,A), B)
    if (B,C) in vertsface:
        for V in vertsface[(B,C)]:
            if V != A:
                if color == vertsface[(B,C)][V][1]:
                    return (True, (B,C), A)
    if (C,B) in vertsface:
        for V in vertsface[(C,B)]:
            if V != A:
                if color == vertsface[(C,B)][V][1]:
                    return (True, (C,B), A)
    return (False, (None,None), None)

def updatevertsface(triangle, vertsface, faceindex):
    color, A,B,C = triangle
    if not (A,B) in vertsface:
        vertsface[(A,B)] = {C:(faceindex,color)}
    else:
        if not C in vertsface[(A,B)]:
            vertsface[(A,B)][C] = (faceindex,color)        
    if not (A,C) in vertsface:
        vertsface[(A,C)] = {B:(faceindex,color)}
    else:
        if not B in vertsface[(A,C)]:
            vertsface[(A,C)][B] = (faceindex,color)        
    if not (B,C) in vertsface:
        vertsface[(B,C)] = {A:(faceindex,color)}
    else:
        if not A in vertsface[(B,C)]:
            vertsface[(B,C)][A] = (faceindex,color)

for color, A, B, C in triangles:
    Ax = A.real
    Ay = A.imag
    Av = (Ax,Ay,0.0)
    Bx = B.real
    By = B.imag
    Bv = (Bx,By,0.0)
    Cx = C.real
    Cy = C.imag
    Cv = (Cx,Cy,0.0)
    face = []
##    if check:
##        faceind, fc = vertsface[pair]
##        face = list(faces[faceind])
##        A,B = pair
##        C = add
##        Ax = A.real
##        Ay = A.imag
##        Av = (Ax,Ay,0.0)
##        Bx = B.real
##        By = B.imag
##        Bv = (Bx,By,0.0)
##        Cx = C.real
##        Cy = C.imag
##        Cv = (Cx,Cy,0.0)
##        Cind = None
##        if Cv in vertindex:
##            Cind = vertindex[Cv]
##        else:
##            vertices.append(Cv)
##            Cind = len(vertices)-1
##            vertindex[Cv] = Cind
##        if Bv in vertindex:
##            Bind = vertindex[Bv]
##            Binsertind = face.index(Bind)
##            face.insert(Binsertind, Cind)
##        faces[faceind] = face
##        updatevertsface((color,A,B,C), vertsface, faceind)
##    else:    
    if Av in vertindex:
        face.append(vertindex[Av])
    else:
        vertices.append(Av)
        Aind = len(vertices)-1
        face.append(Aind)
        vertindex[Av] = Aind
    if Bv in vertindex:
        face.append(vertindex[Bv])
    else:
        vertices.append(Bv)
        Bind = len(vertices)-1
        face.append(Bind)
        vertindex[Bv] = Bind
    if Cv in vertindex:
        face.append(vertindex[Cv])
    else:
        vertices.append(Cv)
        Cind = len(vertices)-1
        face.append(Cind)
        vertindex[Cv] = Cind
    faces.append(tuple(face))
    faceind = len(faces)-1
    updatevertsface((color,A,B,C), vertsface, faceind)

##for color, A, B, C in triangles:
##    check, pair, add = connectivity((color,A,B,C), vertsface)
##    if check:
##        faceind, fc = vertsface[pair]
##        face = list(faces[faceind])
##        A,B = pair
##        C = add
##        Ax = A.real
##        Ay = A.imag
##        Av = (Ax,Ay,0.0)
##        Bx = B.real
##        By = B.imag
##        Bv = (Bx,By,0.0)
##        Cx = C.real
##        Cy = C.imag
##        Cv = (Cx,Cy,0.0)
##        Cind = None
##        if Cv in vertindex:
##            Cind = vertindex[Cv]
##        else:
##            vertices.append(Cv)
##            Cind = len(vertices)-1
##            vertindex[Cv] = Cind
##        if Bv in vertindex:
##            Bind = vertindex[Bv]
##            Binsertind = face.index(Bind)
##            face.insert(Binsertind, Cind)
##        faces[faceind] = face

meshName = "PenroseGraph"
obName = "PenroseGraphObj"
me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)
ob.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(ob)
me.from_pydata(vertices,[],faces)      
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

for vertpair in vertsface:
    if len(vertsface[vertpair]) > 1:
        colorbreak = False
        for value in vertsface[vertpair]:
            s,color = vertsface[vertpair][value]
            if color == 0:
                colorbreak = True
                cfaces[s].select = True
##        if colorbreak:
##            continue
##        A,B = vertpair
##        Ax = A.real
##        Ay = A.imag
##        Av = (Ax,Ay,0.0)
##        Bx = B.real
##        By = B.imag
##        Bv = (Bx,By,0.0)
##        Aind = vertindex[Av]
##        Bind = vertindex[Bv]
##        cvertices[Aind].select = True
##        cvertices[Bind].select = True
##        bpy.ops.object.mode_set(mode = 'EDIT')
##        bpy.ops.mesh.dissolve_edges()
##        bpy.ops.mesh.select_all(action = 'DESELECT')
##        bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.dissolve_edges()
