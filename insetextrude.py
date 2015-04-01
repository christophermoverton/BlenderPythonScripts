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
dimx = 3  ## can change >= 2
dimy = 3 ## can change >= 2 
TFACES = 0   #do not modify
COLSIZE = None  #do not modify
ZCOUNT = 0  ## do not modify this
##get selected faces
i = 0
facetoindex = {}
for face in faces:
   if face.select:
      selectedfaces.append(face)
      facetoindex[i] = face
   i += 1
TFACES = i
print("TFaces: ", TFACES)
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
   if len(nfs) < 3:
      nfs.append(None)
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
   pick2 = None
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

            
      countdict[face] = count
      nonadjdict[face] = nonadj
   c1 = False
   c2 = False
   if COLSIZE == None:
      c1 = countdict[faces[0]] == 0 and ZCOUNT > 1
      c2 = countdict[faces[1]] == 0 and ZCOUNT > 1
   else:
      c1 = countdict[faces[0]] == 0 and ZCOUNT > int((TFACES/COLSIZE)/2-2)
      c2 = countdict[faces[1]] == 0 and ZCOUNT > int((TFACES/COLSIZE)/2-2)      
   if countdict[faces[0]] < countdict[faces[1]]: ##and c1:
      pick = faces[0]
##   elif countdict[faces[0]] < countdict[faces[1]] and not c1:
##      pick = faces[1]
   elif countdict[faces[0]] > countdict[faces[1]]: ## and c2:
      pick = faces[1]
##   elif countdict[faces[0]] > countdict[faces[1]] and not c2:
##      pick = faces[0]
   elif countdict[faces[0]] == countdict[faces[1]]:
      if nonadjdict[faces[0]]:
         pick = faces[1]
      else:
         pick = faces[0]
   if countdict[faces[0]] < countdict[faces[1]] and c1:
      pick2 = faces[1]
   elif countdict[faces[0]] < countdict[faces[1]] and not c1:
      pick2 = faces[0]
   elif countdict[faces[0]] > countdict[faces[1]] and c2:
      pick2 = faces[0]
   elif countdict[faces[0]] > countdict[faces[1]] and not c2:
      pick2 = faces[1]
   else:
      pick2 = pick
   c1 = countdict[faces[0]] == 0
   c2 = countdict[faces[1]] == 0
   if c1 or c2:
      global ZCOUNT
      
      ZCOUNT += 1
   return pick, pick2

processselect2 = []
orderedfacelist=[]
directionlist = []
ccheck = False

##if minv == 1:
   
if minv == 2:

   ccheck = True
columnsize = None
rowsize = None
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
         j = 0 
         
         while ((pick not in orderedfacelist) and i <100):
            ##orderedfacelist.append(pick)

            picks,cornerf = findadjface(pick, facetofaces, orderedfacelist)
            revisedpicks = []
            for pick in picks:
               if not pick == None:
                  orderedfacelist.append(pick)
                  revisedpicks.append(pick)
            processselect2.append(revisedpicks)
            ##print("orderedfacelist: ",orderedfacelist)
            ##print("picks: ",picks)
            contingents = [picks[1],picks[2]]
            if not None in contingents:
               pick, pick2 = chooseoppositepick(contingents, facetofaces,
                                               orderedfacelist, facetoverts)
               if pick2 != None:
                  
                  directionlist.append(pick2)
            else:
               pick = None
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
            if not pick == None:
               pick = getneighborpick(pick, facetofaces, orderedfacelist)
            
            ##print("pick: ", pick)
            if pick == None:
               pick = nrpick
               firstcolumn = True
               if columnsize == None:
                  columnsize = i+1
                  COLSIZE = columnsize*2
               j += 1
            if pick == None:
               pick = picks[0]
            ##print("final pick: ", pick)
            i+=1
         rowsize = j-2
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
rowsize = int((TFACES/COLSIZE)/2)
processselect3 = []
totalcolumns = 2*columnsize
totalrows = 2*rowsize
rcolumnsize = int(totalcolumns/dimx)
if totalcolumns/dimx - rcolumnsize > 0:
   rcolumnsize += 1
rrowsize = int(totalrows/dimy)
if totalrows/dimy - rrowsize > 0:
   rrowsize += 1
print("Process select2: ", processselect2)
print("Column size: ", columnsize)
print("Row size: ", rowsize)
print("RRow Size: ", rrowsize)
print("RColumn Size: ", rcolumnsize)
print("direction list: ", directionlist)
if dimx > 2 or dimy > 2:
   partialx = False
   partialy = False
   rangex = int(dimx/2)
   rangey = int(dimy/2)
   if dimx%2 != 0:
      partialx = True
      rangex = int(dimx/2)+1
   if dimy%2 != 0:
      partialy = True
      rangey = int(dimy/2)+1
   for i in range(0,rrowsize):
      top = False
      if partialy:
         if i%2 == 0:
            top = True
         else:
            top = False
      for j in range(0,rcolumnsize):
         picks = []
         front = False
         if partialx:
            if j%2 == 0:
               front = True
            else:
               front = False
         cr = i%2 == 0
         cc = j%2 == 0         
         for k in range(0,rangex):
            for l in range(0,rangey):
               ##check row and column

               t1 = False
               t2 = False
               if cr and cc:
                  t1 = k==int(dimx/2)
                  t2 = l==int(dimy/2)
               elif cr and not cc:
                  t1 = k==0
                  t2 = l==int(dimy/2)
               elif not cr and cc:
                  t1 = k==int(dimx/2)
                  t2 = l==0
               elif not cr and not cc:
                  t1 = k==0
                  t2 = l==0
                  
               coordx = k + int((dimx*j)/2)
               coordy = l + int((dimy*i)/2)
               coord = coordx + coordy*columnsize
               ipicks = []
               print("coord: ", coord)
               if coordx*2 >= totalcolumns:
                  continue
               if coord <= len(processselect2)-1:
                  ipicks = processselect2[coord]
               else:
                  continue
               if t1 and not t2:
                  if len(ipicks) == 4:
                     if partialx:
                        if front:
                           if ipicks[1] in directionlist:
                              picks.append(ipicks[0])
                              picks.append(ipicks[2])
                           else:
                              picks.append(ipicks[0])
                              picks.append(ipicks[1])
                        else:
                           if ipicks[1] in directionlist:
                              picks.append(ipicks[3])
                              picks.append(ipicks[1])
                           else:
                              picks.append(ipicks[3])
                              picks.append(ipicks[2])
                     else:
                        for ipick in ipicks:
                           picks.append(ipick)
                  else:
                     if partialx:
                        if front:
                           picks.append(ipicks[0])
                        else:
                           picks.append(ipicks[1])
                     else:
                        for ipick in ipicks:
                           picks.append(ipick)                     
               elif not t1 and not t2:
                  for ipick in ipicks:
                     picks.append(ipick)
               elif not t1 and t2:
                  if len(ipicks) == 4:
                     if partialy:
                        if not top:
                           if ipicks[1] in directionlist:
                              picks.append(ipicks[3])
                              picks.append(ipicks[2])
                           else:
                              picks.append(ipicks[3])
                              picks.append(ipicks[1])
                        else:
                           if ipicks[1] in directionlist:
                              picks.append(ipicks[0])
                              picks.append(ipicks[1])
                           else:
                              picks.append(ipicks[0])
                              picks.append(ipicks[2])
                     else:
                        for ipick in ipicks:
                           picks.append(ipick)
                  else:
                     if partialy:
                        if not top:
                           picks.append(ipicks[1])
                        else:
                           picks.append(ipicks[0])
                     else:
                        for ipick in ipicks:
                           picks.append(ipick)
               elif t1 and t2:
                  if partialx and partialy:
                     if top and front:
                        picks.append(ipicks[0])
                     elif not top and front:
                        if ipicks[1] in directionlist:
                           picks.append(ipicks[2])
                        else:
                           picks.append(ipicks[1])
                     elif top and not front:
                        if ipicks[1] in directionlist:
                           picks.append(ipicks[1])
                        else:
                           picks.append(ipicks[2])
                     elif not top and not front:
                        picks.append(ipicks[3])
                  else:
                     for ipick in ipicks:
                        picks.append(ipick)
         processselect3.append(picks)
else:
   processselect3 = processselect2
         
processselect2 = processselect3                          
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
