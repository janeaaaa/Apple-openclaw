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

print('[INFO] Creating blue background cover with white text...')

# 创建蓝色背景+白字封面
width, height = 900, 500
img = Image.new('RGB', (width, height), color=(30, 60, 120))
draw = ImageDraw.Draw(img)

# 添加一些光晕效果
random.seed(123)
for _ in range(10):
    x = random.randint(0, width)
    y = random.randint(0, height)
    r = random.randint(50, 150)
    # 绘制半透明光晕
    for i in range(r, 0, -5):
        alpha = int(255 * (1 - i/r) * 0.3)
        color = (60, 100, 180)
        draw.ellipse([x-i, y-i, x+i, y+i], fill=color)

# 添加标题文字 - AI的6个月
from PIL import ImageFont
try:
    font_large = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 50)
    font_small = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 30)
except:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

# 绘制标题
draw.text((50, 180), "AI的6个月", fill=(255, 255, 255), font=font_large)
draw.text((50, 250), "=", fill=(200, 200, 200), font=font_small)
draw.text((50, 300), "现实3年", fill=(255, 255, 255), font=font_large)
draw.text((50, 370), "这是普通人最后的机会窗口", fill=(180, 180, 180), font=font_small)

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
            
            # 创建新草稿
            print('[INFO] Creating new draft with proper formatting...')
            
            # 标题
            title = 'AI的6个月 = 现实3年：这是普通人最后的机会窗口'
            
            # 摘要
            digest = 'AI的6个月，等于现实世界的3年。换句话说，AI进化一年，相当于人类社会发展五年。'
            
            # 使用标准排版格式 (类似之前成功的"阿里又放大招"风格)
            content = '''<p style="font-size:16px;color:#333333;line-height:1.8;"><strong>当AI一年跑完人类五年的路，你准备好了吗？</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-top:15px;">最近，AI圈流传着一个细思极恐的说法：</p>

<p style="font-size:16px;color:#333333;line-height:1.8;background:#f5f5f5;padding:15px;border-left:4px solid #1E90FF;margin:20px 0;"><strong>AI的6个月，等于现实世界的3年。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;">换句话说，AI进化一年，相当于人类社会发展五年。这个说法来自一位资深AI从业者的观察，瞬间在科技圈炸开了锅。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-top:15px;"><strong>但我想说：不管你信不信，这个窗口，可能真没剩多久了。</strong></p>

<h2 style="color:#1E90FF;font-size:18px;margin-top:30px;margin-bottom:15px;">01｜AI正在用「压缩式进化」甩开人类</h2>

<p style="font-size:15px;color:#666666;line-height:1.8;">让我们先把镜头拉远，看看AI这一年到底发生了什么：</p>

<ul style="font-size:14px;color:#666666;line-height:2;padding-left:20px;margin:15px 0;">
<li style="margin-bottom:8px;"><strong>2024年初</strong>：Claude 3 opus惊艳全网，大家还在讨论"AI能不能写代码"</li>
<li style="margin-bottom:8px;"><strong>2024年中</strong>：GPT-4o发布，AI开始"听懂"语音、看懂画面</li>
<li style="margin-bottom:8px;"><strong>2024年底</strong>：o1模型发布，AI开始具备推理能力</li>
<li style="margin-bottom:8px;"><strong>2025年</strong>：Claude 4来了，有人说"已经完胜人类程序员"</li>
<li style="margin-bottom:8px;"><strong>2026年（现在）</strong>：最新的Claude版本被意外泄露，代号「卡皮巴拉」，业界震惊</li>
</ul>

<p style="font-size:15px;color:#333333;line-height:1.8;margin-top:15px;"><strong>你发现了吗？</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;">每一次发布都间隔不到半年，但每一次的能力跃升都像是跨越了一个时代。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-top:15px;">这就是AI的可怕之处——<strong>它不是线性增长，而是指数级进化。</strong></p>

<h2 style="color:#1E90FF;font-size:18px;margin-top:30px;margin-bottom:15px;">02｜为什么说「6个月=3年」？</h2>

<p style="font-size:15px;color:#666666;line-height:1.8;"><strong>从模型能力看：</strong></p>
<ul style="font-size:14px;color:#666666;line-height:2;padding-left:20px;margin:15px 0;">
<li style="margin-bottom:8px;">2024年：AI能帮你写邮件、总结文章</li>
<li style="margin-bottom:8px;">2025年：AI能帮你写代码、做PPT、分析数据</li>
<li style="margin-bottom:8px;">2026年：AI已经能"思考"了，它不再是工具，而是搭档</li>
</ul>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-top:15px;"><strong>从行业变化看：</strong></p>
<ul style="font-size:14px;color:#666666;line-height:2;padding-left:20px;margin:15px 0;">
<li style="margin-bottom:8px;">以前一个新技术落地要3-5年</li>
<li style="margin-bottom:8px;">现在AI领域6个月就是一次大更新</li>
<li style="margin-bottom:8px;">你刚学会一个AI工具，它的下一代可能已经出来了</li>
</ul>

<p style="font-size:15px;color:#333333;line-height:1.8;margin-top:15px;"><strong>这意味着什么？</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;"><strong>人类引以为傲的"经验积累"，正在被AI用几个月就"学会"。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-top:15px;">一个资深程序员十年的代码经验，AI几个月就能掌握。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;">一个设计师十年的审美积累，AI几个月就能超越。</p>

<h2 style="color:#1E90FF;font-size:18px;margin-top:30px;margin-bottom:15px;">03｜留给普通人的时间不多了</h2>

<p style="font-size:15px;color:#666666;line-height:1.8;">听到这里，你可能觉得慌——</p>

<p style="font-size:15px;color:#666666;line-height:1.8;background:#f5f5f5;padding:15px;margin:15px 0;">"那普通人还玩什么？直接等死算了？"</p>

<p style="font-size:15px;color:#333333;line-height:1.8;"><strong>别急，听我说完。</strong></p>

<p style="font-size:15px;color:#333333;line-height:1.8;"><strong>正因为AI进化太快，反而给普通人留了一个"结构性优势窗口"。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-top:15px;">什么意思？</p>

<p style="font-size:15px;color:#666666;line-height:1.8;">现在的AI再强，它也是一个"通才"——什么都会，但什么都不精。</p>

<ul style="font-size:14px;color:#666666;line-height:2;padding-left:20px;margin:15px 0;">
<li style="margin-bottom:8px;">它知道怎么写代码，但<strong>不知道你们公司的业务逻辑</strong></li>
<li style="margin-bottom:8px;">它知道怎么画画，但<strong>不知道你老板的审美偏好</strong></li>
<li style="margin-bottom:8px;">它知道怎么分析数据，但<strong>不知道你那个行业的独特规律</strong></li>
</ul>

<p style="font-size:15px;color:#1E90FF;line-height:1.8;margin-top:15px;"><strong>而这些"隐性知识"，只有扎根在各行各业的普通人知道。</strong></p>

<h2 style="color:#1E90FF;font-size:18px;margin-top:30px;margin-bottom:15px;">04｜普通人怎么抓住这波机会？</h2>

<p style="font-size:16px;color:#333333;margin-top:10px;"><strong>方向一：成为「AI+行业」的桥梁</strong></p>
<p style="font-size:15px;color:#666666;line-height:1.8;margin-top:10px;">不要试图去和AI比技术，去和AI比配合。</p>
<p style="font-size:15px;color:#666666;line-height:1.8;margin-top:10px;"><strong>学会用AI放大你的专业能力：</strong></p>
<ul style="font-size:14px;color:#666666;line-height:2;padding-left:20px;margin:15px 0;">
<li style="margin-bottom:8px;">设计师 → 用AI生成初稿，你负责精修和创意</li>
<li style="margin-bottom:8px;">程序员 → 用AI写基础代码，你负责架构和优化</li>
<li style="margin-bottom:8px;">运营 → 用AI做数据分析，你负责策略和执行</li>
</ul>

<p style="font-size:15px;color:#1E90FF;line-height:1.8;margin-top:15px;"><strong>AI不会取代你，但会用AI的人会取代你。</strong></p>

<p style="font-size:16px;color:#333333;margin-top:25px;"><strong>方向二：抢占「AI认知差」</strong></p>
<p style="font-size:15px;color:#666666;line-height:1.8;margin-top:10px;">很多人还没意识到AI已经多强了。</p>
<p style="font-size:15px;color:#666666;line-height:1.8;margin-top:10px;">你不需要成为技术大牛，你只需要比身边的人先会用AI。</p>

<p style="font-size:15px;color:#1E90FF;line-height:1.8;margin-top:15px;"><strong>这就是信息差，也是普通人最容易抓住的红利。</strong></p>

<h2 style="color:#1E90FF;font-size:18px;margin-top:30px;margin-bottom:15px;">05｜写在最后</h2>

<p style="font-size:15px;color:#666666;line-height:1.8;">AI的进化速度确实让人焦虑。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-top:15px;">但我想说句公道话：</p>

<p style="font-size:16px;color:#333333;margin-top:15px;"><strong>焦虑本身没用，行动才有。</strong></p>

<p style="font-size:15px;color:#666666;line-height:1.8;margin-top:15px;">6个月说长不长，说短不短。</p>

<p style="font-size:15px;color:#666666;line-height:1.8;">它可能是你被AI甩开的距离，也可以是你甩开别人的机会。</p>

<p style="font-size:16px;color:#1E90FF;text-align:center;margin:30px 0;"><strong>关键是，你得开始。</strong></p>

<hr style="border:none;border-top:1px solid #eeeeee;margin:30px 0;">

<p style="font-size:14px;color:#999999;text-align:center;">你觉得AI会影响你的工作吗？欢迎在评论区聊聊。</p>
<p style="font-size:14px;color:#999999;text-align:center;margin-top:10px;">如果觉得有用，点个「在看」让更多人看到。</p>'''
            
            # 创建草稿
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
                print('[DRAFT RESULT]', r3)
                
                if 'media_id' in r3:
                    print('[OK] SUCCESS!')
                    print('Draft Media ID:', r3['media_id'])
                else:
                    print('[ERROR]', r3)

os.remove(tmp_path)