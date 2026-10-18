import re, sys

sys.stdout.reconfigure(encoding='utf-8')
cjk_pattern = re.compile(r'[\u4e00-\u9fff]')

for p in ['chapters/chapter-5-wuzhui-2/chapter_vi.md', 'chapters/chapter-5-wuzhui-1/chapter_vi.md', 'chapters/chapter-4-fate-2/chapter_vi.md']:
    c = open(p, encoding='utf-8').read()
    chinese_lines = []
    for line in c.splitlines():
        # Exclude lines that are explicitly showing Chinese originals like "nguyên văn: ..." or titles in parentheses
        if cjk_pattern.search(line):
            chinese_lines.append(line)
    print(f"=== {p} ===")
    print(f"  Total lines with Chinese: {len(chinese_lines)}")
    for l in chinese_lines[:5]:
        print(f"    {l[:100]}")
