import re, sys, glob
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
cjk_pattern = re.compile(r'[\u4e00-\u9fff]')

for p in sorted(glob.glob('chapters/*/index.html')):
    c = open(p, encoding='utf-8').read()
    soup = BeautifulSoup(c, 'html.parser')
    
    # Check all elements with data-zh
    untranslated = []
    for el in soup.find_all(lambda e: e.has_attr('data-zh')):
        # Skip option in select if we will check menu separately
        is_option = el.name == 'option'
        zh = el.get('data-zh', '').strip()
        vi = el.get('data-vi', '').strip()
        
        # If vi is empty, or vi equals zh, or vi contains Chinese
        if not vi or vi == zh or cjk_pattern.search(vi):
            untranslated.append((el.name, el.get('class', []), zh, vi))
            
    print(f"=== {p} ===")
    print(f"  Total elements with data-zh: {len(soup.find_all(lambda e: e.has_attr('data-zh')))}")
    print(f"  Untranslated or Chinese in data-vi: {len(untranslated)}")
    for name, cls, zh, vi in untranslated:
        print(f"    <{name} class='{cls}'>")
        print(f"      ZH: {zh}")
        print(f"      VI: {vi}")
