import bpy
##this continguous strips of selected faces should be unidirectional
## and be non contiguous in the orthogonal direction in single face sequences along the user specified direction
##a modification of the code could be applied for processing squares of selected faces possibly.
##a non cooridnate checking squares completion method for instance might use a neighbor intersection
##test relative to two cosequently chosen faces, but we have to ensure that we are picking 
##the right desired square for user desired tiling.  Would likely need to include a coordinate 
##sequencing method where iterating through the data set by neighbor vertex.
##alternately perhaps applying creating an integer key sequence map between selected faces, 
##presuming that all faces are ordered in obj.data.polygons set
# retrieve the active object
bpy.ops.object.mode_set(mode = 'OBJECT')
obj = bpy.context.active_object
faces = obj.data.polygons
selectedfaces = []
vertstofaces = {}
facetofaces = {}
operatefaces = 2
##get selected faces
i = 0
facetoindex = {}
for face in faces:
   if face.select:
      selectedfaces.append(face)
      facetoindex[i] = face
   i += 1
##get facetofaces (neighboring faces for each selected face)
for face in selectedfaces:
   verts = face.vertices
   vfacesmatch = []
   vfacesmatchcheck = False
   for vert in verts:
      if vert in vertstofaces:
         for vface in vertstofaces[vert]:
            if vface in vfacesmatch:
                vfacesmatchcheck = True
                if face in facetofaces:
                   facetofaces[face.index].append(vface)
                else:
                   facetofaces[face.index] = [vface]
                if vface in facetofaces:
                    facetofaces[vface].append(face.index)
                else:
                    facetofaces[vface] = [face.index]
            else:  
               vfacesmatch.append(vface)
         vertstofaces[vert].append(face.index)
      else:
         vertstofaces[vert] = [face.index]
##finish bimap completions
for face in facetofaces:
   for nface in facetofaces[face]:
      checkr = False
      for nrface in facetofaces[nface]:
         if nrface == face:
            checkr = True
      if not checkr:
         facetofaces[nface].append(face)
## process selected faces
finishedprocessing = []
print(facetofaces)
print(selectedfaces)
print(vertstofaces)
facetofacesk = list(facetofaces.keys())
facetofacesk.reverse()
## find end point face on a row
i = 0
for face in facetofacesk:
   if len(facetofaces[face])==1:
      a = facetofacesk[0]
      facetofacesk[0] = face
      facetofacesk[i] = a
      break
   i += 1
for face in facetofacesk:
   ##orderedfacelist = [facetofacesk[0]]
   if ((not face in orderedfacelist) and len(facetofaces[face])==1):
      orderedfacelist.append(face)
      pick = facetofaces[face][0]
      i = 0
      while ((pick not in orderedfacelist) and i <100):
         orderedfacelist.append(pick)
         for face in facetofaces[pick]:
            if face in orderedfacelist:
               continue
            else:
               pick = face
         i+=1
print(orderedfacelist)
##process
for face in orderedfacelist:
   processselect = []
   i = 1
   print(finishedprocessing)
   if face in finishedprocessing:
      continue
   nextface = face
   processselect.append(nextface)
   while i < operatefaces:
      for neighbor in facetofaces[nextface]:
         if ((neighbor in finishedprocessing) or (neighbor in processselect)):
            continue
         else:
            processselect.append(neighbor)
            nextface = neighbor
      i += 1
   bpy.ops.object.mode_set(mode = 'EDIT')
   bpy.ops.mesh.select_all(action = 'DESELECT')
   # reselect the originally selected face
   bpy.ops.object.mode_set(mode = 'OBJECT')
   print(processselect)
   for face in processselect:
      obj.data.polygons[face].select = True
   bpy.ops.object.mode_set(mode = 'EDIT')
   bpy.ops.mesh.inset(use_boundary=True, use_even_offset=True, use_relative_offset=False,
                      use_edge_rail=False, thickness=0.1, depth=0.0, use_outset=False,
                      use_select_inset=False, use_individual=False, use_interpolate=True)

   obj.data.update()
   for face in processselect:
       finishedprocessing.append(face)
       
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_all(action = 'DESELECT')
   # reselect the originally selected face
bpy.ops.object.mode_set(mode = 'OBJECT')
for face in orderedfacelist:
   obj.data.polygons[face].select = True

bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.extrude_faces_move(
    MESH_OT_extrude_faces_indiv={"mirror":True}, 
    TRANSFORM_OT_shrink_fatten={"value":-.01,
    "mirror":False,
    "proportional":'DISABLED',
    "proportional_edit_falloff":'SMOOTH',
    "proportional_size":1,
    "snap":False,
    "snap_target":'CLOSEST',
    "snap_point":(0, 0, 0),
    "snap_align":False,
    "snap_normal":(0, 0, 0),
    "release_confirm":False})
obj.data.update()
