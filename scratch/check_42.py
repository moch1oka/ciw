import sys
sys.stdout.reconfigure(encoding='utf-8')
c = open('chapters/chapter-4-fate-2/index.html', encoding='utf-8').read()
idx = c.find('data-vi="第五章 乌骓 · 二"')
if idx != -1:
    print(c[idx-50:idx+150])
else:
    print('Not found with data-vi!')
    idx = c.find('第五章 乌骓 · 二')
    print(c[idx-50:idx+150])
