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

print('[INFO] Creating cover for GPT-5.4 article...')

# 创建封面 - 蓝色背景+白字风格
width, height = 900, 500
img = Image.new('RGB', (width, height), color=(20, 50, 100))
draw = ImageDraw.Draw(img)

# 添加装饰
random.seed(8888)
for _ in range(25):
    x = random.randint(0, width)
    y = random.randint(0, height)
    r = random.randint(30, 100)
    for i in range(r, 0, -15):
        color = (50, 80, 160)
        draw.ellipse([x-i, y-i, x+i, y+i], fill=color)

# 加载字体
font_paths = [r'C:\Windows\Fonts\msyh.ttc', r'C:\Windows\Fonts\simhei.ttf']
font_large = None
font_small = None
for fp in font_paths:
    try:
        font_large = ImageFont.truetype(fp, 40)
        font_small = ImageFont.truetype(fp, 24)
        break
    except:
        continue
if font_large is None:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

# 绘制标题 - 用英文代替中文避免乱码
draw.text((60, 150), "GPT-5.4", fill=(255, 255, 255), font=font_large)
draw.text((320, 150), "is", fill=(150, 150, 180), font=font_small)
draw.text((360, 150), "HERE!", fill=(255, 200, 50), font=font_large)

# 副标题
draw.text((60, 320), "1M", fill=(255, 255, 255), font=font_large)
draw.text((180, 320), "Token", fill=(180, 180, 180), font=font_small)
draw.text((300, 320), "Context", fill=(180, 180, 180), font=font_small)
draw.text((480, 320), "+", fill=(255, 200, 50), font=font_large)
draw.text((530, 320), "Excel AI", fill=(180, 180, 180), font=font_small)

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
            
            title = '炸裂！ChatGPT突然宣布重磅更新，打工人都沸腾了'
            digest = '100万token上下文！这意味着什么？'
            
            content = '''<p style="font-size:16px;color:#333333;line-height:1.8;margin-bottom:20px;"><strong>100万token上下文！这意味着什么？</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">刚刚，OpenAI扔出一颗深水炸弹。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;"><strong>3月5日，ChatGPT发布GPT-5.4。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">有人可能觉得：又发布新模型？有什么稀奇的。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">但这次不一样。</p>

<p style="font-size:16px;color:#1E90FF;line-height:1.8;margin-bottom:20px;"><strong>因为它的能力提升，足以让每个打工人都沸腾。</strong></p>

<p style="font-size:18px;color:#1E90FF;font-weight:bold;margin-top:30px;margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid #eee;">01｜GPT-5.4到底有多强？</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">一句话概括：</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;"><strong>它能同时处理100万token的内容。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">100万token是什么概念？</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">普通AI一次能处理几万个字，GPT-5.4能处理<strong>100万字</strong>。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">相当于同时阅读5本《哈利波特》，还能记住每一页的细节。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;"><strong>而且它的速度比上一代快了25%。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">价格却更便宜。</p>

<p style="font-size:18px;color:#1E90FF;font-weight:bold;margin-top:30px;margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid #eee;">02｜打工人的福利来了</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">最让人激动的是这个功能：</p>

<p style="font-size:16px;color:#333333;line-height:1.8;margin-bottom:15px;"><strong>ChatGPT for Excel 正式发布。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">简单说，就是把AI直接塞进Excel里。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">你只需要用自然语言描述你的需求：</p>

<p style="font-size:15px;color:#666666;line-height:1.8;background:#f7f7f7;padding:15px 15px 15px 20px;border-left:4px solid #1E90FF;margin:15px 0;">"帮我做一个季度销售分析报告"</p>
<p style="font-size:15px;color:#666666;line-height:1.8;background:#f7f7f7;padding:15px 15px 15px 20px;border-left:4px solid #1E90FF;margin:15px 0;">"计算不同区域的增长率"</p>
<p style="font-size:15px;color:#666666;line-height:1.8;background:#f7f7f7;padding:15px 15px 15px 20px;border-left:4px solid #1E90FF;margin:15px 0;">"找出这个表格里的异常数据"</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;"><strong>AI直接帮你写公式、画图表、做分析。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">不用学Excel，不用记函数，一个命令搞定。</p>

<p style="font-size:18px;color:#1E90FF;font-weight:bold;margin-top:30px;margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid #eee;">03｜这对普通人意味着什么？</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">很多人可能会想：AI又变强了，跟我有什么关系？</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;"><strong>关系大了。</strong></p>

<p style="font-size:16px;color:#333333;margin-bottom:10px;"><strong>① 重复性工作将被大幅替代</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">以前你要花几小时整理的数据，现在AI几分钟就搞定。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">不是帮你"写得更快"，而是<strong>帮你"做得更少"</strong>。</p>

<p style="font-size:16px;color:#333333;margin-bottom:10px;"><strong>② 门槛大幅降低</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">你不需要会Excel，不需要懂代码。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;"><strong>只要你会说话，AI就能帮你干活。</strong></p>

<p style="font-size:16px;color:#333333;margin-bottom:10px;"><strong>③ 职场竞争力重新洗牌</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">会用AI的人，和不会用AI的人，差距会越拉越大。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">不是AI取代你，是<strong>会用AI的人取代你</strong>。</p>

<p style="font-size:18px;color:#1E90FF;font-weight:bold;margin-top:30px;margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid #eee;">04｜我的判断</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">GPT-5.4的发布，意味着AI从"玩具"正式变成"工具"。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">以前我们说"AI要改变世界"，听起来很虚。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">现在它真的在<strong>改变你的工作方式</strong>。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">Excel、PPT、文档、数据分析……</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">这些你每天都要做的事，正在被AI重新定义。</p>

<p style="font-size:18px;color:#1E90FF;text-align:center;margin:30px 0;font-weight:bold;">AI时代，工具已经就位，你准备好了吗？</p>

<hr style="border:none;border-top:1px solid #eeeeee;margin:30px 0;">

<p style="font-size:14px;color:#999999;text-align:center;margin-bottom:10px;">你觉得AI会取代你的工作吗？你会用ChatGPT for Excel吗？评论区聊聊。</p>
<p style="font-size:14px;color:#999999;text-align:center;">如果觉得有用，点个「在看」，让更多人了解这个重磅更新。</p>'''
            
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