import bpy, bmesh
import random

##bpy.ops.mesh.inset(use_boundary=True, use_even_offset=True,
##                   use_relative_offset=False,
##                   use_edge_rail=False, thickness=0.001, depth=0.0,
##                   use_outset=False,
##                   use_select_inset=False, use_individual=False,
##                   use_interpolate=True)
global Height,Scale,ScaleOn
Height = .1
Scale = .95
ScaleOn = True

def Centroid(walk):
    ## Compute A  for a non self intersecting closed polygon
    A = 0
    i = 0
    for i,vert in enumerate(walk):
        x,y = vert
        if i == len(walk)-1:
            xp1,yp1 = walk[0]
        else:
            xp1,yp1 = walk[i+1]
        A += x*yp1-xp1*y
    A*=.5
    Cx = 0
    Cy = 0
    for i,vert in enumerate(walk):
        x,y = vert
        if i == len(walk)-1:
            xp1,yp1 = walk[0]
        else:
            xp1,yp1 = walk[i+1]
        Cx += (x+xp1)*(x*yp1-xp1*y)
        Cy += (y+yp1)*(x*yp1-xp1*y)
    Cx *= 1/(6*A)
    Cy *= 1/(6*A)
    return Cx,Cy

def batchrextrude(height = Height, scale = Scale, scaleon = ScaleOn,
                  setFV = False):
##    if height != None:
##        Height = height
##    if scale != None:
##        Scale = scale
##    if scaleon != None:
##        ScaleOn = scaleon
    Height = height
    Scale = scale
    ScaleOn = scaleon

    bpy.ops.object.mode_set(mode = 'EDIT')
    obj = bpy.context.active_object
    faces = obj.data.polygons
    vertices = obj.data.vertices
    t_bm = bmesh.from_edit_mesh(obj.data)
    verts = list(t_bm.verts)        
    selectedfaces = []
    setverts = []
    setfaces = []
    if setFV:
        for v in verts:
            x,y,z = v.co
            setverts += [[x,y,z]]
    for face in faces:
       if face.select:
          selectedfaces.append(face)
    print('length of selected faces: ', len(selectedfaces))
    
    for fin, face in enumerate(selectedfaces):
        skip = random.random()
        prevwalk = face.vertices
        print('vertices: ', list(prevwalk))
        if skip < .15:
            if setFV:
                nwalk = []
                nwalkv = [] ## used for setFV bmesh to internal indexing method
                nwalkverts = []
                for index, vert in enumerate(prevwalk):
                    x,y,z = verts[vert].co
                    nwalkverts.append([x,y,z])
                setfaces += [list(prevwalk)]
##                setverts += nwalkverts
            continue
        rescales = random.randint(1,5)
        terrace = random.random()
        newprevwalk = []
        for vert in prevwalk:
            newprevwalk.append(verts[vert])
        prevwalk = newprevwalk
        terraceb = None
        if terrace > .35:
            terraceb = True
            rescales *= 2
        else:
            terraceb = False
        cwalk = []
        for index, vert in enumerate(face.vertices):
            x1,y1,z1 = vertices[vert].co
            cwalk.append([x1,y1])
        cx,cy = Centroid(cwalk)
        height = 0
        if not ScaleOn:
            height += random.random()*Height
            nwalk = []
            nwalkv = [] ## used for setFV bmesh to internal indexing method
            nwalkverts = []
            for index, vert in enumerate(prevwalk):
                x,y,z = vert.co
                z += height
                t_v1 = t_bm.verts.new((x,y,z))
                nwalk.append(t_v1)
                nwalkv.append(len(t_bm.verts)-1)
                nwalkverts.append([x,y,z])
            for index, vert in enumerate(prevwalk):
                nindex = None
                if index == len(prevwalk)-1:
                    nindex = 0
                else:
                    nindex = index+1
                vert2 = prevwalk[nindex]
                v1, v2 = None,None
                if type(vert) == int:
                    v1 = verts[vert]
                    v2 = verts[vert2]
                else:
                    v1 = vert
                    v2 = vert2
                vert3 = nwalk[nindex]
                vert4 = nwalk[index]
    ##            faces.add(1)
    ##            faces[-1].vertices_raw = [vert,vert2,vert3,vert4]
                t_face = t_bm.faces.new([v1,v2,vert3,vert4])
            prevwalk = nwalk[0:len(nwalk)]
            nface = []
            for vert in prevwalk:
                nface.append(vert)
            t_face = t_bm.faces.new(nface)
            setfaces += [nwalkv]
            setverts += nwalkverts
                
            obj.data.update(calc_edges=True)      
            continue
        
        for i in range(rescales):
            Scale = random.uniform(.5,.95)
            faceind = len(faces)
            vertind = len(vertices)
            if terraceb:
                if i%2!=0:
                    height += random.random()*Height
            else:
                height += random.random()*Height
            ## add new scaled vertices
            nwalk = []
            for index, vert in enumerate(prevwalk):
                x,y,z = vert.co
                ## translate coordinates
                xtr = x - cx
                ytr = y - cy
                xs = None
                ys = None
                if terraceb:
                    if i % 2 == 0:
                        xs = xtr*Scale
                        ys = ytr*Scale
                    else:
                        xs = xtr
                        ys = ytr
                else:
                    xs = xtr*Scale
                    ys = ytr*Scale
                xs += cx
                ys += cy
                z += height
                # add 1 verts  
    ##            vertices.add(1)
    ##            vertices[-1].co = (xs,ys,z)
                t_v1 = t_bm.verts.new((xs,ys,z))
                nwalk.append(t_v1)
            
            for index, vert in enumerate(prevwalk):
                nindex = None
                if index == len(prevwalk)-1:
                    nindex = 0
                else:
                    nindex = index+1
                vert2 = prevwalk[nindex]
                v1, v2 = None,None
                if type(vert) == int:
                    v1 = verts[vert]
                    v2 = verts[vert2]
                else:
                    v1 = vert
                    v2 = vert2
                vert3 = nwalk[nindex]
                vert4 = nwalk[index]
    ##            faces.add(1)
    ##            faces[-1].vertices_raw = [vert,vert2,vert3,vert4]
                t_face = t_bm.faces.new([v1,v2,vert3,vert4])
            prevwalk = nwalk[0:len(nwalk)]
        nface = []
        for vert in prevwalk:
            nface.append(vert)
        t_face = t_bm.faces.new(nface)

    obj.data.update(calc_edges=True)
    bpy.ops.object.mode_set(mode = 'OBJECT')
    if setFV:
        return (setfaces,setverts)
