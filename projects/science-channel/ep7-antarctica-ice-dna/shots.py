# Shot plan shared by build.py (Blender), diagram.py (Pillow) and finish.py (captions, mix). Durations in seconds.
# Blender cameras are named SET_X (see build.py for the sets). "diag_*" and "end_card" are Pillow frames in the same range.
FPS = 24
SHOTS = [
 dict(name="s01_field",      cam="FIELD_A",   dur=14.0),   # n01
 dict(name="s02_chunk",      cam="CHUNK_A",   dur=15.0),
 dict(name="s03_cores",      cam="CORES_A",   dur=15.0),   # n02
 dict(name="diag_layers",    cam=None,        dur=22.5),
 dict(name="s04_sea",        cam="SEA_A",     dur=19.0),   # n03
 dict(name="s05_diatoms",    cam="DIATOM_A",  dur=19.5),
 dict(name="diag_dna",       cam=None,        dur=18.0),   # n04
 dict(name="s06_clay",       cam="MICRO_A",   dur=16.5),
 dict(name="s07_transform",  cam="MICRO_B",   dur=32.0),   # n05
 dict(name="s08_divide",     cam="MICRO_C",   dur=35.0),   # n06
 dict(name="diag_revive",    cam=None,        dur=36.0),   # n07
 dict(name="diag_siberia",   cam=None,        dur=24.0),   # n08
 dict(name="s09_whillans",   cam="LAKE_A",    dur=28.0),   # n09
 dict(name="s10_mercer",     cam="LAKE_B",    dur=31.5),   # n10
 dict(name="s11_shelf",      cam="SHELF_A",   dur=16.0),   # n11
 dict(name="diag_map",       cam=None,        dur=24.0),
 dict(name="diag_risk",      cam=None,        dur=18.0),   # n12
 dict(name="s12_shore",      cam="SHELF_B",   dur=16.0),
 dict(name="s13_bergs",      cam="SHELF_C",   dur=16.0),   # n13
 dict(name="diag_treaty",    cam=None,        dur=20.0),
 dict(name="diag_jobs",      cam=None,        dur=18.0),   # n14
 dict(name="s14_station",    cam="STATION_A", dur=15.0),
 dict(name="s15_end",        cam="FIELD_Z",   dur=26.0),   # n15
 dict(name="end_card",       cam=None,        dur=14.0),
]
