# -*- coding: utf-8 -*-
import os, importlib, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')

for f in sorted(os.listdir('translations')):
    if f.startswith('trans_') and f.endswith('.py'):
        mod_name = 'translations.' + f[:-3]
        mod = importlib.import_module(mod_name)
        keys = [k for k in dir(mod) if not k.startswith('__')]
        for k in keys:
            val = getattr(mod, k)
            if isinstance(val, list):
                # check if list of lists or list of strings
                sub_lens = [len(x) if isinstance(x, list) else 1 for x in val]
                total = sum(sub_lens)
                is_nested = any(isinstance(x, list) for x in val)
                print(f"{f} -> {k}: len={len(val)}, nested={is_nested}, total_items={total}")
