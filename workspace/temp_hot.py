# -*- coding: utf-8 -*-
import urllib.request
import re
import json
import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

# 百度热搜
url = 'https://top.baidu.com/board?tab=realtime'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req, timeout=10)
    data = resp.read().decode('utf-8')
    m = re.search(r'"newsList":(\[.*?\])', data, re.DOTALL)
    if m:
        news = json.loads(m.group(1))
        for i, n in enumerate(news[:15]):
            print(f'{i+1}. {n.get("title", "")}')
except Exception as e:
    print('Error:', e)
