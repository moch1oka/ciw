import subprocess, os, re, sys, tempfile

sys.stdout.reconfigure(encoding='utf-8')
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
html_file = os.path.abspath('chapters/chapter-5-wuzhui-2/index.html')

# Create a test wrapper that sets localStorage and checks result
wrapper_html = f"""
<!DOCTYPE html>
<html>
<body>
<iframe id="testframe" src="file:///{html_file}" style="width:1000px; height:800px;"></iframe>
<script>
window.addEventListener('message', () => {{}});
setTimeout(() => {{
  const frameDoc = document.getElementById('testframe').contentDocument;
  console.log('FRAME LANG:', frameDoc.documentElement.lang);
  console.log('FRAME TITLE:', frameDoc.title);
  const firstText = frameDoc.querySelector('p.text');
  console.log('FRAME FIRST TEXT:', firstText ? firstText.textContent : 'none');
}}, 1000);
</script>
</body>
</html>
"""
wrapper_path = os.path.abspath('scratch/test_wrapper.html')
with open(wrapper_path, 'w', encoding='utf-8') as f:
    f.write(wrapper_html)

# Test with a separate user data dir to test fresh localStorage
user_data_dir = tempfile.mkdtemp()
cmd = [
    chrome_path,
    '--headless',
    '--disable-gpu',
    f'--user-data-dir={user_data_dir}',
    '--dump-dom',
    f'file:///{html_file}'
]
res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
print("--- Fresh user profile test ---")
print("Lang:", re.search(r'<html[^>]*>', res.stdout).group(0))
m_text = re.search(r'<p class="text[^"]*"[^>]*>(.*?)</p>', res.stdout)
print("First text:", m_text.group(0) if m_text else 'none')
