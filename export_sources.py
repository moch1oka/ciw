import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open('data/all_chapters.json', 'r', encoding='utf-8') as f:
    all_ch = json.load(f)

source_data = {}
for ch in all_ch:
    ch_id = ch['dir']
    source_data[ch_id] = {
        'title_zh': ch['title_zh'],
        'title_en': ch['title_en'],
        'panels': []
    }
    for p in ch['panels']:
        source_data[ch_id]['panels'].append({
            'panel_index': p['panel_index'],
            'type': p.get('type', 'image'),
            'image_src': p.get('image_src'),
            'video_src': p.get('video_src'),
            'zh': p['texts'].get('zh', []),
            'en': p['texts'].get('en', [])
        })

with open('translations/source_texts.json', 'w', encoding='utf-8') as f:
    json.dump(source_data, f, ensure_ascii=False, indent=2)

print("Saved translations/source_texts.json successfully!")
