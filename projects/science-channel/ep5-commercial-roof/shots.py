# Shot plan shared by build.py (Blender), diagram.py (Pillow) and finish.py (captions, mix). Durations in seconds.
# s0->s1 = the STAGE number the scene moves through during the shot:
#   0 new  .. 1 years 1-5  .. 2 years 5-15  .. 3 the leak (years ~15-18)  .. 3.3-4.6 restoration steps  .. 5 coated.
# Cameras: A hero wide from the flat-roof parapet corner across both roofs; E low on the metal roof at the screws;
# D the roof drain; B low across the ponding toward the RTU; C the rooftop-unit curb; F inside under the deck;
# G the hatch, parapet and scupper; H push-in version of A for the close.
# "diag_*" and "end_card" are not rendered by Blender: diagram.py draws them into the same frame range.
FPS = 24
SHOTS = [
 dict(name="s01_new_A",        cam="A", s0=0,   s1=0,   dur=12.0),
 dict(name="s02_new_E",        cam="E", s0=0,   s1=0,   dur=8.0),
 dict(name="s03_new_D",        cam="D", s0=0,   s1=0,   dur=8.0),
 dict(name="s04_y1to5_A",      cam="A", s0=0,   s1=1,   dur=14.0),
 dict(name="s05_y1to5_E",      cam="E", s0=.6,  s1=1.2, dur=10.0),
 dict(name="s06_y1to5_C",      cam="C", s0=1,   s1=1.3, dur=8.0),
 dict(name="diag_heat",        cam=None, s0=1,  s1=1,   dur=18.0),
 dict(name="s07_y5to15_A",     cam="A", s0=1,   s1=2,   dur=14.0),
 dict(name="s08_y5to15_E",     cam="E", s0=1.3, s1=2,   dur=10.0),
 dict(name="s09_pond_D",       cam="D", s0=1.5, s1=2.2, dur=10.0),
 dict(name="s10_seam_B",       cam="B", s0=2,   s1=2.5, dur=10.0),
 dict(name="s11_curb_C",       cam="C", s0=2.2, s1=2.7, dur=10.0),
 dict(name="s12_inside_F",     cam="F", s0=2.6, s1=3,   dur=11.0),
 dict(name="diag_leak",        cam=None, s0=3,  s1=3,   dur=34.0),
 dict(name="s13_fork_A",       cam="A", s0=3,   s1=3,   dur=10.0),
 dict(name="s14_wash_G",       cam="G", s0=3.2, s1=4,   dur=9.0),
 dict(name="s15_screws_E",     cam="E", s0=3.3, s1=4.6, dur=11.0),
 dict(name="s16_patch_D",      cam="D", s0=3.2, s1=4.6, dur=10.0),
 dict(name="s17_coat_C",       cam="C", s0=4.2, s1=5,   dur=8.0),
 dict(name="s18_coat_A",       cam="A", s0=4.3, s1=5,   dur=14.0),
 dict(name="diag_cool",        cam=None, s0=5,  s1=5,   dur=30.0),
 dict(name="s19_close_H",      cam="H", s0=5,   s1=5,   dur=22.0),
 dict(name="end_card",         cam=None, s0=5,  s1=5,   dur=12.0),
]
