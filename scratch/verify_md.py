# -*- coding: utf-8 -*-
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

for d in sorted(os.listdir('chapters')):
    vi_path = os.path.join('chapters', d, 'chapter_vi.md')
    bi_path = os.path.join('chapters', d, 'chapter_vi_bilingual.md')
    
    vi_sz = os.path.getsize(vi_path) if os.path.exists(vi_path) else 0
    bi_sz = os.path.getsize(bi_path) if os.path.exists(bi_path) else 0
    
    vi_lines = len(open(vi_path, encoding='utf-8').readlines()) if os.path.exists(vi_path) else 0
    bi_lines = len(open(bi_path, encoding='utf-8').readlines()) if os.path.exists(bi_path) else 0
    
    print(f"{d}: chapter_vi.md={vi_lines} lines ({vi_sz}B) | chapter_vi_bilingual.md={bi_lines} lines ({bi_sz}B)")
