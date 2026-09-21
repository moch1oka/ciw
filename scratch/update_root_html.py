# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from bs4 import BeautifulSoup

path = 'index.html'
content = open(path, encoding='utf-8').read()

# 1. Add <option value="vi">Tiếng Việt</option> to language-select
if 'value="vi"' not in content:
    content = content.replace(
        '<option value="zh">简体</option>',
        '<option value="vi">Tiếng Việt</option><option value="zh">简体</option>'
    )

# 2. Add vi to languageMeta
if "vi: {" not in content:
    vi_meta = "vi: { htmlLang: 'vi', title: 'Vân Trùng Danh mục đọc truyện · v5.1.39' },"
    content = content.replace(
        "zh: { htmlLang: 'zh-CN',",
        vi_meta + "\n        zh: { htmlLang: 'zh-CN',"
    )

soup = BeautifulSoup(content, 'html.parser')

# 3. Add data-vi to root elements
title_el = soup.find(id='site-title')
if title_el: title_el['data-vi'] = 'Vân Trùng'

subtitle_el = soup.find('p', class_='subtitle')
if subtitle_el: subtitle_el['data-vi'] = 'Chúng ta bé nhỏ như loài kiến, nhưng lại rực rỡ tựa những vì sao.'

cat_title = soup.find('h2', class_='catalog-title')
if cat_title: cat_title['data-vi'] = 'Các Chương'

chapter_names_vi = [
    'Chương 0: Mở đầu',
    'Chương 1: Hi Dương',
    'Chương 2: Người Trong Mây · I',
    'Chương 2: Người Trong Mây · II',
    'Chương 2: Người Trong Mây · III',
    'Chương 3: Ngoài Nón Ánh Sáng · I',
    'Chương 3: Ngoài Nón Ánh Sáng · II',
    'Chương 4: Nón Định Mệnh · I',
    'Chương 4: Nón Định Mệnh · II',
    'Chương 5: Ô Chuy · I'
]

rows = soup.find_all('a', class_='chapter-row')
for i, r in enumerate(rows):
    name_el = r.find(class_='chapter-name')
    if name_el and i < len(chapter_names_vi):
        name_el['data-vi'] = chapter_names_vi[i]
    meta_el = r.find(class_='chapter-meta')
    if meta_el:
        meta_el['data-vi'] = 'Chương hiện có thể đọc'
    action_el = r.find(class_='chapter-action')
    if action_el:
        action_el['data-vi'] = 'Bắt đầu đọc'

with open(path, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("Root index.html successfully updated with Tiếng Việt!")
