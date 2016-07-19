import bpy,bmesh

ob = bpy.data.objects['Land']

bpy.ops.object.mode_set(mode='EDIT')
mesh=bmesh.from_edit_mesh(bpy.context.object.data)
selvertices = []
for v in mesh.verts:
    if v.select:
       x,y,z = ob.matrix_world*v.co
       selvertices.append([x,y,z])

