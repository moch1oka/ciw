# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('chapters/chapter-0-prologue/chapter_data.json', encoding='utf-8'))
for i, p in enumerate(data['panels']):
    img = p.get('image_src')
    zh = p['texts'].get('zh', [])
    print(f"Panel {i+1}: img={img}, zh_len={len(zh)}, zh={zh[:1]}")
