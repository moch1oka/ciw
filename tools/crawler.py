import os
import sys
import re
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://cloudinsect.com/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

LANG_ATTR_MAP = {
    'zh': 'data-zh',
    'zhHant': 'data-zh-hant',
    'en': 'data-en',
    'ja': 'data-ja',
    'ko': 'data-ko',
    'es': 'data-es',
    'fr': 'data-fr',
    'ru': 'data-ru',
    'ar': 'data-ar',
    'ptBR': 'data-pt-br'
}

CHAPTERS_CONFIG = [
    {
        'id': 'chapter-0',
        'dir': 'chapter-0-prologue',
        'file': 'chapter-0-prologue.html',
        'title_zh': '第零章 楔子',
        'title_en': 'Chapter 0: Prologue'
    },
    {
        'id': 'chapter-1',
        'dir': 'chapter-1-xiyang',
        'file': 'chapter-1-xiyang.html',
        'title_zh': '第一章 希扬',
        'title_en': 'Chapter 1: Xiyang'
    },
    {
        'id': 'chapter-2-1',
        'dir': 'chapter-2-cloud-dwellers-1',
        'file': 'chapter-2-cloud-dwellers.html',
        'title_zh': '第二章 云中人 · 一',
        'title_en': 'Chapter 2: Cloud Dwellers · Part 1'
    },
    {
        'id': 'chapter-2-2',
        'dir': 'chapter-2-cloud-dwellers-2',
        'file': 'chapter-2-cloud-dwellers-2.html',
        'title_zh': '第二章 云中人 · 二',
        'title_en': 'Chapter 2: Cloud Dwellers · Part 2'
    },
    {
        'id': 'chapter-2-3',
        'dir': 'chapter-2-cloud-dwellers-3',
        'file': 'chapter-2-cloud-dwellers-3.html',
        'title_zh': '第二章 云中人 · 三',
        'title_en': 'Chapter 2: Cloud Dwellers · Part 3'
    },
    {
        'id': 'chapter-3-1',
        'dir': 'chapter-3-beyond-light-cone-1',
        'file': 'chapter-3-beyond-light-cone-1.html',
        'title_zh': '第三章 光锥之外 · 一',
        'title_en': 'Chapter 3: Beyond Light Cone · Part 1'
    },
    {
        'id': 'chapter-3-2',
        'dir': 'chapter-3-beyond-light-cone-2',
        'file': 'chapter-3-beyond-light-cone-2.html',
        'title_zh': '第三章 光锥之外 · 二',
        'title_en': 'Chapter 3: Beyond Light Cone · Part 2'
    },
    {
        'id': 'chapter-4-1',
        'dir': 'chapter-4-fate-1',
        'file': 'chapter-4-fate-1.html',
        'title_zh': '第四章 命运之锥 · 一',
        'title_en': 'Chapter 4: Cone of Fate · Part 1'
    },
    {
        'id': 'chapter-4-2',
        'dir': 'chapter-4-fate-2',
        'file': 'chapter-4-fate-2.html',
        'title_zh': '第四章 命运之锥 · 二',
        'title_en': 'Chapter 4: Cone of Fate · Part 2'
    },
    {
        'id': 'chapter-5-1',
        'dir': 'chapter-5-wuzhui-1',
        'file': 'chapter-5-wuzhui-1.html',
        'title_zh': '第五章 乌骓 · 一',
        'title_en': 'Chapter 5: Wuzhui · Part 1'
    },
    {
        'id': 'chapter-5-2',
        'dir': 'chapter-5-wuzhui-2',
        'file': 'chapter-5-wuzhui-2.html',
        'title_zh': '第五章 乌骓 · 二',
        'title_en': 'Chapter 5: Wuzhui · Part 2'
    }
]

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS_DIR = os.path.join(WORKSPACE_DIR, "chapters")
ASSETS_DIR = os.path.join(WORKSPACE_DIR, "assets")
DATA_DIR = os.path.join(WORKSPACE_DIR, "data")

os.makedirs(CHAPTERS_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

session = requests.Session()
session.headers.update(HEADERS)


def download_file_to(url, target_path, retries=5):
    """Download a file directly to target_path with stream and retries."""
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
        return True, target_path, "Already exists"

    for attempt in range(retries):
        try:
            r = session.get(url, timeout=60, stream=True)
            if r.status_code == 200:
                with open(target_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=65536):
                        if chunk:
                            f.write(chunk)
                return True, target_path, "Success"
            else:
                time.sleep(1)
        except Exception:
            time.sleep(1 + attempt)
    return False, target_path, f"Failed after {retries} attempts"


def extract_text_piece(element, lang_key):
    target_attr = LANG_ATTR_MAP.get(lang_key, f'data-{lang_key}')
    if element.has_attr(target_attr):
        return element[target_attr]
    children_with_attr = element.find_all(lambda tag: tag.has_attr(target_attr))
    if children_with_attr:
        parts = [c[target_attr] for c in children_with_attr if c.get(target_attr)]
        return ' '.join(parts)
    return element.get_text(strip=True)


def parse_chapter_content(soup):
    """Extract structured panels and text across all available languages supporting both DOM architectures."""
    mains = soup.find_all('main', class_='comic')
    has_data_attrs = bool(soup.find('p', attrs={'data-en': True}))
    panels = []

    if has_data_attrs:
        # Architecture B (e.g. Chapter 4-2, 5-1): single main with data-* attributes on p/span
        main = mains[0]
        current_panel = None
        for child in main.children:
            if not hasattr(child, 'name') or not child.name:
                continue

            if child.name == 'figure':
                v = child.find('video')
                i = child.find('img')
                v_src = v.get('src') if v else None
                p_src = v.get('poster') if v else None
                i_src = i.get('src') if i else None

                if not i_src and p_src:
                    i_src = p_src

                is_valid = False
                if i_src and not i_src.startswith(('assets/', '../../assets/')):
                    is_valid = True
                if v_src and not v_src.startswith(('assets/cloud-insect-logo', '../../assets/cloud-insect-logo')):
                    is_valid = True

                if is_valid:
                    media_type = 'motion' if v_src and i_src else ('video' if v_src else 'image')
                    v_clean = f"media/{os.path.basename(v_src)}" if v_src else None
                    i_clean = f"media/{os.path.basename(i_src)}" if i_src else None
                    p_clean = f"media/{os.path.basename(p_src)}" if p_src else None

                    current_panel = {
                        'panel_index': len(panels) + 1,
                        'type': media_type,
                        'image_src': i_clean,
                        'video_src': v_clean,
                        'poster_src': p_clean,
                        'orig_img_url': urljoin(BASE_URL, i_src) if i_src else None,
                        'orig_vid_url': urljoin(BASE_URL, v_src) if v_src else None,
                        'orig_poster_url': urljoin(BASE_URL, p_src) if p_src else None,
                        'texts': {lang: [] for lang in LANG_ATTR_MAP}
                    }
                    panels.append(current_panel)

            elif child.name == 'p' and 'text' in child.get('class', []):
                if current_panel is None:
                    current_panel = {
                        'panel_index': 0,
                        'type': 'prologue_intro',
                        'image_src': None,
                        'video_src': None,
                        'poster_src': None,
                        'orig_img_url': None,
                        'orig_vid_url': None,
                        'orig_poster_url': None,
                        'texts': {lang: [] for lang in LANG_ATTR_MAP}
                    }
                    panels.append(current_panel)

                for lang in LANG_ATTR_MAP:
                    t_val = extract_text_piece(child, lang)
                    if t_val:
                        current_panel['texts'][lang].append(t_val)

        languages = list(LANG_ATTR_MAP.keys())

    else:
        # Architecture A (Chapters 0 - 4-1): multiple main.comic tags (one per language)
        lang_mains = {}
        for m in mains:
            lang = m.get('data-lang-page') or 'zh'
            lang_mains[lang] = m

        ref_lang = 'zh' if 'zh' in lang_mains else list(lang_mains.keys())[0]
        ref_main = lang_mains[ref_lang]

        current_panel = None
        for child in ref_main.children:
            if not hasattr(child, 'name') or not child.name:
                continue

            if child.name == 'figure':
                video = child.find('video')
                img = child.find('img')
                video_src = video.get('src') if video else None
                poster_src = video.get('poster') if video else None
                img_src = img.get('src') if img else None

                if not img_src and poster_src:
                    img_src = poster_src

                is_valid = False
                if img_src and not img_src.startswith(('assets/', '../../assets/')):
                    is_valid = True
                if video_src and not video_src.startswith(('assets/cloud-insect-logo', '../../assets/cloud-insect-logo')):
                    is_valid = True

                if is_valid:
                    media_type = 'motion' if video_src and img_src else ('video' if video_src else 'image')
                    v_clean = f"media/{os.path.basename(video_src)}" if video_src else None
                    i_clean = f"media/{os.path.basename(img_src)}" if img_src else None
                    p_clean = f"media/{os.path.basename(poster_src)}" if poster_src else None

                    current_panel = {
                        'panel_index': len(panels) + 1,
                        'type': media_type,
                        'image_src': i_clean,
                        'video_src': v_clean,
                        'poster_src': p_clean,
                        'orig_img_url': urljoin(BASE_URL, img_src) if img_src else None,
                        'orig_vid_url': urljoin(BASE_URL, video_src) if video_src else None,
                        'orig_poster_url': urljoin(BASE_URL, poster_src) if poster_src else None,
                        'texts': {}
                    }
                    panels.append(current_panel)

            elif child.name == 'p' and 'text' in child.get('class', []):
                text_val = child.get_text(strip=True)
                if text_val:
                    if current_panel is None:
                        current_panel = {
                            'panel_index': 0,
                            'type': 'prologue_intro',
                            'image_src': None,
                            'video_src': None,
                            'poster_src': None,
                            'orig_img_url': None,
                            'orig_vid_url': None,
                            'orig_poster_url': None,
                            'texts': {}
                        }
                        panels.append(current_panel)
                    if ref_lang not in current_panel['texts']:
                        current_panel['texts'][ref_lang] = []
                    current_panel['texts'][ref_lang].append(text_val)

        for lang, m in lang_mains.items():
            if lang == ref_lang:
                continue

            panel_iter_idx = 0 if panels and panels[0]['panel_index'] == 0 else -1
            for child in m.children:
                if not hasattr(child, 'name') or not child.name:
                    continue
                if child.name == 'figure':
                    v = child.find('video')
                    i = child.find('img')
                    is_media = False
                    if i and i.get('src') and not i['src'].startswith(('assets/', '../../assets/')):
                        is_media = True
                    if v and v.get('src') and not v['src'].startswith(('assets/cloud-insect-logo', '../../assets/cloud-insect-logo')):
                        is_media = True
                    if is_media:
                        panel_iter_idx += 1
                elif child.name == 'p' and 'text' in child.get('class', []):
                    text_val = child.get_text(strip=True)
                    if text_val and 0 <= panel_iter_idx < len(panels):
                        target_p = panels[panel_iter_idx]
                        if lang not in target_p['texts']:
                            target_p['texts'][lang] = []
                        target_p['texts'][lang].append(text_val)

        languages = list(lang_mains.keys())

    return panels, languages


def write_chapter_markdown(ch_dir, ch_info, panels):
    def format_media_md(p):
        lines = []
        if p.get('video_src'):
            v = p['video_src']
            if not v.startswith('./'):
                v = f"./{v}"
            lines.append(f'<video src="{v}" controls loop muted playsinline width="100%"></video>\n')
            if p.get('image_src'):
                img = p['image_src']
                if not img.startswith('./'):
                    img = f"./{img}"
                lines.append(f'*(Ảnh tĩnh: ![Panel {p["panel_index"]}]({img}))*\n')
        elif p.get('image_src'):
            img = p['image_src']
            if not img.startswith('./'):
                img = f"./{img}"
            lines.append(f'![Panel {p["panel_index"]}]({img})\n')
        return "\n".join(lines)

    # 1. Bilingual
    with open(os.path.join(ch_dir, "chapter_bilingual.md"), 'w', encoding='utf-8') as f:
        f.write(f"# 云虫 / CloudInsect - {ch_info['title_zh']} ({ch_info['title_en']})\n\n---\n\n")
        for p in panels:
            m_md = format_media_md(p)
            if m_md:
                f.write(f"{m_md}\n")
            zh_texts = p['texts'].get('zh', [])
            en_texts = p['texts'].get('en', [])
            max_len = max(len(zh_texts), len(en_texts))
            for i in range(max_len):
                zh_t = zh_texts[i] if i < len(zh_texts) else ""
                en_t = en_texts[i] if i < len(en_texts) else ""
                if zh_t:
                    f.write(f"**ZH**: {zh_t}\n\n")
                if en_t:
                    f.write(f"**EN**: {en_t}\n\n")
            f.write("\n")

    # 2. English
    with open(os.path.join(ch_dir, "chapter_en.md"), 'w', encoding='utf-8') as f:
        f.write(f"# CloudInsect - {ch_info['title_en']}\n\n*Original Title: {ch_info['title_zh']}*\n\n---\n\n")
        for p in panels:
            m_md = format_media_md(p)
            if m_md:
                f.write(f"{m_md}\n")
            for t in p['texts'].get('en', []):
                f.write(f"> {t}\n\n")
            f.write("\n")

    # 3. Chinese
    with open(os.path.join(ch_dir, "chapter_zh.md"), 'w', encoding='utf-8') as f:
        f.write(f"# 云虫 - {ch_info['title_zh']}\n\n---\n\n")
        for p in panels:
            m_md = format_media_md(p)
            if m_md:
                f.write(f"{m_md}\n")
            for t in p['texts'].get('zh', []):
                f.write(f"> {t}\n\n")
            f.write("\n")


def process_chapter(ch_info):
    ch_dir = os.path.join(CHAPTERS_DIR, ch_info['dir'])
    media_dir = os.path.join(ch_dir, "media")
    os.makedirs(media_dir, exist_ok=True)

    url = urljoin(BASE_URL, ch_info['file'])
    r = session.get(url)
    if r.status_code != 200:
        print(f"Error fetching {url}: {r.status_code}")
        return None

    soup = BeautifulSoup(r.text, 'html.parser')

    for script in soup.find_all('script'):
        if script.get('src') and 'challenge-platform' in script['src']:
            script.decompose()
        elif script.string and 'challenge-platform' in script.string:
            script.decompose()

    panels, languages = parse_chapter_content(soup)

    downloads = []
    for p in panels:
        if p.get('orig_vid_url') and p.get('video_src'):
            downloads.append((p['orig_vid_url'], os.path.join(ch_dir, p['video_src'])))
        if p.get('orig_img_url') and p.get('image_src'):
            downloads.append((p['orig_img_url'], os.path.join(ch_dir, p['image_src'])))
        if p.get('orig_poster_url') and p.get('poster_src'):
            downloads.append((p['orig_poster_url'], os.path.join(ch_dir, p['poster_src'])))

    for link in soup.find_all('link'):
        href = link.get('href')
        if href and href.startswith('assets/'):
            link['href'] = f"../../{href}"

    for script in soup.find_all('script'):
        src = script.get('src')
        if src and src.startswith('assets/'):
            script['src'] = f"../../{src}"

    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            if src.startswith('assets/'):
                img['src'] = f"../../{src}"
            else:
                fname = os.path.basename(src)
                if '/pro/' in src:
                    img['src'] = f"media/pro/{fname}"
                elif '/web/' in src:
                    img['src'] = f"media/web/{fname}"
                else:
                    img['src'] = f"media/{fname}"

    for video in soup.find_all('video'):
        src = video.get('src')
        if src:
            v_name = os.path.basename(src)
            if '/pro/' in src:
                video['src'] = f"media/pro/{v_name}"
            elif '/web/' in src:
                video['src'] = f"media/web/{v_name}"
            else:
                video['src'] = f"media/{v_name}"
        poster = video.get('poster')
        if poster:
            p_name = os.path.basename(poster)
            if '/pro/' in poster:
                video['poster'] = f"media/pro/{p_name}"
            elif '/web/' in poster:
                video['poster'] = f"media/web/{p_name}"
            else:
                video['poster'] = f"media/{p_name}"

    for a in soup.find_all('a', href=True):
        href = a['href']
        if href in ['/', 'index.html']:
            a['href'] = "../../index.html"
        else:
            for target_ch in CHAPTERS_CONFIG:
                if href == target_ch['file']:
                    a['href'] = f"../{target_ch['dir']}/index.html"

    for opt in soup.find_all('option'):
        val = opt.get('value')
        if val:
            for target_ch in CHAPTERS_CONFIG:
                if val == target_ch['file']:
                    opt['value'] = f"../{target_ch['dir']}/index.html"

    with open(os.path.join(ch_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write(str(soup))

    write_chapter_markdown(ch_dir, ch_info, panels)

    clean_panels = []
    for p in panels:
        cp = dict(p)
        cp.pop('orig_img_url', None)
        cp.pop('orig_vid_url', None)
        cp.pop('orig_poster_url', None)
        clean_panels.append(cp)

    ch_data = {
        'id': ch_info['id'],
        'dir': ch_info['dir'],
        'file': ch_info['file'],
        'title_zh': ch_info['title_zh'],
        'title_en': ch_info['title_en'],
        'available_languages': languages,
        'panel_count': len([p for p in clean_panels if p.get('image_src') or p.get('video_src')]),
        'panels': clean_panels
    }
    with open(os.path.join(ch_dir, "chapter_data.json"), 'w', encoding='utf-8') as f:
        json.dump(ch_data, f, ensure_ascii=False, indent=2)

    return ch_data, downloads


def process_homepage():
    r = session.get(BASE_URL)
    soup = BeautifulSoup(r.text, 'html.parser')

    for script in soup.find_all('script'):
        if script.get('src') and 'challenge-platform' in script['src']:
            script.decompose()
        elif script.string and 'challenge-platform' in script.string:
            script.decompose()

    for a in soup.find_all('a', href=True):
        href = a['href']
        for target_ch in CHAPTERS_CONFIG:
            if href == target_ch['file']:
                a['href'] = f"chapters/{target_ch['dir']}/index.html"

    index_str = str(soup)
    index_str = index_str.replace('chapter-5-wuzhui-1-images/catalog-xiang-yu.jpg', 'assets/chapter-banners/catalog-xiang-yu.jpg')
    index_str = index_str.replace('images/chapter-5-wuzhui-2/cover-mahina-profile.jpg', 'assets/chapter-banners/cover-mahina-profile.jpg')

    with open(os.path.join(WORKSPACE_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(index_str)

    asset_urls = [
        'assets/cloud-insect-logo-v4.2.03.png',
        'assets/site-footer.css?v=5.1.39',
        'assets/site-footer.js?v=5.1.39',
        'assets/pager-prev.png',
        'assets/pager-next.png',
        'assets/narration-mark.svg',
        'assets/wlop-art-jost.woff2',
        'assets/wlop-art-entry.webp',
        'assets/cloudinsect-home-bg-v2.mp4',
        'assets/wallpapers/wp0.mp4',
        'assets/wallpapers/wp1.mp4',
        'assets/wallpapers/wp8.mp4',
        'assets/wallpapers/xiang-yu-riverside-home-bg-seamless-10s.mp4',
        'assets/wallpapers/wp0-poster.jpg',
        'assets/wallpapers/wp1-poster.jpg',
        'assets/wallpapers/wp8-poster.jpg',
        'assets/wallpapers/xiang-yu-riverside-home-bg-final-10s-poster.jpg',
        'assets/chapter-banners/chapter-0-prologue.jpg',
        'assets/chapter-banners/chapter-1-xiyang.jpg',
        'assets/chapter-banners/chapter-2-cloud-dwellers-1.jpg',
        'assets/chapter-banners/chapter-2-cloud-dwellers-2.jpg',
        'assets/chapter-banners/chapter-2-cloud-dwellers-3.jpg',
        'assets/chapter-banners/chapter-3-beyond-light-cone-1.jpg',
        'assets/chapter-banners/chapter-3-beyond-light-cone-2.jpg',
        'assets/chapter-banners/chapter-4-fate-1.jpg',
        'assets/chapter-banners/chapter-4-fate-2.jpg',
        'chapter-5-wuzhui-1-images/catalog-xiang-yu.jpg',
        'images/chapter-5-wuzhui-2/cover-mahina-profile.jpg'
    ]

    downloads = []
    for a_url in asset_urls:
        full_url = urljoin(BASE_URL, a_url)
        clean = a_url.split('?')[0]
        if 'catalog-xiang-yu.jpg' in clean:
            target = os.path.join(ASSETS_DIR, "chapter-banners", "catalog-xiang-yu.jpg")
        elif 'cover-mahina-profile.jpg' in clean:
            target = os.path.join(ASSETS_DIR, "chapter-banners", "cover-mahina-profile.jpg")
        else:
            target = os.path.join(WORKSPACE_DIR, clean)
        downloads.append((full_url, target))

    return downloads


def main():
    print("==================================================")
    print("  CLOUD INSECT (云虫) ORGANIZED CHAPTER CRAWLER   ")
    print("==================================================")

    all_downloads = []

    print(">>> Processing Homepage and Global Assets...")
    home_downloads = process_homepage()
    all_downloads.extend(home_downloads)

    all_summary = []
    for ch in CHAPTERS_CONFIG:
        print(f">>> Processing {ch['dir']} ({ch['title_zh']})...")
        res = process_chapter(ch)
        if res:
            data, ch_downloads = res
            all_summary.append(data)
            all_downloads.extend(ch_downloads)

    with open(os.path.join(DATA_DIR, "all_chapters.json"), 'w', encoding='utf-8') as f:
        json.dump(all_summary, f, ensure_ascii=False, indent=2)

    root_readme = os.path.join(WORKSPACE_DIR, "README.md")
    with open(root_readme, 'w', encoding='utf-8') as f:
        f.write("# Vân Trùng (云虫 / Cloud Insect) - Trọn bộ các Chapter\n\n")
        f.write("Tác giả: **WLOP** | Website gốc: [cloudinsect.com](https://cloudinsect.com/)\n\n")
        f.write("Toàn bộ truyện đã được tải về và sắp xếp ngăn nắp theo từng thư mục chapter độc lập, gồm đầy đủ **hình ảnh, hoạt cảnh video chuyển động, văn bản 10 ngôn ngữ và bản đọc Offline trên trình duyệt**.\n\n")
        f.write("## 🚀 Cách đọc truyện:\n")
        f.write("1. **Đọc trên trình duyệt (Khuyên dùng):** Mở trực tiếp file [`index.html`](./index.html) tại thư mục gốc để vào giao diện mục lục chọn chapter, hoặc mở file `index.html` trong từng thư mục chapter.\n")
        f.write("2. **Đọc dạng Markdown:** Xem các file `.md` trong từng thư mục chapter bên dưới.\n\n")
        f.write("## 📚 Danh sách các Chapter:\n\n")
        f.write("| # | Tên tiếng Trung | Tên tiếng Anh | Motion Video | Thư mục Chapter | Bản Song Ngữ | Đọc Offline |\n")
        f.write("|---|-----------------|---------------|:------------:|-----------------|--------------|:-----------:|\n")
        for idx, ch in enumerate(CHAPTERS_CONFIG, 1):
            has_v = "🎬 Có Video" if ch['id'] in ['chapter-4-2', 'chapter-5-1'] else "🖼️ Ảnh tĩnh"
            d = ch['dir']
            f.write(f"| {idx:02d} | {ch['title_zh']} | {ch['title_en']} | {has_v} | [`chapters/{d}/`](./chapters/{d}/) | [Song ngữ](./chapters/{d}/chapter_bilingual.md) | [Mở HTML](./chapters/{d}/index.html) |\n")

    print(f"\n=== Downloading {len(all_downloads)} media & assets in parallel ===")
    completed = 0
    total = len(all_downloads)
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(download_file_to, url, path): path for url, path in all_downloads}
        for future in as_completed(futures):
            path = futures[future]
            completed += 1
            if completed % 30 == 0 or completed == total:
                print(f"[{completed}/{total}] Checked/Downloaded: {os.path.basename(path)}")

    print("\n==================================================")
    print(" HOÀN TẤT! Toàn bộ file đã được sắp xếp ngăn nắp.")
    print("==================================================")


if __name__ == '__main__':
    main()
