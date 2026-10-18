import re, sys

sys.stdout.reconfigure(encoding='utf-8')
cjk_pattern = re.compile(r'[\u4e00-\u9fff]')

c = open('chapters/chapter-5-wuzhui-2/index.html', encoding='utf-8').read()
matches = re.findall(r'<[^>]+data-vi="([^"]*)"[^>]*>', c)
for full_tag in re.finditer(r'<[^>]+data-vi="([^"]*)"[^>]*>', c):
    vi_val = full_tag.group(1)
    if cjk_pattern.search(vi_val):
        print("TAG:", full_tag.group(0)[:150])
        print("  data-vi:", vi_val)
        print("---")
