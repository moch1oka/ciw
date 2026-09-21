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

print(f"Targets count: {len(targets)}, Source texts count: {len(all_zh_in_source)}")

# Let's inspect targets vs source
for i in range(min(15, len(targets))):
    t_zh = targets[i].get('data-zh', '')
    s_zh = all_zh_in_source[i] if i < len(all_zh_in_source) else '---'
    print(f"[{i+1}] Target: {t_zh[:30]} | Source: {s_zh[:30]}")
