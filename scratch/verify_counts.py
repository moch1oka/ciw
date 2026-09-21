# -*- coding: utf-8 -*-
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath('.'))

from translations.trans_ch0 import TRANSLATIONS_CH0
from translations.trans_ch1 import TRANSLATIONS_CH1
from translations.trans_ch2_1 import TRANSLATIONS_CH2_1
from translations.trans_ch2_2 import TRANSLATIONS_CH2_2
from translations.trans_ch2_3 import TRANSLATIONS_CH2_3
from translations.trans_ch3_1 import TRANSLATIONS_CH3_1
from translations.trans_ch3_2 import TRANSLATIONS_CH3_2
from translations.trans_ch4_1 import TRANSLATIONS_CH4_1
from translations.trans_ch4_2 import TRANSLATIONS_CH4_2
from translations.trans_ch5_1 import TRANSLATIONS_CH5_1

ALL_TRANS = {
    'chapter-0-prologue': TRANSLATIONS_CH0,
    'chapter-1-xiyang': TRANSLATIONS_CH1,
    'chapter-2-cloud-dwellers-1': TRANSLATIONS_CH2_1,
    'chapter-2-cloud-dwellers-2': TRANSLATIONS_CH2_2,
    'chapter-2-cloud-dwellers-3': TRANSLATIONS_CH2_3,
    'chapter-3-beyond-light-cone-1': TRANSLATIONS_CH3_1,
    'chapter-3-beyond-light-cone-2': TRANSLATIONS_CH3_2,
    'chapter-4-fate-1': TRANSLATIONS_CH4_1,
    'chapter-4-fate-2': TRANSLATIONS_CH4_2,
    'chapter-5-wuzhui-1': TRANSLATIONS_CH5_1,
}

for ch_dir, trans_list in ALL_TRANS.items():
    json_path = os.path.join('chapters', ch_dir, 'chapter_data.json')
    data = json.load(open(json_path, encoding='utf-8'))
    zh_count = sum(len(p['texts']['zh']) for p in data['panels'])
    print(f"{ch_dir}: panels={len(data['panels'])}, zh_in_json={zh_count}, trans_len={len(trans_list)}, match={zh_count == len(trans_list)}")
