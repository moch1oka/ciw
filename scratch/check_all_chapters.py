# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

all_data = json.load(open('data/all_chapters.json', encoding='utf-8'))
print("all_chapters type:", type(all_data), "len:", len(all_data))
if isinstance(all_data, list):
    print("item 0 keys:", list(all_data[0].keys()))
elif isinstance(all_data, dict):
    print("keys:", list(all_data.keys()))
