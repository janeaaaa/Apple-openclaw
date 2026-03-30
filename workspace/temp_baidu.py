# -*- coding: utf-8 -*-
import urllib.request
import re
import json
import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

url = 'https://top.baidu.com/board?tab=realtime'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req, timeout=10)
    data = resp.read().decode('utf-8')
    # 尝试hotList
    m = re.search(r'"hotList":(\[.*?\])', data, re.DOTALL)
    if m:
        news = json.loads(m.group(1))
        for i, n in enumerate(news[:15]):
            print(f'{i+1}. {n.get("title", "")}')
    else:
        # 尝试其他方式提取
        m2 = re.search(r'"hotList":(.*?),"banner"', data)
        if m2:
            print('Found hotList pattern 2')
            print(m2.group(1)[:200])
except Exception as e:
    print('Error:', e)
