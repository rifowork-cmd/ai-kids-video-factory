"""Generate an original animated 3D bunny and colored balls in Blender background mode.
Run: blender -b -t 2 --python src/blender_scene.py -- --output output/3d-silent.mp4
"""
import bpy
import math
import sys
from pathlib import Path
from mathutils import Vector

args = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
output = "output/3d-silent.mp4"
if "--output" in args:
    output = args[args.index("--output")+1]
Path(output).parent.mkdir(parents=True, exist_ok=True)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)

def material(name, color, roughness=0.7):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = roughness
    return m

white = material("Bunny cream", (0.94,0.90,0.83))
pink = material("Inner ears", (0.97,0.48,0.57))
dark = material("Eyes", (0.06,0.06,0.10))
floor_mat = material("Soft mint floor", (0.63,0.83,0.77))
colors = [material("Red", (0.95,0.17,0.22)), material("Blue",(0.12,0.42,0.92)),material("Yellow",(1,0.74,0.09))]

def sphere(name, location, scale, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, location=location)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.shade_smooth()
    o.data.materials.append(mat)
    return o

bpy.ops.mesh.primitive_cube_add(size=2, location=(0,0,-0.23))
ground = bpy.context.object
ground.name = "Floor"
ground.scale = (7,7,0.2)
ground.data.materials.append(floor_mat)

bunny_parts = []
def part(name, xyz, scale, mat):
    obj = sphere(name, xyz, scale, mat)
    bunny_parts.append(obj)
    return obj

part("Body",(-1.45,0,0.87),(.65,.45,.83),white)
part("Head",(-1.45,-.05,1.82),(.62,.52,.58),white)
part("Left ear",(-1.78,0,2.62),(.21,.23,.65),white)
part("Right ear",(-1.12,0,2.62),(.21,.23,.65),white)
part("Left inner ear",(-1.78,-.19,2.64),(.12,.07,.46),pink)
part("Right inner ear",(-1.12,-.19,2.64),(.12,.07,.46),pink)
part("Left eye",(-1.69,-.52,1.91),(.095,.07,.12),dark)
part("Right eye",(-1.21,-.52,1.91),(.095,.07,.12),dark)
part("Nose",(-1.45,-.57,1.69),(.11,.06,.075),pink)
part("Left foot",(-1.78,-.35,.28),(.28,.3,.18),white)
part("Right foot",(-1.11,-.35,.28),(.28,.3,.18),white)

# Parent to an empty so the bunny can bounce as a group.
bpy.ops.object.empty_add(location=(0,0,0))
rig = bpy.context.object
rig.name = "Bunny animation rig"
for obj in bunny_parts:
    obj.parent = rig
    obj.matrix_parent_inverse = rig.matrix_world.inverted()

balls = []
for i, mat in enumerate(colors):
    balls.append(sphere(["Red ball","Blue ball","Yellow ball"][i],(1.4,0,.6),(.58,)*3,mat))
    balls[-1].hide_render = True

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 8
scene.render.threads_mode = "FIXED"
scene.render.threads = 2
scene.render.resolution_x = 640
scene.render.resolution_y = 360
scene.render.resolution_percentage = 100
scene.render.fps = 12
scene.frame_start = 1
scene.frame_end = 180
scene.render.image_settings.color_mode = "RGB"
scene.render.image_settings.file_format = "PNG"
frames_dir = Path(output).resolve().parent / "frames"
frames_dir.mkdir(parents=True, exist_ok=True)
scene.render.filepath = str(frames_dir / "frame_")
scene.render.film_transparent = False
scene.world.color = (0.82,0.86,0.92)

for frame in range(1,181):
    t=(frame-1)/12
    rig.location.z = .10 * abs(math.sin(t*math.pi*1.1))
    rig.rotation_euler.z = .08*math.sin(t*1.5)
    rig.keyframe_insert(data_path="location",frame=frame)
    rig.keyframe_insert(data_path="rotation_euler",frame=frame)
    active=min(int(t//5),2)
    for i,ball in enumerate(balls):
        visible=(i==active)
        ball.hide_render=not visible
        ball.keyframe_insert(data_path="hide_render",frame=frame)
        if visible:
            ball.location.x = 1.4 + .22*math.sin(t*2.2)
            ball.location.z = .59 + .4*abs(math.sin(t*2.7))
            ball.rotation_euler.y = t*1.4
            ball.keyframe_insert(data_path="location",frame=frame)
            ball.keyframe_insert(data_path="rotation_euler",frame=frame)

def point_camera(obj, target):
    direction=Vector(target)-obj.location
    obj.rotation_euler=direction.to_track_quat("-Z","Y").to_euler()

bpy.ops.object.camera_add(location=(0,-8,3.0))
cam=bpy.context.object
point_camera(cam,(0,0,1.35))
scene.camera=cam
bpy.ops.object.light_add(type="AREA",location=(-3,-4,7))
light=bpy.context.object
light.data.energy=900
light.data.shape="DISK"
light.data.size=6
bpy.ops.object.light_add(type="AREA",location=(4,2,5))
bpy.context.object.data.energy=650
bpy.context.object.data.size=5
bpy.ops.render.render(animation=True)
frames = sorted(frames_dir.glob("frame_*.png"))
if len(frames) != scene.frame_end - scene.frame_start + 1:
    raise RuntimeError(f"Expected 180 PNG frames, found {len(frames)}")
print(f"Rendered {len(frames)} PNG frames")
