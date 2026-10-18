import subprocess, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
html_file = os.path.abspath('chapters/chapter-5-wuzhui-2/index.html')

cmd = [
    chrome_path, '--headless', '--disable-gpu', '--dump-dom',
    f'file:///{html_file}'
]
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
idx = res.stdout.find('Hạng Vũ ngoảnh đầu lại')
print('Found Hạng Vũ in rendered DOM:', idx != -1)
if idx != -1:
    print(res.stdout[idx-50:idx+400])
