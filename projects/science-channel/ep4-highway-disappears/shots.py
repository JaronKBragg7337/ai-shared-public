# Shot plan shared by build.py (Blender) and finish.py (captions, mix). Durations in seconds; s0->s1 = the stage number
# the scene moves through during the shot (0 clean, 1 first summer, 2 first fall, 3 first winter, 4 years 2-5, 5 years 5-20,
# 6 years 20-50). Cameras: A low on the shoulder looking down the lanes to the overpass; D from the overpass deck looking back;
# B the drain inlet; C the sign; E low on the lane at the hero pothole; F under the overpass; G = A with a slow push (the close).
# "diagram" shots are not rendered by Blender: diagram.py draws them (the freeze-thaw cutaway) into the same frame range.
FPS = 24
SHOTS = [
 dict(name="s01_year0_A",      cam="A", s0=0,   s1=0,   dur=12.0),
 dict(name="s02_year0_D",      cam="D", s0=0,   s1=0,   dur=9.0),
 dict(name="s03_summer_A",     cam="A", s0=0,   s1=1,   dur=13.0),
 dict(name="s04_summer_B",     cam="B", s0=.9,  s1=1.1, dur=8.0),
 dict(name="s05_fall_A",       cam="A", s0=1.1, s1=2,   dur=11.0),
 dict(name="s06_fall_B",       cam="B", s0=1.6, s1=2.2, dur=9.0),
 dict(name="s07_winter_D",     cam="D", s0=2.2, s1=3,   dur=11.0),
 dict(name="s08_winter_E",     cam="E", s0=3,   s1=3,   dur=6.0),
 dict(name="diag_freeze",      cam=None, s0=3,  s1=3,   dur=34.0),
 dict(name="s09_y2to5_A",      cam="A", s0=3,   s1=4,   dur=14.0),
 dict(name="s10_y2to5_E",      cam="E", s0=3.4, s1=4.3, dur=12.0),
 dict(name="s11_y5to20_A",     cam="A", s0=4,   s1=5,   dur=17.0),
 dict(name="s12_y5to20_D",     cam="D", s0=4.3, s1=5.2, dur=12.0),
 dict(name="s13_sign_C",       cam="C", s0=4.2, s1=5.4, dur=12.0),
 dict(name="s14_burrow_B",     cam="B", s0=5,   s1=5,   dur=7.0),
 dict(name="s15_y20to50_D",    cam="D", s0=5,   s1=6,   dur=15.0),
 dict(name="s16_overpass_F",   cam="F", s0=5,   s1=6,   dur=13.0),
 dict(name="s17_close_G",      cam="G", s0=6,   s1=6,   dur=27.0),
 dict(name="end_card",         cam=None, s0=6,  s1=6,   dur=12.0),
]
