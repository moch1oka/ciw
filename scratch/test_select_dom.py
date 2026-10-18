import subprocess, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
html_file = os.path.abspath('chapters/chapter-5-wuzhui-2/index.html')

cmd = [
    chrome_path,
    '--headless',
    '--disable-gpu',
    '--dump-dom',
    f'file:///{html_file}'
]
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
m = re.search(r'<select[^>]*class="language-select"[^>]*>([\s\S]*?)</select>', res.stdout)
if m:
    print('Rendered select tag:', m.group(0))
