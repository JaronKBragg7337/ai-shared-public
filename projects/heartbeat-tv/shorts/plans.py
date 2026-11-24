PLANS = {
 "coral": dict(dir="still-unknown/ep2-coral-castle", src="stillunknown-ep2-coral-castle-vertical.mp4", out="stillunknown-ep2-coral-castle-short.mp4",
               series="Still Unknown", voice="af_heart", delogo=[(16, 16, 76, 38)], w=400, keep="s1 s4 s8 s9 s10 s16 s17".split()),
}
SU = dict(series="Still Unknown", voice="af_heart", delogo=[(16, 16, 76, 38)])
PLANS["dark"] = dict(SU, dir="still-unknown/ep1-dark-energy", src="stillunknown-ep1-dark-energy-vertical.mp4", out="stillunknown-ep1-dark-energy-short.mp4", keep="s1 s3 s4 s6 s8 s11 s12".split())
PLANS["gob"] = dict(dir="lost-places/ep1-gobekli", src="lostplaces-ep1-gobekli-vertical.mp4", out="lostplaces-ep1-gobekli-short.mp4", series="Lost Places", voice="bm_george", delogo=[], w=170, keep="s1 s4 s5 s11".split())
PLANS["ai"] = dict(dir="ai-explained/ep1-consciousness", src="aiexplained-ep1-consciousness-vertical.mp4", out="aiexplained-ep1-consciousness-short.mp4", series="AI Explained", voice="bm_george", delogo=[], w=260, keep="a1 a2 a3 a5 a6 a15".split())
PLANS["earth"] = dict(dir="earth/ep1-oxygen", src="earth-ep1-oxygen-vertical.mp4", out="earth-ep1-oxygen-short.mp4", series="Earth", voice="bm_george", delogo=[], w=330, keep="s1 s3 s8 s10 s12".split())
PLANS["mmx"] = dict(dir="space-now/ep1-mmx", src="spacenow-ep1-mmx-vertical.mp4", out="spacenow-ep1-mmx-short.mp4", series="Space Now", voice="am_michael", delogo=[], w=260, keep="s1 s5 s6 s8".split())
PLANS["vib"] = dict(SU, dir="still-unknown/ep3-vibration-stone", src="stillunknown-ep3-vibration-stone-vertical.mp4", out="stillunknown-ep3-vibration-stone-short.mp4", keep="s1 s6 s7 s11 s14".split(), w=200)
PLANS["hwy"] = dict(dir="science-channel/ep4-highway-disappears", src="science-ep4-highway-disappears-vertical.mp4", out="science-ep4-highway-disappears-short.mp4", series="Science", voice="bm_george", off=1.0, plan_cmd=1, w=260, keep="n01 n02 n04 n09 n10".split())
PLANS["sci5"] = dict(dir="science-channel/ep5-commercial-roof", src="science-ep5-commercial-roof-vertical.mp4", out="science-ep5-commercial-roof-short.mp4", series="Science", voice="bm_george", off=1.0, plan_cmd=1, w=200, keep="n01 n03 n05 n06 n08 n12".split())
PLANS["sci6"] = dict(dir="science-channel/ep6-phobos", src="science-ep6-phobos-vertical.mp4", out="science-ep6-phobos-short.mp4", series="Science", voice="bm_george", off=1.0, plan_cmd=1, w=200, keep="n01 n02 n03 n04 n12".split(), trim={"n12": 2})
PLANS["sci7"] = dict(dir="science-channel/ep7-antarctica-ice-dna", src="science-ep7-antarctica-ice-vertical.mp4", out="science-ep7-antarctica-ice-short.mp4", series="Science", voice="bm_george", off=1.0, plan_cmd=1, w=200, keep="n01 n03 n09 n15".split())
OQ = dict(series="Open Questions", voice="bm_george", delogo=[])
PLANS["oq2"] = dict(OQ, dir="open-questions/ep2-no-brain", src="openquestions-ep2-no-brain-vertical.mp4", out="openquestions-ep2-no-brain-short.mp4", keep="s1 s2 s5 s6 s12".split(), w=160)
PLANS["oq3"] = dict(OQ, dir="open-questions/ep3-birthplace", src="openquestions-ep3-birthplace-vertical.mp4", out="openquestions-ep3-birthplace-short.mp4", keep="s1 s4 s5 s6 s13".split(), w=160)
PLANS["oq4"] = dict(OQ, dir="open-questions/ep4-gravity", src="openquestions-ep4-gravity-vertical.mp4", out="openquestions-ep4-gravity-short.mp4", keep="s1 s2 s6 s8 s12".split(), w=160)
PLANS["h5"] = dict(dir="history-channel/ep5-1816", src="history-ep5-1816-vertical.mp4", out="history-ep5-1816-short.mp4", series="History", voice="bm_george", delogo=[], keep="s1 s2 s3 s7".split(), w=170)
PLANS["an"] = dict(dir="animals/ep1-death", src="animals-ep1-death-vertical.mp4", out="animals-ep1-death-short.mp4", series="Animals", voice="bm_george", delogo=[], keep="s1 s3 s4 s9 s12".split(), w=170)
PLANS["su4"] = dict(SU, dir="still-unknown/ep4-voynich", src="stillunknown-ep4-voynich-vertical.mp4", out="stillunknown-ep4-voynich-short.mp4", keep="s1 s2 s3 s5 s15".split(), w=170)
PLANS["su5"] = dict(SU, dir="still-unknown/ep5-wow", src="stillunknown-ep5-wow-vertical.mp4", out="stillunknown-ep5-wow-short.mp4", keep="s1 s6 s8 s9 s15".split(), w=170)
