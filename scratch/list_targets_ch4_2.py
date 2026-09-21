# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('chapters/chapter-4-fate-2/index.html', encoding='utf-8'), 'html.parser')
targets = soup.find_all(lambda el: el.has_attr('data-zh') and el.has_attr('data-zh-hant') and el.has_attr('data-en') and el.name != 'option')
print(f"Total non-option targets in ch4-2: {len(targets)}")
for i, t in enumerate(targets):
    zh = t.get('data-zh')
    en = t.get('data-en')
    print(f"  [{i+1}] <{t.name} class='{t.get('class')}'> ZH: {zh[:35]} | EN: {en[:35]}")
