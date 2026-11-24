"""Create vertical YouTube Shorts from queued shows, without changing the originals.

Uses the opening as the hook, ending at a detected pause near 60 seconds when
possible. A pause is only a heuristic, not a guarantee of a sentence boundary.
Run: python tools/make_short_cuts.py [--dry-run] [--limit N] [--id SHOW_ID]
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = Path(r"C:\Users\lilli\Projects\heartbeat-observatory")
QUEUE = ROOT / "state" / "social-queue.json"
MIN_SECONDS, TARGET_SECONDS, MAX_SECONDS = 55.0, 60.0, 75.0


def run(args, **kwargs):
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", **kwargs)


def probe(ffprobe, source):
    result = run([ffprobe, "-v", "error", "-show_entries",
                  "format=duration:stream=codec_type,width,height:stream_tags=rotate:stream_side_data=rotation",
                  "-of", "json", str(source)])
    if result.returncode:
        raise RuntimeError(f"ffprobe failed: {result.stderr.strip()}")
    info = json.loads(result.stdout)
    video = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    if not video:
        raise ValueError("no video stream")
    width, height = video.get("width", 0), video.get("height", 0)
    rotation = int(video.get("tags", {}).get("rotate", 0))
    for side in video.get("side_data_list", []):
        rotation = int(side.get("rotation", rotation))
    if abs(rotation) % 180 == 90:
        width, height = height, width
    if not width or not height or width >= height:
        raise ValueError(f"not vertical ({width}x{height})")
    return float(info["format"]["duration"]), any(s.get("codec_type") == "audio" for s in info["streams"])


def choose_end(ffmpeg, source, duration, has_audio):
    # Analyze only the relevant region; timestamps remain relative to its start.
    if not has_audio:
        return min(TARGET_SECONDS, duration), "no audio; fixed endpoint"
    result = run([ffmpeg, "-hide_banner", "-nostats", "-ss", "54", "-t", "21",
                  "-i", str(source), "-vn", "-af", "silencedetect=noise=-35dB:d=0.25",
                  "-f", "null", "-"])
    if result.returncode:
        raise RuntimeError(f"silence detection failed: {result.stderr.strip()[-500:]}")
    pauses = [54.0 + float(n) for n in re.findall(r"silence_start:\s*([\d.]+)", result.stderr)]
    candidates = [t for t in pauses if MIN_SECONDS <= t <= min(MAX_SECONDS, duration)]
    if candidates:
        end = min(candidates, key=lambda t: abs(t - TARGET_SECONDS))
        return end, "detected pause (review recommended)"
    return min(TARGET_SECONDS, duration), "no pause detected; fixed endpoint (review recommended)"


def probe_av(av, source):
    with av.open(str(source)) as container:
        video = next((s for s in container.streams if s.type == "video"), None)
        if not video:
            raise ValueError("no video stream")
        width, height = video.codec_context.width, video.codec_context.height
        rotation = int(video.metadata.get("rotate", 0))
        if abs(rotation) % 180 == 90:
            width, height = height, width
        if not width or not height or width >= height:
            raise ValueError(f"not vertical ({width}x{height})")
        if container.duration is None:
            raise ValueError("unknown duration")
        return container.duration / av.time_base, bool(container.streams.audio)


def choose_end_av(av, np, source, duration, has_audio):
    if not has_audio:
        return min(TARGET_SECONDS, duration), "no audio; fixed endpoint"
    # Collect only the 54–75 second audio window, preserving channels. A silence
    # requires every channel to stay below -35 dB for at least 0.25 seconds.
    rate = 44100
    pieces = []
    with av.open(str(source)) as container:
        audio = container.streams.audio[0]
        resampler = av.AudioResampler(format="fltp", rate=rate)
        for frame in container.decode(audio):
            for converted in resampler.resample(frame):
                if converted.time is None:
                    raise ValueError("audio has no timestamps for silence detection")
                start = float(converted.time)
                samples = converted.to_ndarray()
                lo = max(0, int((54.0 - start) * rate))
                hi = min(samples.shape[1], int((75.0 - start) * rate))
                if hi > lo:
                    pieces.append(np.max(np.abs(samples[:, lo:hi]), axis=0))
                if start + converted.samples / rate >= 75.0:
                    break
            if frame.time is not None and float(frame.time) >= 75.0:
                break
    if pieces:
        quiet = np.concatenate(pieces) < 10 ** (-35 / 20)
        changes = np.diff(np.concatenate(([False], quiet, [False])).astype(np.int8))
        starts = np.flatnonzero(changes == 1)
        ends = np.flatnonzero(changes == -1)
        candidates = [54.0 + int(start) / rate for start, end in zip(starts, ends)
                      if end - start >= rate * 0.25
                      and MIN_SECONDS <= 54.0 + int(start) / rate <= min(MAX_SECONDS - 0.2, duration)]
        if candidates:
            end = min(candidates, key=lambda t: abs(t - TARGET_SECONDS))
            return end, "detected pause (review recommended)"
    return min(TARGET_SECONDS, duration), "no pause detected; fixed endpoint (review recommended)"


def remux_av(av, source, temporary, end):
    # Copy complete packets, including dependencies for reordered video frames.
    # This avoids any quality loss and keeps timestamps and original audio.
    with av.open(str(source)) as original, av.open(str(temporary), "w", options={"movflags": "+faststart"}) as output:
        selected = [s for s in original.streams if s.type in ("video", "audio")]
        mapping = {s.index: output.add_stream_from_template(s) for s in selected}
        start = (original.start_time or 0) / av.time_base
        for packet in original.demux(*selected):
            if packet.dts is None or float(packet.dts * packet.time_base) - start >= end:
                continue
            packet.stream = mapping[packet.stream.index]
            output.mux(packet)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="inspect and report cuts without writing media")
    parser.add_argument("--limit", type=int, default=None, help="process at most this many missing cuts")
    parser.add_argument("--id", help="process only the show with this queue ID")
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be at least 1")
    ffmpeg, ffprobe = shutil.which("ffmpeg"), shutil.which("ffprobe")
    av = np = None
    if not ffmpeg or not ffprobe:
        try:
            import av
            import numpy as np
        except ImportError:
            print("ERROR: install ffmpeg and ffprobe on PATH, or PyAV and numpy", file=sys.stderr)
            return 1
        print("FFmpeg tools unavailable; using PyAV for silence detection and lossless packet copying")
    shows = json.loads(QUEUE.read_text(encoding="utf-8"))["shows"]
    if args.id:
        shows = [show for show in shows if show.get("id") == args.id]
        if not shows:
            print(f"ERROR: no show with ID {args.id!r}", file=sys.stderr)
            return 1
        if len(shows) != 1 or not shows[0].get("file"):
            print(f"ERROR: show ID {args.id!r} is ambiguous or has no file", file=sys.stderr)
            return 1
    made = skipped = failed = attempted = 0
    seen = set()
    for show in shows:
        name = show.get("file")
        if not name:
            continue
        source = (SITE / name).resolve()
        if not source.is_relative_to(SITE.resolve()):
            print(f"ERROR {name}: path is outside the site directory")
            failed += 1
            continue
        output = source.with_name(source.stem + "-short.mp4")
        if output in seen:
            continue
        seen.add(output)
        if output.exists():
            print(f"SKIP {output.name}: already exists")
            skipped += 1
            continue
        if args.limit is not None and attempted >= args.limit:
            break
        attempted += 1
        temporary = None
        try:
            if not source.is_file():
                raise FileNotFoundError(f"source missing: {source}")
            duration, has_audio = probe_av(av, source) if av else probe(ffprobe, source)
            if duration < MIN_SECONDS:
                raise ValueError(f"source is only {duration:.1f}s; cannot make a 55–75s cut")
            end, reason = (choose_end_av(av, np, source, duration, has_audio) if av
                           else choose_end(ffmpeg, source, duration, has_audio))
            print(f"{'DRY ' if args.dry_run else ''}CUT {source.name} -> {output.name}: 0–{end:.2f}s; {reason}", flush=True)
            if args.dry_run:
                made += 1
                continue
            with tempfile.NamedTemporaryFile(prefix=output.stem + ".", suffix=".tmp.mp4",
                                             dir=output.parent, delete=False) as temp:
                temporary = Path(temp.name)
            if av:
                remux_av(av, source, temporary, end)
            else:
                result = run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
                              "-t", f"{end:.3f}", "-map", "0:v:0", "-map", "0:a:0?",
                              # 1 s fade to black + silence so a cut mid-sentence lands softly (Claude 11/11)
                              "-vf", f"fade=t=out:st={max(0, end - 1):.3f}:d=1",
                              "-af", f"afade=t=out:st={max(0, end - 1.2):.3f}:d=1.2",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                              "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(temporary)])
                if result.returncode:
                    raise RuntimeError(f"ffmpeg failed: {result.stderr.strip()}")
            # Check the actual output, and never let an incomplete file look finished.
            actual, _ = probe_av(av, temporary) if av else probe(ffprobe, temporary)
            if not MIN_SECONDS <= actual <= MAX_SECONDS:
                raise ValueError(f"output duration {actual:.2f}s outside 55–75s")
            if output.exists():
                raise FileExistsError(f"output appeared during encoding: {output}")
            temporary.rename(output)
            made += 1
        except (OSError, ValueError, KeyError, RuntimeError, json.JSONDecodeError) as exc:
            print(f"ERROR {name}: {exc}", file=sys.stderr)
            failed += 1
        finally:
            if temporary is not None and temporary.exists():
                temporary.unlink()
    print(f"{'Would make' if args.dry_run else 'Made'} {made}; skipped {skipped}; errors {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
