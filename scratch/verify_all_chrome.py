import subprocess, os, re, sys, glob

sys.stdout.reconfigure(encoding='utf-8')
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

all_chapters = sorted(glob.glob('chapters/*/index.html'))
print(f"Verifying all {len(all_chapters)} chapters with headless Chrome...")

for ch in all_chapters:
    html_file = os.path.abspath(ch)
    cmd = [
        chrome_path,
        '--headless',
        '--disable-gpu',
        '--dump-dom',
        f'file:///{html_file}'
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    html_tag = re.search(r'<html[^>]*>', res.stdout)
    lang_val = html_tag.group(0) if html_tag else 'NONE'
    m_title = re.search(r'<title>(.*?)</title>', res.stdout)
    title = m_title.group(1) if m_title else 'NONE'
    
    # Check that it rendered in vi
    is_vi = 'lang="vi"' in lang_val
    print(f"[{'PASS' if is_vi else 'FAIL'}] {ch} -> lang: {lang_val[:25]} | title: {title}")
