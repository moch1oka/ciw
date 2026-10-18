import sys, glob, re
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
cjk_pattern = re.compile(r'[\u4e00-\u9fff]')

for p in sorted(glob.glob('chapters/*/index.html')):
    c = open(p, encoding='utf-8').read()
    soup = BeautifulSoup(c, 'html.parser')
    
    # Check Architecture A
    if soup.find('main', attrs={'data-lang-page': 'vi'}):
        vi_main = soup.find('main', attrs={'data-lang-page': 'vi'})
        # Find any Chinese text in vi_main
        chinese_in_vi_main = []
        for text in vi_main.stripped_strings:
            if cjk_pattern.search(text):
                # ignore single characters if deliberate
                chinese_in_vi_main.append(text)
        if chinese_in_vi_main:
            print(f"=== {p} [Arch A] has Chinese in data-lang-page='vi' ===")
            for t in chinese_in_vi_main:
                print(f"  - {t}")
    else:
        # Architecture B: simulate applyLanguage('vi')
        targets = soup.find_all(lambda el: el.has_attr('data-zh'))
        for t in targets:
            vi = t.get('data-vi', '')
            t.string = vi
        
        main_el = soup.find('main')
        chinese_in_main = []
        for text in main_el.stripped_strings:
            if cjk_pattern.search(text):
                chinese_in_main.append(text)
        if chinese_in_main:
            print(f"=== {p} [Arch B] has Chinese in rendered text ===")
            for t in chinese_in_main:
                print(f"  - {t[:120]}")
