import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
soup = BeautifulSoup(open('chapters/chapter-5-wuzhui-2/index.html', encoding='utf-8'), 'html.parser')
main = soup.find('main')
non_target_texts = []
for p in main.find_all(['p', 'span', 'summary', 'dd', 'dt', 'div', 'h1', 'h2', 'h3']):
    # Check if element itself has data-zh
    if not p.has_attr('data-zh') and p.find_parent(attrs={'data-zh': True}) is None:
        # Check direct text or children
        # If it has children with data-zh, exclude
        if not p.find_all(attrs={'data-zh': True}):
            t = p.get_text(strip=True)
            if t:
                non_target_texts.append((p.name, p.get('class', []), t))

print(f'Count of non-target texts: {len(non_target_texts)}')
for tag, cls, t in non_target_texts:
    print(f'<{tag} class="{cls}">{t[:80]}</{tag}>')
