# Shared numbers for the Pioneer/truck space scenes (Unreal cm; X forward, Y right, Z up; left-handed like Unreal).
# Pioneer local frame: +X = high-gain dish axis (points at Earth). Spin is about +X.
import math
# dish (2.74 m)
DISH_R = 137.0; DISH_DEPTH = 40.0; DISH_X0 = -12.0           # vertex (centre back of the bowl) at x = -12
DISH_F = DISH_R ** 2 / (4 * DISH_DEPTH)                       # focal length ~117 cm
DISH_T = 3.0
def dish_x(r): return DISH_X0 + r * r / (4 * DISH_F)          # front (concave) surface
# hexagonal equipment bus: 71 cm sides (circumradius 71), 36 cm tall, behind the dish
BUS_R = 71.0; BUS_X1 = -20.0; BUS_X0 = -56.0; BUS_XM = (BUS_X0 + BUS_X1) / 2
BOOM_X = -40.0
RTG_PHI = (90.0, 210.0); MAG_PHI = 330.0                       # booms 120 deg apart around the spin axis
RTG_BOOM_END = 300.0; RTG_LEN = 40.0; RTG_RC = 11.0; RTG_RF = 24.0
RTG_CENTERS = (208.0, 258.0)                                   # two SNAP-19 RTGs per boom, end to end
MAG_END = 660.0                                                # magnetometer ~6.6 m from centre
# struts from the bus top corners to the dish back; plaque between two of them
STRUT_R_DISH = 105.0
PLAQUE_W = 23.0; PLAQUE_H = 15.0   # W runs around the spin axis (tangential), H along the axis
PLAQUE_PHI = 0.0           # angle (around X) of the plaque's outward normal
PLAQUE_X = -11.0
def strut_r_at(x):         # strut runs from (BUS_X1, BUS_R) to (dish back at STRUT_R_DISH)
    xd = dish_x(STRUT_R_DISH) - DISH_T
    t = (x - BUS_X1) / (xd - BUS_X1)
    return BUS_R + t * (STRUT_R_DISH - BUS_R)
# plaque centre: on the chord between struts at phi = +-30 deg, pushed 2 cm out
PLAQUE_RAD = strut_r_at(PLAQUE_X) * math.cos(math.radians(30)) + 2.0
def ydir(phi):  # unit vector in the local Y-Z plane
    a = math.radians(phi); return (0.0, math.cos(a), math.sin(a))
def local(x, phi, r):
    d = ydir(phi); return (x, d[1] * r, d[2] * r)
PLAQUE_C = local(PLAQUE_X, PLAQUE_PHI, PLAQUE_RAD)
# anchors for on-screen labels (Pioneer local)
ANCH = {"bus": (BUS_XM, 0.0, 0.0), "rtg1": local(BOOM_X, RTG_PHI[0], 233.0), "rtg2": local(BOOM_X, RTG_PHI[1], 233.0),
        "mag": local(BOOM_X, MAG_PHI, 600.0), "plaque": PLAQUE_C, "dish": (dish_x(80), 0.0, 0.0)}
# truck (truck local: X forward, origin on the ground under the middle)
TRK_ROOFDISH_PIVOT = (-40.0, 0.0, 338.0)
TRK_NOZZLE = (-612.0, 0.0, 185.0)
