# -*- coding: utf-8 -*-
import os, json, sys
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('chapters/chapter-0-prologue/chapter_data.json', encoding='utf-8'))
print("chapter_data keys:", list(data.keys()))
if 'panels' in data and len(data['panels']) > 0:
    print("panel 0 keys:", list(data['panels'][0].keys()))
    print("panel 0 content:", data['panels'][0])
