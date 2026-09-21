# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

html = open('chapters/chapter-4-fate-2/index.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')
main = soup.find('main', class_='comic')
targets = main.find_all(lambda el: el.has_attr('data-zh'))

ch4_2_data = json.load(open('translations/source_texts.json', encoding='utf-8'))['chapter-4-fate-2']
all_zh_in_source = []
for p in ch4_2_data['panels']:
    all_zh_in_source.extend(p['zh'])

for i in range(len(targets)):
    t_zh = targets[i].get('data-zh', '')
    s_zh = all_zh_in_source[i] if i < len(all_zh_in_source) else '---'
    if t_zh != s_zh:
        print(f"Divergence at index {i+1}:")
        print(f"  Target: {t_zh}")
        print(f"  Source: {s_zh}")
        print(f"  Target tag: <{targets[i].name} class='{targets[i].get('class')}'>")
        break
