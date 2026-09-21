# -*- coding: utf-8 -*-
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')

from translations.trans_ch3_2 import TRANSLATIONS_CH3_2
from translations.trans_ch4_1 import TRANSLATIONS_CH4_1
from translations.trans_ch4_2 import TRANSLATIONS_CH4_2
from translations.trans_ch5_1 import TRANSLATIONS_CH5_1

FLAT_TRANS = {
    'chapter-3-beyond-light-cone-2': TRANSLATIONS_CH3_2,
    'chapter-4-fate-1': TRANSLATIONS_CH4_1,
    'chapter-4-fate-2': TRANSLATIONS_CH4_2,
    'chapter-5-wuzhui-1': TRANSLATIONS_CH5_1,
}

for ch_name, trans_list in FLAT_TRANS.items():
    data = json.load(open(f'chapters/{ch_name}/chapter_data.json', encoding='utf-8'))
    idx = 0
    mismatches = []
    for i, p in enumerate(data['panels']):
        count = len(p['texts'].get('zh', []))
        sub = trans_list[idx:idx+count]
        if len(sub) != count:
            mismatches.append((i+1, count, len(sub)))
        idx += count
    print(f"=== {ch_name} ===")
    print(f"  Total processed: {idx} / {len(trans_list)}, mismatches: {mismatches}")
