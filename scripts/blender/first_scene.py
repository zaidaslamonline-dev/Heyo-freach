import bpy, math, os
from mathutils import Vector

# Procedural cinematic Roblox-inspired establishing scene.
OUT = os.environ.get("OUTPUT_DIR", "render")
os.makedirs(OUT, exist_ok=True)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.materials, bpy.data.cameras, bpy.data.lights):
    pass

def mat(name, color, metallic=0.0, rough=0.55, emission=0.0):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    bs=m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value=(*color,1)
    bs.inputs["Metallic"].default_value=metallic
    bs.inputs["Roughness"].default_value=rough
    if emission:
        bs.inputs["Emission Color"].default_value=(*color,1)
        bs.inputs["Emission Strength"].default_value=emission
    return m

gold=mat("Warm ivory stone",(0.72,0.58,0.31),.15,.42)
gold_trim=mat("Polished gold",(1.0,.62,.12),.7,.25)
sky_blue=mat("Heavenly blue",(0.17,.48,.72),.05,.42)
red_ground=mat("Ashen crimson",(0.22,.035,.045),.05,.8)
dark=mat("Charcoal metal",(.055,.075,.095),.7,.3)
skin=mat("Warm skin",(.72,.39,.23),0,.65)
blue=mat("Peter blue tunic",(.055,.25,.58),.05,.48)
green=mat("Leo green tunic",(.12,.38,.23),.05,.48)
robot=mat("Slave machinery",(.22,.28,.32),.75,.35)
white=mat("Cloud",(.88,.92,1),0,.8)
wingmat=mat("Feather gold",(1,.72,.2),.45,.32,0.15)

def cube(name, loc, scale, material, bevel=.08):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o=bpy.context.object; o.name=name
    o.dimensions=scale; bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:o.data.materials.append(material)
    if bevel:
        mod=o.modifiers.new("Soft bevels","BEVEL"); mod.width=bevel; mod.segments=3
        o.modifiers.new("Weighted corner normals","WEIGHTED_NORMAL")
    return o

def uv(name, loc, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material); return o

def text_obj(body, loc, size, material, rot=(math.pi/2,0,0)):
    cu=bpy.data.curves.new(body,"FONT"); cu.body=body; cu.size=size; cu.extrude=.012
    ob=bpy.data.objects.new(body,cu); bpy.context.collection.objects.link(ob); ob.location=loc; ob.rotation_euler=rot
    ob.data.materials.append(material); return ob

# Ground plane split by the colossal wall.
cube("Heaven plaza",(-4,2,-.35),(11,34,.7),gold)
cube("Slave wasteland",(7,2,-.42),(12,34,.84),red_ground)
# Architectural edge lines and paving.
for x in range(-9,2,2):
    cube("Golden paving seam",(x,0,.015),(.035,28,.025),gold_trim,.005)
for x in range(3,14,2):
    cube("Cracked red paving",(x,0,.02),(.035,28,.025),dark,.005)

# Massive dividing wall and sealed central gate.
cube("The dividing wall",(1.35,2,5.4),(1.25,34,11.2),gold_trim,.18)
cube("Gate dark inset",(.68,-1.5,4.0),(.12,5.2,7.6),dark,.08)
cube("Gate inner glow",(.59,-1.5,4.0),(.08,4.55,6.9),mat("Gate light",(.95,.54,.08),.2,.3,2.0),.03)
for z in [1.0,2.4,3.8,5.2,6.6,8.0,9.4]:
    cube("Wall engraved band",(.58,2,z),(.16,34,.08),gold,.02)
# Towers behind the heavenly side.
for x,y,h in [(-8,8,10),(-5,12,13),(-1,10,8),(-7,-5,8),(-3,-8,11)]:
    cube("Palace tower",(x,y,h/2),(2.3,2.3,h),gold,.18)
    cube("Tower crown",(x,y,h+.5),(3.0,3.0,1.0),gold_trim,.12)
    uv("Tower dome",(x,y,h+1.25),(1.15,1.15,1.0),gold_trim)
# Distant slave factories and smokestacks.
for x,y,h in [(5,9,7),(9,12,9),(12,6,6),(7,-7,8),(11,-10,6)]:
    cube("Factory block",(x,y,h/2),(3.4,4.2,h),dark,.12)
    for dx in [-.8,0,.8]:
        cube("Factory furnace",(x+dx,y-2.12,2.0),(.35,.08,1.0),mat("Furnace ember",(.9,.08,.015),.1,.3,1.4),.02)
# Floating cloud islands and flying-car silhouettes in the bright world.
for x,y,z in [(-8,0,10),(-5,5,12),(-1,-7,11)]:
    uv("Soft cloud",(x,y,z),(2.0,.8,.55),white)
    uv("Cloud lobe",(x+1.2,y,z+.15),(1.2,.75,.5),white)
cube("Flying car body",(-5,-1,8),(3.0,1.25,.55),sky_blue,.22)
for x in [-6,-4]:
    uv("Flying car engine",(x,-1,7.65),(.38,.38,.28),gold_trim)

# Build blocky characters facing camera (-Y). Characters are deliberately readable at portrait scale.
def character(name, x, y, tunic, with_wings=False, robot_arm=False):
    # feet, legs, torso, arms, head
    cube(name+" left leg",(x-.23,y,.62),(.36,.42,1.15),dark,.07)
    cube(name+" right leg",(x+.23,y,.62),(.36,.42,1.15),dark,.07)
    cube(name+" torso",(x,y,1.72),(.95,.48,1.25),tunic,.12)
    cube(name+" left arm",(x-.64,y,1.75),(.32,.42,1.12),skin,.08)
    arm_mat=robot if robot_arm else skin
    cube(name+" right arm",(x+.64,y,1.75),(.32,.42,1.12),arm_mat,.08)
    cube(name+" neck",(x,y,2.43),(.25,.28,.28),skin,.04)
    cube(name+" head",(x,y,2.92),(.82,.72,.82),skin,.14)
    # eyes on front face
    uv(name+" left eye",(x-.17,y-.372,3.02),(.055,.035,.075),dark)
    uv(name+" right eye",(x+.17,y-.372,3.02),(.055,.035,.075),dark)
    if with_wings:
        for side in [-1,1]:
            wing=cube(name+" golden wing",(x+side*.82,y+.22,2.35),(.72,.22,1.65),wingmat,.2)
            wing.rotation_euler[1]=side*-.32
            for j in range(3):
                feather=uv(name+" feather",(x+side*(.92+j*.12),y+.10,1.85+j*.38),(.25,.12,.48),wingmat)
                feather.rotation_euler[1]=side*-.25
    if robot_arm:
        for z in [1.35,1.75,2.15]:
            cube(name+" arm piston",(x+.64,y-.225,z),(.23,.035,.09),gold_trim,.025)

character("Peter",-3.4,-5,blue,True,False)
character("Leo",-1.25,-6,green,True,False)
character("Rose",5.2,-3,mat("Rose muted red",(.48,.13,.16)),False,True)
character("Worker",8.1,1,mat("Worker brown",(.30,.18,.12)),False,True)
# Tiny guards establish the danger without clutter.
for x,y in [(10,-1),(6,5)]:
    character("Guard",x,y,dark,False,True)

# Signs in each world, legible as environmental storytelling.
text_obj("GODS' WORLD",(-7,-9,5.2),.72,gold_trim)
text_obj("SLAVES' WORLD",(5.1,-9,5.2),.62,white)

# Lighting: warm gold on left, ominous red on right.
world=bpy.data.worlds.new("Dusk world") if not bpy.data.worlds else bpy.data.worlds[0]
scene=bpy.context.scene; scene.world=world; world.use_nodes=True
world.node_tree.nodes["Background"].inputs[0].default_value=(.035,.045,.075,1)
world.node_tree.nodes["Background"].inputs[1].default_value=.35

def area(name, loc, color, power, size, target):
    bpy.ops.object.light_add(type="AREA", location=loc); l=bpy.context.object; l.name=name
    l.data.energy=power; l.data.shape="DISK"; l.data.size=size; l.data.color=color
    l.rotation_euler=(Vector(target)-l.location).to_track_quat("-Z","Y").to_euler()
area("Golden key",(-7,-8,15),(1.0,.72,.38),2100,10,(-3,0,2))
area("Cold fill",(0,-10,9),(.38,.58,1.0),1000,9,(0,0,3))
area("Crimson rim",(10,3,12),(1.0,.035,.02),2600,8,(8,0,3))

# Portrait camera, slow lateral push for a living establishing shot.
bpy.ops.object.camera_add(location=(-.2,-25,8.0)); cam=bpy.context.object; cam.name="Story camera"
target=Vector((.0,0,4.3))
cam.rotation_euler=(target-cam.location).to_track_quat("-Z","Y").to_euler()
cam.data.lens=42; cam.data.sensor_fit="VERTICAL"; cam.data.sensor_height=24
scene.camera=cam
cam.location.x=-.35; cam.keyframe_insert(data_path="location",frame=1)
cam.location.x=.35; cam.keyframe_insert(data_path="location",frame=48)
# Slightly animated clouds for parallax.
for ob in [o for o in scene.objects if o.name.startswith("Soft cloud")]:
    ob.keyframe_insert(data_path="location",frame=1); ob.location.y+=.4; ob.keyframe_insert(data_path="location",frame=48)

scene.render.engine = "BLENDER_EEVEE_NEXT" if bpy.app.version >= (4, 2, 0) else "BLENDER_EEVEE"
if hasattr(scene, "eevee"):
    scene.eevee.taa_render_samples = 32
scene.render.resolution_x=576; scene.render.resolution_y=1024; scene.render.resolution_percentage=100
scene.render.fps=12; scene.frame_start=1; scene.frame_end=48
scene.render.image_settings.file_format="PNG"; scene.render.image_settings.color_mode="RGBA"
scene.render.filepath=os.path.join(OUT,"frame_")
scene.view_settings.view_transform="AgX"
scene.view_settings.look="AgX - Medium High Contrast"
scene.render.image_settings.color_depth="8"
scene.camera.data.dof.use_dof=False
scene.render.film_transparent=False
# Keep shadows and ambient occlusion crisp without expensive path tracing.
scene.render.filepath=os.path.join(OUT,"frame_")
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,"first_scene.blend"))
for frame in range(scene.frame_start,scene.frame_end+1):
    scene.frame_set(frame)
    scene.render.filepath=os.path.join(OUT,f"frame_{frame:04d}.png")
    bpy.ops.render.render(write_still=True)
print("Rendered", scene.frame_end, "frames to", OUT)
