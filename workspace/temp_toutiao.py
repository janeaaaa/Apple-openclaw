# -*- coding: utf-8 -*-
import urllib.request
import json
import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

# 今日头条热搜
url = 'https://www.toutiao.com/api/pc/feed/?category=news_hot&utm_source=toutiao&widen=1&max_behot_time=0'

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read().decode('utf-8'))
    if 'data' in data:
        for i, item in enumerate(data['data'][:10]):
            title = item.get('title', '')
            if title:
                print(f'{i+1}. {title}')
except Exception as e:
    print('Error:', e)
