# -*- coding: utf-8 -*-
import winreg
import os
import json
import urllib.request
import io
import sys
import tempfile
import random
from PIL import Image, ImageDraw

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment')
appid, _ = winreg.QueryValueEx(key, 'WECHAT_APP_ID')
appsecret, _ = winreg.QueryValueEx(key, 'WECHAT_APP_SECRET')
winreg.CloseKey(key)

# 获取token
url = 'https://api.weixin.qq.com/cgi-bin/stable_token'
data = json.dumps({
    'grant_type': 'client_credential',
    'appid': appid,
    'secret': appsecret
}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req, timeout=30) as response:
    result = json.loads(response.read().decode('utf-8'))
    access_token = result['access_token']

print('[INFO] Creating better cover image...')

# 创建一张更有科技感的封面图
width, height = 900, 500
img = Image.new('RGB', (width, height))
draw = ImageDraw.Draw(img)

# 渐变背景 - 深蓝到紫色
for y in range(height):
    r = int(10 + (y / height) * 30)
    g = int(20 + (y / height) * 50)
    b = int(60 + (y / height) * 100)
    for x in range(width):
        img.putpixel((x, y), (r, g, b))

# 添加一些科技感的线条
random.seed(42)
for _ in range(30):
    x1 = random.randint(0, width)
    y1 = random.randint(0, height)
    x2 = x1 + random.randint(-200, 200)
    y2 = y1 + random.randint(-50, 50)
    color = (random.randint(100, 200), random.randint(150, 255), random.randint(200, 255))
    draw.line([(x1, y1), (x2, y2)], fill=color, width=2)

# 添加圆形光点
for _ in range(20):
    x = random.randint(0, width)
    y = random.randint(0, height)
    r = random.randint(5, 30)
    color = (random.randint(150, 255), random.randint(200, 255), 255)
    draw.ellipse([x-r, y-r, x+r, y+r], fill=color)

# 保存图片
tmp_path = tempfile.mktemp(suffix='.jpg')
img.save(tmp_path, 'JPEG', quality=95)

print('[INFO] Uploading cover...')

# 上传图片
url = 'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=' + access_token

with open(tmp_path, 'rb') as f:
    image_data = f.read()

boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = b'--' + boundary.encode() + b'\r\n'
body += b'Content-Disposition: form-data; name="media"; filename="cover.jpg"\r\n'
body += b'Content-Type: image/jpeg\r\n\r\n'
body = body + image_data + b'\r\n--' + boundary.encode() + b'--\r\n'

req = urllib.request.Request(url, data=body, headers={
    'Content-Type': 'multipart/form-data; boundary=' + boundary
})

with urllib.request.urlopen(req, timeout=30) as resp:
    r = json.loads(resp.read().decode('utf-8'))
    print('[UPLOAD RESULT]', r)
    
    if 'url' in r:
        thumb_url = r['url']
        print('[OK] Cover uploaded')
        
        # 上传为永久素材获取media_id
        url2 = 'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=' + access_token + '&type=image'
        
        body2 = b'--' + boundary.encode() + b'\r\n'
        body2 += b'Content-Disposition: form-data; name="media"; filename="cover.jpg"\r\n'
        body2 += b'Content-Type: image/jpeg\r\n\r\n'
        body2 = body2 + image_data + b'\r\n--' + boundary.encode() + b'--\r\n'
        
        req2 = urllib.request.Request(url2, data=body2, headers={
            'Content-Type': 'multipart/form-data; boundary=' + boundary
        })
        
        with urllib.request.urlopen(req2, timeout=30) as resp2:
            r2 = json.loads(resp2.read().decode('utf-8'))
            print('[MATERIAL RESULT]', r2)
            thumb_media_id = r2.get('media_id')
            print('[INFO] thumb_media_id:', thumb_media_id)

os.remove(tmp_path)