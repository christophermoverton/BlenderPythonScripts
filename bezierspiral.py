import bpy
from bpy_extras.io_utils import unpack_list
import math
import mathutils

points = []
num_Points = 100
nPoints_Cycle = 7
rinc = 2*math.pi/nPoints_Cycle
radian = 0.0
radius = 0.0

for i in range(num_Points):
    a = mathutils.Vector([1.0, 0.0, 0.0])
    b = mathutils.Vector([0.0,0.0,1.0])
    c = mathutils.Quaternion(b,radian)
    d = c*a
    d *= radius
    radian += rinc
    radius = radian
    point = [d.x, d.y, d.z]
    points.append(point)
print(points)
curvedata = bpy.data.curves.new(name="Curve", type='CURVE')
ob = bpy.data.objects.new("CurveObj", curvedata)
bpy.context.scene.objects.link(ob)

##spline = curvedata.splines.new('BEZIER')

polyline = curvedata.splines.new('BEZIER')
polyline.bezier_points.add(len(points)-1)
polyline.bezier_points.foreach_set("co", unpack_list(points))
print(len(spline.bezier_points))