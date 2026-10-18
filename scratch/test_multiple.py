import subprocess, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

for ch in ['chapters/chapter-0-prologue/index.html', 'chapters/chapter-4-fate-2/index.html', 'chapters/chapter-5-wuzhui-1/index.html', 'chapters/chapter-5-wuzhui-2/index.html']:
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
    # Check visible text
    print(f"=== {ch} ===")
    print(f"  html tag: {lang_val}")
    print(f"  title: {title}")
