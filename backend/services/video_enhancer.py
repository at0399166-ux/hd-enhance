from pathlib import Path
import subprocess

def enhance_video(src: Path, out: Path, scale: int, sharpen: float, denoise: int):
    filters = []
    if denoise:
        filters.append("hqdn3d=1.5:1.5:6:6")
    filters.append(f"scale=iw*{scale}:ih*{scale}:flags=lanczos")
    if sharpen > 0:
        amount = min(max(sharpen, 0.1), 2.0)
        filters.append(f"unsharp=5:5:{amount}:5:5:0")
    vf = ",".join(filters)
    cmd = [
        "ffmpeg", "-y", "-i", str(src),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "128k", str(out)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
