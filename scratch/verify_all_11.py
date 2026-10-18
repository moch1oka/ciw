import glob
import re

print("Testing all 11 chapters for 'vi' language handling...")

for p in sorted(glob.glob('chapters/*/index.html')):
    c = open(p, encoding='utf-8').read()
    
    # 1. languageMeta has vi?
    m_meta = re.search(r'languageMeta\s*=\s*(\{[\s\S]*?\});', c)
    has_meta_vi = False
    if m_meta:
        has_meta_vi = ('vi:' in m_meta.group(1)) or ('"vi":' in m_meta.group(1)) or ("'vi':" in m_meta.group(1))
    
    # 2. Arch A (data-lang-page="vi") or Arch B (data-vi on elements)
    is_arch_a = 'data-lang-page="vi"' in c
    
    # 3. If Arch B, how many elements have data-vi
    data_vi_count = len(re.findall(r'data-vi="[^"]*"', c))
    
    # 4. Check if readStoredValue('cloudinsect-lang') || 'vi' is present
    has_default_vi = "readStoredValue('cloudinsect-lang') || 'vi'" in c
    
    # 5. Check if select has value="vi"
    has_select_vi = '<option value="vi">' in c
    
    print(f"Chapter: {p}")
    print(f"  has_meta_vi: {has_meta_vi}")
    print(f"  arch: {'A' if is_arch_a else 'B'}")
    print(f"  data_vi_count: {data_vi_count}")
    print(f"  has_default_vi: {has_default_vi}")
    print(f"  has_select_vi: {has_select_vi}")
