import os
import urllib.request
import urllib.parse
from PIL import Image, ImageFilter, ImageEnhance

raw_dir = r"g:\localpulse-ai\demos\mothers-hut-redesign\assets\locations\raw"
upscaled_dir = r"g:\localpulse-ai\demos\mothers-hut-redesign\assets\locations\upscaled"

os.makedirs(raw_dir, exist_ok=True)
os.makedirs(upscaled_dir, exist_ok=True)

base_url = "https://mothershut.com/"

location_images = [
    # Named Theme Halls & Dining Zones
    ("gallery/bagicha-1.webp", "bagicha_garden_hall_01.webp"),
    ("gallery/basudha-2.webp", "basudha_heritage_hall_02.webp"),
    ("gallery/mothers-hut-basudha-1.jpg", "basudha_heritage_hall_01.jpg"),
    ("gallery/chowringhee-1.webp", "chowringhee_vintage_calcutta_01.webp"),
    ("gallery/heart-of-the-world-1.webp", "heart_of_the_world_banquet_01.webp"),
    ("gallery/lahar-1.webp", "lahar_wave_hall_01.webp"),
    ("gallery/pargola-1.webp", "pargola_terrace_hall_01.webp"),
    
    # Official Zone Cards
    ("assets/img/cache/BAGICHA.webp", "zone_card_bagicha.webp"),
    ("assets/img/cache/BASUDHA.webp", "zone_card_basudha.webp"),
    ("assets/img/cache/CHOWRINGHEE.webp", "zone_card_chowringhee.webp"),
    ("assets/img/cache/HEART-OF-THE-WORLD.webp", "zone_card_heart_of_the_world.webp"),
    ("assets/img/cache/LAHAR.webp", "zone_card_lahar.webp"),
    ("assets/img/cache/PARGOLA.webp", "zone_card_pargola.webp"),

    # Banquet & Event Facilities
    ("assets/img/banquet_bg.jpg", "banquet_hall_interior_bg.jpg"),
    ("assets/img/cache/banquet_hall.webp", "banquet_hall_seating.webp"),
    ("assets/img/cache/banquet_party.webp", "banquet_celebration_lawn.webp"),
    ("assets/img/cache/banquet_food.webp", "banquet_buffet_counter.webp"),
    ("assets/img/banquet_food.jpeg", "banquet_food_spread.jpeg"),

    # Facility & Dining Hall Hero Views
    ("assets/img/cache/hero1.webp", "facility_interior_hero1.webp"),
    ("assets/img/cache/hero2.webp", "facility_interior_hero2.webp"),
    ("assets/img/hero2.jpg", "facility_interior_hero2_orig.jpg"),
    ("assets/img/cache/hero3.webp", "facility_interior_hero3.webp"),

    # Kitchen & Craft
    ("assets/img/chef.jpg", "kitchen_mothers_workforce.jpg"),
    ("assets/img/cache/chef.webp", "kitchen_mothers_card.webp"),
    ("assets/img/dish_highlight.jpg", "restaurant_signature_spread.jpg"),
    ("assets/img/cache/dish_highlight.webp", "restaurant_signature_card.webp"),
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

downloaded = []

print("=== STEP 1: DOWNLOADING ALL LOCATION IMAGES FROM MOTHERSHUT.COM ===")
for path_on_server, local_name in location_images:
    full_url = urllib.parse.urljoin(base_url, path_on_server)
    local_path = os.path.join(raw_dir, local_name)
    try:
        req = urllib.request.Request(full_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            with open(local_path, "wb") as f:
                f.write(data)
            print(f"[OK] Downloaded: {local_name} ({len(data)} bytes) from {path_on_server}", flush=True)
            downloaded.append((local_name, local_path))
    except Exception as e:
        print(f"[WARN] Failed to download {path_on_server}: {e}", flush=True)

print(f"\nSuccessfully downloaded {len(downloaded)} raw location images.\n")

print("=== STEP 2: HIGH-FIDELITY UPSCALING & SHARPENING ===")
upscaled_results = []

for local_name, raw_path in downloaded:
    try:
        with Image.open(raw_path) as im:
            orig_w, orig_h = im.size
            orig_mode = im.mode

            # Target upscale: 2x or 3x so minimum long edge is at least 2400px (or at least 2x original)
            scale_factor = 2.0
            if max(orig_w, orig_h) < 1000:
                scale_factor = max(2.5, 2400.0 / max(orig_w, orig_h))
            
            target_w = int(round(orig_w * scale_factor))
            target_h = int(round(orig_h * scale_factor))

            # Convert palette/P mode or RGBA to RGB for JPEG compatibility, preserve alpha for WebP/PNG
            is_alpha = (orig_mode in ('RGBA', 'LA') or ('transparency' in im.info))

            # Upscale using high-precision Lanczos interpolation
            upscaled = im.resize((target_w, target_h), resample=Image.Resampling.LANCZOS)

            # High-end photography post-processing:
            # 1. Subtle UnsharpMask to restore micro-contrast and edge definition
            upscaled = upscaled.filter(ImageFilter.UnsharpMask(radius=1.8, percent=125, threshold=2))
            
            # 2. Gentle color vibrance & contrast enhancement (1.04x) for rich Bengali spice tones
            if not is_alpha:
                contrast_enhancer = ImageEnhance.Contrast(upscaled)
                upscaled = contrast_enhancer.enhance(1.04)
                color_enhancer = ImageEnhance.Color(upscaled)
                upscaled = color_enhancer.enhance(1.05)

            # Save high-res JPG and WebP versions
            base_name, _ = os.path.splitext(local_name)
            out_jpg = os.path.join(upscaled_dir, f"{base_name}_upscaled.jpg")
            out_webp = os.path.join(upscaled_dir, f"{base_name}_upscaled.webp")

            if is_alpha:
                upscaled.save(out_webp, "WEBP", quality=95, method=6)
                # For JPG convert to RGB with warm dark background
                rgb_im = Image.new("RGB", upscaled.size, (28, 25, 23))
                rgb_im.paste(upscaled, mask=upscaled.split()[-1])
                rgb_im.save(out_jpg, "JPEG", quality=95, optimize=True)
            else:
                rgb_im = upscaled.convert("RGB")
                rgb_im.save(out_jpg, "JPEG", quality=95, optimize=True)
                rgb_im.save(out_webp, "WEBP", quality=95, method=6)

            file_size_jpg = os.path.getsize(out_jpg)
            print(f"[UPSCALED] {local_name}: {orig_w}x{orig_h} -> {target_w}x{target_h} ({file_size_jpg // 1024} KB)", flush=True)
            upscaled_results.append({
                "name": local_name,
                "orig_res": f"{orig_w}x{orig_h}",
                "new_res": f"{target_w}x{target_h}",
                "jpg_path": out_jpg,
                "webp_path": out_webp,
                "size_kb": file_size_jpg // 1024
            })
    except Exception as e:
        print(f"[ERROR] Failed to upscale {local_name}: {e}", flush=True)

print(f"\n=== FINISHED: Upscaled {len(upscaled_results)} location images with studio-grade fidelity ===")
