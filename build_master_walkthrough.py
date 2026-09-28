import os
import subprocess

videos = [
    'assets/locations/walkthrough/_camera_track_in_1080p_20260928163709.mp4', # 01: Entrance & Central Corridor
    'assets/locations/walkthrough/_camera_track_in_1080p_20260928163512.mp4', # 02: Chowringhee Colonial Hall
    'assets/locations/walkthrough/_camera_track_in_1080p_20260928163605.mp4', # 03: Basudha Rural Terracotta
    'assets/locations/walkthrough/_camera_track_in_1080p_20260928163413.mp4', # 04: Heart of the World Banquet
    'assets/locations/walkthrough/_camera_track_1080p_20260928163137.mp4',    # 05: Pargola Terrace Pavilion
    'assets/locations/walkthrough/_camera_track_in_1080p_20260928163246.mp4', # 06: Sweets Counter & Inner Hall
]

# Write concat list
concat_txt = 'assets/locations/walkthrough/concat_list.txt'
with open(concat_txt, 'w') as f:
    for v in videos:
        abs_p = os.path.abspath(v).replace('\\', '/')
        f.write(f"file '{abs_p}'\n")

output_mp4 = 'assets/locations/walkthrough/master_walkthrough_track.mp4'

# Encode with 1080p, 30fps, GOP=2 for instantaneous subpixel scrub response
cmd = [
    'ffmpeg', '-y',
    '-f', 'concat', '-safe', '0', '-i', concat_txt,
    '-vf', 'fps=30,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2',
    '-c:v', 'libx264',
    '-profile:v', 'main',
    '-level', '4.1',
    '-pix_fmt', 'yuv420p',
    '-preset', 'veryfast',
    '-crf', '22',
    '-g', '2',             # keyframe every 2 frames = 0.06s instant random seek
    '-keyint_min', '2',
    '-an',                 # muted for hero scroll
    '-movflags', '+faststart',
    output_mp4
]

print("Executing concat & GOP=2 optimization...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    print(f"Master walkthrough created successfully: {output_mp4} ({os.path.getsize(output_mp4)/1024/1024:.2f} MB)")
else:
    print("Error:", res.stderr)
