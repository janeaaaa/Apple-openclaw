# -*- coding: utf-8 -*-
import winreg
import os
import json
import urllib.request
import io
import sys
import tempfile
import random
from PIL import Image, ImageDraw, ImageFont

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

print('[INFO] Creating cover for Manus article...')

# 创建封面 - 蓝底白字风格
width, height = 900, 500
img = Image.new('RGB', (width, height), color=(40, 40, 80))
draw = ImageDraw.Draw(img)

# 添加装饰光点
random.seed(1234)
for _ in range(25):
    x = random.randint(0, width)
    y = random.randint(0, height)
    r = random.randint(30, 90)
    for i in range(r, 0, -15):
        color = (70, 80, 150)
        draw.ellipse([x-i, y-i, x+i, y+i], fill=color)

# 加载字体
font_paths = [r'C:\Windows\Fonts\msyh.ttc', r'C:\Windows\Fonts\simhei.ttf']
font_large = None
font_small = None
for fp in font_paths:
    try:
        font_large = ImageFont.truetype(fp, 36)
        font_small = ImageFont.truetype(fp, 22)
        break
    except:
        continue
if font_large is None:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

# 绘制标题 - 用英文字母代替中文避免乱码
draw.text((60, 160), "Manus", fill=(255, 255, 255), font=font_large)
draw.text((250, 160), "x", fill=(200, 200, 200), font=font_small)
draw.text((280, 160), "Meta", fill=(255, 200, 50), font=font_large)
draw.text((420, 160), "?", fill=(255, 100, 100), font=font_large)

# 副标题
draw.text((60, 320), "138", fill=(255, 255, 255), font=font_large)
draw.text((180, 320), "Billion", fill=(180, 180, 180), font=font_small)
draw.text((320, 320), "USD", fill=(255, 200, 50), font=font_small)
draw.text((420, 320), "Deal", fill=(180, 180, 180), font=font_small)

# 保存
tmp_path = tempfile.mktemp(suffix='.png')
img.save(tmp_path, 'PNG')

print('[INFO] Uploading cover...')

# 上传
url = 'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=' + access_token

with open(tmp_path, 'rb') as f:
    image_data = f.read()

boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = b'--' + boundary.encode() + b'\r\n'
body += b'Content-Disposition: form-data; name="media"; filename="cover.png"\r\n'
body += b'Content-Type: image/png\r\n\r\n'
body = body + image_data + b'\r\n--' + boundary.encode() + b'--\r\n'

req = urllib.request.Request(url, data=body, headers={'Content-Type': 'multipart/form-data; boundary=' + boundary})

with urllib.request.urlopen(req, timeout=30) as resp:
    r = json.loads(resp.read().decode('utf-8'))
    print('[UPLOAD]', r)
    
    if 'url' in r:
        # 获取永久素材
        url2 = 'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=' + access_token + '&type=image'
        body2 = b'--' + boundary.encode() + b'\r\n'
        body2 += b'Content-Disposition: form-data; name="media"; filename="cover.png"\r\n'
        body2 += b'Content-Type: image/png\r\n\r\n'
        body2 = body2 + image_data + b'\r\n--' + boundary.encode() + b'--\r\n'
        
        req2 = urllib.request.Request(url2, data=body2, headers={'Content-Type': 'multipart/form-data; boundary=' + boundary})
        with urllib.request.urlopen(req2, timeout=30) as resp2:
            r2 = json.loads(resp2.read().decode('utf-8'))
            thumb_media_id = r2.get('media_id')
            print('[MEDIA ID]', thumb_media_id)
            
            # 创建草稿
            print('[INFO] Creating draft...')
            
            title = '头条重磅！中国AI公司被Meta收购后，高管被限制出境'
            digest = '138亿的交易，踩了红线？科技圈又炸了。'
            
            content = '''<p style="font-size:16px;color:#333333;line-height:1.8;margin-bottom:20px;"><strong>138亿的交易，踩了红线？</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">科技圈又炸了。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">就在一周前，一则消息让整个AI圈沸腾：</p>

<p style="font-size:16px;color:#333333;line-height:1.8;margin-bottom:20px;"><strong>Meta以约20亿美元（约138亿人民币）收购了中国AI公司Manus。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">这本来是个"国产AI出海成功"的励志故事。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">但谁能想到，剧情反转得这么快——</p>

<p style="font-size:16px;color:#1E90FF;line-height:1.8;margin-bottom:20px;"><strong>交易三个月后，相关高管被限制出境。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">这到底是怎么回事？</p>

<p style="font-size:18px;color:#1E90FF;font-weight:bold;margin-top:30px;margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid #eee;">01｜Manus是谁？凭什么值138亿？</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">先科普一下Manus。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">它是2025年3月发布的"全球首款通用型AI智能体"，由中国的创业公司Monica研发。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">说人话就是：比ChatGPT更牛，它不只是聊天，是真的能帮你干活。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;"><strong>它的厉害之处：</strong></p>

<p style="font-size:14px;color:#666666;line-height:2;margin-bottom:10px;">● 能自主拆解复杂任务</p>
<p style="font-size:14px;color:#666666;line-height:2;margin-bottom:10px;">● 能调用各种工具帮你执行</p>
<p style="font-size:14px;color:#666666;line-height:2;margin-bottom:10px;">● 8个月内ARR（年度经常性收入）突破1亿美元</p>
<p style="font-size:14px;color:#666666;line-height:2;margin-bottom:20px;">● 处理了147万亿token数据</p>

<p style="font-size:15px;color:#333333;line-height:1.8;margin-bottom:15px;"><strong>这是什么概念？</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">很多AI公司烧了几十亿美元都没做到的成绩，Manus用8个月就实现了。</p>

<p style="font-size:15px;color:#1E90FF;line-height:1.8;margin-bottom:20px;"><strong>难怪Meta愿意花138亿买它。</strong></p>

<p style="font-size:18px;color:#1E90FF;font-weight:bold;margin-top:30px;margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid #eee;">02｜收购背后的隐患</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">按理说，中国AI公司被国际巨头收购，应该是件值得庆祝的事。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">但这次不一样。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;"><strong>因为这笔交易触碰了中国的监管红线。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">2025年3月，Meta正式完成收购。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">但到了2025年底/2026年初，传出消息：</p>

<p style="font-size:16px;color:#1E90FF;line-height:1.8;background:#f7f7f7;padding:15px 15px 15px 20px;border-left:4px solid #ff6600;margin:15px 0;"><strong>参与这笔交易的中国籍高管，被限制出境。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">据知情人士透露，相关部门认为这笔交易涉及敏感技术外流，需要审查。</p>

<p style="font-size:18px;color:#1E90FF;font-weight:bold;margin-top:30px;margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid #eee;">03｜这意味着什么？</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">这件事的影响，远比我们想象的大。</p>

<p style="font-size:16px;color:#333333;margin-bottom:10px;"><strong>对AI行业：</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">以后中国AI公司出海，技术出口会面临更严格的审查。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">你想把技术卖给外国公司？先问问监管部门答不答应。</p>

<p style="font-size:16px;color:#333333;margin-bottom:10px;"><strong>对创业者：</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">Manus的创始团队本来是想"借船出海"，借助国际资本走向全球。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">但现在看来，这条路走不通了。</p>

<p style="font-size:15px;color:#1E90FF;line-height:1.8;margin-bottom:20px;"><strong>中国AI，注定要自己走出去。</strong></p>

<p style="font-size:16px;color:#333333;margin-bottom:10px;"><strong>对普通人：</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">你可能会想，这跟我有什么关系？</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">关系大了。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;"><strong>你以后用的AI产品，可能都会被"国产"这两个字重新定义。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">政府正在用实际行动告诉全世界：<strong>核心技术，不能随便卖。</strong></p>

<p style="font-size:18px;color:#1E90FF;font-weight:bold;margin-top:30px;margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid #eee;">04｜我的判断</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">Manus事件不会是孤例。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">以后会有更多类似的故事上演——</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">有技术的公司想卖，但政府不让卖。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;"><strong>这不是"卡脖子"，这是在"筑篱笆"。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">对中国AI行业来说，这既是挑战，也是机会。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">挑战是：短期内融资、退出会更难。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">机会是：国产AI必须自己长大，不能再依赖"出卖技术"这条路。</p>

<p style="font-size:18px;color:#1E90FF;text-align:center;margin:30px 0;font-weight:bold;">中国AI，注定要靠自己站起来。</p>

<hr style="border:none;border-top:1px solid #eeeeee;margin:30px 0;">

<p style="font-size:14px;color:#999999;text-align:center;margin-bottom:10px;">你怎么看待Manus事件？你觉得政府限制技术外流是对的，还是会阻碍创新？评论区聊聊。</p>
<p style="font-size:14px;color:#999999;text-align:center;">如果觉得有用，点个「在看」，让更多人了解这个重磅事件。</p>'''
            
            articles = [{
                'title': title,
                'author': '小帅',
                'digest': digest,
                'content': content,
                'thumb_media_id': thumb_media_id,
                'need_open_comment': 1,
                'only_fans_can_comment': 0
            }]
            
            url3 = 'https://api.weixin.qq.com/cgi-bin/draft/add?access_token=' + access_token
            data3 = json.dumps({'articles': articles}, ensure_ascii=False).encode('utf-8')
            req3 = urllib.request.Request(url3, data=data3, headers={'Content-Type': 'application/json; charset=utf-8'})
            
            with urllib.request.urlopen(req3, timeout=30) as resp3:
                r3 = json.loads(resp3.read().decode('utf-8'))
                print('[RESULT]', r3)
                
                if 'media_id' in r3:
                    print('[OK] SUCCESS!')
                    print('Draft Media ID:', r3['media_id'])
                else:
                    print('[ERROR]', r3)

os.remove(tmp_path)