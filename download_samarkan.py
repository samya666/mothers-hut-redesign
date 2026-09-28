import urllib.request
import re
import os

os.makedirs('assets/fonts', exist_ok=True)
cdn_url = 'https://fonts.cdnfonts.com/css/samarkan'
req = urllib.request.Request(cdn_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        css = resp.read().decode('utf-8')
        print("CSS:", css[:200])
        matches = re.findall(r'url\((.*?)\)', css)
        for m in matches:
            clean_url = m.strip('\'"')
            ext = 'woff' if '.woff' in clean_url else 'ttf'
            target = f'assets/fonts/samarkan.{ext}'
            font_req = urllib.request.Request(clean_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(font_req, timeout=10) as f_resp:
                with open(target, 'wb') as out_f:
                    out_f.write(f_resp.read())
            print(f"Downloaded {target}, size: {os.path.getsize(target)} bytes")
except Exception as e:
    print("Download error:", e)
