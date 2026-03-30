# -*- coding: utf-8 -*-
import winreg
import os
import json
import urllib.request
import io
import sys
import tempfile
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment')
appid, _ = winreg.QueryValueEx(key, 'WECHAT_APP_ID')
appsecret, _ = winreg.QueryValueEx(key, 'WECHAT_APP_SECRET')
winreg.CloseKey(key)

print('[INFO] Getting token...')

# 使用 stable token
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

print('[INFO] Uploading cover image...')

# 创建测试图片
img = Image.new('RGB', (900, 500), color=(30, 30, 60))
tmp_path = tempfile.mktemp(suffix='.jpg')
img.save(tmp_path, 'JPEG')

# 上传图片到微信服务器
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

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        r = json.loads(resp.read().decode('utf-8'))
        print('[UPLOAD RESULT]', r)
        
        if 'url' in r:
            thumb_url = r['url']
            print('[OK] Image uploaded:', thumb_url)
            
            # 尝试上传为永久素材获取media_id
            url2 = 'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=' + access_token + '&type=image'
            
            body2 = b'--' + boundary.encode() + b'\r\n'
            body2 += b'Content-Disposition: form-data; name="media"; filename="cover.jpg"\r\n'
            body2 += b'Content-Type: image/jpeg\r\n\r\n'
            body2 = body2 + image_data + b'\r\n--' + boundary.encode() + b'--\r\n'
            
            req2 = urllib.request.Request(url2, data=body2, headers={
                'Content-Type': 'multipart/form-data; boundary=' + boundary
            })
            
            try:
                with urllib.request.urlopen(req2, timeout=30) as resp2:
                    r2 = json.loads(resp2.read().decode('utf-8'))
                    print('[MATERIAL RESULT]', r2)
            except Exception as e:
                print('[MATERIAL ERROR]', e)
except Exception as e:
    print('[UPLOAD ERROR]', e)

os.remove(tmp_path)