import random
import math
## Another random polygon generator.  Experimenting with the use of elliptic
## forms here, but because of polar angle deacceleration on the ellipse
## with increasing angle in this code use, equal angle subdivision
## only leads with high orders of n for the n gon curve approximation
## versus linear form at the outset...
## Instead I've left open a Force circle restriction which is e =0 or a=b
## case of the ellipse (a circle).  The circle doesn't provision velocity
## change in traversing with equal angle step subdivisions, and thus yields
## 'purer' geometric forms of lesser order (relative the circle) n gon
## types.

##  Instead to make use of a more elliptic form of such n gon geometry
## with the controls found in step subdivision with circles, I've opted
## to rescale the data set which works well relative to finding the
## direct solution to such problem.  
AxisSizeMinMax = (.1,10)
MaxPolygonEdges = (3,15)
Anglediv = (0,180)
Randomstepsubdiv = False
ForceCircle = True
RandomYScaling = False
RandomXScaling = True
UseMaximumAngle = True
def getfocus(a, e):
    ## where a is the major axis length
    ## e is the eccentricity of the ellipse
    return a*e

def gete(a,b):
    ## where a is the major axis and b is the semi major axis lengths
    return (1-(b/a)**2.0)**.5

def getEllipsePosition(theta, a, e, f):
    r = a*(1-e**2.0)/(1-e*math.cos(theta))
    xr = r*math.cos(theta)
    yr = r*math.sin(theta)
    fx,fy = f
    return (fx+xr, fy+yr)

mins,maxs = AxisSizeMinMax
a1 = random.uniform(mins,maxs)
a2 = random.uniform(mins,maxs)
minedgs, maxedgs = MaxPolygonEdges
minangle, maxangle = Anglediv
a = max(a1,a2)
b = min(a1,a2)
if ForceCircle:
    b = a

eangles = []
## pick number of edges
edgenumber = random.randint(minedgs,maxedgs)
even = edgenumber % 2 == 0
edgediv = None
if not even:
    eangles.append(0.0)
    edgenumber -= 1
    edgediv = edgenumber/2
else:
    edgediv = edgenumber/2

angle1 = random.randint(minangle,maxangle)
angle2 = random.randint(minangle,maxangle)
while angle1 == angle2:
    angle2 = random.randint(minangle,maxangle)
minangle = min(angle1,angle2)
maxangle = max(angle1,angle2)
if UseMaximumAngle:
    minangle = 0.0
    maxangle = 180.0

## subdivide the the min max angle interval by edge div
angleinterval = maxangle - minangle
angleistep = angleinterval/edgediv
## now we make randomly irregular subdivision step
anglesteps = []
prev = 0.0
print('edgediv: ', edgediv)
for i in range(0,int(edgediv)):
    if Randomstepsubdiv:
        astep = random.uniform(prev,(i+1)*angleistep)
    else:
        astep = (i+1)*angleistep
    prev = astep
    anglesteps.append(astep)

print(anglesteps)

for astep in anglesteps:
    ai = anglesteps.index(astep)
    astep += minangle
    anglesteps[ai] = astep

print(anglesteps)

eangles += anglesteps
## get eccentricity
e = gete(a,b)
f = getfocus(a, e)
f = (-f,0.0)
positivepos = []
negativepos = []
for theta in eangles:
    theta = theta *math.pi/180.0
    x, y = getEllipsePosition(theta, a, e, f)
    positivepos.append((x,y,0.0))
    x, y = getEllipsePosition(-theta, a, e, f)
    negativepos.append((x,y,0.0))

negativepos = negativepos[::-1]
positions = positivepos
for pos in negativepos:
    if not pos in positivepos:
        positions.append(pos)

print(positions)
faces = []
face = []
i = 0
for pos in positions:
    face.append(i)
    i += 1
faces.append(tuple(face))
randx = 1.0
randy = 1.0
if RandomXScaling:
    randx = random.random()
if RandomYScaling:
    randy = random.random()
if RandomXScaling or RandomYScaling:
    i = 0
    for pos in positions:
        x,y,z = pos
        x *= randx
        y *= randy
        positions[i] = (x,y,z)
        i+=1 
meshName = "Polygon"
obName = "PolygonObj"
me = bpy.data.meshes.new(meshName)
ob = bpy.data.objects.new(obName, me)
ob.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(ob)
me.from_pydata(positions,[],faces)      
me.update(calc_edges=True) 
