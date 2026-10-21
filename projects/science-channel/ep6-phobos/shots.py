# Shot plan shared by build.py (Blender), diagram.py (Pillow) and finish.py (captions, mix). Durations in seconds.
# Cameras (all in a frame with Phobos at the origin and Mars 9,376 km away on +Y; scene unit = 1 km):
#   A/A2/A3 hero: Phobos in the foreground, Mars behind.           B/B2 flyover: low across the groove fields.
#   C/C2 surface: standing on Phobos, Mars in the sky.             D stickney: the big crater end.
#   E deimos: Deimos close with Mars small behind (the comparison). F spiral: far from Mars, the orbit tightening (Phobos
#   enlarged x25 for visibility, labelled).                        G ring: the break-up into a ring (a model, labelled).
# "diag_*" and "end_card" are Pillow frames, drawn into the same frame range.
FPS = 24
SHOTS = [
 dict(name="s01_hero_A",       cam="A",  dur=14.0),
 dict(name="s02_flyover_B",    cam="B",  dur=14.0),
 dict(name="s03_surface_C",    cam="C",  dur=24.0),
 dict(name="diag_orbit",       cam=None, dur=30.0),
 dict(name="s05_tide_A2",      cam="A2", dur=18.0),
 dict(name="s04_deimos_E",     cam="E",  dur=14.0),
 dict(name="s06_spiral_F",     cam="F",  dur=36.0),
 dict(name="s07_ring_G",       cam="G",  dur=32.0),
 dict(name="s08_stickney_D",   cam="D",  dur=14.0),
 dict(name="s09_grooves_B2",   cam="B2", dur=14.0),
 dict(name="diag_grooves",     cam=None, dur=37.0),
 dict(name="diag_origin",      cam=None, dur=34.0),
 dict(name="diag_mmx",         cam=None, dur=37.0),
 dict(name="s10_sample_C2",    cam="C2", dur=26.0),
 dict(name="s11_close_A3",     cam="A3", dur=28.0),
 dict(name="end_card",         cam=None, dur=12.0),
]
