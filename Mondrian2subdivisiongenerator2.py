#Mondrian like subdivision generator 2
## Different approach relative the first generator.  In this case, using
## an ordering based approach as described in the wiki.
global dimx
global dimy
dimx = 1000
dimy = 1300
totalnodes = 10
meshName = "Mondrian"
obName = "MondrianObj"
##me = bpy.data.meshes.new(meshName)
##ob = bpy.data.objects.new(obName, me)
##ob.location = bpy.context.scene.cursor_location
##bpy.context.scene.objects.link(ob)
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
   attr['child1'] = None
   attr['childq1'] = None
   attr['child2'] = None
   attr['childq2'] = None
   attr['child3'] = None
   attr['childq3'] = None
   attr['child4'] = None
   attr['childq4'] = None
   attr['parent'] = None
   attr['parentquadrant'] = None
   randomxlist.append(randposx)
   randomylist.append(randposy)
   nodes[i+1] = attr
   nodepostoi[(randposx,randposy)] = i+1
nodeposlist = list(nodepostoi.keys())   

## each parent has 4 quadrant branches given by a min max position set
## and a child index branch
## processing node precedent
##  Need fast position indexing tree lookup and assignment
## poslookuptree -> ['index'] and poslookuptree -> ['postree']
def findparent(nodepos, poslookuptree, minmaxcordlist):
    ## using a minpos, maxpos tuple coordinate identifier
    parenti = None
    nodeposx, nodeposy = nodepos
    i = 0
    for minmaxpositions in poslookuptree:
        minpos, maxpos = minmaxpositions
        minx, miny = minpos
        maxx, maxy = maxpos
        t1 = nodeposx >= minx
        t2 = nodeposx <= maxx
        t3 = nodeposy >= miny
        t4 = nodeposy <= maxy
        if t1 and t2 and t3 and t4:
            if poslookuptree[minmaxpositions]['postree'] != None:
                minmaxcordlist.append(minmaxpositions)
                poslookupt = poslookuptree[minmaxpositions]['postree']
                parenti, i, minmaxcoordlist = findparent(nodepos, poslookupt,
                                                         minmaxcordlist)
            else:
                parenti = poslookuptree[minmaxpositions]['index']
                return parenti, i, minmaxcoordlist
        i += 1
    return parenti, i, minmaxcoordlist

def setparent(nodepos, poslookuptree, minmaxcoordlist):
    if len(minmaxcoordlist) > 1:
        mmcoord = minmaxcoordlist[0]
        del minmaxcoordlist[0]
        poslookuptree2 = poslookuptree[mmcoord]['postree']
        setparent(nodepos,poslookuptree2, minmaxcoordlist)
    else:
        mmcoord = minmaxcoordlist[0]
        nodeposx, nodeposy = nodepos
        minpos, maxpos = mmcoord
        minx, miny = minpos
        maxx, maxy = maxpos
        q1minpos = (minx, nodeposy)
        q1maxpos = (nodeposx, maxy)
        q2minpos = nodepos
        q2maxpos = maxpos
        q3minpos = minpos
        q3maxpos = nodepos
        q4minpos = (nodeposx, miny)
        q4maxpos = (maxx, nodeposy)
        q1coord = (q1minpos,q1maxpos)
        q2coord = (q2minpos,q2maxpos)
        q3coord = (q3minpos,q3maxpos)
        q4coord = (q4minpos,q4maxpos)
        qlist = [q1coord,q2coord,q3coord,q4coord]
        attr = {}
        attr['index'] = None
        attr['postree'] = None
        ptreedict = poslookuptree[mmcoord]['postree']
        for q in qlist:
            ptreedict[q] = attr
##  poslookuptree
poslookuptree = {}
for nodepos in nodeposlist:
    attr = {}
    attr['child']

