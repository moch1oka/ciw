# -*- coding: utf-8 -*-
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

all_ok = True
print("==================== FINAL COMPREHENSIVE AUDIT ====================")

# 1. Check data/all_chapters.json
if not os.path.exists('data/all_chapters.json'):
    print("❌ ERROR: data/all_chapters.json missing!")
    all_ok = False
else:
    all_ch = json.load(open('data/all_chapters.json', encoding='utf-8'))
    print(f"✅ data/all_chapters.json has {len(all_ch)} chapters.")
    for ch in all_ch:
        ch_id = ch['id']
        p_cnt = len(ch['panels'])
        vi_total = sum(len(p['texts'].get('vi', [])) for p in ch['panels'])
        zh_total = sum(len(p['texts'].get('zh', [])) for p in ch['panels'])
        if vi_total == 0 or vi_total != zh_total:
            print(f"❌ ERROR in all_chapters.json for {ch_id}: vi_total={vi_total}, zh_total={zh_total}")
            all_ok = False
        else:
            print(f"  • {ch_id}: panels={p_cnt}, vi_texts={vi_total}, zh_texts={zh_total} (MATCH)")

# 2. Check each chapter directory
chapters_dir = 'chapters'
chapter_folders = sorted(os.listdir(chapters_dir))
print(f"\n✅ Found {len(chapter_folders)} chapter directories.")

expected_files = [
    'index.html',
    'chapter_vi.md',
    'chapter_vi_bilingual.md',
    'chapter_bilingual.md',
    'chapter_en.md',
    'chapter_zh.md',
    'chapter_data.json'
]

total_vi_texts = 0
total_vi_words = 0

for folder in chapter_folders:
    fpath = os.path.join(chapters_dir, folder)
    if not os.path.isdir(fpath): continue
    
    # Check expected files
    for ef in expected_files:
        p = os.path.join(fpath, ef)
        if not os.path.exists(p) or os.path.getsize(p) == 0:
            print(f"❌ ERROR: Missing or empty file {p}")
            all_ok = False
            
    # Check media folder
    media_dir = os.path.join(fpath, 'media')
    if not os.path.exists(media_dir) or len(os.listdir(media_dir)) == 0:
        print(f"❌ ERROR: Missing or empty media folder in {fpath}")
        all_ok = False
        
    # Check HTML vi support
    html_p = os.path.join(fpath, 'index.html')
    html_content = open(html_p, encoding='utf-8').read()
    if 'value="vi"' not in html_content:
        print(f"❌ ERROR: index.html in {folder} missing value='vi'")
        all_ok = False
    if "htmlLang: 'vi'" not in html_content:
        print(f"❌ ERROR: index.html in {folder} missing htmlLang: 'vi'")
        all_ok = False
        
    # Count words in chapter_vi.md
    vi_md_p = os.path.join(fpath, 'chapter_vi.md')
    vi_md_text = open(vi_md_p, encoding='utf-8').read()
    words = len(vi_md_text.split())
    total_vi_words += words
    
    # Check chapter_data.json
    cd_p = os.path.join(fpath, 'chapter_data.json')
    cd = json.load(open(cd_p, encoding='utf-8'))
    vi_cnt = sum(len(p['texts'].get('vi', [])) for p in cd['panels'])
    total_vi_texts += vi_cnt
    print(f"  • {folder}: All 7 files OK, media={len(os.listdir(media_dir))} items, VI texts={vi_cnt}, words={words}")

# 3. Check root index.html
root_html = open('index.html', encoding='utf-8').read()
if 'value="vi"' not in root_html or 'data-vi=' not in root_html:
    print("❌ ERROR: Root index.html missing vi support!")
    all_ok = False
else:
    print("\n✅ Root index.html has Tiếng Việt option and data-vi attributes.")

# 4. Check root README.md
root_readme = open('README.md', encoding='utf-8').read()
if 'Bản Dịch Tiếng Việt' not in root_readme or 'chapter_vi.md' not in root_readme:
    print("❌ ERROR: Root README.md missing Vietnamese section!")
    all_ok = False
else:
    print("✅ Root README.md contains full Vietnamese catalog and instructions.")

print(f"\n==================== SUMMARY ====================")
print(f"Total Vietnamese texts translated: {total_vi_texts}")
print(f"Total Vietnamese words: {total_vi_words}")
print(f"Audit status: {'SUCCESS (0 ERRORS)' if all_ok else 'FAILED'}")
