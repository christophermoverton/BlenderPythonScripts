import bpy
from bpy import context
import math
import random

## run SelectionVertices.py script prior to running this in console

def gravity(z,vi,t):
   ## t is time since tinitial
   return .5*-9.8*t*t + vi*t + z

def solvet(z, vi):
   a = -9.8*.5
   b = vi
   c = z
   if (b*b -4.0*a*c) < 0:
      t1 = None
      t2 = None
   else:
      t1 = b+math.sqrt((b*b -4.0*a*c))
      t2 = b-math.sqrt((b*b -4.0*a*c))
   if t1 > 0:
      return t1
   if t2 > 0:
      return t2
   return None
   
def solveh(vi,t):
   return .5*9.8*t*t - vi*t
numFallingObjs = 5
fobj_list = []
vi = -9.8
tf = 7.0 ## in frames 30 sec  per frame is the standard so 1 frame equals 1/30.0 seconds

tfs = 7.0/30.0
## read vertex data on terrain
vdat = {}
objname = "Land"
obj = bpy.data.objects[objname]
## populate object names 
for i in range(0,numFallingObjs):
   fobj_list.append("D"+str(i))


for v in obj.data.vertices:
   x,y,z = obj.matrix_world*v.co
   if (x,y) in vdat:
   
      vdat[(x,y)] = max(vdat[(x,y)],z)
   else:
      vdat[(x,y)] = z

selvertices2 = selvertices[0:len(selvertices)]
framedat = []
coorddat = []
for i in range(0,numFallingObjs):
   vpick = random.randint(0,len(selvertices2))
   x,y,z = selvertices2[vpick] 
   tf1 = float(tf) + float(random.randint(0,5))
   tfs1 = tf1/30.0
   h = solveh(vi,tfs1)
   newz = vdat[(x,y)]+h
   framedat.append(tfs1)
   coorddat.append((x,y,newz))
   del selvertices2[vpick]
   
bpy.ops.object.mode_set(mode='OBJECT')
bpy.data.objects['Land'].select = False
for i, co in enumerate(coorddat):
   bpy.context.scene.objects.active = bpy.data.objects['W_rfe203']  ##obj
   bpy.context.scene.update() 
   bpy.ops.object.duplicate()
   bpy.context.object.location = co
   for frame in range(1, int(framedat[i])):
      tstep = float(frame)/30.0
      h = gravity(co.z,vi,tstep)
      th = co.z-h
      bpy.ops.transform.translate(value=(0, 0, -h))
      # create keyframe
      bpy.ops.anim.keyframe_insert_menu(type='Location')
   
 

