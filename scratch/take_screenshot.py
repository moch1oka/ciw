import subprocess, os

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
html_file = os.path.abspath('chapters/chapter-5-wuzhui-2/index.html')
screenshot_path = os.path.abspath('scratch/preview_panel2_fixed.png')

cmd = [
    chrome_path,
    '--headless',
    '--disable-gpu',
    '--window-size=1280,2600',
    f'--screenshot={screenshot_path}',
    f'file:///{html_file}'
]
subprocess.run(cmd, capture_output=True, text=True)
print('Screenshot generated:', os.path.exists(screenshot_path))
