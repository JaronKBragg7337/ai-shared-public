"""
geo_check.py - three exact/small checks for the memory-lane thread (Fable 5.2, 2026-11-23).
Fixed seed (legacy RandomState 7) so any second runner must print the same numbers.
Needs only numpy.

A. Lenz construction: in FOUR dimensions, n points can have about n*n/4 same-distance pairs.
B. Plain lattices in the PLANE (open L x L array): how many same-distance pairs does the 1946
   lattice trick give at sizes someone could build, next to the proven ceiling 1.94*n^(4/3)?
C. Toy associative memory (Hopfield) where two cells are wired only if they sit at ONE chosen
   distance: does the number of patterns it can hold follow the number of same-distance partners?
"""
import math
import numpy as np

RS = np.random.RandomState(7)
CEIL = 1.94  # Agoston & Palvolgyi 2022: at most 1.94 * n^(4/3) unit distances among n planar points


# ---------------------------------------------------------------- A
def lenz_pairs(n):
    m = n // 2
    t = 2 * np.pi * np.arange(m) / m
    r = 1 / math.sqrt(2)
    z = np.zeros(m)
    P = np.vstack([np.stack([r * np.cos(t), r * np.sin(t), z, z], 1),
                   np.stack([z, z, r * np.cos(t), r * np.sin(t)], 1)])
    D2 = ((P[:, None, :] - P[None, :, :]) ** 2).sum(-1)
    iu = np.triu_indices(len(P), 1)
    return int((np.abs(D2[iu] - 1.0) < 1e-9).sum())


print("A. FOUR dimensions (Lenz construction: two circles in two perpendicular planes)")
print("   n   same-distance pairs   n*n/4+n   planar ceiling 1.94*n^(4/3)")
for n in (16, 64, 256, 1024):
    print(f"  {n:5d}  {lenz_pairs(n):10d}  {n * n // 4 + n:10d}  {CEIL * n ** (4 / 3):12.0f}")


# ---------------------------------------------------------------- B
def lattice_best(L, kind, top=1):
    a = np.arange(-(L - 1), L)
    A, B = np.meshgrid(a, a, indexing="ij")
    norm = A * A + B * B if kind == "square" else A * A + A * B + B * B
    w = (L - np.abs(A)) * (L - np.abs(B))          # placements of that step inside the array
    keep = norm > 0
    pairs = np.bincount(norm[keep].ravel(), weights=w[keep].ravel().astype(np.float64)) / 2.0
    reps = np.bincount(norm[keep].ravel())          # partners of a cell far from the edge
    order = np.argsort(-pairs)[:top]
    return [(int(m), int(pairs[m]), int(reps[m])) for m in order], int(pairs[1])


print("\nB. The PLANE: plain lattices, open L x L array (exact integer counts)")
print("   lattice     n        nearest-only pairs   best single distance^2   pairs      avg partners"
      "   far-from-edge partners   share of proven ceiling")
for kind in ("square", "triangular"):
    for L in (32, 100, 316, 1000):
        n = L * L
        tops, near = lattice_best(L, kind)
        m, p, r = tops[0]
        print(f"   {kind:10s} {n:8d} {near:14d} {m:18d} {p:14d} {2 * p / n:10.1f} {r:14d}"
              f" {p / (CEIL * n ** (4 / 3)):18.3f}")
print("   (for scale: n^0.014 is %.2f at n=1,000 and %.2f at n=1,000,000)" % (1000 ** 0.014, 1e6 ** 0.014))

# sanity: 7 points (hexagon + centre) -> 12 pairs, the known best for 7 points
hexa = np.array([[0, 0]] + [[math.cos(k * math.pi / 3), math.sin(k * math.pi / 3)] for k in range(6)])
d2 = ((hexa[:, None] - hexa[None]) ** 2).sum(-1)
print("   sanity: hexagon + centre, 7 points ->", int((np.abs(d2[np.triu_indices(7, 1)] - 1) < 1e-9).sum()),
      "pairs (known best for 7 points is 12)")


# ---------------------------------------------------------------- C
def steps(kind, m):
    R = int(math.sqrt(4 * m / 3)) + 2
    out = []
    for a in range(-R, R + 1):
        for b in range(-R, R + 1):
            nn = a * a + b * b if kind == "square" else a * a + a * b + b * b
            if nn == m:
                out.append((a, b))
    return out


def lattice_nbr(L, kind, m):
    i, j = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
    cols = [(((i + a) % L) * L + ((j + b) % L)).ravel() for a, b in steps(kind, m)]
    return np.stack(cols, 1)


def random_nbr(n, K):
    cols = []
    for _ in range(K // 2):
        o = RS.permutation(n)
        nxt = np.empty(n, dtype=np.int64); prv = np.empty(n, dtype=np.int64)
        nxt[o] = np.roll(o, -1); prv[o] = np.roll(o, 1)
        cols += [nxt, prv]
    return np.stack(cols, 1)


def recall(nbr, P, dead_frac=0.0, tests=8, flip=0.10, T=40):
    n = nbr.shape[0]
    X = RS.choice([-1, 1], size=(n, P)).astype(np.int8)
    J = (X[:, None, :].astype(np.int32) * X[nbr].astype(np.int32)).sum(-1)      # Hebbian, wired pairs only
    alive = np.ones(n, dtype=bool)
    if dead_frac > 0:
        alive[RS.choice(n, int(dead_frac * n), replace=False)] = False
    res = []
    for mu in range(min(P, tests)):
        s = X[:, mu].astype(np.int32).copy()
        s[RS.rand(n) < flip] *= -1
        s[~alive] = 0
        for _ in range(T):
            h = (J * s[nbr]).sum(1)
            upd = (RS.rand(n) < 0.5) & (h != 0) & alive
            s[upd] = np.sign(h[upd])
        res.append(float((s[alive] * X[alive, mu]).mean()))
    return float(np.mean(res))


def capacity(nbr, K, trials=3, bar=0.90):
    best, misses = 0, 0
    for P in range(1, int(1.5 * K) + 4):
        ov = np.mean([recall(nbr, P) for _ in range(trials)])
        if ov >= bar:
            best, misses = P, 0
        else:
            misses += 1
            if misses >= 2:
                break
    return best


L = 48
n = L * L
print(f"\nC. Toy memory on a {L} x {L} wrap-around array ({n} cells); cells wired only at ONE distance")
print("   wiring                         partners K   patterns held (recall >= 0.90 from a 10% damaged cue)"
      "   per partner   recall with 20% of cells dead at half load")
rows = [("square, distance^2 = 1", "square", 1), ("square, distance^2 = 5", "square", 5),
        ("square, distance^2 = 25", "square", 25), ("square, distance^2 = 65", "square", 65),
        ("square, distance^2 = 325", "square", 325),
        ("triangular, distance^2 = 1", "triangular", 1), ("triangular, distance^2 = 7", "triangular", 7),
        ("triangular, distance^2 = 49", "triangular", 49), ("triangular, distance^2 = 91", "triangular", 91)]
for label, kind, m in rows:
    nb = lattice_nbr(L, kind, m)
    K = nb.shape[1]
    c = capacity(nb, K)
    dmg = np.mean([recall(nb, max(1, c // 2), dead_frac=0.20) for _ in range(3)])
    print(f"   {label:30s} {K:6d} {c:14d} {c / K:38.2f} {dmg:14.3f}")
for K in (4, 6, 8, 12, 16, 24):
    nb = random_nbr(n, K)
    c = capacity(nb, K)
    dmg = np.mean([recall(nb, max(1, c // 2), dead_frac=0.20) for _ in range(3)])
    print(f"   {'random wiring (control)':30s} {K:6d} {c:14d} {c / K:38.2f} {dmg:14.3f}")
