import sys
import json
import os

sys.stdout.reconfigure(encoding='utf-8')

with open('translations/source_texts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for ch_key, ch_val in data.items():
    txt_path = f"translations/{ch_key}_source.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(f"=== {ch_key}: {ch_val['title_zh']} / {ch_val['title_en']} ===\n\n")
        for p in ch_val['panels']:
            idx = p['panel_index']
            zh = p['zh']
            en = p['en']
            f.write(f"--- Panel {idx} ({len(zh)} texts) ---\n")
            for i in range(len(zh)):
                en_str = en[i] if i < len(en) else ""
                f.write(f"ZH: {zh[i]}\n")
                f.write(f"EN: {en_str}\n\n")
            if not zh:
                f.write("(No text)\n\n")

print("Exported all 10 chapters to readable text files in translations/.")
