import glob, re

for p in sorted(glob.glob('chapters/*/index.html')):
    c = open(p, encoding='utf-8').read()
    # find all options in chapter-select
    m = re.findall(r'<select[^>]*class="chapter-select"[^>]*>([\s\S]*?)</select>', c)
    if m:
        opts = re.findall(r'<option[^>]*value="([^"]*)"[^>]*>', m[0])
        print(p, 'Total chapter options:', len(opts), 'Values:', opts[:2])
    else:
        print(p, 'NO chapter-select found!')
