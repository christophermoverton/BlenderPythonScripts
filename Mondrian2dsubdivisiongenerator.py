#Mondrian like subdivision generator
import bpy
import random
dimx = 50
dimy = 65
totalnodes = 3
meshName = "Mondrian"
obName = "MondrianObj"
me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)
##track edges on mondrian generator and vertices
nodes = {}
nodepostoi = {}
for i in range(0,totalnodes):
   attr = {}
   randposx = random.randint(0,dimx)
   randposy = random.randint(0,dimy)
   attr['position'] = (randposx,randposy)
   attr['left'] = None
   attr['right'] = None
   attr['up'] = None
   attr['down'] = None
   nodes[i] = attr
   nodepostoi[(randposx,randposy)] = i
nodeposlist = list(nodepostoi.keys())   
#node ordering
nodexrank = nodeposlist[0:len(nodeposlist)]
nodeyrank = nodeposlist[0:len(nodeposlist)]
nodexrank.sort(key=lambda tup: tup[0])
nodeyrank.sort(key=lambda tup: tup[1])
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
    for cr in range(0,totalnodes-1):
        attr = {}
        nodeval = yrank*factor+copynranks[cr]
        posy = nodes[copynranks[cr]]['position'][1]
        attr['position'] = (posx,posy) 
        attr['left'] = None
        attr['right'] = None
        nodevald = None
        crnodepos = nodeyirank.index(copynranks[cr])
        if crnodepos > 0:
            if nodeyirank[crnodepos-1] == yrank:
                nodevald = yrank
                nodes[yrank]['top'] = copynranks[cr]
            else:
                nodevald = yrank*factor + nodeyirank[crnodepos-1]
        attr['down'] = nodevald
        nodevald = None
        if crnodepos < len(nodeyirank)-1:
            if nodeyirank[crnodepos+1] == yrank:
                nodevald = yrank
                nodes[yrank]['down'] = copynranks[cr]
            else:
                nodevald = yrank*factor + nodeyirank[crnodepos+1]
        attr['top'] = nodevald
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
         if nodexirank[crnodepos-1] == xrank:
             nodevald = xrank
             nodes[xrank]['right'] = copynranks[cr]
         else:
             nposx = nodes[nodexirank[cr-1]]['position'][0]
             nodevald = crossingnodesrev[(nposx,posy)]
      attr['left'] = nodevald
      nodevald = None
      if crnodepos < len(nodexirank)-1:
         if nodexirank[crnodepos+1] == yrank:
             nodevald = xrank
             nodes[xrank]['left'] = copynranks[cr]
         else:
             nposx = nodes[nodexirank[cr+1]]['position'][0]
             nodevald = crossingnodesrev[(nposx,posy)]
      attr['right'] = nodevald
      crossingnodes[nodeval] = attr
## randomize crossings
## crossing = 1 vertical  crossing = 0 lateral
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
   boundarydictrev[(xboundary,ypos)] = i
   boundarydict[i] = attr
   prevnode = i
   if i == -1:
      nprevnode = i
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
         xmaxpos = nodes[nodexirank[len(nodeyirank)-1]]['position'][0]
         coord = (xmaxpos, ypos)
         leftnode = None
         if coord in crossingnodesrev:
            leftnode = crossingnodesrev[coord]
         if coord in nodepostoi:
            leftnode = nodepostoi[coord]
         attr['left'] = rightnode         
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
         boundarydictrev[(xpos,0)] = i
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
   
##pass to complete connections between boundary and non boundary nodes
for node in boundarydict:
   if completeref[node]['up'] != None:
      neignode = completeref[node]['up']
      if completeref[neignode]['down'] == None:
         completeref[neignode]['down'] = node
         boundarydict[node]['crossing'] = completeref[neignode]['crossing']
         completeref[node]['crossing'] = completeref[neignode]['crossing']
         if neighnode in crossingnodes:
            crossingnodes[neighnode]['down'] = node
         if neighnode in nodes:
            nodes[neighnode]['down'] = node
   if completeref[node]['down'] != None:
      neignode = completeref[node]['down']
      if completeref[neignode]['up'] == None:
         completeref[neignode]['up'] = node
         boundarydict[node]['crossing'] = completeref[neignode]['crossing']
         completeref[node]['crossing'] = completeref[neignode]['crossing']
         if neighnode in crossingnodes:
            crossingnodes[neighnode]['up'] = node
         if neighnode in nodes:
            nodes[neighnode]['up'] = node
   if completeref[node]['left'] != None:
      neignode = completeref[node]['left']
      if completeref[neignode]['right'] == None:
         completeref[neignode]['right'] = node
         boundarydict[node]['crossing'] = completeref[neignode]['crossing']
         completeref[node]['crossing'] = completeref[neignode]['crossing']
         if neighnode in crossingnodes:
            crossingnodes[neighnode]['right'] = node
         if neighnode in nodes:
            nodes[neighnode]['right'] = node
   if completeref[node]['right'] != None:
      neignode = completeref[node]['right']
      if completeref[neignode]['left'] == None:
         completeref[neignode]['left'] = node
         boundarydict[node]['crossing'] = completeref[neignode]['crossing']
         completeref[node]['crossing'] = completeref[neignode]['crossing']
         if neighnode in crossingnodes:
            crossingnodes[neighnode]['left'] = node
         if neighnode in nodes:
            nodes[neighnode]['left'] = node
## finished completion on boundary pass
         
##recursive function to check crossing
def checkcross(crossval, node, crossingnodes, dirswitch, crosslist):
   check = False
   if crossval:
      if dirswitch:
         topnode = crossingnodes[node]['top']
         crosslist.append(topnode)
         if topnode in crossingnodes:
            ncrossval = crossingnodes[topnode]['crossing']
            if ncrossval:
               return checkcross(ncrossval,topnode,crossingnodes,dirswitch,
                                 crosslist)
               
            else:
               return (False, topnode, crosslist)
         else:
            if topnode == None:
               return (False, None, crosslist)
            else:
               return (True, topnode, crosslist)
      else:
         downnode = crossingnodes[node]['down']
         crosslist.append(downnode)
         if downnode in crossingnodes:
            ncrossval = crossingnodes[downnode]['crossing']
            if ncrossval:
               return checkcross(ncrossval,downnode,crossingnodes,dirswitch,
                                 crosslist)
            else:
               return (False, downnode, crosslist)
         else:
            if downnode == None:
               return (False, None, crosslist)
            else:
               return (True, downnode, crosslist)
   else:
      if dirswitch:
         rightnode = crossingnodes[node]['right']
         crosslist.append(rightnode)
         if rightnode in crossingnodes:
            ncrossval = crossingnodes[rightnode]['crossing']
            if not ncrossval:
               return checkcross(ncrossval,rightnode,crossingnodes,dirswitch,
                                 crosslist)
            else:
               return (False, rightnode, crosslist)
         else:
            if rightnode == None:
               return (False, None, crosslist)
            else:
               return (True, rightnode, crosslist)
      else:
         leftnode = crossingnodes[node]['left']
         crosslist.append(leftnode)
         if leftnode in crossingnodes:
            ncrossval = crossingnodes[leftnode]['crossing']
            if not ncrossval:
               return checkcross(ncrossval,leftnode,crossingnodes,dirswitch,
                                 crosslist)
            else:
               return (False, leftnode, crosslist)
         else:
            if leftnode == None:
               return (False, None, crosslist)
            else:
               return (True, leftnode, crosslist)

##to check crossing nodes list, if a node is found it marked
## marked at the crossing node in the given direction.
## this is used in identifying the vertices for face construction
def checkneighbornode(crosslist, crossingnodes, direction):
   if direction in ['up','down']:
      oppdirections = ['left','right']
   else:
      oppdirections = ['up','down']
   crosslistdict = {}
   for cnode in crosslist:
      oppddict = {}
      for oppdirection in oppdirections:
         oppdddict[oppdirection] = False
      cnodedict = crossingnodes[cnode]
      for oppdirection in oppdirections:
         nnode = cnodedict[oppdirection]
         if nnode not in crossingnodes:
            if nnode != None:
               oppddict[nnode] = True
      crosslistdict[cnode] = oppdict
   return crosslistdict

         
##function to check within face subdivision area
def nodecolumncheck(minpos, maxpos, nodearank, crosslist, direction,
                    completeref):
   for node in crosslist:
      pos = None
      if node in completeref:
         pos = completeref[node]['position']
      else:
         if direction:
            
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
for node in nodes:
   #top crossval = 1, dirswitch = 1
   switches1 = [0,1]
   switches2 = [0,1]
   for switch1 in switches1:
      for switch2 in switches2:
         check, nnode crosslist = checkcross(switch1, node,
                                             crossingnodes, switch2)
   
         crosslistdict = checkneighbornode(crosslist, crossingnodes,
                                           direction)
   crossval = nodes[node]['up']
   if crossval:
      
#construct faces and vertices from nodes
for node in nodes:
    
