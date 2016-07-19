import bpy
from bpy import context
import math
import random

## run SelectionVertices.py script prior to running this in console
## all modifiers (e.g., deform, smooth or anything else) must be applied to the mesh computed
## before using script.  Height data read from mesh otherwise is done so on pre modified mesh.
## 

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
   
def solvet2(vi,vf):
   return (vf-vi)/(-9.8)
   
def solveh(vi,t):
   return .5*9.8*t*t - vi*t

def solvehf(vi,t):
   return -.5*9.8*t*t + vi*t

def solvevf(vi,t):
   return -9.8*t + vi
   
numFallingObjs = 5
fobj_list = []
vi = -9.8
tf = 7.0 ## in frames 30 sec  per frame is the standard so 1 frame equals 1/30.0 seconds

tfs = 7.0/30.0
dampingfactor = .7
bounces = 1
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
bouncedat = []  ## set as (initial_height,final_height,timetofinalheightinframes) tuple
##bounce2dat = []
for i in range(0,numFallingObjs):
   vpick = random.randint(0,len(selvertices2))
   x,y,z = selvertices2[vpick] 
   tf1 = float(tf) + float(random.randint(0,5))
   tfs1 = tf1/30.0
   h = solveh(vi,tfs1)
   vf = solvevf(vi,tfs1)
   t2 = solvet2(-vf*dampingfactor,0.0)
   hf = solvehf(vf,t2) ## bounce
   print("Solve Height: " + str(h))
   print("original height: " + str(vdat[(x,y)]))
   print("time: " + str(tfs1))
   newz = vdat[(x,y)]+h
   framedat.append(tf1)
   coorddat.append((x,y,newz))
   boundat.append((vdat[(x,y)],hf+vdat[(x,y)],int(t2*30.0)))
   del selvertices2[vpick]
Scene_Name = bpy.context.scene.name   
bpy.ops.object.mode_set(mode='OBJECT')
bpy.data.objects['Land'].select = False
bpy.context.scene.update()
for i, co in enumerate(coorddat):
   bpy.data.objects['W_rfe203'].select=True  ##obj
   bpy.context.scene.update() 
   bpy.ops.object.duplicate(linked=False)
   bpy.data.objects['W_rfe203'].select=False
   bpy.context.scene.update()
   bpy.ops.object.make_single_user(type='SELECTED_OBJECTS',
                                   object=True, obdata=True,animation=True)
   bpy.context.scene.update()
   objname = "W_rfe203"+".00"+str(i+1)
   bpy.data.scenes[Scene_Name].frame_set(0)
   obj = bpy.data.objects[objname]
   obj.location = co[0:len(co)]
   print(obj.location)
##   print(bpy.ops.anim.keying_set_add())
##   print(bpy.ops.anim.keying_set_active_set(i)) 
##   print(bpy.ops.anim.keying_set_path_add())
   print(bpy.context.scene.update()) 
   print(obj.keyframe_insert(data_path="location"))
   ## if there are existing key frames use this
##   for num in range(0, 30):
##      bpy.context.active_object.keyframe_delete('location', frame=num)
   for frame in range(1, int(framedat[i])+1):
      tstep = float(frame)/30.0
      h = gravity(co[2],vi,tstep)
      bpy.data.scenes[Scene_Name].frame_set(frame)
      print(h)
      ##th = co[2]-h
      ##print(bpy.ops.transform.translate(value=(0, 0, -th)))
      obj.location = (obj.location.x, obj.location.y, h)
      bpy.context.scene.update()
      
      # create keyframe
      print(obj.keyframe_insert(data_path="location"))
      bpy.context.scene.update() 
   ## apply bounceposv
   hi,hf,tf = bouncedat[i]
   bpy.data.scenes[Scene_Name].frame_set(frame+tf)
   obj.location = (obj.location.x, obj.location.y, hf)
   # create keyframe
   print(obj.keyframe_insert(data_path="location"))
   ##apply bouncenegv
   bpy.data.scenes[Scene_Name].frame_set(frame+2*tf)
   obj.location = (obj.location.x, obj.location.y, hi)
   # create keyframe
   print(obj.keyframe_insert(data_path="location"))   
   obj.select=False
   bpy.context.scene.update() 
   
   bpy.ops.object.select_all(action='DESELECT')
   
 

