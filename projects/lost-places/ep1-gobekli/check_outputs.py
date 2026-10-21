"""Independent final-file checks: real streams/durations, complete decode, audio levels.
Writes only inside this episode folder. Never changes the delivered files.
"""
import subprocess,json,math
from pathlib import Path
files=['lostplaces-ep1-gobekli.mp4','lostplaces-ep1-gobekli-vertical.mp4']
expected=json.loads(Path('timeline.json').read_text())['total']
results=[]
for name in files:
    raw=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',name]))
    video=next(s for s in raw['streams'] if s['codec_type']=='video')
    aud=next(s for s in raw['streams'] if s['codec_type']=='audio')
    duration=float(raw['format']['duration']);assert 240<=duration<=420,(name,duration)
    assert abs(duration-expected)<.15,(duration,expected)
    assert video['codec_name']=='h264' and aud['codec_name']=='aac'
    w,h=video['width'],video['height']
    assert (w,h)==((1080,1920) if 'vertical' in name else (1280,720))
    decode=subprocess.run(['ffmpeg','-v','error','-threads','2','-i',name,'-f','null','-'],capture_output=True,text=True)
    assert decode.returncode==0 and not decode.stderr.strip(),decode.stderr
    levels=subprocess.run(['ffmpeg','-v','info','-i',name,'-vn','-af','volumedetect','-f','null','-'],capture_output=True,text=True,check=True)
    Path('levels-'+('vertical' if 'vertical' in name else 'land')+'.log').write_text(levels.stderr,encoding='utf8')
    # Decode the delivered media for visual review, one sample from every scene.
    samples=[]
    for i,s in enumerate(json.loads(Path('timeline.json').read_text())['segs']):
        t=s['start']+s['dur']*.55
        target=f'stills/final-{i+1:02d}-'+('port' if 'vertical' in name else 'land')+'.jpg'
        subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',name,'-frames:v','1','-q:v','2',target],check=True)
        samples.append(target)
    results.append(dict(file=name,bytes=Path(name).stat().st_size,duration=duration,width=w,height=h,fps=video['avg_frame_rate'],video=video['codec_name'],audio=aud['codec_name'],full_decode='PASS',samples=samples))
Path('output_checks.json').write_text(json.dumps(results,indent=2),encoding='utf8')
print(json.dumps(results,indent=2))
