import sys, re, glob
sys.stdout.reconfigure(encoding='utf-8')

for p in sorted(glob.glob('chapters/*/index.html')):
    c = open(p, encoding='utf-8').read()
    m = re.search(r'languageMeta\s*=\s*(\{[\s\S]*?\});', c)
    if m:
        meta = m.group(1)
        has_vi = ('vi:' in meta) or ('"vi":' in meta)
        m_title = re.search(r'[\'"]vi[\'"]\s*:\s*\{[^}]*?title\s*:\s*[\'"]([^\'"]*)[\'"]', meta)
        title = m_title.group(1) if m_title else 'NONE'
        print(f'{p}: has_vi={has_vi}, title={title}')
    else:
        print(f'{p}: NO languageMeta')
