import math
import bpy

def slope(edge):
    a, b = edge
    ax,ay = a
    bx,by = b
    return (by - ay)/(bx - ax)

def distance(a,b):
    ax,ay = a
    bx,by = b
    return (abs((ax-bx)**2)+abs((ay-by)**2))**.5

def slopenormal(edgeslope):
    if edgeslope == 0:
        return 9e20
    return - 1/edgeslope

def norm(vec):
    ##2d norm
    vx, vy = vec
    d = (abs(vx**2)+abs(vy**2))**.5
    vx = vx/d
    vy = vy/d
    return [vx,vy]

def scalemultvec(scalar,vec):
    vx,vy = vec
    return [scalar*vx,scalar*vy]

def ltolintersect(line1,line2):
    ## line is given of the form (a,c) for instance,
    ## where y = ax + c is the form of the line equation
    a,c = line1
    b,d = line2
    return ((d-c)/(a-b),(a*d-b*c)/(a-b))

def getLine(slope,point):
    x1,y1 = point
    return (slope, y1-slope*x1)

def midpoint(edge):
    a,b = edge
    return ((a[0]+b[0])/2.0,(a[1]+b[1])/2.0)

def addvecs(vec1,vec2):
    vx1,vy1 = vec1
    vx2,vy2 = vec2
    return [vx1+vx2,vy1+vy2]

def v1equalv2(v1,v2):
    v1x,v1y = v1
    v2x,v2y = v2
    if v1x == v2x and v1y == v2y:
        return True
    else:
        return False

def computeNodePairLine(C1,C2,NodePairLine):
    ## always keyed (c1,c2)
    ## C1 and C2 keyed with tuple (nodeindex,(center,radius))
    ## for circle packing center is in complex coordinates
    ## It is important to know that CirclePacks are approximation
    ## according to the numerical methods used for CirclePack
    ## meaning that Circle may not be perfectly and exactly tangent
    ## in relation to one another.  This means that we may need to find
    ## medians where tangency is not completely a given.
    ## This means that we find the tangent point on each of the circle
    ## relative to its provided radius and test both points for position
    ## equality where either point is furnished by vectors running
    ## from one circle center to other.  If they are equal then both
    ## circles are completely tangent and generally we are nearly done
    ## computing the dual graph line (we just compute the normal slope
    ## of such line between circle centers) and use our provided tangent
    ## point in determining the line.  Otherwise, we'd need to find the
    ## the median between either tangent point on either circle, and
    ## then similarly compute the inverse negative (or normal slope) of
    ## of the original line between circle centers.
    c1node, cpackc1 = C1
    c2node, cpackc2 = C2
    ##print('C1: ', C1)
    ##print('C2: ', C2)
    center1, radius1 = cpackc1
    cx1 = float(center1.real)
    cy1 = float(center1.imag)
    c1 = [cx1,cy1]
    ##print('c1: ', c1)
    center2, radius2 = cpackc2
    cx2 = float(center2.real)
    cy2 = float(center2.imag)
    c2 = [cx2,cy2]
    ##print('c2: ', c2)
    ## two opposite vectors c1-c2 and c2-c1
    v1 = [cx1-cx2,cy1-cy2]  ## in the direction of c1 from c2
    v2 = [cx2-cx1,cy2-cy1]  ## in the direction of c2 from c1
    ##print('v1: ', v1)
    ##print('v2: ', v2)
    v1 = norm(v1) 
    v2 = norm(v2)
    v1 = scalemultvec(radius2,v1) ## tangent point on c2 almost, right length
    ## right direction, but vector not at the right origin
    v2 = scalemultvec(radius1,v2) ## tangent point on c1 almost
    ## translate vectors to their respective points of origin
    v1 = addvecs(v1,c2)
    v2 = addvecs(v2,c1)
    if v1equalv2(v1,v2):
        edge = (v1,c2)
        m = slope(edge)
        m = slopenormal(m)
        line = getLine(m,v1)
        NodePairLine[(c1node,c2node)] = line
    else:
        edge = (v1,v2)
        mpoint = midpoint(edge)
        edge = (mpoint,c1)
        m = slope(edge)
        m = slopenormal(m)
        line = getLine(m,mpoint)
        NodePairLine[(c1node,c2node)] = line
    
NodePairLine = {}
TripleIntersect = {}
vertices = []
faces = []

## A circle pack alongside a given Complex is needed here

def gDualGraphN(Cpack,Complex,Root, NodePairLine, TripleIntersect,
                vertices, faces):
    ## Root is the root node in which to generate dual graph
    ## nodes.
    ## Root nodes should only be 'interior' node from such Complex.
    ## Complex should be in the form of corresponding Complex node keys,
    ## irrespective of interior, exterior designations, with all nodes
    ## having walk (cycle) neighbors indicated.
    ## On Complex dictionary cycle walk for a root node is keyed
    ## 'neighbors' with a list set.
    ## Cpack should have the same corresponding node labels as Complex.
    ## NodePairLine is a tracking dictionary to reduce computation load
    ## by tracking what has already previously been computed.
    ## TripleIntersect is a two level dictionary set.  One level
    ## is given by a double node pair followed by a triple third key
    ## which is valued to the intersect vertex index (for the dual graph).
    ## This is for tracking and to avoid adding duplicate vertices.
    ## This is done by computation of double line intersections
    ## where double lines are generated from tangency point computations
    ## between each neighboring node to root and the neighboring node to
    ## neighboring node.  These intersections form the dual graph vertices.
    ## All of these vertices together in a walk computation around the root
    ## node form the face of the Dual Graph of a root node.  
    neighbors = Complex[Root]['neighbors']
    face = []
    for index, neighbor in enumerate(neighbors):

        nneighbor = None
        nindex = None
        if index == len(neighbors)-1:
            nindex = 0
            nneighbor = neighbors[0]
        else:
            nindex = index+1
            nneighbor = neighbors[nindex]
        ## first we check to see that a given node triple
        ## has not already a computed intersect vertex.
        p1 = (neighbor,nneighbor)
        p2 = (nneighbor,neighbor)
        u1 = (neighbor,nneighbor) in TripleIntersect
        u2 = (nneighbor,neighbor) in TripleIntersect
        u3 = None
        if u1:
            if Root in TripleIntersect[p1]:
                u3 = TripleIntersect[p1][Root]
        if u2:
            if Root in TripleIntersect[p2]:
                u3 = TripleIntersect[p2][Root]
        if u3 == None:
            t1 = (Root,neighbor) in NodePairLine
            t2 = (neighbor,Root) in NodePairLine        
            t3 = (Root,nneighbor) in NodePairLine
            t4 = (nneighbor,Root) in NodePairLine

            if not t1 and not t2:
                ## compute NodePairLine and store
                C1 = (Root,Cpack[Root])
                C2 = (neighbor,Cpack[neighbor])
                computeNodePairLine(C1,C2,NodePairLine)
            if not t3 and not t4:
                ## compute NodePairLine and store
                C1 = (Root,Cpack[Root])
                C2 = (nneighbor,Cpack[nneighbor])
                computeNodePairLine(C1,C2,NodePairLine)
            line1 = None
            line2 = None
            if t2:
                line1 = NodePairLine[(neighbor,Root)]
            else:
                line1 = NodePairLine[(Root,neighbor)]
            if t4:
                line2 = NodePairLine[(nneighbor,Root)]
            else:
                line2 = NodePairLine[(Root,nneighbor)]
            triplepoint = ltolintersect(line1,line2)
            vertices.append(triplepoint)
            tindex = len(vertices)-1
            face.append(tindex)
            TripleIntersect[(Root,neighbor)] = {nneighbor:tindex}
            TripleIntersect[(Root,nneighbor)] = {neighbor:tindex}
        else:
            face.append(u3)
    faces.append(face)

def generateDualGraph(pack,CPack, NodePairLine,
                      TripleIntersect, vertices, faces):
    ## pack is interior,exterior,and full complex tuple dictionary package
    interior,exterior,Complex = pack
    for node in interior:
        gDualGraphN(CPack,Complex,node, NodePairLine, TripleIntersect,
                vertices, faces)
    verticesc = []
    for vert in vertices:
        vx,vy = vert
        verticesc.append((vx,vy,0.0))
    vertices = verticesc
    meshName = "CirclePackingDualGraph"
    obName = "CirclePackingDualGraphObj"
    me = bpy.data.meshes.new(meshName)
    ob = bpy.data.objects.new(obName, me)
    ob.location = bpy.context.scene.cursor_location
    bpy.context.scene.objects.link(ob)
    me.from_pydata(vertices,[],faces)      
    me.update(calc_edges=True)

generateDualGraph(packs[0],cpack,NodePairLine,
                  TripleIntersect, vertices, faces)

