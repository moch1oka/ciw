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
print('DOM length:', len(res.stdout))
print('html lang:', re.search(r'<html[^>]*>', res.stdout).group(0))
m_title = re.search(r'<title>(.*?)</title>', res.stdout)
print('title:', m_title.group(1) if m_title else 'NONE')
m_texts = re.findall(r'<p class="text[^"]*"[^>]*>(.*?)</p>', res.stdout)
for t in m_texts[:5]:
    print('Rendered text:', t[:100])
