# Shot plan shared by build.py (Blender), diagram.py (Pillow) and finish.py (captions, mix). Durations in seconds.
FPS = 24
SHOTS = [
 dict(name="s01_earth",     cam="EARTH_A",   dur=26.0),   # n01
 dict(name="diag_three",    cam=None,        dur=33.5),   # n02
 dict(name="s02_plate",     cam="PLATE_A",   dur=17.0),   # n03
 dict(name="diag_law",      cam=None,        dur=18.5),
 dict(name="s03_station",   cam="STATION_A", dur=14.0),   # n04
 dict(name="s04_radwing",   cam="STATION_B", dur=13.5),
 dict(name="diag_suit",     cam=None,        dur=32.0),   # n05
 dict(name="s05_sat",       cam="SAT_A",     dur=18.0),   # n06
 dict(name="diag_orbitdc",  cam=None,        dur=24.0),
 dict(name="diag_radiator", cam=None,        dur=24.0),   # n07
 dict(name="s06_fins",      cam="SAT_B",     dur=16.0),
 dict(name="diag_debate",   cam=None,        dur=25.5),   # n08
 dict(name="s07_end",       cam="EARTH_Z",   dur=30.0),   # n09
 dict(name="end_card",      cam=None,        dur=12.0),
]
