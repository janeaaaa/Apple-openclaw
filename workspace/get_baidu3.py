# -*- coding: utf-8 -*-
import urllib.request
import re

url = 'https://top.baidu.com/board?tab=realtime'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')

# The text might be double-encoded - let's check for Chinese characters
matches = re.findall(r'"word":"([^"]+)"', html)
print(f"Found {len(matches)} words")

# Print first few in hex to understand encoding
for i, w in enumerate(matches[:3]):
    print(f"{i+1}. {w}")
    print(f"   hex: {w.encode('utf-8').hex()}")