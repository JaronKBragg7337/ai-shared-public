# trims the Kokoro clips, lays them on a timeline, writes timeline.json + voice.wav + music.wav
import json, subprocess, numpy as np, wave
GAP, LEAD, TAIL = 0.4, 0.7, 2.8
segs = json.load(open("script.json"))
t = LEAD; tl = []
for s in segs:
    out = f"audio/t_{s['id']}.wav"
    subprocess.run(['ffmpeg','-y','-v','error','-i',f"audio/{s['id']}.wav",'-af',
      'silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.1,areverse',
      '-ar','24000','-ac','1',out],check=True)
    d = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out]))
    tl.append(dict(id=s['id'], start=round(t,3), dur=round(d,3), text=s['text'])); t += d + GAP
total = t - GAP + TAIL
json.dump(dict(total=round(total,3), segs=tl), open('timeline.json','w'), indent=1)
# voice track
cmd = ['ffmpeg','-y','-v','error']
for s in tl: cmd += ['-i', f"audio/t_{s['id']}.wav"]
fc = ''.join(f"[{i}]adelay={int(s['start']*1000)}:all=1[a{i}];" for i,s in enumerate(tl))
fc += ''.join(f"[a{i}]" for i in range(len(tl))) + f"amix=inputs={len(tl)}:normalize=0,loudnorm=I=-16:TP=-1.5,apad=whole_dur={total}[v]"
subprocess.run(cmd+['-filter_complex',fc,'-map','[v]','-ar','44100','-ac','2','audio/voice.wav'],check=True)
# music bed (AI Explained): soft synthesized glass-bell arpeggio over a low drone, D dorian, slow and sparse (CC0, generated here)
sr=44100; n=int(total*sr); x=np.arange(n)/sr
rng=np.random.default_rng(13)
L=np.zeros(n); R=np.zeros(n)
scale=[146.83,164.81,174.61,196.0,220.0,246.94,261.63,293.66,329.63,349.23,392.0]
pat=[0,2,4,2,5,4,2,1, 0,3,5,3,6,5,3,2]
step=0.9; k=0; t0=0.0
while t0<total:
    f=scale[pat[k%len(pat)]+ (3 if (k//16)%2 else 0)]; a=int(t0*sr); ln=int(2.6*sr); b=min(n,a+ln)
    if a>=n: break
    tt=np.arange(b-a)/sr; env=np.exp(-tt*2.1)*np.minimum(1,tt/0.01)
    w=(np.sin(2*np.pi*f*tt)+0.35*np.sin(2*np.pi*f*2.76*tt)*np.exp(-tt*5)+0.2*np.sin(2*np.pi*f*5.4*tt)*np.exp(-tt*9))*env*0.11
    pan=0.25+0.5*((k*0.37)%1.0); L[a:b]+=w*(1-pan); R[a:b]+=w*pan
    t0+=step; k+=1
for f,g in ((73.42,0.05),(110.0,0.03),(146.83,0.02)):
    d=np.sin(2*np.pi*f*x)*(1+0.2*np.sin(2*np.pi*0.07*x+f))*g; L+=d; R+=d
fade=np.minimum(1,x/2.5)*np.minimum(1,(total-x)/3.0)
st=np.stack([L*fade,R*fade],1); st=st/np.abs(st).max()*0.9
with wave.open('audio/music.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st*32767).astype('<i2').tobytes())
print('total',total)
