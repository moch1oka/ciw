# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

html = open('chapters/chapter-4-fate-2/index.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')
main = soup.find('main', class_='comic')

p_list = main.find_all('p', class_=lambda c: c and 'text' in c)
print(f"Total <p class='text...'> in main.comic: {len(p_list)}")

panels = main.find_all('figure', class_='panel')
print(f"Total <figure class='panel'> in main.comic: {len(panels)}")

# Let's check ch5-1 too
html5 = open('chapters/chapter-5-wuzhui-1/index.html', encoding='utf-8').read()
soup5 = BeautifulSoup(html5, 'html.parser')
main5 = soup5.find('main', class_='comic')
p5_list = main5.find_all('p', class_=lambda c: c and 'text' in c)
print(f"Total <p class='text...'> in ch5-1 main.comic: {len(p5_list)}")
print(f"Total <figure class='panel'> in ch5-1 main.comic: {len(main5.find_all('figure', class_='panel'))}")
