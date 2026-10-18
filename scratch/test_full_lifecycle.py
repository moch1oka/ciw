import subprocess, os, re, sys, tempfile

sys.stdout.reconfigure(encoding='utf-8')
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
html_file = os.path.abspath('chapters/chapter-5-wuzhui-2/index.html')
user_data_dir = tempfile.mkdtemp()

# Step 1: Create a small helper page in the same origin (same directory) that sets localStorage to 'zh'
set_zh_page = os.path.abspath('scratch/set_zh.html')
with open(set_zh_page, 'w', encoding='utf-8') as f:
    f.write("""<!DOCTYPE html><html><body><script>
localStorage.setItem('cloudinsect-lang', 'zh');
document.write('SET_DONE');
</script></body></html>""")

# Run Chrome to set 'zh' in localStorage
cmd1 = [
    chrome_path, '--headless', '--disable-gpu',
    f'--user-data-dir={user_data_dir}', '--dump-dom',
    f'file:///{set_zh_page}'
]
subprocess.run(cmd1, capture_output=True, text=True)

# Step 2: Now open chapter-5-wuzhui-2 and verify it reads 'zh'
cmd2 = [
    chrome_path, '--headless', '--disable-gpu',
    f'--user-data-dir={user_data_dir}', '--dump-dom',
    f'file:///{html_file}'
]
res2 = subprocess.run(cmd2, capture_output=True, text=True, encoding='utf-8', errors='replace')
print("Step 2 (when localStorage is 'zh'):")
m_text2 = re.search(r'<p class="text[^"]*"[^>]*>(.*?)</p>', res2.stdout)
print("  Lang:", re.search(r'<html[^>]*>', res2.stdout).group(0))
print("  First text:", m_text2.group(0) if m_text2 else 'none')

# Step 3: Now simulate user selecting 'vi' in dropdown (sets localStorage to 'vi')
set_vi_page = os.path.abspath('scratch/set_vi.html')
with open(set_vi_page, 'w', encoding='utf-8') as f:
    f.write("""<!DOCTYPE html><html><body><script>
localStorage.setItem('cloudinsect-lang', 'vi');
document.write('SET_VI_DONE');
</script></body></html>""")

subprocess.run([
    chrome_path, '--headless', '--disable-gpu',
    f'--user-data-dir={user_data_dir}', '--dump-dom',
    f'file:///{set_vi_page}'
], capture_output=True, text=True)

# Step 4: Now reload chapter-5-wuzhui-2 and verify it renders 'vi' and STAYS 'vi'
cmd4 = [
    chrome_path, '--headless', '--disable-gpu',
    f'--user-data-dir={user_data_dir}', '--dump-dom',
    f'file:///{html_file}'
]
res4 = subprocess.run(cmd4, capture_output=True, text=True, encoding='utf-8', errors='replace')
print("Step 4 (after user selected 'vi'):")
m_text4 = re.search(r'<p class="text[^"]*"[^>]*>(.*?)</p>', res4.stdout)
print("  Lang:", re.search(r'<html[^>]*>', res4.stdout).group(0))
print("  First text:", m_text4.group(0) if m_text4 else 'none')

# Step 5: Check localStorage value to ensure it did NOT get overwritten back to 'zh'
check_ls_page = os.path.abspath('scratch/check_ls.html')
with open(check_ls_page, 'w', encoding='utf-8') as f:
    f.write("""<!DOCTYPE html><html><body><script>
document.write('FINAL_STORED_LANG=' + localStorage.getItem('cloudinsect-lang'));
</script></body></html>""")
res5 = subprocess.run([
    chrome_path, '--headless', '--disable-gpu',
    f'--user-data-dir={user_data_dir}', '--dump-dom',
    f'file:///{check_ls_page}'
], capture_output=True, text=True)
m_ls = re.search(r'FINAL_STORED_LANG=[a-zA-Z0-9_-]+', res5.stdout)
print("Step 5 (persisted localStorage check):", m_ls.group(0) if m_ls else 'NOT FOUND')
