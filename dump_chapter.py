import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

ch_dir = sys.argv[1]
with open(f'chapters/{ch_dir}/chapter_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"=== {ch_dir} ({data['title_zh']}) ===")
for p in data['panels']:
    idx = p['panel_index']
    zh_list = p['texts'].get('zh', [])
    en_list = p['texts'].get('en', [])
    print(f"Panel {idx}: {len(zh_list)} texts")
    for i in range(max(len(zh_list), len(en_list))):
        zh = zh_list[i] if i < len(zh_list) else ""
        en = en_list[i] if i < len(en_list) else ""
        print(f"  [{i+1}] ZH: {zh}")
        print(f"      EN: {en}")
