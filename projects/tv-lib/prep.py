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
# music bed: slow minor-key pad (Am - F - C - G), soft, generated here (CC0)
sr=44100; n=int(total*sr); x=np.arange(n)/sr
chords=[[220.0,261.63,329.63],[174.61,220.0,261.63],[130.81,164.81,196.0,261.63],[196.0,246.94,293.66]]
L=np.zeros(n); R=np.zeros(n); bar=8.0
for i in range(int(total/bar)+2):
    t0=i*bar; a=int(t0*sr); b=min(n,int((t0+bar+1.5)*sr))
    if a>=n: break
    tt=np.arange(b-a)/sr; env=np.minimum(1,tt/2.0)*np.minimum(1,(bar+1.5-tt)/1.5)
    for k,f in enumerate(chords[i%4]):
        for det,pan in ((0.997,0.35),(1.003,0.65)):
            w=np.sin(2*np.pi*f*det*tt+k)*env*0.05*(1+0.3*np.sin(2*np.pi*0.11*tt+k))
            L[a:b]+=w*(1-pan); R[a:b]+=w*pan
        bass=np.sin(2*np.pi*(f/2)*tt)*env*0.03; L[a:b]+=bass; R[a:b]+=bass
fade=np.minimum(1,x/2.0)*np.minimum(1,(total-x)/2.5)
st=np.stack([L*fade,R*fade],1); st=st/np.abs(st).max()*0.9
with wave.open('audio/music.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st*32767).astype('<i2').tobytes())
print('total',total)
