# Shot plan shared by build.py (Blender), diagram.py (Pillow) and finish.py (captions, mix). Durations in seconds.
FPS = 24
SHOTS = [
 dict(name="s01_pump",      cam="PUMP_A",    dur=18.0),   # n01
 dict(name="s02_desert",    cam="DESERT_A",  dur=28.5),   # n02
 dict(name="diag_murphy",   cam=None,        dur=35.0),   # n03
 dict(name="diag_shingo",   cam=None,        dur=14.0),   # n04
 dict(name="s03_springs",   cam="SPRINGS_A", dur=17.0),
 dict(name="diag_nozzles",  cam=None,        dur=18.5),   # n05
 dict(name="s04_neck",      cam="NECK_A",    dur=20.0),
 dict(name="s05_shifter",   cam="SHIFT_A",   dur=14.0),   # n06
 dict(name="diag_interlock", cam=None,       dur=14.0),
 dict(name="s06_micro",     cam="MICRO_A",   dur=25.0),   # n07
 dict(name="s07_sim",       cam="SIM_A",     dur=16.0),   # n08
 dict(name="s08_usbc",      cam="USB_A",     dur=20.5),   # n09
 dict(name="s09a_pump",     cam="PUMP_W",    dur=5.5),    # n10
 dict(name="s09b_shift",    cam="SHIFT_W",   dur=1.8),
 dict(name="s09c_micro",    cam="MICRO_W",   dur=1.8),
 dict(name="s09d_sim",      cam="SIM_W",     dur=1.8),
 dict(name="s09e_usb",      cam="USB_W",     dur=3.0),
 dict(name="s09f_desert",   cam="DESERT_Z",  dur=9.1),
 dict(name="end_card",      cam=None,        dur=12.0),
]
