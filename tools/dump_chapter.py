import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ch_dir = sys.argv[1] if len(sys.argv) > 1 else 'chapter-0-prologue'
ch_path = os.path.join(ROOT_DIR, 'chapters', ch_dir, 'chapter_data.json')

if not os.path.exists(ch_path):
    print(f"Error: Chapter path not found: {ch_path}")
    print("Available chapters:")
    for d in sorted(os.listdir(os.path.join(ROOT_DIR, 'chapters'))):
        print(f"  - {d}")
    sys.exit(1)

with open(ch_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"==================================================")
print(f"   {ch_dir} ({data.get('title_zh', '')} / {data.get('title_vi', '')})")
print(f"==================================================")
for p in data.get('panels', []):
    idx = p.get('panel_index', 0)
    zh_list = p.get('texts', {}).get('zh', [])
    vi_list = p.get('texts', {}).get('vi', [])
    print(f"\n--- Panel {idx}: {len(zh_list)} texts ---")
    for i in range(max(len(zh_list), len(vi_list))):
        zh = zh_list[i] if i < len(zh_list) else ""
        vi = vi_list[i] if i < len(vi_list) else ""
        print(f"  [{i+1}] ZH: {zh}")
        print(f"      VI: {vi}")
