import re, sys, glob

sys.stdout.reconfigure(encoding='utf-8')

# Regex for CJK characters
cjk_pattern = re.compile(r'[\u4e00-\u9fff]')

for p in sorted(glob.glob('chapters/*/index.html')):
    c = open(p, encoding='utf-8').read()
    matches = re.findall(r'data-vi="([^"]*)"', c)
    chinese_in_vi = []
    for m in matches:
        if cjk_pattern.search(m):
            chinese_in_vi.append(m)
    print(f"=== {p} ===")
    print(f"  Total data-vi attributes: {len(matches)}")
    print(f"  data-vi containing Chinese: {len(chinese_in_vi)}")
    for s in chinese_in_vi[:5]:
        print(f"    - {s[:100]}")
