import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(ROOT_DIR, 'translations', 'source_texts.json')

if not os.path.exists(src_path):
    print("source_texts.json not found, generating...")
    import subprocess
    subprocess.run([sys.executable, os.path.join(ROOT_DIR, 'tools', 'export_sources.py')], check=True)

with open(src_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for ch_key, ch_val in data.items():
    txt_path = os.path.join(ROOT_DIR, 'translations', f'{ch_key}_source.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(f"=== {ch_key}: {ch_val.get('title_zh', '')} / {ch_val.get('title_vi', '')} ===\n\n")
        for p in ch_val.get('panels', []):
            idx = p.get('panel_index', 0)
            zh = p.get('zh', [])
            vi = p.get('vi', [])
            f.write(f"--- Panel {idx} ({len(zh)} texts) ---\n")
            for i in range(max(len(zh), len(vi))):
                zh_str = zh[i] if i < len(zh) else ""
                vi_str = vi[i] if i < len(vi) else ""
                f.write(f"ZH: {zh_str}\n")
                f.write(f"VI: {vi_str}\n\n")
            if not zh and not vi:
                f.write("(No text)\n\n")

print(f"Exported all {len(data)} chapters to readable text files in translations/.")
