# 团队技能补充计划

> 创建时间：2026-03-24
> 目标：为团队智能体补充GitHub高价值项目技能

---

## 📋 任务清单

### 🔴 进行中
- [ ] 批量安装GitHub高价值项目

### 📦 已安装汇总

#### AI相关
| 项目 | 状态 | 需静静确认 |
|------|------|------------|
| firecrawl | ✅ CLI已装 | API key |
| privateGPT | ✅ 已克隆 | 本地LLM配置 |
| anything-llm | ✅ 已克隆 | 本地LLM配置 |
| mindsearch | ✅ 已克隆 | 配置 |
| llama | ✅ 已克隆 | 配置 |

#### 工具相关
| 项目 | 状态 | 需静静确认 |
|------|------|------------|
| you-get | ✅ pip已装 | 无 |
| meilisearch | ✅ pip已装 | 自建服务 |
| fastapi | ✅ pip已装 | 无 |
| streamlit | ✅ pip已装 | 无 |
| yt-dlp | ✅ 已克隆 | 无 |
| selenium | ✅ pip已装 | 无 |

#### AI框架
| 项目 | 状态 | 需静静确认 |
|------|------|------------|
| langchain | ✅ pip已装 | 无 |
| huggingface_hub | ✅ pip已装 | 无 |
| anthropic | ✅ pip已装 | API key |
| cohere | ✅ pip已装 | API key |
| ollama | ✅ pip已装 | 需安装客户端 |

#### 文档处理
| 项目 | 状态 | 需静静确认 |
|------|------|------------|
| pypdf | ✅ pip已装 | 无 |
| pymupdf | ✅ pip已装 | 无 |
| python-docx | ✅ pip已装 | 无 |
| python-pptx | ✅ pip已装 | 无 |

#### 社交平台SDK
| 项目 | 状态 | 需静静确认 |
|------|------|------------|
| tweepy (Twitter) | ✅ pip已装 | API key |
| discord.py | ✅ pip已装 | Token |
| wechatpy | ✅ pip已装 | 企业微信配置 |

#### 爬虫/请求
| 项目 | 状态 | 需静静确认 |
|------|------|------------|
| selenium | ✅ pip已装 | 无 |
| playwright | ✅ pip已装 | 无 |
| aiohttp | ✅ pip已装 | 无 |
| beautifulsoup4 | ✅ pip已装 | 无 |

#### 效率工具
| 项目 | 状态 | 需静静确认 |
|------|------|------------|
| schedule | ✅ pip已装 | 无 |
| flask-cors | ✅ pip已装 | 无 |
| qrcode | ✅ pip已装 | 无 |

---

## 🔒 详细安全检查记录

### GitHub项目安全检查

| 项目 | 安全检查 | 风险 | 措施 |
|------|---------|------|------|
| privateGPT | ✅ 检查代码结构 | 🟢低 | 本地运行，数据不外泄 |
| developer-roadmap | ✅ 纯文档 | 🟢极低 | 无风险 |
| anything-llm | ✅ 检查配置 | 🟢低 | 本地LLM |
| mindsearch | ✅ 需配置 | 🟡中 | 需安全配置 |
| llama | ✅ Facebook开源 | 🟢低 | 需本地运行 |
| yt-dlp | ⚠️ 下载工具 | 🟡中 | 版权合规使用 |
| public-apis | ✅ 纯文档 | 🟢极低 | 无风险 |

### Python包安全检查

| 包 | 检查结果 | 风险 | 备注 |
|----|---------|------|------|
| langchain | ✅ 官方包 | 🟢低 | 安全 |
| anthropic | ✅ 官方SDK | 🟢低 | API key保护 |
| selenium | ⚠️ 浏览器控制 | 🟡中 | 沙箱运行 |
| playwright | ⚠️ 浏览器控制 | 🟡中 | 沙箱运行 |
| tweepy | ⚠️ 第三方 | 🟡中 | API key保护 |
| discord.py | ✅ 官方包装 | 🟢低 | Token保护 |
| wechatpy | ✅ 官方SDK | 🟢低 | 企业微信配置 |
| cryptography | ✅ 加密库 | 🟢低 | 安全 |
| pyOpenSSL | ✅ SSL库 | 🟢低 | 安全 |
| sentry-sdk | ⚠️ 监控SDK | 🟡中 | 数据上传 |
| loguru | ✅ 日志库 | 🟢低 | 安全 |
| feedparser | ✅ RSS解析 | 🟢低 | 安全 |
| dateparser | ✅ 日期解析 | 🟢低 | 安全 |

### 注意事项
1. 所有API key/Token存储需加密（使用python-dotenv）
2. 浏览器自动化工具需在沙箱环境运行
3. 下载工具注意版权合规
4. 本地LLM优先于云端API
5. sentry-sdk会收集运行数据，考虑是否启用

#### 纯文档（直接可用）
| 项目 | 状态 |
|------|------|
| developer-roadmap | ✅ |
| public-apis | ✅ |

#### 失败
| 项目 | 状态 | 说明 |
|------|------|------|
| whisper | ❌ 失败 | 依赖下载超时 |

### ⏳ 待执行

#### 第一轮：小帅技能补充（公众号方向）
| 序号 | 任务 | 项目 | 状态 |
|------|------|------|------|
| 1 | 安装/配置 firecrawl | firecrawl | ✅ CLI已安装 |
| 2 | 整合热点抓取工作流 | firecrawl | ⏳ 需API key |
| 3 | 测试热点抓取效果 | firecrawl | ⏳ |

#### 第二轮：小美技能补充（设计方向）
| 序号 | 任务 | 项目 | 状态 |
|------|------|------|------|
| 4 | 安装/配置 whisper | whisper | ❌ 依赖下载超时 |
| 5 | 整合语音转文字工作流 | whisper | ⏳ |
| 6 | 测试语音识别效果 | whisper | ⏳ |

#### 第三轮：Zero技能补充（客服方向）
| 序号 | 任务 | 项目 | 状态 |
|------|------|------|------|
| 7 | 安装/配置 private-gpt | private-gpt | ✅ 已克隆到本地 |
| 8 | 整合客服知识库 | private-gpt | ⏳ 需配置本地LLM |
| 9 | 测试问答效果 | private-gpt | ⏳ |

#### 第四轮：小苹果技能补充（管理方向）
| 序号 | 任务 | 项目 | 状态 |
|------|------|------|------|
| 10 | 安装/配置 developer-roadmap | developer-roadmap | ✅ 已克隆 |
| 11 | 安装AI相关 - mindsearch | mindsearch | ✅ 已克隆 |
| 12 | 安装AI相关 - anything-llm | anything-llm | ✅ 已克隆 |
| 13 | 安装工具 - you-get | you-get | ✅ pip已安装 |
| 14 | 安装工具 - meilisearch | meilisearch | ✅ pip已安装 |
| 15 | 安装工具 - fastapi | fastapi | ✅ pip已安装 |
| 16 | 安装API - public-apis | public-apis | ✅ 已克隆 |

---

## ⚠️ 注意事项

1. **每个项目完成后必须汇报**：不能偷偷做完就不说了
2. **遇到问题立即暂停**：不要自己扛着，及时问静静
3. **测试通过才算完成**：不能只是安装好就结束
4. **记录到memory**：每次完成都更新今日记录

---

## 🎯 验收标准

| 项目 | 验收条件 |
|------|----------|
| firecrawl | 能够抓取指定网页并提取内容 |
| whisper | 能够识别音频并输出文字 |
| private-gpt | 能够基于文档回答问题 |
| developer-roadmap | 能够生成学习路径 |