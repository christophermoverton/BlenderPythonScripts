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
for node in nodes:
    yrank = nodeyirank.index(node)
    posx = nodes[node]['position'][0]
    copynranks = nodeyirank[0:len(nodeyirank)]
    del copynranks[yrank]
    for cr in range(0,totalnodes-1):
        attr = {}
        nodeval = yrank*10+copynranks[cr]
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
                nodevald = yrank*10 + nodeyirank[crnodepos-1]
        attr['down'] = nodevald
        nodevald = None
        if crnodepos < len(nodeyirank)-1:
            if nodeyirank[crnodepos+1] == yrank:
                nodevald = yrank
                nodes[yrank]['down'] = copynranks[cr]
            else:
                nodevald = yrank*10 + nodeyirank[crnodepos+1]
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
#construct faces and vertices from nodes
for node in nodes:
    
