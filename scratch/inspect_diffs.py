# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')

from translations.trans_ch2_3 import CHAPTER_2_3_VI
from translations.trans_ch3_1 import CHAPTER_3_1_VI

data2_3 = json.load(open('chapters/chapter-2-cloud-dwellers-3/chapter_data.json', encoding='utf-8'))
p17_zh = data2_3['panels'][16]['texts'].get('zh', [])
p17_en = data2_3['panels'][16]['texts'].get('en', [])
p17_vi = CHAPTER_2_3_VI[16]

print("=== ch2_3 Panel 17 ===")
print(f"zh len: {len(p17_zh)}, en len: {len(p17_en)}, vi len: {len(p17_vi)}")
for i in range(max(len(p17_zh), len(p17_vi))):
    zh_t = p17_zh[i] if i < len(p17_zh) else '---'
    vi_t = p17_vi[i] if i < len(p17_vi) else '---'
    print(f"[{i+1}] ZH: {zh_t[:30]} | VI: {vi_t[:30]}")

data3_1 = json.load(open('chapters/chapter-3-beyond-light-cone-1/chapter_data.json', encoding='utf-8'))
p14_zh = data3_1['panels'][13]['texts'].get('zh', [])
p14_en = data3_1['panels'][13]['texts'].get('en', [])
p14_vi = CHAPTER_3_1_VI[13]

print("\n=== ch3_1 Panel 14 ===")
print(f"zh len: {len(p14_zh)}, en len: {len(p14_en)}, vi len: {len(p14_vi)}")
for i in range(max(len(p14_zh), len(p14_vi))):
    zh_t = p14_zh[i] if i < len(p14_zh) else '---'
    vi_t = p14_vi[i] if i < len(p14_vi) else '---'
    print(f"[{i+1}] ZH: {zh_t[:30]} | VI: {vi_t[:30]}")
