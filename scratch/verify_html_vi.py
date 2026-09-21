# -*- coding: utf-8 -*-
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

for d in sorted(os.listdir('chapters')):
    p = os.path.join('chapters', d, 'index.html')
    if os.path.exists(p):
        content = open(p, encoding='utf-8').read()
        has_opt = 'value="vi"' in content
        has_meta = "htmlLang: 'vi'" in content
        has_main_vi = 'data-lang-page="vi"' in content
        has_data_vi = 'data-vi=' in content
        print(f"{d}: opt_vi={has_opt}, meta_vi={has_meta}, main_vi={has_main_vi}, data_vi={has_data_vi}")
