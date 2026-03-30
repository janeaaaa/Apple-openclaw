# -*- coding: utf-8 -*-
import winreg
import os
import sys
import io

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 从注册表读取环境变量
try:
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment')
    appid, _ = winreg.QueryValueEx(key, 'WECHAT_APP_ID')
    appsecret, _ = winreg.QueryValueEx(key, 'WECHAT_APP_SECRET')
    winreg.CloseKey(key)
    print('[INFO] APPID from registry:', appid[:10] + '...')
except Exception as e:
    print('[ERROR] Failed to read registry:', e)
    sys.exit(1)

os.environ['WECHAT_APPID'] = appid
os.environ['WECHAT_APPSECRET'] = appsecret

# 读取channel.py
script_path = r'C:\Users\Administrator\.openclaw\workspace\Content Expert-小帅\skills\channel-1.0.6\scripts\channel.py'
with open(script_path, 'r', encoding='utf-8') as f:
    script_content = f.read()

# 替换emoji为文本
script_content = script_content.replace('print("❌', 'print("[ERROR]')
script_content = script_content.replace('print("✅', 'print("[OK]')
script_content = script_content.replace('print("📝', 'print("[INFO]')
script_content = script_content.replace('print("💡', 'print("[TIP]')
script_content = script_content.replace('print("🎨', 'print("[COVER]')

# 设置参数
sys.argv = [
    'channel.py', 
    'create', 
    'AI的6个月 = 现实3年：这是普通人最后的机会窗口',
    '--file', 
    r'C:\Users\Administrator\.openclaw\workspace\Content Expert-小帅\article.txt',
    '--author', 
    '小帅'
]

# 执行
exec(script_content)