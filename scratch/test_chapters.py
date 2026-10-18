import glob
import re

for p in sorted(glob.glob('chapters/*/index.html')):
    c = open(p, encoding='utf-8').read()
    m = re.search(r'languageMeta\s*=\s*(\{[\s\S]*?\});', c)
    if not m:
        print(f"{p}: NO languageMeta found!")
        continue
    meta_str = m.group(1)
    has_vi = ('vi:' in meta_str) or ('"vi":' in meta_str) or ("'vi':" in meta_str)
    has_select_script = 'data-cloudinsect-language-select' in c
    has_vi_option = 'value="vi"' in c
    
    # Check if vi is first in language-select or if default lang is vi
    m_default_lang = re.search(r"let lang = readStoredValue\('cloudinsect-lang'\) \|\| '([^']+)'", c)
    default_lang = m_default_lang.group(1) if m_default_lang else 'unknown'
    
    # Check Architecture:
    arch = 'B' if 'main class="comic" data-lang-page=' not in c else 'A'
    
    print(f"{p} [Arch {arch}]: vi_in_meta={has_vi}, vi_in_select={has_vi_option}, default_lang={default_lang}")
