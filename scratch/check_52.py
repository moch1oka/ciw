import subprocess, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

# Let's test what happens when chapter-5-wuzhui-2 has vi in languageMeta
# Let's see lines 1280-1285 of chapter-5-wuzhui-2/index.html
c = open('chapters/chapter-5-wuzhui-2/index.html', encoding='utf-8').read()
print('Has vi in ch5.2 languageMeta:', '"vi":' in c or 'vi:' in c)
