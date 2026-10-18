import glob
import re

print("=== CHECKING ALL CHAPTERS ===")
for p in sorted(glob.glob('chapters/*/index.html')):
    c = open(p, encoding='utf-8').read()
    
    # 1. languageMeta
    m_meta = re.search(r'languageMeta\s*=\s*(\{[\s\S]*?\});', c)
    meta_vi = False
    if m_meta:
        meta_vi = ('vi:' in m_meta.group(1)) or ('"vi":' in m_meta.group(1)) or ("'vi':" in m_meta.group(1))
    
    # 2. Does it have vi content?
    has_vi_page = 'data-lang-page="vi"' in c
    has_data_vi = 'data-vi="' in c
    
    # 3. What does applyLanguage do with vi?
    # For Arch A: pages.forEach((page) => { page.hidden = page.dataset.langPage !== lang; });
    # If lang == 'vi', page with data-lang-page="vi" is unhidden!
    
    # 4. In language-select, is 'vi' an option?
    has_vi_opt = '<option value="vi">' in c
    
    print(f"{p}:")
    print(f"  meta_vi: {meta_vi}, vi_opt: {has_vi_opt}, vi_page: {has_vi_page}, data_vi: {has_data_vi}")
