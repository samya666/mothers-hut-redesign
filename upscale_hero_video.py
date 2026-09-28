import os
import subprocess

# 5 clips matching user's requested stages:
# 1. Mother's Hut (Entrance)
# 2. Chowringhee
# 3. Basudha
# 4. Hut of the world (Heart of the world)
# 5. Pargola
videos = [
    'assets/locations/walkthrough/_camera_track_in_1080p_20260928163709.mp4', # 01: Mother's Hut
    'assets/locations/walkthrough/_camera_track_in_1080p_20260928163512.mp4', # 02: Chowringhee
    'assets/locations/walkthrough/_camera_track_in_1080p_20260928163605.mp4', # 03: Basudha
    'assets/locations/walkthrough/_camera_track_in_1080p_20260928163413.mp4', # 04: Hut of the World
    'assets/locations/walkthrough/_camera_track_1080p_20260928163137.mp4',    # 05: Pargola
]

concat_txt = 'assets/locations/walkthrough/concat_5stages.txt'
with open(concat_txt, 'w') as f:
    for v in videos:
        abs_p = os.path.abspath(v).replace('\\', '/')
        f.write(f"file '{abs_p}'\n")

# Upscale to 2560x1440 (2.5K QHD) with Lanczos scaling, unsharp edge mask, and subtle color pop
output_mp4 = 'assets/locations/walkthrough/hero_walkthrough_upscaled.mp4'

cmd = [
    'ffmpeg', '-y',
    '-f', 'concat', '-safe', '0', '-i', concat_txt,
    '-vf', (
        'scale=2560:1440:flags=lanczos,'
        'unsharp=lx=5:ly=5:la=1.2:cx=5:cy=5:ca=0.8,'
        'eq=contrast=1.04:brightness=0.01:saturation=1.12'
    ),
    '-c:v', 'libx264',
    '-profile:v', 'high',
    '-level', '5.1',
    '-pix_fmt', 'yuv420p',
    '-preset', 'fast',
    '-crf', '19',      # Studio grade quality
    '-g', '4',         # Keyframe every 4 frames (0.13s) for instant smooth scrub
    '-keyint_min', '4',
    '-an',
    '-movflags', '+faststart',
    output_mp4
]

print("Starting high-resolution 2.5K upscale & sharpening...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    sz = os.path.getsize(output_mp4) / (1024 * 1024)
    print(f"Upscaled video created successfully: {output_mp4} ({sz:.2f} MB)")
else:
    print("Error:", res.stderr)
