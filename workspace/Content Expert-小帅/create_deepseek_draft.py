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

print('[INFO] Creating cover for DeepSeek article...')

# 创建蓝色背景+白字封面
width, height = 900, 500
img = Image.new('RGB', (width, height), color=(30, 60, 130))
draw = ImageDraw.Draw(img)

# 添加装饰
random.seed(999)
for _ in range(20):
    x = random.randint(0, width)
    y = random.randint(0, height)
    r = random.randint(30, 80)
    for i in range(r, 0, -15):
        color = (60, 100, 190)
        draw.ellipse([x-i, y-i, x+i, y+i], fill=color)

# 加载字体
font_paths = [r'C:\Windows\Fonts\msyh.ttc', r'C:\Windows\Fonts\simhei.ttf']
font_large = None
for fp in font_paths:
    try:
        font_large = ImageFont.truetype(fp, 42)
        break
    except:
        continue
if font_large is None:
    font_large = ImageFont.load_default()

# 绘制标题
draw.text((80, 160), "DeepSeek", fill=(255, 255, 255), font=font_large)
draw.text((400, 160), "?", fill=(255, 200, 50), font=font_large)
draw.text((80, 320), "DeepSeek", fill=(180, 180, 180), font=font_large)
draw.text((380, 320), "?", fill=(150, 150, 150), font=font_large)

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
            
            title = '国产AI突然炸锅！DeepSeek凭啥让硅谷慌了？'
            digest = '一个名不见经传的公司，怎么突然成了全网焦点？一个成立不到一年的中国公司，怎么就突然让硅谷慌了？'
            
            content = '''<p style="font-size:16px;color:#333333;line-height:1.8;margin-bottom:20px;"><strong>一个名不见经传的公司，怎么突然成了全网焦点？</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">最近，科技圈被一个名字刷屏了：<strong>DeepSeek</strong>。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">你说它没听说过？正常。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">但在过去的48小时里，它的热度已经超过了ChatGPT巅峰时期。</p>

<p style="font-size:16px;color:#333333;line-height:1.8;margin-bottom:20px;"><strong>一个成立不到一年的中国公司，怎么就突然让硅谷慌了？</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">今天这篇，给你讲清楚。</p>

<p style="font-size:18px;color:#1E90FF;font-weight:bold;margin-top:30px;margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid #eee;">01｜DeepSeek到底有多火？</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">先看一组数据：</p>

<p style="font-size:14px;color:#666666;line-height:2;margin-bottom:10px;">● <strong>GitHub热榜第一</strong>：开源项目星标数瞬间破万</p>
<p style="font-size:14px;color:#666666;line-height:2;margin-bottom:10px;">● <strong>推特趋势</strong>：#DeepSeek 连续霸榜48小时</p>
<p style="font-size:14px;color:#666666;line-height:2;margin-bottom:10px;">● <strong>硅谷VC圈</strong>：都在问"DeepSeek是谁？"</p>
<p style="font-size:14px;color:#666666;line-height:2;margin-bottom:20px;">● <strong>国内热搜</strong>：#DeepSeek #国产AI #中国大模型</p>

<p style="font-size:15px;color:#333333;line-height:1.8;margin-bottom:15px;"><strong>这是什么概念？</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">上次让全科技圈这么疯狂的，还是ChatGPT发布那天。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;"><strong>但这次，是一个中国公司。</strong></p>

<p style="font-size:18px;color:#1E90FF;font-weight:bold;margin-top:30px;margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid #eee;">02｜DeepSeek凭啥这么牛？</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">说白了就三点：</p>

<p style="font-size:16px;color:#333333;margin-bottom:10px;"><strong>① 性能直接对标GPT-4</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">根据第三方测评，DeepSeek的性能已经接近GPT-4水平。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">关键是：<strong>它完全开源。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">这意味着任何开发者都可以免费使用、可以自己部署、可以随便改。</p>

<p style="font-size:16px;color:#333333;margin-top:20px;margin-bottom:10px;"><strong>② 训练成本只有别人的1/10</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">据官方透露，DeepSeek的训练成本只有同类产品的<strong>十分之一</strong>。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">这是什么概念？</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">别人训练一个大模型要花几亿美元，它只要几千万。</p>

<p style="font-size:15px;color:#1E90FF;line-height:1.8;margin-bottom:20px;"><strong>这性价比，直接把行业规则打碎了。</strong></p>

<p style="font-size:16px;color:#333333;margin-top:20px;margin-bottom:10px;"><strong>③ 中国团队，更懂中文</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">虽然GPT-4也能用中文，但DeepSeek在中文理解、对话风格、表达习惯上，明显更对味。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">很多用户实测后表示：<strong>和它聊天，比和ChatGPT聊天更舒服。</strong></p>

<p style="font-size:18px;color:#1E90FF;font-weight:bold;margin-top:30px;margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid #eee;">03｜硅谷为什么慌了？</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">原因很简单：</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;"><strong>他们没想到，中国公司能这么快。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">过去几年，硅谷一直认为中国在AI领域"落后美国2-3年"。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">但DeepSeek的出现，直接把这个时间差抹平了。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">更让它们不安的是：</p>

<p style="font-size:14px;color:#666666;line-height:2;margin-bottom:10px;">● DeepSeek是开源的，谁都能用</p>
<p style="font-size:14px;color:#666666;line-height:2;margin-bottom:10px;">● 成本这么低，其他公司怎么活？</p>
<p style="font-size:14px;color:#666666;line-height:2;margin-bottom:20px;">● 如果中国AI这么猛，以后谁主导行业标准？</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;"><strong>有硅谷投资人直接说：这可能是中国AI的"iPhone时刻"。</strong></p>

<p style="font-size:18px;color:#1E90FF;font-weight:bold;margin-top:30px;margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid #eee;">04｜普通人能做什么？</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">看到这里你可能想：</p>

<p style="font-size:15px;color:#666666;line-height:1.8;background:#f7f7f7;padding:15px 15px 15px 20px;border-left:4px solid #999999;margin:15px 0;">"跟我有什么关系？我又不写代码。"</p>

<p style="font-size:15px;color:#333333;line-height:1.8;margin-bottom:15px;"><strong>错了，关系大了。</strong></p>

<p style="font-size:16px;color:#333333;margin-bottom:10px;"><strong>机会一：AI从业者更值等了</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">如果你做AI相关工作，DeepSeek的开源意味着更多机会。中小企业也能用上顶级AI了，岗位需求只会更多。</p>

<p style="font-size:16px;color:#333333;margin-bottom:10px;"><strong>机会二：AI应用创业窗口</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">开源+低成本=创业门槛大幅降低。一个人+DeepSeek API，就能做出之前要一个团队才能做的产品。</p>

<p style="font-size:16px;color:#333333;margin-bottom:10px;"><strong>机会三：信息差红利</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">现在知道DeepSeek的人还不多。你先去了解、去尝试，就比身边的人领先一步。</p>

<p style="font-size:18px;color:#1E90FF;font-weight:bold;margin-top:30px;margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid #eee;">05｜我的判断</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;">DeepSeek确实牛，但它能不能改变行业，还有待观察。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:15px;"><strong>不过有一点可以确定：</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-bottom:20px;">中国AI，不再是"跟跑者"了。</p>

<p style="font-size:18px;color:#1E90FF;text-align:center;margin:30px 0;font-weight:bold;">从今天起，全世界都要重新审视中国AI的实力。</p>

<hr style="border:none;border-top:1px solid #eeeeee;margin:30px 0;">

<p style="font-size:14px;color:#999999;text-align:center;margin-bottom:10px;">你觉得DeepSeek能成为下一个ChatGPT吗？你看好国产AI吗？评论区聊聊。</p>
<p style="font-size:14px;color:#999999;text-align:center;">如果觉得有用，点个「在看」，让更多人看到中国AI的崛起。</p>'''
            
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