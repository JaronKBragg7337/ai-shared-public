import unreal
L = lambda m: unreal.log_warning("PROBE | " + str(m))
tw = unreal.MovieSceneTimeWarpVariant()
L("tw %s" % [m for m in dir(tw) if not m.startswith("_")])
for x in dir(unreal):
    if "TimeWarp" in x: L("api %s: %s" % (x, [m for m in dir(getattr(unreal, x)) if not m.startswith("_")][:60]))
p = unreal.MovieSceneSkeletalAnimationParams(); L("params %s" % [m for m in dir(p) if not m.startswith("_")])
