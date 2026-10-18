import os

for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith(('.py', '.js', '.html')):
            p = os.path.join(root, f)
            try:
                c = open(p, encoding='utf-8').read()
                if 'data-cloudinsect-language-select' in c:
                    print(p)
            except:
                pass
