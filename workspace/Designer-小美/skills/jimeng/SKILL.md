---
name: jimeng
description: >
  即梦AI文生图3.1 - 火山引擎即梦AI图片生成服务。使用火山引擎Visual SDK调用即梦3.1模型进行图片生成。
  适用于日常图片生成任务（公众号配图、社交媒体图片等）。
  长图、易拉宝等物料类图片建议使用seede。
allowed-tools:
  - Read
  - Write
  - Edit
  - exec
---

# 即梦AI文生图3.0

即梦AI是火山引擎提供的AI图片生成服务，适用于日常图片生成任务。

## 使用场景

- 公众号配图
- 社交媒体图片
- 文章封面图
- 日常运营图片

## 不适用场景

- 长图拼接 → 使用 seede
- 易拉宝/展板 → 使用 seede
- 复杂物料设计 → 使用 seede

## erequisites

1. Python 3.7+
2. volcengine SDK: `pip install volcengine`
3. 火山引擎 Access Key 和 Secret Key

## 配置

使用环境变量配置AK/SK：
- AccessKey: 通过 `JIMENG_AK` 环境变量设置
- SecretKey: 通过 `JIMENG_SK` 环境变量设置（或使用base64编码后的SK通过 `JIMENG_SK_BASE64` 设置）

**注意：AK/SK已从代码中移除，请勿将密钥直接写入代码！**

## 使用方法

### 命令行调用

```bash
python scripts/jimeng.py "A cute cat sitting on grass" --size 1024x1024 --num 1
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| prompt | 图片描述 | 必填 |
| size | 图片尺寸 | 1024x1024 |
| num | 生成数量 | 1 |
| style | 风格 | realistic |

### 可用尺寸

- 1024x1024 (方形)
- 1024x576 (16:9)
- 576x1024 (9:16)
- 1024x768 (4:3)
- 768x1024 (3:4)

## Python API

```python
from jimeng import JimengImage

client = JimengImage(
    ak='your_access_key',
    sk='your_secret_key'
)

# 生成图片
result = client.generate(
    prompt='A cute cat',
    size='1024x1024',
    num=1
)

print(result['image_url'])
```

## 输出

图片生成成功后，返回：
- `image_url`: 图片下载链接
- `task_id`: 任务ID
- `request_id`: 请求ID

## 注意事项

1. 即梦API有调用配额限制，请合理使用
2. 生成图片需要等待几秒钟
3. 如果遇到Access Denied错误，检查AK/SK是否正确，或联系客服确认服务开通状态
