# -*- coding: utf-8 -*-
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')

from translations.trans_ch0 import CHAPTER_0_VI
from translations.trans_ch1 import CHAPTER_1_VI
from translations.trans_ch2_1 import CHAPTER_2_1_VI
from translations.trans_ch2_2 import CHAPTER_2_2_VI
from translations.trans_ch2_3 import CHAPTER_2_3_VI
from translations.trans_ch3_1 import CHAPTER_3_1_VI

def check_nested(ch_name, vi_panels):
    data = json.load(open(f'chapters/{ch_name}/chapter_data.json', encoding='utf-8'))
    print(f"=== {ch_name} (panels in json: {len(data['panels'])}, vi_panels: {len(vi_panels)}) ===")
    for i, (p, vi) in enumerate(zip(data['panels'], vi_panels)):
        zh_len = len(p['texts'].get('zh', []))
        en_len = len(p['texts'].get('en', []))
        vi_len = len(vi)
        if zh_len != vi_len:
            print(f"  Panel {i+1}: zh={zh_len}, en={en_len}, vi={vi_len}")

check_nested('chapter-0-prologue', CHAPTER_0_VI)
check_nested('chapter-1-xiyang', CHAPTER_1_VI)
check_nested('chapter-2-cloud-dwellers-1', CHAPTER_2_1_VI)
check_nested('chapter-2-cloud-dwellers-2', CHAPTER_2_2_VI)
check_nested('chapter-2-cloud-dwellers-3', CHAPTER_2_3_VI)
check_nested('chapter-3-beyond-light-cone-1', CHAPTER_3_1_VI)
