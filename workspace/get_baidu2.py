# -*- coding: utf-8 -*-
import urllib.request
import re

url = 'https://top.baidu.com/board?tab=realtime'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')

# Look for any JSON-like content with 'word' keys
matches = re.findall(r'"word":"([^"]+)"', html)
print("Found words:")
for i, w in enumerate(matches[:20]):
    print(f"{i+1}. {w}")