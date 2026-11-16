import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ch_key = sys.argv[1] if len(sys.argv) > 1 else 'chapter-0-prologue'
src_path = os.path.join(ROOT_DIR, 'translations', 'source_texts.json')

if not os.path.exists(src_path):
    print(f"Generating source_texts.json first...")
    import subprocess
    subprocess.run([sys.executable, os.path.join(ROOT_DIR, 'tools', 'export_sources.py')], check=True)

with open(src_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

if ch_key not in data:
    print(f"Error: Chapter key '{ch_key}' not found in source_texts.json.")
    print("Available keys:")
    for k in data.keys():
        print(f"  - {k}")
    sys.exit(1)

print(f"==================================================")
print(f"   {ch_key}: {data[ch_key].get('title_zh', '')} / {data[ch_key].get('title_vi', '')}")
print(f"==================================================")

for p in data[ch_key].get('panels', []):
    idx = p.get('panel_index', 0)
    zh_list = p.get('zh', [])
    vi_list = p.get('vi', [])
    if zh_list:
        print(f"\n--- Panel {idx} ({len(zh_list)} texts) ---")
        for i in range(len(zh_list)):
            vi_txt = vi_list[i] if i < len(vi_list) else ""
            print(f"[{i+1}] ZH: {zh_list[i]}")
            print(f"    VI: {vi_txt}")
    else:
        print(f"\n--- Panel {idx} (No text) ---")
