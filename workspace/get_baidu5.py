# -*- coding: utf-8 -*-
import urllib.request
import re

url = 'https://top.baidu.com/board?tab=realtime'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, timeout=10).read()

# Try different encodings
for enc in ['utf-8', 'gbk', 'gb2312', 'gb18030']:
    try:
        content = html.decode(enc)
        matches = re.findall(r'"word":"([^"]+)"', content)
        if matches:
            print(f"Encoding: {enc}")
            for i, w in enumerate(matches[:10]):
                print(f"{i+1}. {w}")
            break
    except:
        pass