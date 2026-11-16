import subprocess
import os

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
html_path = os.path.abspath("chapters/chapter-5-wuzhui-2/index.html")
out_img = os.path.abspath(r"C:\Users\mochioka\.gemini\antigravity\brain\51ee8a03-eca8-40f5-bee9-7d531a31cb9c\test_ch52_render.png")

cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--window-size=1280,3000",
    f"--screenshot={out_img}",
    f"file:///{html_path.replace(os.sep, '/')}"
]

print("Running chrome screenshot...")
res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
print("Output file exists:", os.path.exists(out_img))
if os.path.exists(out_img):
    print("Size:", os.path.getsize(out_img))
