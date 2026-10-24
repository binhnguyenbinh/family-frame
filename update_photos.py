import urllib.request
import re
import json
import os
import sys

ALBUM_URL = 'https://photos.app.goo.gl/7TEGaisCTURZWh5YA'

def main():
    print("[*] Fetching album from Google Photos...")
    req = urllib.request.Request(
        ALBUM_URL, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode('utf-8')
    except Exception as e:
        print(f"[!] Error fetching album: {e}")
        sys.exit(1)

    matches = re.findall(r'(https:\/\/lh3\.googleusercontent\.com\/pw\/[a-zA-Z0-9_\-]+)', html)
    photos = list(dict.fromkeys(matches))

    if not photos:
        print("[!] No photos found! Aborting to avoid blanking out the album.")
        sys.exit(1)

    print(f"[*] Successfully fetched {len(photos)} photos.")

    curr_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(curr_dir, "index.html")

    with open(index_path, "r", encoding="utf-8") as f:
        old_content = f.read()

    new_json = json.dumps([p + "=w2048-h1536" for p in photos], indent=2)

    # Check if photos already match
    old_match = re.search(r'var photos = (\[.*?\]);', old_content, flags=re.DOTALL)
    if old_match and old_match.group(1).strip() == new_json.strip():
        print("[+] Photos list is already up to date. No changes needed.")
        return False

    new_content = re.sub(r'var photos = \[.*?\];', f'var photos = {new_json};', old_content, flags=re.DOTALL)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[+] Updated index.html with {len(photos)} photos!")
    return True

if __name__ == '__main__':
    main()
