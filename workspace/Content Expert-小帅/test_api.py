# -*- coding: utf-8 -*-
import winreg
import os
import json
import urllib.request
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment')
appid, _ = winreg.QueryValueEx(key, 'WECHAT_APP_ID')
appsecret, _ = winreg.QueryValueEx(key, 'WECHAT_APP_SECRET')
winreg.CloseKey(key)

print('[INFO] AppID:', appid)

# 使用 stable token
url = 'https://api.weixin.qq.com/cgi-bin/stable_token'
data = json.dumps({
    'grant_type': 'client_credential',
    'appid': appid,
    'secret': appsecret,
    'force_refresh': True
}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req, timeout=30) as response:
    result = json.loads(response.read().decode('utf-8'))
    access_token = result['access_token']

print('[INFO] Testing APIs...')

# 测试各种接口
apis = [
    '/cgi-bin/getcallbackip',
    '/cgi-bin/get_menu',
    '/cgi-bin/user/get',
]

for api in apis:
    try:
        url = 'https://api.weixin.qq.com' + api + '?access_token=' + access_token
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            r = json.loads(resp.read().decode('utf-8'))
            if r.get('errcode') == 0:
                print('[OK] ' + api)
            else:
                msg = str(r.get('errmsg', ''))[:30]
                print('[FAIL] ' + api + ': ' + str(r.get('errcode')) + ' - ' + msg)
    except Exception as e:
        err = str(e)[:40]
        print('[ERROR] ' + api + ': ' + err)