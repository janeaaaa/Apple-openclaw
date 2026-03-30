#!/usr/bin/env python3
"""
即梦AI文生图3.1 Python CLI
火山引擎 Visual SDK
"""

import argparse
import json
import sys
import os
import time
import base64
import os

def get_credentials():
    """获取AK/SK"""
    ak = os.environ.get('JIMENG_AK')
    sk = os.environ.get('JIMENG_SK') or os.environ.get('JIMENG_SK_BASE64')
    if not ak or not sk:
        raise ValueError("请设置环境变量 JIMENG_AK 和 JIMENG_SK（或 JIMENG_SK_BASE64）")
    return ak, sk

def generate_image(prompt, size='1024x1024', num=1, style='realistic', output=None):
    """生成图片"""
    from volcengine.visual.VisualService import VisualService
    
    service = VisualService()
    ak, sk = get_credentials()
    service.set_ak(ak)
    service.set_sk(sk)
    
    # 解析尺寸
    width, height = map(int, size.split('x'))
    
    # 提交任务
    resp = service.cv_sync2async_submit_task({
        'req_key': 'jimeng_t2i_v31',
        'prompt': prompt,
        'seed': -1,
        'width': width,
        'height': height
    })
    
    task_id = resp['data']['task_id']
    print(f'Task ID: {task_id}', file=sys.stderr)
    
    # 等待生成
    print('Waiting for image generation...', file=sys.stderr)
    time.sleep(8)
    
    # 查询结果
    result = service.cv_sync2async_get_result({
        'req_key': 'jimeng_t2i_v31',
        'task_id': task_id,
        'req_json': '{"return_url":true}'
    })
    
    if result['data']['binary_data_base64']:
        img_data = result['data']['binary_data_base64'][0]
        img_bytes = base64.b64decode(img_data)
    elif result['data']['image_urls']:
        # 如果返回的是URL，需要下载
        import urllib.request
        url = result['data']['image_urls'][0]
        print(f'Downloading from {url}', file=sys.stderr)
        img_bytes = urllib.request.urlopen(url).read()
    else:
        return {'success': False, 'error': 'No image data'}
    
    # 保存文件
    if output is None:
        output = 'jimeng_output.jpg'
    
    with open(output, 'wb') as f:
        f.write(img_bytes)
    
    return {
        'success': True,
        'output': output,
        'task_id': task_id
    }

def main():
    parser = argparse.ArgumentParser(description='即梦AI文生图3.1')
    parser.add_argument('prompt', help='图片描述')
    parser.add_argument('--size', default='1024x1024', help='图片尺寸')
    parser.add_argument('--num', type=int, default=1, help='生成数量')
    parser.add_argument('--style', default='realistic', help='风格')
    parser.add_argument('--output', '-o', help='输出文件路径')
    
    args = parser.parse_args()
    
    result = generate_image(
        args.prompt, 
        args.size, 
        args.num, 
        args.style,
        args.output
    )
    
    if result['success']:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
