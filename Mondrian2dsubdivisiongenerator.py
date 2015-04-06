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
i = 0
checki = 0
for xboundary in xboundaries:
   attr = {}
   attr['left'] = None
   attr['right'] = None
   attr['up'] = None
   attr['down'] = None
   ypos = 0
   attr['position'] = (xboundary, ypos)
   boundarydictrev[(xboundary,ypos)] = i
   boundarydict[i] = attr
   if i == checki:
      prevnode = i
   i += 1
   for node in nodeyirank:
      attr = {}
      attr['left'] = None
      attr['right'] = None
      attr['up'] = None
      attr['down'] = None
      ypos = nodes[node]['position'][1]
      attr['position'] = (xboundary,ypos)
      attr['down'] = prevnode
      boundarydict[prevnode]['up'] = i
      boundarydictrev[(xboundary,ypos)] = i
      boundarydict[i] = attr
      prevnode = i
      i += 1
   attr = {}
   attr['left'] = None
   attr['right'] = None
   attr['up'] = None
   attr['down'] = None
   ypos = dimy
   attr['position'] = (xboundary, ypos)
   attr['down'] = prevnode
   boundarydictrev[(xboundary,ypos)] = i
   boundarydict[i] = attr
   i += 1
   checki = i
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
         check, nnode crosslist = checkcross(True, node,
                                             crossingnodes, True)
   
         crosslistdict = checkneighbornode(crosslist, crossingnodes,
                                           direction)
   crossval = nodes[node]['up']
   if crossval:
      
#construct faces and vertices from nodes
for node in nodes:
    
