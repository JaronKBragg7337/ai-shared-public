# foot-lock speed: the actor moves so the planted (lower) foot stays still on the floor -> speed profile per clip (cm/s, 120 Hz)
import json, numpy as np
d = json.load(open('feet.json'))
def profile(n, axis=1):
    F = d[n]['frames']; t = np.array([f['t'] for f in F]); l = np.array([f['l'] for f in F]); r = np.array([f['r'] for f in F])
    dt = np.gradient(t)
    vl = -np.gradient(l[:, axis]) / dt; vr = -np.gradient(r[:, axis]) / dt
    # soft weight by height: lower foot dominates
    zl, zr = l[:, 2], r[:, 2]; k = 1.5
    wl = 1 / (1 + np.exp((zl - zr) / k)); v = wl * vl + (1 - wl) * vr
    v = np.convolve(v, np.ones(13) / 13, mode='same')
    return t, v
if __name__ == '__main__':
    out = {}
    for n in d:
        ax = 0 if 'LR' in n or 'RL' in n else 1
        t, v = profile(n, ax); out[n] = {"t": t.tolist(), "v": v.tolist(), "axis": ax}
        print(n, 'mean %.1f' % v.mean(), ' '.join('%.0f' % x for x in v[::12]))
    json.dump(out, open('speeds.json', 'w'))
