import bpy,bmesh

ob = bpy.data.objects['land']
mesh=bmesh.from_edit_mesh(bpy.context.object.data)
selectionverts = []
for v in mesh.verts:
    if v.select:
       vertices.append(v)

