# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

def examine_fragments(ch_dir):
    soup = BeautifulSoup(open(f'chapters/{ch_dir}/index.html', encoding='utf-8'), 'html.parser')
    targets = soup.find_all(lambda el: el.has_attr('data-zh') and el.has_attr('data-zh-hant') and el.has_attr('data-en') and el.name != 'option')
    
    # Check parent-child or group structure
    p_tags = soup.find('main', class_='comic').find_all('p')
    print(f"=== {ch_dir} ===")
    print(f"Total <p>: {len(p_tags)}")
    split_p = []
    for i, p in enumerate(p_tags):
        spans = p.find_all('span', attrs={'data-zh': True})
        if len(spans) > 0:
            split_p.append((i+1, len(spans), [s.get('data-zh') for s in spans]))
    print(f"Paragraphs with child spans with data-zh: {len(split_p)}")
    for item in split_p[:5]:
        print(f"  P {item[0]} has {item[1]} spans: {item[2]}")

examine_fragments('chapter-4-fate-2')
examine_fragments('chapter-5-wuzhui-1')
