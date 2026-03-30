# -*- coding: utf-8 -*-
import urllib.request
import re

url = 'https://top.baidu.com/board?tab=realtime'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')

matches = re.findall(r'"word":"([^"]+)"', html)

# Write to file
with open(r'C:\Users\Administrator\.openclaw\workspace\hot_list.txt', 'w', encoding='utf-8') as f:
    for i, w in enumerate(matches[:30]):
        f.write(f"{i+1}. {w}\n")

print("Wrote file")