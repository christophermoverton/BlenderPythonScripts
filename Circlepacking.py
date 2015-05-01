
## What is the Apollonius Problem.  Basically for three circles we are
## looking to find the circle x,y,r that is tangent to all three circles
##simultaneously.  This applies as a completion to this algorithim.

##we are looking for min r I believe in this solution.
## 

##obtained from http://rosettacode.org/wiki/Problem_of_Apollonius
from collections import namedtuple
import math
import random
 
Circle = namedtuple('Circle', 'x, y, r')

def solveApollonius(c1, c2, c3, s1, s2, s3):
    '''
    >>> solveApollonius((0, 0, 1), (4, 0, 1), (2, 4, 2), 1,1,1)
    Circle(x=2.0, y=2.1, r=3.9)
    >>> solveApollonius((0, 0, 1), (4, 0, 1), (2, 4, 2), -1,-1,-1)
    Circle(x=2.0, y=0.8333333333333333, r=1.1666666666666667) 
    '''
    x1, y1, r1 = c1
    x2, y2, r2 = c2
    x3, y3, r3 = c3
 
    v11 = 2*x2 - 2*x1
    v12 = 2*y2 - 2*y1
    v13 = x1*x1 - x2*x2 + y1*y1 - y2*y2 - r1*r1 + r2*r2
    v14 = 2*s2*r2 - 2*s1*r1
 
    v21 = 2*x3 - 2*x2
    v22 = 2*y3 - 2*y2
    v23 = x2*x2 - x3*x3 + y2*y2 - y3*y3 - r2*r2 + r3*r3
    v24 = 2*s3*r3 - 2*s2*r2
 
    w12 = v12/v11
    w13 = v13/v11
    w14 = v14/v11
 
    w22 = v22/v21-w12
    w23 = v23/v21-w13
    w24 = v24/v21-w14
 
    P = -w23/w22
    Q = w24/w22
    M = -w12*P-w13
    N = w14 - w12*Q
 
    a = N*N + Q*Q - 1
    b = 2*M*N - 2*N*x1 + 2*P*Q - 2*Q*y1 + 2*s1*r1
    c = x1*x1 + M*M - 2*M*x1 + P*P + y1*y1 - 2*P*y1 - r1*r1
 
    # Find a root of a quadratic equation. This requires the circle centers not to be e.g. colinear
    D = b*b-4*a*c
    rs = (-b-math.sqrt(D))/(2*a)
 
    xs = M+N*rs
    ys = P+Q*rs
 
    return Circle(xs, ys, rs)
 

c1, c2, c3 = Circle(0.0, 0.0, 1.0), Circle(4.0, 0.0, 1.0), Circle(2.0, 4.0, 2.0)
print(solveApollonius(c1, c2, c3, 1, 1, 1))    #Expects "Circle[x=2.00,y=2.10,r=3.90]" (green circle in image)
print(solveApollonius(c1, c2, c3, -1, -1, -1)) #Expects "Circle[x=2.00,y=0.83,r=1.17]" (red circle in image)

def solveTwoTangentC(c1,c2, phi):
##     Where tangent circles C, C1, and C2 are exterior relative to one another
##     and C having origin O((r1+r) cos phi
##    , (r1+r) sin phi), C1 origin (0,0) and C2 origin (r1+r2,0)
##     and phi is the angle subtended from C1C2 to C1C then
##     r = 2r1r2/(r2-r1(r2+r1)cos phi)-r1 .
    x1,y1,r1 = c1
    x2,y2,r2 = c2
    r = (2*r1*r2)/(r2-r1*(r2+r1)*math.cos(phi))-r1
    x = (r1+r)*math.cos(phi)
    y = (r1+r)*math.sin(phi)

    return Circle(x,y,r)

def solveSingleTangentC(c1,phi,r):
    x1,y1,r1 = c1
    x = (r1+r)*math.cos(phi)
    y = (r1+r)*math.sin(phi)
    return Circle(x,y,r)

##  For a randomly assigned angle phi, a tangent circle is constructed
## by the following criteria:
##If all neighboring tangent circles are within 60 degrees of a new
## randomly assigned angle phi, then such tangent circles are considered
##neighboring and relating angles subtending from the base of the parent(primary)
## circle).  If there exist more than two neighboring angles less than 45
## degrees, we choose the minimum closest neighbors of all such angles such
## that a set of two closest neighboring angles suffice.  In this case, phi,
## is discarded in terms of setting the new tangent circle, but both
##minimum neighboring tangent circles are used in determining the next (using
## the Apollonius method).
## If phi finds no neighboring angle in proximity, then it is called solitary,
## and its tangent is solved using solveSingleTangent.
## If there exists only one neighbor to phi, then the solveTwoTangentC
## method is used.

##Further important definitions:
##  A primary(parent) circle for packing construction is filled (done)
##  when one of two conditions have sufficed.  One either the maximum
## allotment of tangent circles have been packed around it, or the set of
## partial arc closures contains the parent tangent circle itself.
## A partial closure of the circle occurs when a randomly
## assign a arc angle parameter to each circle in this case is exceeed.
## A Tangent circle is always assigned a fixed subarc mapping where any
## subtended angle (and corresponding neighboring tangent circle) are
## placed inside any such subarc coordinate.  No  more than 1 tangent
## circle can reside in such subarc coordinate, and when such has occured,
## the sub arc is described as closed.
## A partial subarc may be given, for instance,
## randomly as a parameter ranging from 3 degrees to 10 degrees.
##  Closing a subarc either by reaching a minimum density angle, or
## that minimum tangent circle size is exceeding to the solution
## of tangent circles for a given subtending phi.  Minimum tangent circle
## size may be fixed globally or assigned randomly within desired range
## locally to a parent. An iterated test on the arc boundaries may
## be set in place in closing a subarc.  This is done in minimum size
## testing, so that for instance, if on the neighboring subarc, the solution
## at the next subarc sequence yields a tangent circle less than
## a minimum tangent circle requirement, then such subarc is defined as closed.
## An iterated process of testing is complete until finding that on a given
## neighboring subarc boundary that relative an original tangent boundary,
## to a given directional subarc maximum one finds a subtending angle
## that produces a sufficiently large enough tangent.

## A maximum allotment of tangent circles will be described as the maximum
## possible tangent circles assigned to a primary parent circle.
## Packing density of the primary parent has been described above.  Closure
## results when 360/pdensity arc segments have reached maximum density.


##Packing method for random assignments:
##  Initialize the Graph with a parent circle randomly assigned to a given
##  size within desired specification.  The coordinate value of this circle
## will be fixed at origin (dimx/2,dimy/2) for now.
## A Queue system Q may be constructed for packing where any new tangent circle
## is added to the Q and any finished packing on a Q circle is discarded from
## the list (by criteria indicated above).
## Construction stops in the Q when the graph of desired tangent circle node
## has filled (overlapped a construction fill area), or potentitally a node
## quota can terminate any further work done on the node.
## That is the first condition states that once we can no longer add new
## tangent circles and we have exhausted from the queue all existing tangent
## circles, then the algorithm is complete, or we have reached a desired
##graph quota and the algorithm terminates.

## This leads to one final rule graph boundaries rule.  Namely that a subarc is
## closed when the tangent point extends outside of a boundary range.  Note:
## however new tangent circles can extend outside of a given graph boundary
## range, but a contact tangent point between circles cannot.

##variables
Mincirclesize = .25
global Minphirange
Minphirange = (math.pi/360.0*3.0, math.pi/360.0*10.0)
Minneighborphi = math.pi/360.0*60.0
Minappolloniusphi = math.pi/360.0*45.0
Rcirclesize = (.25, 10.0) ## use random.uniform()
Maxcircles = 10000
Tangents = (2,6)

dimx = 50.0
dimy = 50.0
Circles = {}
Q = []
## initialize the parent
attr = {}
rcsizex, rcsizey = Rcirclesize
pradius = random.uniform(rcsizex,rcsizey)
pcircle = (dimx/2.0,dimy/2, pradius)
attr['neighbors'] = {}
attr['faces'] = None
minmphi,maxmphi = Minphirange
attr['minphi'] = random.uniform(minmphi,maxmphi)
attr['subarcs'] = None
attr['subarcsord'] = None  ##ordered subarcs list
attr['closures'] = None
attr['circle'] = pcircle
attr['tangents'] = random.randint(Tangents[0],Tangents[1])
Circles[pcircle] = attr
Q.append(Circles[pcircle])

def binarysearch(phi, btree):
    for val in btree:
        circle, angle = val
        if phi > angle:
            if type(btree[val]['u']) == dict:
                return binarysearch(phi, btree[val]['u'])
            else:
                return btree[val]['u']
        else:
            if btree[val]['l'] == dict:
                return binarysearch(phi, btree[val]['l'])
            else:
                return btree[val]['l']

def addbinary(circle, phi, btree):
    for val in btree:
        circle, angle = val
        if phi > angle:
            if type(btree[val]['u']) == dict:
                addbinary(circle, phi, btree[val]['u'])
            else:
                c2,angle2 = btree[val]['u']
                if phi > angle2:
                    newtree = {}
                    newtree['u'] = (circle,phi)
                    newtree['l'] = btree[val]['u']
                    attr = {}
                    attr[(circle,phi)] = newtree
                    btree[val]['u'] = attr
                else:
                    newtree = {}
                    newtree['l'] = (circle,phi)
                    newtree['u'] = btree[val]['u']
                    attr = {}
                    attr[(circle,phi)] = newtree
                    btree[val]['u'] = attr                    
        else:
            if type(btree[val]['l']) == dict:
                addbinary(circle, phi, btree[val]['l'])
            else:
                c2,angle2 = btree[val]['l']
                if phi > angle2:
                    newtree = {}
                    newtree['u'] = (circle,phi)
                    newtree['l'] = btree[val]['l']
                    attr = {}
                    attr[(circle,phi)] = newtree
                    btree[val]['l'] = attr
                else:
                    newtree = {}
                    newtree['l'] = (circle,phi)
                    newtree['u'] = btree[val]['u']
                    attr = {}
                    attr[(circle,phi)] = newtree
                    btree[val]['l'] = attr

def getbinarytreevals(vals, btree):
    for val in btree:
        circle, angle = val
        for bound in btree[val]:
            if type(btree[val][bound]) == dict:
                return getbinarytreevals(phi, btree[val]['u'])
            else:
                if not btree[val][bound] in vals:
                    vals.append(btree[val][bound])

def getinitbinarytree(cphi):
    newtree = {}
    newtree['u'] = cphi
    newtree['l'] = cphi
    attr = {}
    attr[cphi] = newtree
    return attr

def addTangentNPrimary(c1, cphi2, Circles, subarc, nsarc
                       subarc2 = None):
    c2, phi2 = cphi2
    ## add neighbor
    c1dict = Circles[c1]
    neighbors = c1dict['neighbors']  
    neighbors[c2] = {'angle':phi2}
    subarcs = c1dict['subarcs']
    subarcsord = c1dict['subarcsord']
    ##if subarc in c1dict['subarcs']:
    ## Conditions for subarcs:
    ## subarc2 not none means we are joining subarc to subarc2
    ## this occurs with Apollonius condition positive or
    ## Apollonius test failure.  Otherwise subarc2 None means
    ## we are adding a distinct subarc.
    ## nsarc is the neighboring subarc given upper bound
    if subarc2 == None:
        subarcs[subarc] = getinitbinarytree(cphi2)
        if nsarc = None:
            subarcsord.append(subarc)
        else:
            nindex = subarcsord.index(nsarc)
            subarcsord.insert(nindex, subarc)    
        

While len(Q) != 0 or len(Circles) >= Maxcircles:
    ##pick Q[0]
    circledict = Q[0]
    ## pick random phi
    subarcs = circledict['subarcsord']
    subarcsord = circledict['subarcsord']
    neighbors = circledict['Neighbors']
    while len(neighbors) < circledict['tangents']:
        rphi = None
        if subarcs == None:
            rphi = random.uniform(0,2*math.pi)
            pradius = random.uniform(rcsizex,rcsizey)
            solveSingleTangentC(c1,phi,r)
        else:
            ##pick random filled subarc
            rsubarci = random.randint(0,len(subarcsord)-1)
            rsubarc = subarcsord[rsubarci]
            ##pick a direction clockwise or counterclockwise
            rsarcdir = random.uniform(0,1)
            if rsarcdir < .5:
                rsarcdir = -1
            else:
                rsarcdir = 1
            nrsubarc = None
            if rsubarci+rsarcdir > len(subarcsord)-1:
                nrsubarc = rsubarcord[0]
            elif rsubarci+rsarcdir < 0:
                nrsubarc = rsubarcord[len(rsubarcord)-1]
            else:
                nrsubarc = subarcsord[rsubarci+rsarcdir]
            ## find min max arcboundaries
            if rsarcdir == 1:
                ## rsubarc right nrsubarc left
                minarc = rsubarc[1]
                maxarc = nrsubarc[0]
                if maxarc < minarc:
                    maxarc = 2*math.pi + maxarc
            else:
                minarc = nrsubarc[1]
                maxarc = rsubarc[0]
                if maxarc < minarc:
                    maxarc = 2*math.pi + maxarc
            rphi = random.randint(minarc,maxarc)
            if rphi > 2*math.pi:
                rphi = rphi - 2*math.pi
            ##get nearest left right neighbors
            uppertree = subarcs[maxarc]
            lowertree = subarcs[minarc]
            nucircle, nuphi = binarysearch(rphi, uppertree)
            nlcircle, nlphi = binarysearch(rphi, lowertree)
