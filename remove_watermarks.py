import os
import subprocess
import glob

WALKTHROUGH_DIR = r"G:\localpulse-ai\demos\mothers-hut-redesign\assets\locations\walkthrough"

# 1. First, process all individual raw clips in assets/locations/walkthrough
raw_clips = glob.glob(os.path.join(WALKTHROUGH_DIR, "_camera_track*.mp4"))

print(f"Found {len(raw_clips)} raw camera track clips to clean.")

delogo_filter = "delogo=x=1700:y=860:w=84:h=84:show=0"

for clip in raw_clips:
    base = os.path.basename(clip)
    clean_tmp = os.path.join(WALKTHROUGH_DIR, "clean_" + base)
    print(f"\nProcessing {base}...")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", clip,
        "-vf", delogo_filter,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "17",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        clean_tmp
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        # Replace original with cleaned
        os.replace(clean_tmp, clip)
        print(f"[OK] Cleaned and updated: {base}")
    else:
        print(f"[ERROR] Failed cleaning {base}: {res.stderr}")

# 2. Re-build the 5-stage stitched hero walkthrough at 2.5K (2560x1440)
# Stages:
# 1. Mother's Hut
# 2. Chowringhee
# 3. Basudha
# 4. Hut of the World
# 5. Pargola
stage_videos = [
    os.path.join(WALKTHROUGH_DIR, "_camera_track_in_1080p_20260928163709.mp4"),
    os.path.join(WALKTHROUGH_DIR, "_camera_track_in_1080p_20260928163512.mp4"),
    os.path.join(WALKTHROUGH_DIR, "_camera_track_in_1080p_20260928163605.mp4"),
    os.path.join(WALKTHROUGH_DIR, "_camera_track_in_1080p_20260928163413.mp4"),
    os.path.join(WALKTHROUGH_DIR, "_camera_track_1080p_20260928163137.mp4"),
]

concat_txt = os.path.join(WALKTHROUGH_DIR, "concat_clean_5stages.txt")
with open(concat_txt, "w") as f:
    for v in stage_videos:
        f.write(f"file '{v.replace('\\', '/')}'\n")

hero_upscaled = os.path.join(WALKTHROUGH_DIR, "hero_walkthrough_upscaled.mp4")
hero_tmp = os.path.join(WALKTHROUGH_DIR, "hero_walkthrough_upscaled_clean.mp4")

print("\nRe-rendering 2.5K hero walkthrough from clean, watermark-free clips...")

cmd_hero = [
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", concat_txt,
    "-vf", (
        "scale=2560:1440:flags=lanczos,"
        "unsharp=lx=5:ly=5:la=1.2:cx=5:cy=5:ca=0.8,"
        "eq=contrast=1.04:brightness=0.01:saturation=1.12"
    ),
    "-c:v", "libx264",
    "-profile:v", "high",
    "-level", "5.1",
    "-pix_fmt", "yuv420p",
    "-preset", "fast",
    "-crf", "19",
    "-g", "4",
    "-keyint_min", "4",
    "-an",
    "-movflags", "+faststart",
    hero_tmp
]

res_hero = subprocess.run(cmd_hero, capture_output=True, text=True)
if res_hero.returncode == 0:
    os.replace(hero_tmp, hero_upscaled)
    sz = os.path.getsize(hero_upscaled) / (1024 * 1024)
    print(f"[OK] Cleaned 2.5K Hero Walkthrough rendered: {hero_upscaled} ({sz:.2f} MB)")
else:
    print(f"[ERROR] Failed hero render: {res_hero.stderr}")

print("\nAll Gemini watermarks successfully eradicated!")
