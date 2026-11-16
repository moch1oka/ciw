import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(ROOT_DIR, 'data', 'all_chapters.json')
out_path = os.path.join(ROOT_DIR, 'translations', 'source_texts.json')

if not os.path.exists(data_path):
    print(f"Error: {data_path} not found.")
    sys.exit(1)

with open(data_path, 'r', encoding='utf-8') as f:
    all_ch = json.load(f)

source_data = {}
for ch in all_ch:
    ch_id = ch['dir']
    source_data[ch_id] = {
        'title_zh': ch.get('title_zh', ''),
        'title_vi': ch.get('title_vi', ''),
        'panels': []
    }
    for p in ch.get('panels', []):
        source_data[ch_id]['panels'].append({
            'panel_index': p.get('panel_index', 0),
            'type': p.get('type', 'image'),
            'image_src': p.get('image_src'),
            'video_src': p.get('video_src'),
            'zh': p.get('texts', {}).get('zh', []),
            'vi': p.get('texts', {}).get('vi', [])
        })

with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(source_data, f, ensure_ascii=False, indent=2)

print(f"Saved {out_path} successfully ({len(source_data)} chapters).")
