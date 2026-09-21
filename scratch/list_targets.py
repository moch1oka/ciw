# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

def inspect_chapter_targets(ch_dir):
    soup = BeautifulSoup(open(f'chapters/{ch_dir}/index.html', encoding='utf-8'), 'html.parser')
    targets = soup.find_all(lambda el: el.has_attr('data-zh') and el.has_attr('data-zh-hant') and el.has_attr('data-en') and el.name != 'option')
    print(f"=== {ch_dir}: {len(targets)} targets ===")
    for i, t in enumerate(targets):
        zh = t.get('data-zh')
        en = t.get('data-en')
        print(f"  [{i+1}] <{t.name} class='{t.get('class')}'> ZH: {zh[:35]} | EN: {en[:35]}")

inspect_chapter_targets('chapter-5-wuzhui-1')
