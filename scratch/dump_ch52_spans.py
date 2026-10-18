import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
c = open('chapters/chapter-5-wuzhui-2/index.html', encoding='utf-8').read()
soup = BeautifulSoup(c, 'html.parser')

main = soup.find('main')
elements = main.find_all(lambda el: el.has_attr('data-zh'))
for i in range(20):
    el = elements[i]
    zh = el.get('data-zh', '')
    vi = el.get('data-vi', '')
    print(f"[{i+1}] Tag: <{el.name} class='{el.get('class', [])}'>")
    print(f"  ZH: {zh}")
    print(f"  VI: {vi}")
