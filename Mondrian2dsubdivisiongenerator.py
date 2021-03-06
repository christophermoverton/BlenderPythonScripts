#Mondrian like subdivision generator
##import bpy
import random
global dimx
global dimy
dimx = 1000
dimy = 1300
totalnodes = 10
meshName = "Mondrian"
obName = "MondrianObj"
me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)
ob.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(ob)
##track edges on mondrian generator and vertices
nodes = {}
nodepostoi = {}
randomxlist = []
randomylist = []
def getrand(minv, maxv, randlist):
   val = random.randint(minv,maxv)
   if val not in randlist:
      return val
   else:
      return getrand(minv,maxv,randlist)
   
for i in range(0,totalnodes):
   attr = {}
   randposx = getrand(1,dimx-1,randomxlist)
   randposy = getrand(1,dimy-1,randomylist)
##   randposx = random.randint(0,dimx)
##   randposy = random.randint(0,dimy)
   attr['position'] = (randposx,randposy)
   attr['left'] = None
   attr['right'] = None
   attr['up'] = None
   attr['down'] = None
   attr['crossing'] = None
   randomxlist.append(randposx)
   randomylist.append(randposy)
   nodes[i+1] = attr
   nodepostoi[(randposx,randposy)] = i+1
nodeposlist = list(nodepostoi.keys())   
#node ordering
nodexrank = nodeposlist[0:len(nodeposlist)]
nodeyrank = nodeposlist[0:len(nodeposlist)]
nodexrank.sort(key=lambda tup: tup[0])
nodeyrank.sort(key=lambda tup: tup[1])
#nodes keyed by ypos
ypnodes = {}
for node in nodes:
   ypnodes[nodes[node]['position'][1]] = node

#nodes keyed by xpos
xpnodes = {}
for node in nodes:
   xpnodes[nodes[node]['position'][0]] = node
#finished keying nodes by x and y pos
nodexirank = []
for pos in nodexrank:
    nodexirank.append(nodepostoi[pos])
nodeyirank = []
for pos in nodeyrank:
    nodeyirank.append(nodepostoi[pos])
##set node crossings
crossingnodes = {}
crossingnodesrev = {}
factor = 10
if len(nodeyirank) > 9:
   factor = 100
elif len(nodeyirank) > 99:
   factor = 1000

for node in nodes:
    yrank = nodeyirank.index(node)
    posx = nodes[node]['position'][0]
    copynranks = nodeyirank[0:len(nodeyirank)]
    del copynranks[yrank]
    yrank += 1
    for cr in range(0,totalnodes-1):
        attr = {}
        nodeval = yrank*factor+copynranks[cr]
        ##print(yrank)
        ##print("nodeval: ", nodeval)
        posy = nodes[copynranks[cr]]['position'][1]
        attr['position'] = (posx,posy) 
        attr['left'] = None
        attr['right'] = None
        nodevald = None
        crnodepos = nodeyirank.index(copynranks[cr])
        if crnodepos > 0:
            if nodeyirank[crnodepos-1] == nodeyirank[yrank-1]:
                nodevald = nodeyirank[yrank-1]
                nodes[node]['up'] = nodeval##copynranks[cr]
            else:
                nodevald = yrank*factor + nodeyirank[crnodepos-1]
        attr['down'] = nodevald
        nodevald = None
        if crnodepos < len(nodeyirank)-1:
            if nodeyirank[crnodepos+1] == nodeyirank[yrank-1]:
                nodevald = nodeyirank[yrank-1]
                nodes[node]['down'] = nodeval ##copynranks[cr]
            else:
                nodevald = yrank*factor + nodeyirank[crnodepos+1]
        attr['up'] = nodevald
        crossingnodes[nodeval] = attr
        crossingnodesrev[attr['position']] = nodeval
#2nd pass working on nodexirank indexing
for node in nodes:
   xrank = nodexirank.index(node)
   posy = nodes[node]['position'][1]
   copynranks = nodexirank[0:len(nodexirank)]
   del copynranks[xrank]
   for cr in range(0,totalnodes-1):
      posx = nodes[copynranks[cr]]['position'][0]
      nodeval = crossingnodesrev[(posx,posy)]
      attr = crossingnodes[nodeval]
      nodevald = None
      crnodepos = nodexirank.index(copynranks[cr])
      if crnodepos > 0:
         if nodexirank[crnodepos-1] == nodexirank[xrank]:
             nodevald = nodexirank[xrank]
             nodes[node]['right'] = nodeval##copynranks[cr]
         else:
             nposx = nodes[nodexirank[crnodepos-1]]['position'][0]
             nodevald = crossingnodesrev[(nposx,posy)]
      attr['left'] = nodevald
      nodevald = None
      if crnodepos < len(nodexirank)-1:
         if nodexirank[crnodepos+1] == nodexirank[xrank]:
             nodevald = nodexirank[xrank]
             nodes[node]['left'] = nodeval ##copynranks[cr]
         else:
             nposx = nodes[nodexirank[crnodepos+1]]['position'][0]
             ####print(crossingnodesrev)
             nodevald = crossingnodesrev[(nposx,posy)]
      attr['right'] = nodevald
      crossingnodes[nodeval] = attr
## randomize crossings
## crossing = 1 vertical  crossing = 0 lateral
##print("nodes: ", nodes)
for node in crossingnodes:
   randval = random.random()
   if randval >= .5:
      crossingnodes[node]['crossing'] = 1
   else:
      crossingnodes[node]['crossing'] = 0
      
##build boundary nodes
xboundaries = [0,dimx]
yboundaries = [0,dimy]
boundarydict = {}
boundarydictrev = {}
i = -1
checki = 0
for xboundary in xboundaries:
   attr = {}
   attr['left'] = None
   attr['right'] = None
   attr['up'] = None
   attr['down'] = None
   attr['crossing'] = None
   ypos = 0
   attr['position'] = (xboundary, ypos)
   if xboundary != 0:
      xpos = nodes[nodexirank[len(nodexirank)-1]]['position'][0]
      ##print('xpos: ',xpos)
      bnnode = boundarydictrev[(xpos,ypos)]
      ##print('bnnode', bnnode)
      attr['left'] = bnnode
      boundarydict[bnnode]['right'] = i
   boundarydictrev[(xboundary,ypos)] = i
   boundarydict[i] = attr
   prevnode = i
   i -= 1
   if i == -2:
      nprevnode = prevnode
      for node in nodexirank:
         attr = {}
         attr['left'] = None
         attr['right'] = None
         attr['up'] = None
         attr['down'] = None
         attr['crossing'] = None
         xpos = nodes[node]['position'][0]
         yminpos = nodes[nodeyirank[0]]['position'][1]
         coord = (xpos,yminpos)
         upnode = None
         if coord in crossingnodesrev:
            upnode = crossingnodesrev[coord]
         if coord in nodepostoi:
            upnode = nodepostoi[coord]
         attr['up'] = upnode
         attr['position'] = (xpos,0)
         attr['left'] = nprevnode
         boundarydict[nprevnode]['right'] = i
         boundarydictrev[(xpos,0)] = i
         boundarydict[i] = attr
         nprevnode = i
         i -= 1         
   for node in nodeyirank:
      attr = {}
      attr['left'] = None
      attr['right'] = None
      attr['up'] = None
      attr['down'] = None
      attr['crossing'] = None
      ypos = nodes[node]['position'][1]
      if checki == 0:
         xminpos = nodes[nodexirank[0]]['position'][0]
         coord = (xminpos, ypos)
         rightnode = None
         if coord in crossingnodesrev:
            rightnode = crossingnodesrev[coord]
         if coord in nodepostoi:
            rightnode = nodepostoi[coord]
         attr['right'] = rightnode
      else:
         xmaxpos = nodes[nodexirank[len(nodexirank)-1]]['position'][0]
         coord = (xmaxpos, ypos)
         leftnode = None
         if coord in crossingnodesrev:
            leftnode = crossingnodesrev[coord]
         if coord in nodepostoi:
            leftnode = nodepostoi[coord]
         attr['left'] = leftnode         
      attr['position'] = (xboundary,ypos)
      attr['down'] = prevnode
      boundarydict[prevnode]['up'] = i
      boundarydictrev[(xboundary,ypos)] = i
      boundarydict[i] = attr
      prevnode = i
      i -= 1
   attr = {}
   attr['left'] = None
   attr['right'] = None
   attr['up'] = None
   attr['down'] = None
   attr['crossing'] = None
   ypos = dimy
   attr['position'] = (xboundary, ypos)
   attr['down'] = prevnode
   if xboundary != 0:
      xpos = nodes[nodexirank[len(nodexirank)-1]]['position'][0]
      bnnode = boundarydictrev[(xpos,ypos)]
      attr['left'] = bnnode
      boundarydict[bnnode]['right'] = i
   boundarydictrev[(xboundary,ypos)] = i
   boundarydict[i] = attr
   if checki == 0:
      nprevnode = i
      i -= 1
      for node in nodexirank:
         attr = {}
         attr['left'] = None
         attr['right'] = None
         attr['up'] = None
         attr['down'] = None
         attr['crossing'] = None
         xpos = nodes[node]['position'][0]
         ymaxpos = nodes[nodeyirank[len(nodeyirank)-1]]['position'][1]
         coord = (xpos,ymaxpos)
         downnode = None
         if coord in crossingnodesrev:
            downnode = crossingnodesrev[coord]
         if coord in nodepostoi:
            downnode = nodepostoi[coord]
         attr['down'] = downnode
         attr['position'] = (xpos,dimy)
         attr['left'] = nprevnode
         boundarydict[nprevnode]['right'] = i
         boundarydictrev[(xpos,dimy)] = i
         boundarydict[i] = attr
         nprevnode = i
         i -= 1  
   checki = i
## finished building boundary nodes
   
## compile all nodes into a position lookup dictionary
completerefrev = {}
for pos in nodepostoi:
   completerefrev[pos] = nodepostoi[pos]
for pos in crossingnodesrev:
   completerefrev[pos] = crossingnodesrev[pos]
for pos in boundarydictrev:
   completerefrev[pos] = boundarydictrev[pos]
## finished compiling all nodes into a complete position lookup
##compile all nodes in a lookup directory
completeref = {}
for node in nodes:
   completeref[node] = nodes[node]
for node in crossingnodes:
   completeref[node] = crossingnodes[node]
for node in boundarydict:
   completeref[node] = boundarydict[node]
##finished compiling all nodes

##reindex nodes to vertex list and position to index vert index
##a bit goofy doing this now, but saves work, and I don't feel like
##re writing the above.
vertices = []
vertpostoindex = {}
i = 0
for nodepos in completerefrev:
   ##vertices.append(nodepos)
   npx, npy = nodepos
   vertices.append((float(npx)/dimy,float(npy)/dimy,0.0))
   vertpostoindex[nodepos] = i
   i += 1
##finished reindexing vertices
   
##pass to complete connections between boundary and non boundary nodes
##one way passes have been completed above, but I hadn't ensured
##that bijection relations were fully done.
for node in boundarydict:
   if completeref[node]['up'] != None:
      neignode = completeref[node]['up']
      if completeref[neignode]['down'] == None:
         completeref[neignode]['down'] = node
         boundarydict[node]['crossing'] = completeref[neignode]['crossing']
         completeref[node]['crossing'] = completeref[neignode]['crossing']
         if neignode in crossingnodes:
            crossingnodes[neignode]['down'] = node
         if neignode in nodes:
            nodes[neignode]['down'] = node
   if completeref[node]['down'] != None:
      neignode = completeref[node]['down']
      if completeref[neignode]['up'] == None:
         completeref[neignode]['up'] = node
         boundarydict[node]['crossing'] = completeref[neignode]['crossing']
         completeref[node]['crossing'] = completeref[neignode]['crossing']
         if neignode in crossingnodes:
            crossingnodes[neignode]['up'] = node
         if neignode in nodes:
            nodes[neignode]['up'] = node
   if completeref[node]['left'] != None:
      neignode = completeref[node]['left']
      if completeref[neignode]['right'] == None:
         completeref[neignode]['right'] = node
         boundarydict[node]['crossing'] = completeref[neignode]['crossing']
         completeref[node]['crossing'] = completeref[neignode]['crossing']
         if neignode in crossingnodes:
            crossingnodes[neignode]['right'] = node
         if neignode in nodes:
            nodes[neignode]['right'] = node
   if completeref[node]['right'] != None:
      neignode = completeref[node]['right']
      if completeref[neignode]['left'] == None:
         completeref[neignode]['left'] = node
         boundarydict[node]['crossing'] = completeref[neignode]['crossing']
         completeref[node]['crossing'] = completeref[neignode]['crossing']
         if neignode in crossingnodes:
            crossingnodes[neignode]['left'] = node
         if neignode in nodes:
            nodes[neignode]['left'] = node
## finished completion on boundary pass

##indexing simple polygons over the completeref set
stopcheck = False
startposition = (0,0)
currentnode = completerefrev[startposition]
currentposition = startposition
nextrowval = completeref[currentnode]['right']
polynodesrev = {}
polynodes = {}
i = 0
while not stopcheck:
   columnstepcheck = False
   while not columnstepcheck:
      ####print(completeref[currentnode]['position'])
      polypos = []##[completeref[currentnode]['position']]
      for j in range(0,4):
         currentposition = completeref[currentnode]['position']
         if j == 0:
            nextpos = completeref[currentnode]['up']
            if nextpos == None:
               columnstepcheck = True
               break
         elif j == 1:
            nextpos = completeref[currentnode]['right']
            if nextpos == None:
               columnstepcheck = True
               stopcheck = True
               break
         elif j == 2:
            nextpos = completeref[currentnode]['down']
         elif j == 3:
            nextpos = completeref[currentnode]['left']
            if nextpos == None:
               print('missed assignment: ', currentnode)
            nextpos = completeref[nextpos]['up']
         ##if j != 3:
         polypos.append(currentposition)
         
         currentnode = nextpos
      if columnstepcheck:
         continue
      polynodesrev[tuple(polypos)] = i
      polynodes[i] = tuple(polypos)
      i += 1
   if stopcheck:
      continue
   currentnode = nextrowval
   nextrowval = completeref[currentnode]['right']
##finished indexing simple polygons

##recursive function to check crossing
def checkcross(crossval, node, crossingnodes, dirswitch, crosslist):
   check = False
   if crossval:
      if dirswitch:
         topnode = crossingnodes[node]['up']
##         if topnode in nopasscrosslist:
##            return crosslist
         crosslist.append(topnode)
         if topnode in crossingnodes:
            ncrossval = crossingnodes[topnode]['crossing']
            crossingnone = ncrossval == None  ##node setting
            if ncrossval and not crossingnone:
               return checkcross(crossval,topnode,crossingnodes,dirswitch,
                                 crosslist)
               
            else:
               return crosslist
         else:
            return crosslist

      else:
         downnode = crossingnodes[node]['down']
##         if downnode in nopasscrosslist:
##            return crosslist
         crosslist.append(downnode)
         if downnode in crossingnodes:
            ncrossval = crossingnodes[downnode]['crossing']
            crossingnone = ncrossval == None  ##node setting
            if ncrossval and not crossingnone:
               return checkcross(crossval,downnode,crossingnodes,dirswitch,
                                 crosslist)
            else:
               return crosslist
         else:
            return crosslist

   else:
      if dirswitch:
         rightnode = crossingnodes[node]['right']
##         if rightnode in nopasscrosslist:
##            return crosslist
         crosslist.append(rightnode)
         if rightnode in crossingnodes:
            ncrossval = crossingnodes[rightnode]['crossing']
            crossingnone = ncrossval == None  ##node setting
            if not ncrossval and not crossingnone:
               return checkcross(crossval,rightnode,crossingnodes,dirswitch,
                                 crosslist)
            else:
               return  crosslist
         else:
            return crosslist

      else:
         leftnode = crossingnodes[node]['left']
##         if leftnode in nopasscrosslist:
##            return crosslist
         crosslist.append(leftnode)
         if leftnode in crossingnodes:
            ncrossval = crossingnodes[leftnode]['crossing']
            crossingnone = ncrossval == None  ##node setting
            if not ncrossval and not crossingnone:
               return checkcross(crossval,leftnode,crossingnodes,dirswitch,
                                 crosslist)
            else:
               return crosslist
         else:
            return crosslist


##to check crossing nodes list, if a node is found it marked
## marked at the crossing node in the given direction.
## this is used in identifying the vertices for face construction
def checkneighbornode(crosslist, crossingnodes, nodes, direction):
   cdirection = None
   if direction == 'up':
      cdirection = 'right'
   elif direction == 'left':
      cdirection = 'down'
   elif direction == 'down':
      cdirection = 'right'
   elif direction == 'right':
      cdirection = 'up'
   i = 0
   for cnode in crosslist:
      neighnode = crossingnodes[cnode][cdirection]
      if neighnode in nodes:
         return neighnode,i
      i += 1
   return None, i
      
##function to check within face subdivision area
def nodecolumncheck(minpos, maxpos, pnodes, crosslist, direction,
                    completeref, selfnode):
   check = True
   eqcheck = False
   i = 0
   ##print('crosslist nodecolumncheck: ', crosslist)
   ##print('minpos: ', minpos)
   ##print('maxpos: ', maxpos)
   for node in crosslist:
      pos = completeref[node]['position']
      xpost = (pos[0] == 0) or (pos[0] == dimx)
      ypost = (pos[1] == 0) or (pos[1] == dimy)
      if xpost and ypost:
         continue
      npos = None
      if direction:
         ypos = pos[1]
         if ypost:
            continue
         nodepos = pnodes[ypos]
         if nodepos == selfnode:
            continue
         npos = nodes[nodepos]['position'][0]
      else:
         xpos = pos[0]
         if xpost:
            continue
         nodepos = pnodes[xpos]
         if nodepos == selfnode:
            continue
         npos = nodes[nodepos]['position'][1]
      check1 = npos >= minpos
      check2 = npos <= maxpos
      check3 = npos == minpos
      check4 = npos == maxpos
      if check1 and check2:
         check = False
         if check3 or check4:
            eqcheck = True
      if not check:
         break
      i += 1
   return check, eqcheck, i

##function used 
def buildnodesedge(axispos, crosslist, completeref, direction):
   rcrosslist = []
   for node in crosslist:
      pos = (None,None)
      posx = None
      posy = None
      if direction:
         posx = completeref[node]['position'][0]
         posy = axispos
      else:
         posy = completeref[node]['position'][1]
         posx = axispos
      pos = (posx, posy)
      rcrosslist.append(pos)
   return rcrosslist

def updatecrossings(completeref, rcrossinglist, pcrossinglist):
   if len(rcrossinglist) >= 3:
      i = 0
      for node in pcrossinglist:
         if (i != 0) and (i != len(pcrossinglist)-1):
            rnode = rcrossinglist[i]
            crossingval = completeref[rnode]['crossing']
            completeref[node]['crossing'] = crossingval
            i += 1
   return completeref

##function to build simple polys for intersection testing on a given
##aggregate face
def buildfacesimplepolys(minpos, maxpos, polynodesrev, completerefrev,
                         completeref):
   stopcheck = False
   startposition = minpos
   maxposx = maxpos[0]
   maxposy = maxpos[1]
   currentnode = completerefrev[startposition]
   currentposition = startposition
   nextrowval = completeref[currentnode]['right']
   polynodeslist = []
   postopolynodes = {}
   ##print('buildfacesimplepolys minpos: ', minpos)
   ##print('buildfacesimplepolys maxpos: ', maxpos)
   ##print('nextrowval start: ',nextrowval)
   while not stopcheck:
      columnstepcheck = False
      while not columnstepcheck:
         polypos = []##[completeref[currentnode]['position']]
         for j in range(0,4):
            currentposition = completeref[currentnode]['position']
            if j == 0:
               nextpos = completeref[currentnode]['up']
               ##print('j==0 nextpos: ', nextpos)
               nextposy = None
               if nextpos != None:
                  nextposy = completeref[nextpos]['position'][1]
               t2 = nextpos == None
               if t2:
                  columnstepcheck = True
                  if currentposition[0] >= maxposx:
                     stopcheck = True
                  break
               if nextposy > maxposy:
                  columnstepcheck = True
                  if currentposition[0] >= maxposx:
                     stopcheck = True
                  break
            elif j == 1:
               nextpos = completeref[currentnode]['right']
               nextposx = None
               if nextpos != None:
                  nextposx = completeref[nextpos]['position'][0]
               t2 = nextpos == None
               if t2:
                  columnstepcheck = True
                  stopcheck = True
                  break                  
               if nextposx > maxposx:
                  columnstepcheck = True
                  stopcheck = True
                  break
            elif j == 2:
               nextpos = completeref[currentnode]['down']
            elif j == 3:
               nextpos = completeref[currentnode]['left']
               nextpos = completeref[nextpos]['up']
            ##if j != 3:
            polypos.append(currentposition)
                  
            currentnode = nextpos
         if columnstepcheck:
            continue
         polynodeslist.append(polypos)
         for pos in polypos:
            if pos in postopolynodes:
               postopolynodes[pos].append(polypos)
            else:
               postopolynodes[pos] = [polypos]
      if stopcheck:
         continue
      ##print('polynodeslist: ',polynodeslist)
      currentnode = nextrowval
      ##print('currentnode: ', currentnode)
      nextrowval = completeref[currentnode]['right']
   return polynodeslist, postopolynodes
## end function simple polynode build

##function to reaggregate simple polys returns 4 nodes coordinates
def rebuildfacesimplepolys(rnodepos, rnodepoly, passlist, spostopolys,
                           completeref, completerefrev):
   rnode = completerefrev[rnodepos]
   directions = ['up','down','left','right']
   orthogdirections = []
   rnodeposneighbors = []
   nnodepositiontoindex = {}
   i = 0
   ##assumed that the position indexing for a neighbor node
   ## is always mirror symmetric relative to the previous iteration
   ## for a given direction
   for direction in directions:
      nnode = completeref[rnode][direction]
      nnodepos = None
      if nnode != None:
         nnodepos = completeref[nnode]['position']
      if nnodepos in rnodepoly[0]:
         orthogdirections.append(direction)
         rnodeposneighbors.append(nnodepos)
         nnodepositiontoindex[nnodepos] = rnodepoly[0].index(nnodepos)
      i += 1
   crosslists = []
   ##print('rnodeposneighbors: ', rnodeposneighbors)
   ##print('rnodepoly: ', rnodepoly)
   ##print('spostopolys: ', spostopolys)
   ##print('passlist: ', passlist)
   for nnodepos in rnodeposneighbors:
      nextindex = nnodepositiontoindex[nnodepos]
      ##print('nextindex: ', nextindex)
      inpasslist = True
      neighbornodepos = nnodepos
      processedpolys = rnodepoly
      procpositions = [rnodepos,neighbornodepos]
      prevneighnodepos = neighbornodepos
      i = 0
      while inpasslist and i < 100:
         polyslist = spostopolys[neighbornodepos]
         for poly in polyslist:
            t1 = poly not in processedpolys
            t2 = poly in passlist
            if t1 and t2:
               ##print('processedpoly add: ', poly)
               processedpolys.append(poly)
               neighbornodepos = poly[nextindex]
               procpositions.append(neighbornodepos)
            elif t1 and not t2:
               inpasslist = False
         if prevneighnodepos == neighbornodepos:
            inpasslist = False
         prevneighnodepos = neighbornodepos
         i += 1
      crosslists.append(procpositions)
   ##print ("Crosslists: ", crosslists) 
   list1 = crosslists[0]
   xdist = abs(list1[0][0] -list1[len(list1)-1][0])
   zerox = False
   if xdist == 0:
      zerox = True
   crosslist1 = crosslists[0]
   crosslist2 = crosslists[1]
   node2pos = None
   if zerox:
      node2pos = (crosslist2[len(crosslist2)-1][0],
                  crosslist1[len(crosslist1)-1][1])
   else:
      node2pos = (crosslist1[len(crosslist1)-1][0],
                  crosslist2[len(crosslist2)-1][1])
   ##print('crosslist1[0]: ', crosslist1[0])
   ##print('node2pos',node2pos)
   vertposlist = [crosslist1[0],crosslist1[len(crosslist1)-1],
                  node2pos, crosslist2[len(crosslist2)-1]]
   ## in order to ensure proper keying on this poly we might want to
   ## to ensure that the face is ordered similarly to the simple
   ## poly method where minx, miny is the starting vertex, and
   ## maxx,maxy vert is in the 3rd vertex position, thus I sort
   ## the vertices first by x positions from smallest to largest,
   ##and then different x groups (remember two x's are the same on the
   ##rectangle for each group), sorting by the y's.  I reverse the
   ##the sort order on the 2nd group to ensure the maxx, maxy is
   ##in the 1rst order of the 2nd group or when lists are concatenated
   ##in the 3rd position.  
   vertposlist.sort(key=lambda tup: tup[0])
   vertpos1, vertpos2, vertpos3, vertpos4 = vertposlist
   vertposlist1 = [vertpos1,vertpos2]
   vertposlist2 = [vertpos3,vertpos4]
   vertposlist1.sort(key=lambda tup: tup[1])
   vertposlist2.sort(key=lambda tup: tup[1], reverse = True)
   vertposlist = vertposlist1 + vertposlist2
   return tuple(vertposlist)
## construct vertices faces crossings
facecnt = 0
vertcnt = 0
##rules for crossing
##Node have crossing precedent.
##An edge starting from a crossingnode, does not
##have an edge terminating on a non passing neighbor
##crossing node, but may pass into a crossing node
##if positive for crossing, or in other words, all edges
##starting from a crossing node may not have a 4 direction
##radial pattern but instead contingent on the crossing
##positives assigned.
##Crossingnodes and nodes alike have boundary clearance
##direction leeway.  Meaning we can draw a subdivision edge
##in the direction of the nearest boundary, as long as such
##boundary is on a neighboring.
##All edges starting from a node have 4 direction
##radial pattern.
i = 0
faces = []
nopasscrosslist = []
for node in nodes:
   #top crossval = 1, dirswitch = 1
   switches1 = [0,1]
   switches2 = [0,1]
   for switch1 in switches1:
      for switch2 in switches2:
         crosslist = [node] 
         crosslist = checkcross(switch1, node, completeref,
                                switch2, crosslist)
         ##print('crosslist',crosslist)
         crossendnode = crosslist[len(crosslist)-1]
         if crossendnode == None:
            del crosslist[len(crosslist)-1]
         if len(crosslist) <= 1:
            continue    
         if switch1 and switch2:
            direction = 'up'
         elif switch1 and not switch2:
            direction = 'down'
         elif not switch1 and switch2:
            direction = 'right'
         else:
            direction = 'left'        
         ncheck, nodeindex = checkneighbornode(crosslist, completeref,
                                               nodes, direction)
         if ncheck != None:
            crosslist = crosslist[0:nodeindex+1]
         if switch1 and switch2:
            maxpos = completeref[crosslist[len(crosslist)-1]]['position'][1]
            minpos = completeref[crosslist[0]]['position'][1]
         elif switch1 and not switch2:
            minpos = completeref[crosslist[len(crosslist)-1]]['position'][1]
            maxpos = completeref[crosslist[0]]['position'][1]
         elif not switch1 and switch2:
            maxpos = completeref[crosslist[len(crosslist)-1]]['position'][0]
            minpos = completeref[crosslist[0]]['position'][0]
         else:
            minpos = completeref[crosslist[len(crosslist)-1]]['position'][0]
            maxpos = completeref[crosslist[0]]['position'][0]
            
         switch3 = None
         switch4 = None
         direction3 = None
         direction4 = None
         if direction == 'up':
            #right
            switch3 = False
            switch4 = True
            direction3 = 0
            direction4 = 1
         elif direction == 'right':
            #down
            switch3 = True
            swithc4 = False
            direction3 = 1
            direction4 = 0
         elif direction == 'down':
            #left
            switch3 = False
            switch4 = False
            direction3 = 0
            direction4 = 1
         elif direction == 'left':
            #up
            switch3 = True
            switch4 = True
            direction3 = 1
            direction4 = 0
         pnodes = None
         if not direction3:
            pnodes = xpnodes
         else:
            pnodes = ypnodes
         cnode = crosslist[len(crosslist)-1]
         crosslist2 = [cnode]
         crosslist2 = checkcross(switch3, cnode, completeref,
                                 switch4, crosslist2)
         crossendnode = crosslist2[len(crosslist2)-1]
         if crossendnode == None:
            del crosslist2[len(crosslist2)-1]
         ##print('crosslist2: ', crosslist2)

         ##print('pnodes: ',pnodes)
         ncolchk, eqcheck, c2nindex = nodecolumncheck(minpos, maxpos,
                                                      pnodes, crosslist2,
                                                      direction3, completeref,
                                                      node)
         c2index = None
         if not ncolchk:
            if not eqcheck:
               c2index = c2nindex
            else:
               c2index = c2nindex+1
         else:
            c2index = len(crosslist2)
         crosslist2 = crosslist2[0:c2index]
         if len(crosslist2) <= 1:
            continue
         ##print('crosslist2: ', crosslist2)
         cedgepos3 = None
         cedgepos4 = None
         if direction4:
            cedgepos3 = completeref[crosslist2[len(crosslist2)-1]]['position'][0]
            cedgepos4 = completeref[crosslist[0]]['position'][1]
         else:
            cedgepos3 = completeref[crosslist2[len(crosslist2)-1]]['position'][1]
            cedgepos4 = completeref[crosslist[0]]['position'][0]
         crosslist3 = buildnodesedge(cedgepos3, crosslist, completeref, direction4)
         crosslist4 = buildnodesedge(cedgepos4, crosslist2, completeref, direction3)
         allnodescrosslist = crosslist+crosslist2+crosslist3+crosslist4
         completeref = updatecrossings(completeref, crosslist, crosslist3)
         completeref = updatecrossings(completeref, crosslist2, crosslist4)
         if direction == 'up':
            maxpos = completeref[crosslist2[len(crosslist2)-1]]['position']
            minpos = completeref[crosslist[0]]['position']
         elif direction == 'down':
            minpos = completeref[crosslist2[len(crosslist2)-1]]['position']
            maxpos = completeref[crosslist[0]]['position']
         elif direction == 'right':
            maxpos = completeref[crosslist[len(crosslist)-1]]['position']
            minpos = (completeref[crosslist[0]]['position'][0],
                      completeref[crosslist2[len(crosslist2)-1]]['position'][1])
         elif direction == 'left':
            maxpos = (completeref[crosslist[0]]['position'][0],
                      completeref[crosslist2[len(crosslist2)-1]]['position'][1])
            minpos = completeref[crosslist[len(crosslist)-1]]['position']
         spolys,spostopolys = buildfacesimplepolys(minpos, maxpos,
                                                   polynodesrev,
                                                   completerefrev, completeref)
         ##perform simple poly intersection testing, eliminating
         ##subdivision overlap
         ydiff = maxpos[1] - minpos[1]
         xdiff = maxpos[0] - minpos[0]
         ccontinue = False
         passlist = []
         rootpoly = spostopolys[completeref[node]['position']]
         rnodepos = completeref[node]['position']
         ##print('spolys: ', spolys)
         ##print('nopasscrosslist: ', nopasscrosslist)
         for poly in spolys:
            if poly in nopasscrosslist:
               print('rejected poly: ', poly)
               if poly == rootpoly:
                  ccontinue = True
                  break
            else:
               passlist.append(poly)
         ##print('passlist: ', passlist)
         if ccontinue:
            continue
         vposlist = rebuildfacesimplepolys(rnodepos, rootpoly,
                                           passlist, spostopolys,
                                           completeref, completerefrev)
         for poly in spolys:
            if not poly in nopasscrosslist:
               nopasscrosslist.append(poly)
##         for cnode in allnodescrosslist:
##            if not cnode in nopasscrosslist:
##               nopasscrosslist.append(cnode)
         # Two edges of face determined.
         # Build vertices
##         vpos1 = completeref[crosslist[0]]['position']
##         vpos2 = completeref[crosslist2[0]]['position']
##         vpos3 = completeref[crosslist2[len(crosslist2)-1]]['position']
##         vpos4 = completeref[crosslist3[0]]['position']
         ##print('vposlist: ', vposlist)
         vpos1,vpos2,vpos3,vpos4 = vposlist
         vi1 = vertpostoindex[vpos1]
         vi2 = vertpostoindex[vpos2]
         vi3 = vertpostoindex[vpos3]
         vi4 = vertpostoindex[vpos4]
         facegroup = (vi1,vi2,vi3,vi4)
         faces.append(facegroup)

## work remainders reiterates the same procedure much as given above.
## I've opted to skip this for now, overlap issues still occuring despite
## checks.  Honestly I've opted to go for a simpler construction method
## since a fairly decent percentage of the map is likely filled by use
## of random crossing assignments, so the remainder are regularity filler.
##for polypositionsface in polynodesrev:
##   if list(polypositionsface) in nopasscrosslist:
##      continue
##   else:
##      nodepos = polypositionsface[0]  ## we could randomly pick on this simple
##                                      ## face
##      node = completerefrev[nodepos]
##      switches1 = [0,1]
##      switches2 = [0,1]
##      for switch1 in switches1:
##         for switch2 in switches2:
##            crosslist = [node] 
##            crosslist = checkcross(switch1, node, completeref,
##                                   switch2, crosslist)
##            ##print('crosslist',crosslist)
##            crossendnode = crosslist[len(crosslist)-1]
##            if crossendnode == None:
##               del crosslist[len(crosslist)-1]
##
##            if switch1 and switch2:
##               direction = 'up'
##            elif switch1 and not switch2:
##               direction = 'down'
##            elif not switch1 and switch2:
##               direction = 'right'
##            else:
##               direction = 'left'        
##            ncheck, nodeindex = checkneighbornode(crosslist, completeref,
##                                                  nodes, direction)
##            if ncheck != None:
##               crosslist = crosslist[0:nodeindex+1]
##            if len(crosslist) <= 1:
##               continue    
##            if switch1 and switch2:
##               maxpos = completeref[crosslist[len(crosslist)-1]]['position'][1]
##               minpos = completeref[crosslist[0]]['position'][1]
##            elif switch1 and not switch2:
##               minpos = completeref[crosslist[len(crosslist)-1]]['position'][1]
##               maxpos = completeref[crosslist[0]]['position'][1]
##            elif not switch1 and switch2:
##               maxpos = completeref[crosslist[len(crosslist)-1]]['position'][0]
##               minpos = completeref[crosslist[0]]['position'][0]
##            else:
##               minpos = completeref[crosslist[len(crosslist)-1]]['position'][0]
##               maxpos = completeref[crosslist[0]]['position'][0]
##               
##            switch3 = None
##            switch4 = None
##            direction3 = None
##            direction4 = None
##            if direction == 'up':
##               #right
##               switch3 = False
##               switch4 = True
##               direction3 = 0
##               direction4 = 1
##            elif direction == 'right':
##               #down
##               switch3 = True
##               swithc4 = False
##               direction3 = 1
##               direction4 = 0
##            elif direction == 'down':
##               #left
##               switch3 = False
##               switch4 = False
##               direction3 = 0
##               direction4 = 1
##            elif direction == 'left':
##               #up
##               switch3 = True
##               switch4 = True
##               direction3 = 1
##               direction4 = 0
##            pnodes = None
##            if not direction3:
##               pnodes = xpnodes
##            else:
##               pnodes = ypnodes
##            cnode = crosslist[len(crosslist)-1]
##            crosslist2 = [cnode]
##            crosslist2 = checkcross(switch3, cnode, completeref,
##                                    switch4, crosslist2)
##            crossendnode = crosslist2[len(crosslist2)-1]
##            if crossendnode == None:
##               del crosslist2[len(crosslist2)-1]
##            ##print('crosslist2: ', crosslist2)
##
##            ##print('pnodes: ',pnodes)
##            ncolchk, eqcheck, c2nindex = nodecolumncheck(minpos, maxpos,
##                                                         pnodes, crosslist2,
##                                                         direction3, completeref,
##                                                         node)
##            c2index = None
##            if not ncolchk:
##               if not eqcheck:
##                  c2index = c2nindex
##               else:
##                  c2index = c2nindex+1
##            else:
##               c2index = len(crosslist2)
##            crosslist2 = crosslist2[0:c2index]
##            if len(crosslist2) <= 1:
##               continue
##            ##print('crosslist2: ', crosslist2)
##            cedgepos3 = None
##            cedgepos4 = None
##            if direction4:
##               cedgepos3 = completeref[crosslist2[len(crosslist2)-1]]['position'][0]
##               cedgepos4 = completeref[crosslist[0]]['position'][1]
##            else:
##               cedgepos3 = completeref[crosslist2[len(crosslist2)-1]]['position'][1]
##               cedgepos4 = completeref[crosslist[0]]['position'][0]
##            crosslist3 = buildnodesedge(cedgepos3, crosslist, completeref, direction4)
##            crosslist4 = buildnodesedge(cedgepos4, crosslist2, completeref, direction3)
##            allnodescrosslist = crosslist+crosslist2+crosslist3+crosslist4
##            completeref = updatecrossings(completeref, crosslist, crosslist3)
##            completeref = updatecrossings(completeref, crosslist2, crosslist4)
##            if direction == 'up':
##               maxpos = completeref[crosslist2[len(crosslist2)-1]]['position']
##               minpos = completeref[crosslist[0]]['position']
##            elif direction == 'down':
##               minpos = completeref[crosslist2[len(crosslist2)-1]]['position']
##               maxpos = completeref[crosslist[0]]['position']
##            elif direction == 'right':
##               maxpos = completeref[crosslist[len(crosslist)-1]]['position']
##               minpos = (completeref[crosslist[0]]['position'][0],
##                         completeref[crosslist2[len(crosslist2)-1]]['position'][1])
##            elif direction == 'left':
##               maxpos = (completeref[crosslist[0]]['position'][0],
##                         completeref[crosslist2[len(crosslist2)-1]]['position'][1])
##               minpos = completeref[crosslist[len(crosslist)-1]]['position']
##            spolys,spostopolys = buildfacesimplepolys(minpos, maxpos,
##                                                      polynodesrev,
##                                                      completerefrev, completeref)
##            ##perform simple poly intersection testing, eliminating
##            ##subdivision overlap
##            ydiff = maxpos[1] - minpos[1]
##            xdiff = maxpos[0] - minpos[0]
##            ccontinue = False
##            passlist = []
##            rootpoly = spostopolys[completeref[node]['position']]
##            rnodepos = completeref[node]['position']
##            for poly in spolys:
##               if poly in nopasscrosslist:
##                  ##print('rejectedpoly: ', poly)
##                  if poly == rootpoly:
##                     ccontinue = True
##                     break
##               else:
##                  passlist.append(poly)
##            if ccontinue:
##               continue
##            vposlist = rebuildfacesimplepolys(rnodepos, rootpoly,
##                                              passlist, spostopolys,
##                                              completeref, completerefrev)
##            for poly in passlist:
##               if poly in nopasscrosslist:
##                  print('accepted poly errors: ' , poly)
##               else:
##                  nopasscrosslist.append(poly)
####            for poly in spolys:
####               if not poly in nopasscrosslist:
####                  nopasscrosslist.append(poly)
##
##   ##         for cnode in allnodescrosslist:
##   ##            if not cnode in nopasscrosslist:
##   ##               nopasscrosslist.append(cnode)
##            # Two edges of face determined.
##            # Build vertices
##   ##         vpos1 = completeref[crosslist[0]]['position']
##   ##         vpos2 = completeref[crosslist2[0]]['position']
##   ##         vpos3 = completeref[crosslist2[len(crosslist2)-1]]['position']
##   ##         vpos4 = completeref[crosslist3[0]]['position']
##            ##print('vposlist: ', vposlist)
##            vpos1,vpos2,vpos3,vpos4 = vposlist
##            vi1 = vertpostoindex[vpos1]
##            vi2 = vertpostoindex[vpos2]
##            vi3 = vertpostoindex[vpos3]
##            vi4 = vertpostoindex[vpos4]
##            facegroup = (vi1,vi2,vi3,vi4)
##            faces.append(facegroup)

###work remainders this is ultra simple we simply use single simple faces.
for polypositionsface in polynodesrev:
   if list(polypositionsface) in nopasscrosslist:
      continue
   else:
      vpos1,vpos2,vpos3,vpos4 = polypositionsface  ## we could randomly pick on this simple
      vi1 = vertpostoindex[vpos1]
      vi2 = vertpostoindex[vpos2]
      vi3 = vertpostoindex[vpos3]
      vi4 = vertpostoindex[vpos4]
      facegroup = (vi1,vi2,vi3,vi4)
      faces.append(facegroup)                              ## face
      
me.from_pydata(vertices,[],faces)      
me.update(calc_edges=True)      
#I get closer to finishing!  Whittling away this little program!
