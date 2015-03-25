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
facetoverts = {}
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
      if face.index in facetoverts:
         facetoverts[face.index].append(vert)
      else:
         facetoverts[face.index] = [vert]
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
print(facetoverts)
facetofacesk = list(facetofaces.keys())
facetofacesk.reverse()
## find end point face on a row
minv = len(facetofaces[facetofacesk[0]])
maxv = 0
i = 0
for face in facetofacesk:
   if len(facetofaces[face])<minv:
      a = facetofacesk[0]
      facetofacesk[0] = face
      facetofacesk[i] = a
      minv = len(facetofaces[face])
   if len(facetofaces[face])>maxv:
      maxv = len(facetofaces[face])
   i += 1

def findadjface(face, facetofaces, exclusion):
   nfs = []
   nfssingle = []
   nfs.append(face)
   for nf in facetofaces[face]:
      if not nf in exclusion:
         nfs.append(nf)
   nnfs = []
   nnffind = None
   ##intesect nnf find
   nnffindc = False
   for nf in nfs:
      for nnf in facetofaces[nf]:
         ##print("nnf: ", nnf)
         if nnf in nnfs:
            nnffind = nnf
            nnffindc = True
            break            
         else:
            if (not nnf in nfs) and (not nnf in exclusion):
               nnfs.append(nnf)
      if nnffindc:
         break
   ##print("nnfs: ",nnfs)
   nfs.append(nnffind)
   return (nfs,nnffind)

def getneighborpick(face, facetofaces, exclusion):
   for nface in facetofaces[face]:
      if not nface in exclusion:
         return nface
   return None

def chooseoppositepick(faces, facetofaces, exclusion, facetoverts):
   ##assumes faces is of size 2 for input
   countdict = {}
   nonadjdict = {}
   pick = None
   for face in faces:
      count = 0
##      countpos = 0
##      countposdict = {}
      nonadj = True
      sharedverts = []
      for nface in facetofaces[face]:
         if not nface in exclusion:
           count += 1
           for vert in facetoverts[nface]:
              if not vert in sharedverts:
                 sharedverts.append(vert)
              else:
                 nonadj = False
##            countposdict[nface] = countpos  ##checking adjacency
##         countpos += 1
##      if not len(countposdict)==0:
##         prevkey = countposdict[list(countposdict.keys())[0]]
##         for key in list(countposdict.keys()):
##            if abs(prevkey - countposdict[key])>1:
##               nonadj = True
##            prevkey = countposdict[key]
##      if nonadj:
##         nonadjdict[face] = True
##      else:
##         nonadjdict[face] = False
            
      countdict[face] = count
      nonadjdict[face] = nonadj
   if countdict[faces[0]] < countdict[faces[1]]:
      pick = faces[0]
   elif countdict[faces[0]] > countdict[faces[1]]:
      pick = faces[1]
   elif countdict[faces[0]] == countdict[faces[1]]:
      if nonadjdict[faces[0]]:
         pick = faces[1]
      else:
         pick = faces[0]
   return pick

processselect2 = []
orderedfacelist=[]
ccheck = False

##if minv == 1:
   
if minv == 2:

   ccheck = True
for face in facetofacesk:
   ##orderedfacelist = [facetofacesk[0]]

   if ((not face in orderedfacelist)):
      ##orderedfacelist.append(face)
      if ccheck:
         ##
         firstcolumn = True
         nrpick = None
         pick = face
         ##print("pick at while loop start: ", pick)
         i = 0
         while ((pick not in orderedfacelist) and i <100):
            ##orderedfacelist.append(pick)

            picks,cornerf = findadjface(pick, facetofaces, orderedfacelist)
            for pick in picks:
               orderedfacelist.append(pick)
            processselect2.append(picks)
            ##print("orderedfacelist: ",orderedfacelist)
            ##print("picks: ",picks)
            contingents = [picks[1],picks[2]]
            pick = chooseoppositepick(contingents, facetofaces,
                                      orderedfacelist, facetoverts)
            ##print("pick: ", pick)
            if firstcolumn:
               for tpick in contingents:
                  if tpick != pick:
                     nrpick = tpick
                     nrpick = getneighborpick(nrpick,
                                              facetofaces, orderedfacelist)
                     firstcolumn = False
                     ##print("nrpick: ", nrpick)
                     break
            pick = getneighborpick(pick, facetofaces, orderedfacelist)
            
            ##print("pick: ", pick)
            if pick == None:
               pick = nrpick
               firstcolumn = True
            if pick == None:
               pick = picks[0]
            ##print("final pick: ", pick)
            i+=1       
      else:
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
print("minv: ", minv)
print("Process select: ", processselect2)
##process
if minv == 1:
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
elif minv == 2:
   for faceg in processselect2:
      processselect = faceg
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
