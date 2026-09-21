# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('chapters/chapter-5-wuzhui-1/index.html', encoding='utf-8'), 'html.parser')
targets = soup.find_all(lambda el: el.has_attr('data-zh') and el.has_attr('data-zh-hant') and el.has_attr('data-en'))

print("Total targets matching JS selector in ch5-1:", len(targets))
options = [t for t in targets if t.name == 'option']
non_options = [t for t in targets if t.name != 'option']
print("Options count:", len(options))
print("Non-options count:", len(non_options))

# Check how non-options relate to our 58 texts
for i, t in enumerate(non_options[:5]):
    print(f"[{i+1}] <{t.name} class='{t.get('class')}'> data-zh='{t.get('data-zh')[:30]}'")
