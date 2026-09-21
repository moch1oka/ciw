# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

content = open('chapters/chapter-4-fate-2/index.html', encoding='utf-8').read()
m = re.search(r'const targets = .*?;', content)
if m:
    print('targets definition:', m.group(0))

m_select = re.search(r'const select = document\.querySelector\(\'\.language-select\'\);', content)
print('select hook:', m_select)
