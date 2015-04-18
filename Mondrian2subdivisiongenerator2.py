#Mondrian like subdivision generator 2
## Different approach relative the first generator.  In this case, using
## an ordering based approach as described in the wiki.
import bpy
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
def getrand(minv, maxv, randlist):
   val = random.randint(minv,maxv)
   if val not in randlist:
      return val
   else:
      return getrand(minv,maxv,randlist)
nodes = {}
nodepostoi = {}
randomxlist = []
randomylist = []   
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
def findparent(nodepos, poslookuptree, minmaxcoordlist):
    ## using a minpos, maxpos tuple coordinate identifier
    parenti = None
    nodeposx, nodeposy = nodepos
    print('nodepos: ', nodepos)
    i = 0
    for minmaxpositions in poslookuptree:
        minpos, maxpos = minmaxpositions
        minx, miny = minpos
        maxx, maxy = maxpos
        print('minmaxpositions: ', minmaxpositions)
        t1 = nodeposx >= minx
        t2 = nodeposx <= maxx
        t3 = nodeposy >= miny
        t4 = nodeposy <= maxy
        if t1 and t2 and t3 and t4:
            if poslookuptree[minmaxpositions]['postree'] != None:
                minmaxcoordlist.append(minmaxpositions)
                poslookupt = poslookuptree[minmaxpositions]['postree']
                
                parenti, i, minmaxcoordlist = findparent(nodepos, poslookupt,
                                                         minmaxcoordlist)
                return parenti, i, minmaxcoordlist
            else:
                parenti = poslookuptree[minmaxpositions]['index']
                i = poslookuptree[minmaxpositions]['quadrant']
                minmaxcoordlist.append(minmaxpositions)
                return parenti, i, minmaxcoordlist
        ##i += 1
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
        attr['quadrant'] = None
        ptreedict = {}
        i = 0
        for q in qlist:
            attr['quadrant'] = i
            ptreedict[q] = attr.copy()
            i += 1
        poslookuptree[mmcoord]['postree'] = ptreedict
##  poslookuptree is a quaternary search tree 
poslookuptree = {}
##initialize the position lookup tree
nodepos = nodeposlist[0]
nodeposx, nodeposy = nodeposlist[0]
minpos, maxpos = [(0,0),(dimx,dimy)]
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
attr['quadrant'] = None
ptreedict = {}##poslookuptree[mmcoord]['postree']
i = 0
for q in qlist:
    attr['quadrant'] = i
    ptreedict[q] = attr.copy()
    i += 1
    
nodeposlistc = nodeposlist[0:len(nodeposlist)]
del nodeposlistc[0]
## finish quaternary subdivision assignments
for nodepos in nodeposlistc:
    minmaxcoordlist = []
    parent, quad, minmaxcoordlist = findparent(nodepos, ptreedict,
                                               minmaxcoordlist)
    print('minmaxcoordlist', minmaxcoordlist)
    minmaxcoordlistc = minmaxcoordlist[0:len(minmaxcoordlist)]
    setparent(nodepos, ptreedict, minmaxcoordlistc)

##  if 'postree' node is None then we record the vertices of the quadrant
##  we use the quadrant minmax position to construct the 4 vertices to a face
##  we also append these if not in the list of vertices to a vertex list
##  making note of the position of the vertex in the list we use a vertex
##  position to index mapping, or we can do this all at once in the
##  the read the tree algorithm

##  Will need a quaternary recursive search algorithm that reads the entire
## subdivison tree.
def buildvertsfaces(ptreedict, vertices, faces):
    for minmaxpositions in ptreedict:
        if ptreedict[minmaxpositions]['postree'] == None:
            minpos, maxpos = minmaxpositions
            minpostup = (float(minpos[0])/dimy,float(minpos[1])/dimy,0.0)
            maxpostup = (float(maxpos[0])/dimy,float(maxpos[1])/dimy,0.0)
            minposindex = None
            maxposindex = None
            pos3index = None
            pos2index = None
            if minpostup in vertices:
                minposindex = vertices.index(minpostup)
            else:
                vertices.append(minpostup)
                minposindex = len(vertices)-1
            if maxpostup in vertices:
                maxposindex = vertices.index(maxpostup)
            else:
                vertices.append(maxpostup)
                maxposindex = len(vertices)-1
            pos2 = (float(minpos[0])/dimy,float(maxpos[1])/dimy,0.0)
            pos3 = (float(maxpos[0])/dimy,float(minpos[1])/dimy,0.0)
            if pos2 in vertices:
                pos2index = vertices.index(pos2)
            else:
                vertices.append(pos2)
                pos2index = len(vertices)-1
            if pos3 in vertices:
                pos3index = vertices.index(pos3)
            else:
                vertices.append(pos3)
                pos3index = len(vertices)-1
            face = (minposindex, pos2index, maxposindex, pos3index)
            faces.append(face)
        else:
            ptreedict2 = ptreedict[minmaxpositions]['postree']
            buildvertsfaces(ptreedict2,vertices,faces)
            
## build vertices and faces
vertices = []
faces = []
buildvertsfaces(ptreedict, vertices, faces)
        
me.from_pydata(vertices,[],faces)      
me.update(calc_edges=True)   
