# -*- coding: utf-8 -*-
import urllib.request
import re
import json

url = 'https://top.baidu.com/board?tab=realtime'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')

m = re.search(r'"hotList":\[(.*?)\]', html, re.DOTALL)
if m:
    items = m.group(1)
    # Fix JSON by wrapping in array
    json_str = '[' + items + ']'
    data = json.loads(json_str)
    for item in data[:15]:
        word = item.get('word', '')
        desc = item.get('desc', '')
        print(f"- {word}")
        if desc:
            print(f"  {desc[:100]}")
        print()
else:
    print('No match')