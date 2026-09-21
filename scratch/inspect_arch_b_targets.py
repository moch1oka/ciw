# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

html = open('chapters/chapter-4-fate-2/index.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')
main = soup.find('main', class_='comic')

targets = main.find_all(lambda el: el.has_attr('data-zh'))
# check how many are <p>, <span>, <h1>, etc.
from collections import Counter
print("Tag counts:", Counter(t.name for t in targets))

# Check which ones have child targets
with_children = [t for t in targets if t.find(lambda c: c != t and c.has_attr('data-zh'))]
print("Targets with child targets:", len(with_children))
for t in with_children[:5]:
    print("Parent:", t.name, t.get('class'))
    children = t.find_all(lambda c: c != t and c.has_attr('data-zh'))
    for c in children:
        print("  Child:", c.name, c.get('class'), "data-zh:", c.get('data-zh')[:30])
