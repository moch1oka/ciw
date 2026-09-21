# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

def print_splits(ch_dir):
    soup = BeautifulSoup(open(f'chapters/{ch_dir}/index.html', encoding='utf-8'), 'html.parser')
    p_tags = soup.find('main', class_='comic').find_all('p')
    print(f"==================== {ch_dir} ====================")
    for i, p in enumerate(p_tags):
        spans = p.find_all('span', attrs={'data-zh': True})
        if len(spans) > 0:
            print(f"--- P {i+1} ({len(spans)} spans) ---")
            for j, s in enumerate(spans):
                print(f"  [{j+1}] ZH: {s.get('data-zh')}")
                print(f"      EN: {s.get('data-en')}")

print_splits('chapter-4-fate-2')
print_splits('chapter-5-wuzhui-1')
