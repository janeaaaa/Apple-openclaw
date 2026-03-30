# -*- coding: utf-8 -*-
import os
import sys
import io

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 从注册表读取正确的环境变量名
appid = os.getenv('WECHAT_APP_ID')
appsecret = os.getenv('WECHAT_APP_SECRET')

# 映射到脚本需要的变量名
os.environ['WECHAT_APPID'] = appid
os.environ['WECHAT_APPSECRET'] = appsecret

print('[INFO] Using APPID:', appid)

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

# 设置参数 - 使用英文避免编码问题
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