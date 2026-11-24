
# ================================================================ world: one low-sun sky for the outdoor sets, a dim grey for the rooms
w = bpy.data.worlds.new("World"); sc.world = w; w.use_nodes = True; wn = w.node_tree; wn.nodes.clear()
sky = wn.nodes.new("ShaderNodeTexSky"); sky.sky_type = "MULTIPLE_SCATTERING"
SUN_EL, SUN_ROT = 9.0, 100.0
try: sky.sun_elevation = math.radians(SUN_EL); sky.sun_rotation = math.radians(SUN_ROT); sky.altitude = 300.0; sky.sun_disc = False
except Exception as e: print("sky props", e)
vday = wn.nodes.new("ShaderNodeValue"); vgrey = wn.nodes.new("ShaderNodeValue")
def wmul(a, b):
    n = wn.nodes.new("ShaderNodeMath"); n.operation = "MULTIPLY"; wn.links.new(a, n.inputs[0]); n.inputs[1].default_value = b; return n.outputs[0]
bg_d = wn.nodes.new("ShaderNodeBackground"); wn.links.new(sky.outputs[0], bg_d.inputs["Color"]); wn.links.new(wmul(vday.outputs[0], .5), bg_d.inputs["Strength"])
bg_g = wn.nodes.new("ShaderNodeBackground"); bg_g.inputs["Color"].default_value = (.5, .52, .56, 1); wn.links.new(vgrey.outputs[0], bg_g.inputs["Strength"])
ad = wn.nodes.new("ShaderNodeAddShader"); wn.links.new(bg_d.outputs[0], ad.inputs[0]); wn.links.new(bg_g.outputs[0], ad.inputs[1])
wo_ = wn.nodes.new("ShaderNodeOutputWorld"); wn.links.new(ad.outputs[0], wo_.inputs["Surface"])
SUNV = Vector((math.sin(math.radians(SUN_ROT)) * math.cos(math.radians(SUN_EL)), math.cos(math.radians(SUN_ROT)) * math.cos(math.radians(SUN_EL)), math.sin(math.radians(SUN_EL))))
sun_d = bpy.data.lights.new("Sun", "SUN"); sun_d.angle = math.radians(.53); sun_d.color = (1.0, .86, .7)
sun = bpy.data.objects.new("Sun", sun_d); sc.collection.objects.link(sun); sun.rotation_euler = SUNV.to_track_quat("Z", "Y").to_euler()
SET_WORLD = {"FIELD": (1.0, 0.0, 4.5), "CAPE": (1.0, 0.0, 4.0), "JAR": (1.0, 0.0, 4.0),
             "CORE": (0, .25, 0), "LAB": (0, .03, 0), "GLASS": (0, .004, 0), "SHELF": (0, .05, 0)}
SET_EXP = {"FIELD": -.15, "CAPE": -.3, "JAR": -.3, "SHELF": -.6}

# ---------------------------------------------------------------- camera
cd = bpy.data.cameras.new("Cam"); cam = bpy.data.objects.new("Cam", cd); sc.collection.objects.link(cam); sc.camera = cam
cd.clip_start = .002; cd.clip_end = 20000.0; cd.sensor_width = 36.0; cd.dof.use_dof = True
cam.rotation_mode = "QUATERNION"
def lookat(p, t, up=Vector((0, 0, 1))):
    f = (Vector(t) - Vector(p)).normalized(); r = f.cross(Vector(up)).normalized(); u = r.cross(f)
    return Matrix((r, u, -f)).transposed().to_quaternion()
def fz(x, y): return float(plateau_h(np.array([x]), np.array([y]))[0])
def cam_keys(name):
    """(fraction, pos, target, lens, fstop, focus distance or None)"""
    if name == "FIELD_A":    # low over the plateau, tilting up from the snow to the sky
        o = ORG["FIELD"]; z = fz(0, -6)
        return [(0, o + Vector((0, -6, z + 1.4)), o + Vector((26, 32, z + 2.0)), 28, 16, None), (1, o + Vector((0, -6.3, z + 1.5)), o + Vector((26, 32, z + 20)), 28, 16, None)]
    if name == "FIELD_B":    # close to the surface, ice crystals falling
        o = ORG["FIELD"]; z = fz(0, -2)
        return [(0, o + Vector((-.5, -3.9, z + .5)), o + Vector((.3, -1.0, z + .05)), 40, 5.6, 1.6), (1, o + Vector((-.4, -3.6, z + .42)), o + Vector((.3, -1.0, z + .02)), 40, 5.6, 1.5)]
    if name == "FIELD_C":    # skimming the open snow
        o = ORG["FIELD"]; z = fz(2, -8)
        return [(0, o + Vector((2, -8, z + .5)), o + Vector((0, 12, z - .2)), 30, 11, None), (1, o + Vector((1.6, -5.2, z + .38)), o + Vector((0, 14, z - .2)), 30, 11, None)]
    if name == "FIELD_D":    # toward the low sun, today's snow
        o = ORG["FIELD"]; z = fz(-6, 0)
        return [(0, o + Vector((-6, -1, z + .7)), o + Vector((20, 4, z + .2)), 30, 11, None), (1, o + Vector((-4.4, -.8, z + .6)), o + Vector((20, 4, z + .25)), 30, 11, None)]
    if name == "FIELD_Z":    # end: rise off the snow and tilt up into the sky
        o = ORG["FIELD"]; z = fz(0, -10)
        return [(0, o + Vector((0, -10, z + 1.5)), o + Vector((24, 30, z + .5)), 28, 16, None), (1, o + Vector((0, -22, z + 14)), o + Vector((30, 40, z + 22)), 28, 16, None)]
    if name == "CORE_A":     # macro push into the bubbles
        o = ORG["CORE"]
        return [(0, o + Vector((.07, -.2, CZ + .06)), o + Vector((.03, 0, CZ)), 85, 16, None), (1, o + Vector((.045, -.13, CZ + .035)), o + Vector((.025, 0, CZ)), 85, 16, None)]
    if name == "CORE_A2":
        o = ORG["CORE"]
        return [(0, o + Vector((-.24, -.2, CZ + .07)), o + Vector((-.2, 0, CZ)), 85, 16, None), (1, o + Vector((-.2, -.15, CZ + .05)), o + Vector((-.2, 0, CZ)), 85, 16, None)]
    if name == "CORE_B":     # the core on its cradle; cracks appear
        o = ORG["CORE"]
        return [(0, o + Vector((-.75, -.95, CZ + .45)), o + Vector((0, 0, CZ)), 50, 5.6, None), (1, o + Vector((-.45, -.7, CZ + .3)), o + Vector((0, 0, CZ)), 50, 5.6, None)]
    if name == "CORE_C":     # macro along a crack, then over to the second piece resting
        o = ORG["CORE"]
        return [(0, o + Vector((.3, -.36, CZ + .13)), o + Vector((.15, 0, CZ)), 60, 11, None), (.5, o + Vector((.33, -.33, CZ + .12)), o + Vector((.19, 0, CZ)), 60, 11, None),
                (1, o + Vector((.5, -.38, CZ + .16)), o + Vector((.66, -.02, CZ)), 60, 8, None)]
    if name == "CORE_D":     # a short core section by itself (a generic core, not the Allan Hills core)
        o = ORG["CORE"]
        return [(0, o + Vector((1.25, -.75, CZ + .38)), o + Vector((.68, -.02, CZ)), 60, 5.6, None), (1, o + Vector((1.12, -.62, CZ + .3)), o + Vector((.68, -.02, CZ)), 60, 5.6, None)]
    if name == "LAB_A":
        o = ORG["LAB"]
        return [(0, o + Vector((-.1, -.26, BZ + .12)), o + Vector((0, 0, BZ + .025)), 50, 9, None), (.45, o + Vector((-.07, -.2, BZ + .09)), o + Vector((0, 0, BZ + .025)), 50, 9, None),
                (1, o + Vector((.07, -.4, BZ + .19)), o + Vector((-.1, .07, BZ + .07)), 30, 9, None)]
    if name == "GLASS_A":
        o = ORG["GLASS"]
        return [(0, o + Vector((-.13, -.33, GZ + .1)), o + Vector((0, 0, GZ + .065)), 70, 6, None), (1, o + Vector((-.08, -.23, GZ + .085)), o + Vector((0, 0, GZ + .068)), 70, 6, None)]
    if name == "CAPE_A":     # behind the station looking out to sea, then down to the cylinders
        o = ORG["CAPE"]
        return [(0, o + Vector((-18, -158, cape_z(-18, -158) + 5)), o + Vector((0, -40, hz)), 35, 11, None),
                (.6, o + Vector((-13, -150, cape_z(-13, -150) + 3.6)), o + Vector((0, -40, hz)), 35, 11, None),
                (1, o + Vector((-8.2, -139.5, cape_z(-8.2, -139.5) + 1.7)), o + Vector((hx - 4.9, hy - 3.2, hz + .8)), 35, 8, None)]
    if name == "SHELF_A":    # the old olive cylinder, then the rows
        o = ORG["SHELF"]
        return [(0, o + Vector((-2.7, -1.7, 1.0)), o + Vector((-1.8, -.4, .6)), 45, 4, None), (.45, o + Vector((-2.55, -1.6, .95)), o + Vector((-1.8, -.4, .6)), 45, 4, None),
                (1, o + Vector((1.6, -2.7, 1.6)), o + Vector((0, 1.2, .9)), 32, 8, None)]
    if name == "SHELF_B":
        o = ORG["SHELF"]
        return [(0, o + Vector((3.85, .55, 1.55)), o + Vector((4.6, 1.5, 1.3)), 50, 4, None), (1, o + Vector((4.05, .8, 1.48)), o + Vector((4.6, 1.5, 1.3)), 50, 4, None)]
    if name == "JAR_A":
        o = ORG["JAR"]
        return [(0, o + Vector((-.36, -.46, JZ + .26)), o + Vector((.03, -.02, JZ + .05)), 50, 4, None), (1, o + Vector((-.22, -.3, JZ + .16)), o + Vector((.04, -.03, JZ + .045)), 50, 4, None)]
    raise KeyError(name)

def key_vis(o_, frame, hidden):
    o_.hide_render = hidden; o_.keyframe_insert("hide_render", frame=frame)
SRC_HIDE = {"FlakeSrc", "BubSrc", "GBSrc", "RiseSrc"}
allsets = list(SETS.keys())
for c_ in CRACKS:   # cracks start tiny
    c_.scale = (.01, .01, 1); c_.keyframe_insert("scale", frame=1)
f = 1; cut = set()
def F(fa, fb, u): return int(round(fa + (fb - fa) * u))
for sh in SHOTS:
    n = int(round(sh["dur"] * FPS)); fa, fb = f, f + n - 1
    if sh["cam"] is None: f = fb + 1; continue
    cut.add(fb)
    setname = sh["cam"].split("_")[0]
    for s_ in allsets:
        for o_ in SETS[s_]:
            if o_.name in SRC_HIDE: continue
            key_vis(o_, fa, s_ != setname)
    dy, gr, se = SET_WORLD[setname]
    vday.outputs[0].default_value = dy; vday.outputs[0].keyframe_insert("default_value", frame=fa)
    vgrey.outputs[0].default_value = gr; vgrey.outputs[0].keyframe_insert("default_value", frame=fa)
    sun_d.energy = se; sun_d.keyframe_insert("energy", frame=fa)
    sc.view_settings.exposure = SET_EXP.get(setname, 0.0); sc.view_settings.keyframe_insert("exposure", frame=fa)
    for u, p, t, lens, fs_, fd in cam_keys(sh["cam"]):
        ff = F(fa, fb, u)
        cam.location = p; cam.rotation_quaternion = lookat(p, t)
        cam.keyframe_insert("location", frame=ff); cam.keyframe_insert("rotation_quaternion", frame=ff)
        cd.lens = lens; cd.keyframe_insert("lens", frame=ff)
        cd.dof.aperture_fstop = fs_; cd.dof.keyframe_insert("aperture_fstop", frame=ff)
        cd.dof.focus_distance = fd if fd else (Vector(t) - Vector(p)).length; cd.dof.keyframe_insert("focus_distance", frame=ff)
    c = sh["cam"]
    if c == "FIELD_B":       # crystals drift down
        FL.location = ORG["FIELD"] + Vector((.15, 0, .2)); FL.keyframe_insert("location", frame=fa)
        FL.location = ORG["FIELD"] + Vector((-.1, 0, -1.4)); FL.keyframe_insert("location", frame=fb)
    elif c == "FIELD_A" or c.startswith("FIELD"):
        if c != "FIELD_B":
            for fl_ in fls: key_vis(fl_, fa, True)
    if c == "CORE_B":        # "a small knock can make them burst and the ice crack" (~9.5 s in), the core rings
        for k, (t0, t1) in ((0, (9.3, 10.6)), (1, (9.8, 11.4)), (3, (10.2, 12.0))):
            cr = CRACKS[k]; cr.scale = (.01, .01, 1); cr.keyframe_insert("scale", frame=fa + int(t0 * FPS))
            cr.scale = (1, 1, 1); cr.keyframe_insert("scale", frame=fa + int(t1 * FPS))
    if c == "CORE_C":        # "bubbles or tiny cracks can appear again" (~4 s in)
        cr = CRACKS[2]; cr.scale = (.01, .01, 1); cr.keyframe_insert("scale", frame=fa + int(3.4 * FPS))
        cr.scale = (1, 1, 1); cr.keyframe_insert("scale", frame=fa + int(5.6 * FPS))
    if c == "LAB_A":         # laser on ~2.8 s in; the ice shrinks as it turns to vapor
        t_on = fa + int(2.8 * FPS)
        key_vis(beam, fa, True); key_vis(beam, t_on, False)
        glow.data.energy = 0.0; glow.data.keyframe_insert("energy", frame=fa); glow.data.keyframe_insert("energy", frame=t_on - 1)
        glow.data.energy = .6; glow.data.keyframe_insert("energy", frame=t_on)
        icep.scale = (1, 1, 1); icep.keyframe_insert("scale", frame=t_on)
        icep.scale = (.55, .55, .5); icep.keyframe_insert("scale", frame=fb)
        icep.location = ORG["LAB"] + Vector((0, 0, BZ + .004 + .009)); icep.keyframe_insert("location", frame=t_on)
        icep.location = ORG["LAB"] + Vector((0, 0, BZ + .004 + .0045)); icep.keyframe_insert("location", frame=fb)
    if c == "GLASS_A":       # bubbles leave the melting ice and rise to the surface, again and again
        o = ORG["GLASS"]
        for b_, bx, by, ph, per in RISERS:
            rr = math.hypot(bx, by) or 1e-3; ex = bx / rr * .019; ey = by / rr * .017
            z0, z1 = GZ + .056, GZ + .0775; t = fa - ph * per * FPS
            while t < fb + 1:
                a0 = int(t); a1 = int(t + per * FPS) - 1
                if a1 <= fa + 1: t += per * FPS; continue
                b_.location = o + Vector((.003 + ex, ey, z0)); b_.keyframe_insert("location", frame=max(fa, a0))
                b_.location = o + Vector((.003 + ex * 1.15, ey * 1.15, z1)); b_.keyframe_insert("location", frame=max(fa, a1))
                t += per * FPS
    if c == "CAPE_A":        # the sea moves
        SEA_W.default_value = 0.0; SEA_W.keyframe_insert("default_value", frame=fa)
        SEA_W.default_value = sh["dur"] * .08; SEA_W.keyframe_insert("default_value", frame=fb)
        LINEAR_ANIM.add("__sea__")
    f = fb + 1
def all_curves(idb):
    ad_ = idb.animation_data
    if not ad_ or not ad_.action: return []
    cs = getattr(ad_.action, "fcurves", None)
    if cs is not None: return list(cs)
    try: return [fc for layer in ad_.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
    except Exception: return []
SMOOTH_ANIM |= {icep.name}
for idb in list(bpy.data.objects) + list(bpy.data.lights) + [w.node_tree, sc, SEA_NT]:
    nm = getattr(idb, "name", "")
    for fc in all_curves(idb):
        lin = (nm in LINEAR_ANIM or idb is SEA_NT or nm.startswith("Rise")) and fc.data_path != "hide_render"
        for k in fc.keyframe_points:
            if lin: k.interpolation = "LINEAR"
            elif nm in SMOOTH_ANIM and fc.data_path != "hide_render": k.interpolation = "BEZIER"
            else: k.interpolation = "CONSTANT"
for b_, *_ in RISERS:   # rising bubbles jump back to the start between cycles
    for fc in all_curves(b_):
        if fc.data_path != "location": continue
        kp = fc.keyframe_points
        for i in range(len(kp)):
            kp[i].interpolation = "LINEAR" if i % 2 == 0 else "CONSTANT"
for idb in (cam, cd):
    for fc in all_curves(idb):
        for k in fc.keyframe_points:
            k.interpolation = "CONSTANT" if int(k.co[0]) in cut else "BEZIER"; k.easing = "EASE_IN_OUT"
print("frames", DUR, flush=True)
# ---------------------------------------------------------------- outputs
if arg("--save"): bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(arg("--save")))
def shot_frame(name, u):
    ff = 1
    for sh in SHOTS:
        n_ = int(round(sh["dur"] * FPS))
        if sh["name"] == name or sh["cam"] == name: return ff + int(u * (n_ - 1))
        ff += n_
    raise KeyError(name)
if arg("--hide"):
    for nm_ in arg("--hide").split(","): bpy.data.objects[nm_].hide_render = True; bpy.data.objects[nm_].animation_data_clear()
if arg("--stills"):
    outd = os.path.abspath(arg("--stills")); os.makedirs(outd, exist_ok=True)
    frs = []
    for x in arg("--frames", "1").split(","):
        if ":" in x: nm_, u_ = x.split(":"); frs.append((nm_ + "_" + u_, shot_frame(nm_, float(u_))))
        else: frs.append(("f", int(x)))
    for tag_, fr in frs:
        t0 = time.time(); sc.frame_set(fr); sc.render.filepath = os.path.join(outd, "t_%s_%04d.png" % (tag_, fr)); bpy.ops.render.render(write_still=True); print("STILL", tag_, fr, "%.1fs" % (time.time() - t0), flush=True)
if arg("--anim"):
    outd = os.path.abspath(arg("--anim")); os.makedirs(outd, exist_ok=True)
    f0, f1 = int(arg("--start", sc.frame_start)), int(arg("--end", sc.frame_end))
    skip = set(); ff_ = 1
    for sh in SHOTS:
        n_ = int(round(sh["dur"] * FPS))
        if sh["cam"] is None: skip.update(range(ff_, ff_ + n_))
        ff_ += n_
    step = int(arg("--step", "1"))
    todo = list(range(f0, f1 + 1, step))
    if arg("--ranges"):
        todo = [fr for ab in arg("--ranges").split(",") for fr in range(int(ab.split("-")[0]), int(ab.split("-")[1]) + 1, step)]
    if arg("--shots"):
        names = arg("--shots").split(","); todo = []; ff_ = 1
        for sh in SHOTS:
            n_ = int(round(sh["dur"] * FPS))
            if sh["name"] in names: todo += list(range(ff_ if ff_ % 2 == 1 else ff_ + 1, ff_ + n_, 2))
            ff_ += n_
    deadline = arg("--deadline")   # "HH:MM" local; stop cleanly before it
    for fr in todo:
        if deadline:
            lt = time.localtime(); hh, mm = map(int, deadline.split(":"))
            if (lt.tm_hour, lt.tm_min) >= (hh, mm) and lt.tm_hour < 12: print("DEADLINE STOP", fr, flush=True); break
        p = os.path.join(outd, "f_%04d.png" % fr)
        if fr in skip or (os.path.exists(p) and os.path.getsize(p) > 1000): continue
        t0 = time.time(); sc.frame_set(fr); sc.render.filepath = p; bpy.ops.render.render(write_still=True)
        print("FRAME %d %.1fs" % (fr, time.time() - t0), flush=True)
