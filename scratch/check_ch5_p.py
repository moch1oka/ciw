# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

html5 = open('chapters/chapter-5-wuzhui-1/index.html', encoding='utf-8').read()
soup5 = BeautifulSoup(html5, 'html.parser')
main5 = soup5.find('main', class_='comic')
p5_list = main5.find_all('p', class_=lambda c: c and 'text' in c)

print("First 4 <p> tags:")
for i in range(4):
    p = p5_list[i]
    print(f"p[{i+1}]: class={p.get('class')}, parent={p.parent.name}, text={p.get_text(strip=True)[:60]}")
    print("   attrs:", {k: v for k, v in p.attrs.items() if k.startswith('data-')})
