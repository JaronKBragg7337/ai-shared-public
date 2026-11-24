"""MSI remote screen. Disabled unless state/remote.enable exists; remote.disable always wins."""
import asyncio, ctypes, json, os, time, datetime, urllib.request, urllib.error
from pathlib import Path
from fractions import Fraction
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack, RTCConfiguration, RTCIceServer
from av import VideoFrame
import mss

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / 'state'

def enabled(): return (STATE / 'remote.enable').is_file() and not (STATE / 'remote.disable').exists()
def log(s):
    with (STATE / 'remote-sessions.log').open('a', encoding='utf-8') as f: f.write(datetime.datetime.now().astimezone().isoformat() + ' ' + s + '\n')
def env():
    values = {}
    for line in (Path.home() / '.secrets' / 'keys.env').read_text(encoding='utf-8').splitlines():
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1); values[k.strip()] = v.strip()
    return values

def request(url, key, token, method='GET', data=None):
    headers = {'apikey': key, 'Authorization': 'Bearer ' + token, 'Content-Type':'application/json'}
    req = urllib.request.Request(url, json.dumps(data).encode() if data is not None else None, headers, method=method)
    with urllib.request.urlopen(req, timeout=10) as r: return json.loads(r.read() or b'null')

def buzz(e):
    try:
        req = urllib.request.Request('https://ntfy.sh/' + e['NTFY_TOPIC'], b'Remote screen session started on the MSI.', {'Title':'Remote screen'})
        urllib.request.urlopen(req, timeout=5).close()
    except Exception: log('notification failed')

# Explicit Win32 INPUT layout; SendInput handles Unicode without a keyboard layout assumption.
ULONG_PTR = ctypes.c_size_t
class MOUSEINPUT(ctypes.Structure): _fields_ = [('dx',ctypes.c_long),('dy',ctypes.c_long),('mouseData',ctypes.c_ulong),('dwFlags',ctypes.c_ulong),('time',ctypes.c_ulong),('dwExtraInfo',ULONG_PTR)]
class KEYBDINPUT(ctypes.Structure): _fields_ = [('wVk',ctypes.c_ushort),('wScan',ctypes.c_ushort),('dwFlags',ctypes.c_ulong),('time',ctypes.c_ulong),('dwExtraInfo',ULONG_PTR)]
class HARDWAREINPUT(ctypes.Structure): _fields_ = [('uMsg',ctypes.c_ulong),('wParamL',ctypes.c_ushort),('wParamH',ctypes.c_ushort)]
class UNION(ctypes.Union): _fields_ = [('mi',MOUSEINPUT),('ki',KEYBDINPUT),('hi',HARDWAREINPUT)]
class INPUT(ctypes.Structure): _anonymous_ = ('u',); _fields_ = [('type',ctypes.c_ulong),('u',UNION)]
def send(i):
    if ctypes.windll.user32.SendInput(1, ctypes.byref(i), ctypes.sizeof(INPUT)) != 1: raise OSError('SendInput failed')
def mouse(flags, dx=0, dy=0, data=0): send(INPUT(type=0, mi=MOUSEINPUT(dx,dy,data & 0xffffffff,flags,0,0)))
def key(vk, up=False, scan=0, unicode=False): send(INPUT(type=1, ki=KEYBDINPUT(vk,scan,(2 if up else 0) | (4 if unicode else 0),0,0)))
def inject(m):
    t = m.get('type')
    if t == 'move': mouse(1, max(-120,min(120,int(m['x']))), max(-120,min(120,int(m['y']))))
    elif t == 'click':
        a,b = (8,16) if m.get('button') == 'right' else (2,4); mouse(a); mouse(b)
    elif t == 'scroll': mouse(0x800, data=max(-600,min(600,int(m['amount']))))
    elif t == 'text':
        raw = str(m.get('text',''))[:512].encode('utf-16-le')
        for i in range(0,len(raw),2):
            unit = int.from_bytes(raw[i:i+2], 'little'); key(0,scan=unit,unicode=True); key(0,up=True,scan=unit,unicode=True)
    elif t == 'key':
        vk = {'Enter':13,'Backspace':8,'Escape':27,'Tab':9,'c':67,'v':86}.get(m.get('key'))
        if vk:
            ctrl = m.get('ctrl') is True and vk in (67,86)
            if ctrl: key(17)
            try: key(vk); key(vk,True)
            finally:
                if ctrl: key(17,True)

class POINT(ctypes.Structure): _fields_ = [('x', ctypes.c_long), ('y', ctypes.c_long)]
# 10/27 (Jaron): screen grabs leave out the mouse, so draw a big visible pointer where the cursor is.
BLACK, GOLD = bytes((0, 0, 0)), bytes((0x30, 0xc8, 0xff))
CURSOR = [(dx, dy) for dy in range(0, 48) for dx in range(0, dy // 2 + 1)]   # simple arrow, tip at the cursor
def draw_cursor(buf, w, h, left, top):
    pt = POINT(); ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    cx, cy = pt.x - left, pt.y - top
    for dx, dy in CURSOR:
        x, y = cx + dx, cy + dy
        if 0 <= x < w and 0 <= y < h:
            edge = dx == 0 or dx == dy // 2 or dy == 47
            i = (y * w + x) * 4
            buf[i:i + 3] = BLACK if edge else GOLD   # black outline, gold fill (BGR)
    return buf

class Screen(VideoStreamTrack):
    def __init__(self):
        super().__init__()
        self.zoom = True
        self.region = None
        self.next_frame = time.monotonic()
        self.frame_number = 0

    async def recv(self):
        await asyncio.sleep(max(0, self.next_frame - time.monotonic()))
        self.next_frame = max(self.next_frame + 1 / 15, time.monotonic())
        with mss.mss() as capture:
            mon = capture.monitors[1]
            pt = POINT(); ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
            w = min(1280, mon['width']) if self.zoom else mon['width']
            h = min(800, mon['height']) if self.zoom else mon['height']
            left = max(mon['left'], min(pt.x - w // 2, mon['left'] + mon['width'] - w)) if self.zoom else mon['left']
            top = max(mon['top'], min(pt.y - h // 2, mon['top'] + mon['height'] - h)) if self.zoom else mon['top']
            self.region = (left, top, w, h)
            shot = capture.grab({'left': left, 'top': top, 'width': w, 'height': h})
            buf = draw_cursor(bytearray(shot.bgra), w, h, left, top)
            frame = VideoFrame(w, h, 'bgra')
            frame.planes[0].update(bytes(buf))
            scale = min(1, 960 / w, 600 / h)
            frame = frame.reformat(width=max(2, int(w * scale) // 2 * 2), height=max(2, int(h * scale) // 2 * 2), format='yuv420p')
        frame.pts, frame.time_base = self.frame_number, Fraction(1, 15)
        self.frame_number += 1
        return frame

    def point(self, x, y):
        if self.region:
            left, top, w, h = self.region
            x = max(0, min(1, float(x))); y = max(0, min(1, float(y)))
            ctypes.windll.user32.SetCursorPos(left + round(x * (w - 1)), top + round(y * (h - 1)))

ICE = {"at": 0, "servers": None}
def ice_servers(e):
    """10/27: Cloudflare TURN so cellular phones can connect. Short-lived creds (24 h), refreshed every 6 h and
    published to table remote_ice (admin-only) for the phone page."""
    if ICE["servers"] and time.time() - ICE["at"] < 6 * 3600: return ICE["servers"]
    try:
        u = "https://rtc.live.cloudflare.com/v1/turn/keys/%s/credentials/generate-ice-servers" % e["CF_TURN_KEY_ID"]
        r = urllib.request.urlopen(urllib.request.Request(u, json.dumps({"ttl": 86400}).encode(),
            {"Authorization": "Bearer " + e["CF_TURN_KEY_TOKEN"], "Content-Type": "application/json", "User-Agent": "hb-remote-agent/1"}, method="POST"), timeout=15)
        servers = json.load(r)["iceServers"]
        servers = servers if isinstance(servers, list) else [servers]
        base, sr = e["SUPABASE_URL"].rstrip("/"), e["SUPABASE_SERVICE_ROLE_KEY"]
        body = json.dumps({"id": 1, "servers": servers, "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}).encode()
        urllib.request.urlopen(urllib.request.Request(base + "/rest/v1/remote_ice?on_conflict=id", body,
            {"apikey": sr, "Authorization": "Bearer " + sr, "Content-Type": "application/json", "User-Agent": "hb-remote-agent/1",
             "Prefer": "resolution=merge-duplicates"}, method="POST"), timeout=15)
        ICE.update(at=time.time(), servers=servers)
    except Exception as ex: log("turn refresh failed: " + type(ex).__name__)
    return ICE["servers"]

def rtc_config(e):
    out = [RTCIceServer(urls="stun:stun.cloudflare.com:3478")]
    for sv in ice_servers(e) or []:
        out.append(RTCIceServer(urls=sv["urls"], username=sv.get("username"), credential=sv.get("credential")))
    return RTCConfiguration(iceServers=out)

async def run_session(row, e):
    base, sr = e['SUPABASE_URL'].rstrip('/'), e['SUPABASE_SERVICE_ROLE_KEY']
    token = row.get('token') or ''
    # The auth server validates the JWT; the same user JWT calls the existing admin RPC.
    user = await asyncio.to_thread(request, base+'/auth/v1/user', sr, token)
    admin = await asyncio.to_thread(request, base+'/rest/v1/rpc/is_admin', sr, token, 'POST', {})
    if not user or user.get('id') != row['user_id'] or admin is not True: raise ValueError('unauthorized offer')
    pc = RTCPeerConnection(rtc_config(e)); last = time.monotonic(); started = False
    try:
        screen = Screen(); pc.addTrack(screen)
        @pc.on('datachannel')
        def channel(ch):
            @ch.on('message')
            def message(raw):
                nonlocal last
                if not enabled() or not isinstance(raw,str) or len(raw)>4096: return
                try:
                    m = json.loads(raw)
                    if m.get('type') == 'stop': asyncio.create_task(pc.close()); return
                    if m.get('type') == 'view': screen.zoom = m.get('zoom') is True
                    elif m.get('type') == 'point': screen.point(m['x'], m['y'])
                    else: inject(m)
                    last = time.monotonic()
                except (ValueError, TypeError, KeyError, OSError): pass
        await pc.setRemoteDescription(RTCSessionDescription(sdp=row['offer']['sdp'], type='offer'))
        await pc.setLocalDescription(await pc.createAnswer())
        if not enabled(): return
        await asyncio.to_thread(request, base+'/rest/v1/remote_signals?id=eq.'+row['id'], sr, sr, 'PATCH', {'answer':{'type':pc.localDescription.type,'sdp':pc.localDescription.sdp},'status':'answered','token':None})
        started = True; log('start ' + row['id']); await asyncio.to_thread(buzz,e)
        while enabled() and time.monotonic()-last < 1800 and pc.connectionState not in ('failed','closed','disconnected'):
            await asyncio.sleep(1)
    finally:
        await pc.close()
        if started: log('stop ' + row['id'])
        try: await asyncio.to_thread(request, base+'/rest/v1/remote_signals?id=eq.'+row['id'], sr,sr,'PATCH',{'status':'closed','token':None})
        except Exception: log('could not close signal')

async def main():
    e = env(); base = e['SUPABASE_URL'].rstrip('/'); sr = e['SUPABASE_SERVICE_ROLE_KEY']
    while True:
        await asyncio.to_thread(ice_servers, e)
        if enabled():
            try:
                rows = await asyncio.to_thread(request, base+'/rest/v1/remote_signals?status=eq.waiting&order=created_at.asc&select=id,user_id,created_at,offer,token&limit=1',sr,sr)
                if rows:
                    row=rows[0]
                    created=datetime.datetime.fromisoformat(row['created_at'].replace('Z','+00:00'))
                    if (datetime.datetime.now(datetime.timezone.utc)-created).total_seconds() > 120: raise ValueError('expired offer')
                    await run_session(row,e)
            except Exception as ex:
                if 'row' in locals() and row:
                    try: await asyncio.to_thread(request,base+'/rest/v1/remote_signals?id=eq.'+row['id'],sr,sr,'PATCH',{'status':'rejected','token':None})
                    except Exception: pass
                    row=None
                log('offer rejected or service error: '+type(ex).__name__)
        await asyncio.sleep(2)
if __name__ == '__main__':
    # A named Windows mutex prevents two independently launched agents answering at once.
    mutex = ctypes.windll.kernel32.CreateMutexW(None, True, 'Local\\HeartbeatRemoteScreen')
    if not mutex or ctypes.windll.kernel32.GetLastError() == 183:
        raise SystemExit('Remote agent already running')
    try: asyncio.run(main())
    finally: ctypes.windll.kernel32.CloseHandle(mutex)

