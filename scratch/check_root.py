import sys, re
sys.stdout.reconfigure(encoding='utf-8')
cjk = re.compile(r'[\u4e00-\u9fff]')
c = open('index.html', encoding='utf-8').read()
matches = re.findall(r'data-vi="([^"]*)"', c)
chinese_in_root = [m for m in matches if cjk.search(m)]
print('Root index.html total data-vi:', len(matches))
print('Root index.html Chinese in data-vi:', len(chinese_in_root))
for m in chinese_in_root:
    print('  -', m)
