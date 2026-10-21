import re
L = not PORT
# ---------------------------------------------------------------- Still Unknown shared scene kit (eps 4+), part A: helpers
# Same look as ep1-3 (ep_head.py): violet-black void, thin Segoe Light heads, Consolas data, status tags. Data-driven scenes.
def F(sid, f): return SEG[sid]['start'] + f * SEG[sid]['dur'] - BOUND[sid][0]
def ap(t, sid, f, d=0.8): return ease((t - F(sid, f)) / d)

def night(cv, tt, dim=0.5):
    for (x, y, r, b, ph) in STARS:
        tw = 0.65 + 0.35 * math.sin(tt * 1.1 + ph)
        cv.circ((x * W, y * H), r * 0.9, mix(TXT, BG, b * tw * dim))

def poly(cv, pts, fill): cv.d.polygon([cv.P(p) for p in pts], fill=fill)

def stone_card(cv, x, y, w, h, col, a=1.0):
    cv.rect((x, y, x + w, y + h), mix(INK, BG, a * 0.9)); cv.rect((x, y, x + 5, y + h), mix(col, BG, a))

def split_regions():
    """returns (text_x0, text_y0, text_w, art_rect) for rows scenes with an art panel."""
    x0, y0, x1, y1 = CONT
    if L: return x0, y0 + 10, (x1 - x0) * 0.58, (x0 + (x1 - x0) * 0.58 + 50, y0 - 10, x1, y1 - 20)
    return x0, y0 + 360, x1 - x0, (x0, y0 + 30, x1, y0 + 340)

def S_rows(sid, tags, rows, art=None, size=None):
    """tags: [(label,color,frac)] across the top; rows: [(label,color,text,frac)]; art(cv,t,R,sid)."""
    def fn(cv, t, p):
        night(cv, t, 0.5)
        x0, y0, x1, y1 = CONT
        xx = x0
        for lab, col, f in tags:
            w = tag(cv, xx, y0 - 40, lab, col, ap(t, sid, f) if f is not None else ease(t / 0.8), 20)
            xx += (w if w > 0 else 0) + 16
            if w <= 0: break
        tx, ty, tw, R = split_regions() if art else (x0, y0 + 10, x1 - x0, None)
        if not art and not L: tw = x1 - x0
        yy = ty
        sz = size or (36 if L else 32)
        for lab, col, txt, f in rows:
            aa = ap(t, sid, f)
            if aa > 0:
                tag(cv, tx, yy, lab, col, aa, 20)
                yy = cv.para(tx, yy + 50, txt, 'sans', sz, TXT, tw, 1.2, 'l', aa) + (22 if L else 16)
        if art: art(cv, t, R, sid)
    return fn

def S_table(sid, tags, rows, art=None, kw=250, size=None):
    """rows: [(key, text, color, frac, status_label_or_None, status_color)] key in mono left, text right."""
    def fn(cv, t, p):
        night(cv, t, 0.5)
        x0, y0, x1, y1 = CONT
        xx = x0
        for lab, col, f in tags:
            w = tag(cv, xx, y0 - 40, lab, col, ap(t, sid, f) if f is not None else ease(t / 0.8), 20)
            xx += (w if w > 0 else 0) + 16
            if w <= 0: break
        top = y0 + 10
        if art:
            if L: R = (x0, y0 + 10, x1, y0 + 250); top = y0 + 280
            else: R = (x0, y0 + 10, x1, y0 + 250); top = y0 + 270
            art(cv, t, R, sid)
        n = len(rows)
        rh = ((y1 - top) / max(n, 1)) if L else ((y1 - top) / max(n, 1))
        rh = min(rh, 110 if L else 150)
        for i, (k, txt, col, f, st, stc) in enumerate(rows):
            aa = ap(t, sid, f); yy = top + i * rh
            if aa <= 0: continue
            hline(cv, x0, x1, yy - 8, INK2, aa, 1)
            mono(cv, x0 + 6, yy + 4, k, 26 if L else 24, col, aa)
            sz = size or (30 if L else 28)
            if L:
                tw = (x1 - x0 - kw - (260 if st else 0))
                cv.para(x0 + kw, yy, txt, 'sans', sz, TXT, tw, 1.15, 'l', aa)
                if st: tag(cv, x1 - 10, yy + 2, st, stc, aa, 18, 'r')
            else:
                cv.para(x0 + 6, yy + 34, txt, 'sans', sz, TXT, x1 - x0 - 12, 1.15, 'l', aa)
                if st: tag(cv, x1 - 6, yy - 2, st, stc, aa, 16, 'r')
    return fn

def S_title(sid, ep_no, lines_land, lines_port, sub, tags, art=None):
    def fn(cv, t, p):
        night(cv, t, 0.9)
        y0 = 300 if PORT else 250
        mono(cv, HEAD[0], y0, f'HEARTBEAT TV  /  CH 10  /  STILL UNKNOWN  /  EP {ep_no:02d}', 28 if PORT else 26, CYAN, ease(t / 1.0))
        sz = 100 if PORT else 118
        lines = lines_port if PORT else lines_land
        for k, l in enumerate(lines): big(cv, HEAD[0], y0 + 60 + k * sz * 1.05, l, sz, TXT, ease((t - 0.3 - k * 0.25) / 1.2))
        yy = y0 + 60 + len(lines) * sz * 1.05 + 40
        mono(cv, HEAD[0], yy, sub, 24, DIM, ease((t - 1.5) / 1.0))
        ty = yy + 70; x = HEAD[0]
        for i, (lab, col, f) in enumerate(tags):
            aa = ap(t, sid, f, 0.8)
            if PORT: tag(cv, HEAD[0], ty + i * 62, lab, col, aa)
            else:
                w = tag(cv, x, ty, lab, col, aa); x += (w if w > 0 else 0) + 20
        if art and L: art(cv, t, (1100, 150, W - 60, 900), sid)
    return fn

def S_close(sid, l1, l2, tg1, tg2, last, art=None):
    def fn(cv, t, p):
        night(cv, t, 0.7)
        x0, y0, x1, y1 = CONT
        sz = 120 if L else 100
        big(cv, x0, y0 + 20, l1, sz, TXT, ap(t, sid, 0.30))
        big(cv, x0, y0 + 20 + sz * 1.2, l2, sz, TXT, ap(t, sid, 0.42))
        tag(cv, x0, y0 + 20 + sz * 2.6, tg1, ROSE, ap(t, sid, 0.34), 24); tag(cv, x0 + 330, y0 + 20 + sz * 2.6, tg2, MINT, ap(t, sid, 0.46), 24)
        cv.para(x0, y0 + 20 + sz * 3.4, last, 'light', 36 if L else 34, CYAN, x1 - x0, 1.25, 'l', ap(t, sid, 0.7, 1.2))
        if art: art(cv, t, (1300, 100, W - 60, 800) if L else (600, 1050, W - 60, 1300), sid)
    return fn

def sc_end(cv, t, p):
    night(cv, t, 0.7)
    a = ease(t / 1.0)
    y = 160 if PORT else 70
    mono(cv, HEAD[0], y, 'HEARTBEAT TV  /  CH 10', 26, CYAN, a)
    big(cv, HEAD[0], y + 40, 'still unknown', 110, TXT, a)
    mono(cv, HEAD[0], y + 170, 'heartbeatobservatory.com', 34, CYAN, a)
    yy = y + 240
    mono(cv, HEAD[0], yy, 'SOURCES', 22, DIM, ease((t - 0.6) / 1)); yy += 40
    for i, s in enumerate(SOURCES):
        yy = cv.para(HEAD[0], yy, s, 'mono', 21 if PORT else 22, TXT, (W - 2 * HEAD[0]) * (1 if PORT else 0.95), 1.25, 'l', ease((t - 0.8 - i * 0.15) / 0.8)) + 10

def rrect(cv, b, fill, edge=None, a=1.0, w=2):
    cv.rect(b, mix(fill, BG, a));
    if edge: cv.outline(b, mix(edge, BG, a), w)
