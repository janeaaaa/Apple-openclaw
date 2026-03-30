# -*- coding: utf-8 -*-
import urllib.request
import re
import html

url = 'https://top.baidu.com/board?tab=realtime'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html_content = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')

matches = re.findall(r'"word":"([^"]+)"', html_content)
print(f"Found {len(matches)} words")
print()

for i, w in enumerate(matches[:20]):
    # Try to decode HTML entities if present
    try:
        # The text appears to be double-encoded
        decoded = html.unescape(w)
        # Check if it's still garbled, try another decode
        if '?' in decoded or len(decoded) < 3:
            # Try decoding from the raw bytes
            decoded = w.encode('utf-8').decode('utf-8')
    except:
        decoded = w
    
    print(f"{i+1}. {decoded}")