# -*- coding: utf-8 -*-
import urllib.request
import re

url = 'https://top.baidu.com/board?tab=realtime'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req, timeout=10)
html = response.read().decode('utf-8')

match = re.search(r'"hotList":\[(.*?)\]', html, re.DOTALL)
if match:
    items = match.group(1)
    words = re.findall(r'"word":"([^"]+)"', items)
    for w in words[:20]:
        print(w)