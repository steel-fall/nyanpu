import bpy
import bmesh
import math


def remove_all():
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)

    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)


def add_body():
    # add sphere
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=1,
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, 0),
        scale=(1, 1, 1))

    # get mesh
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(bpy.context.object.data)

    # delete vertex under z = 0.5
    bm.verts.ensure_lookup_table()
    for v in bm.verts:
        co = v.co @ bpy.context.object.matrix_world
        if co.z < -0.5:
            v.select = True
        else:
            v.select = False
    bpy.ops.mesh.delete(type='VERT')

    # add face
    bm.edges.ensure_lookup_table()
    for e in bm.edges:
        if e.is_boundary:
            e.select = True
        else:
            e.select = False
    bpy.ops.mesh.edge_face_add()
    bpy.ops.mesh.poke()

    # delete vertex y < 0
    for v in bm.verts:
        co = v.co @ bpy.context.object.matrix_world
        if co.y < -0.01:
            v.select = True
        else:
            v.select = False
    bpy.ops.mesh.delete(type='VERT')

    # add mirror
    bpy.ops.object.modifier_add(type='MIRROR')
    bpy.context.object.modifiers["ミラー"].use_axis[0] = False
    bpy.context.object.modifiers["ミラー"].use_axis[1] = True
    bpy.context.object.modifiers["ミラー"].use_axis[2] = False

    # add subdivision surface
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.transform.resize(value=(0.9, 1, 1))


def add_ears():
    # get mesh
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(bpy.context.object.data)

    bm.verts.ensure_lookup_table()
    for v in bm.verts:
        co = v.co @ bpy.context.object.matrix_world
        if abs(co.x) < 0.001:
            if 0.70 < co.z < 0.95:
                v.select = True
    bpy.ops.transform.translate(value=(0, 0.15, 0.4))


def add_eyes():
    # add sphere
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=1,
        align='WORLD',
        location=(0.65, 0.35, 0.4),
        scale=(-0.15, -0.15, -0.15))

    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # add mirror
    bpy.ops.object.modifier_add(type='MIRROR')
    bpy.context.object.modifiers["ミラー"].use_axis[0] = False
    bpy.context.object.modifiers["ミラー"].use_axis[1] = True
    bpy.context.object.modifiers["ミラー"].use_axis[2] = False


def add_mouth():
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.mesh.primitive_cube_add(
        size=1,
        align='WORLD',
        location=(0.85, 0, 0.13),
        scale=(0.1, 0.1, 0.1))

    # get mesh
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type='FACE')
    bm = bmesh.from_edit_mesh(bpy.context.object.data)

    bm.faces.ensure_lookup_table()
    for f in bm.faces:
        co = f.calc_center_median() @ bpy.context.object.matrix_world
        if co.y > 0.001:
            f.select = True
        else:
            f.select = False
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={
            "value": (0, 0.2, 0),
            "constraint_axis": (False, False, True)})

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        align='WORLD',
        location=(0.85, 0.2, 0.23),
        scale=(0.1, 0.1, 0.1))
    bpy.data.objects[2].select_set(True)
    bpy.data.objects[3].select_set(True)
    bpy.ops.object.join()
    bpy.ops.transform.rotate(value=2/8*math.pi, orient_axis='X')
    bpy.ops.transform.translate(value=(0, 0.012, 0))
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # add mirror
    bpy.ops.object.modifier_add(type='MIRROR')
    bpy.context.object.modifiers["ミラー"].use_axis[0] = False
    bpy.context.object.modifiers["ミラー"].use_axis[1] = True
    bpy.context.object.modifiers["ミラー"].use_axis[2] = False


if __name__ == "__main__":
    remove_all()
    add_body()
    add_ears()
    add_eyes()
    add_mouth()
