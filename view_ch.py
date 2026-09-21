import sys
import json

sys.stdout.reconfigure(encoding='utf-8')
ch_key = sys.argv[1]

with open('translations/source_texts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"==================================================")
print(f"   {ch_key}: {data[ch_key]['title_zh']} / {data[ch_key]['title_en']}")
print(f"==================================================")

for p in data[ch_key]['panels']:
    idx = p['panel_index']
    zh_list = p['zh']
    en_list = p['en']
    if zh_list:
        print(f"\n--- Panel {idx} ({len(zh_list)} texts) ---")
        for i in range(len(zh_list)):
            en_txt = en_list[i] if i < len(en_list) else ""
            print(f"[{i+1}] ZH: {zh_list[i]}")
            print(f"    EN: {en_txt}")
    else:
        print(f"\n--- Panel {idx} (No text) ---")
