import glob
import re

c = open('chapters/chapter-5-wuzhui-2/index.html', encoding='utf-8').read()
m = re.findall(r'data-i18n-(?:alt|title|aria-label)-zh="[^"]*"', c)
print('Count of data-i18n-*-zh in ch5.2:', len(m))

# Check how many have -vi
m_vi = re.findall(r'data-i18n-(?:alt|title|aria-label)-vi="[^"]*"', c)
print('Count of data-i18n-*-vi in ch5.2:', len(m_vi))
