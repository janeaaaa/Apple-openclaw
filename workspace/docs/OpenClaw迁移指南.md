# OpenClaw 完整迁移指南

> 本文档用于将备份的 OpenClaw 项目恢复到新设备/新环境
> 备份仓库：https://github.com/janeaaaa/Apple-openclaw

---

## 📋 迁移前检查清单

### 新环境需要具备
- [ ] Node.js v18+（检查：node -v）
- [ ] npm（检查：npm -v）
- [ ] Git（检查：git --version）
- [ ] OpenClaw 安装（npm install -g openclaw）

---

## 🔧 迁移步骤

### 第一步：克隆备份仓库

```bash
# 克隆到本地
git clone https://github.com/janeaaaa/Apple-openclaw.git ~/.openclaw-backup
```

### 第二步：复制核心配置

```bash
# 进入备份目录
cd ~/.openclaw-backup

# 复制核心配置文件
copy openclaw.json %USERPROFILE%\.openclaw\openclaw.json
copy gateway.cmd %USERPROFILE%\.openclaw\gateway.cmd
```

### 第三步：复制 agents 配置

```bash
# 复制 agents 目录
xcopy /E /I agents %USERPROFILE%\.openclaw\agents
```

### 第四步：复制工作空间

```bash
# 复制 workspace 目录
xcopy /E /I workspace %USERPROFILE%\.openclaw\workspace
```

### 第五步：复制定时任务和日志

```bash
# 复制 cron 配置
copy cron\jobs.json %USERPROFILE%\.openclaw\cron\jobs.json

# 复制 cron runs（如需要）
xcopy /E /I cron\runs %USERPROFILE%\.openclaw\cron\runs

# 复制其他配置文件
copy completions\* %USERPROFILE%\.openclaw\completions\
copy devices\paired.json %USERPROFILE%\.openclaw\devices\paired.json
copy feishu\dedup\default.json %USERPROFILE%\.openclaw\feishu\dedup\default.json
```

### 第六步：初始化 credentials（必须）

```bash
# 创建 credentials 目录
mkdir %USERPROFILE%\.openclaw\credentials

# 手动添加以下密钥（联系静静获取）：
# - MiniMax API Key
# - 飞书 Bot Token
# - 微信公众号 AppID/Secret
```

### 第七步：初始化 identity（如需要）

```bash
# 创建 identity 目录（设备配对信息）
mkdir %USERPROFILE%\.openclaw\identity

# 如果需要在新设备配对，运行：
openclaw device pair
```

---

## ✅ 恢复后验证

### 1. 检查配置文件

```bash
openclaw status
```

### 2. 启动 Gateway

```bash
openclaw gateway start
```

### 3. 检查 skills

```bash
openclaw skills list
```

### 4. 验证飞书连接

```bash
openclaw feishu test
```

---

## ⚠️ 注意事项

### 需要重新配置的项

| 目录/文件 | 说明 | 处理方式 |
|-----------|------|----------|
| `credentials/` | API密钥 | 手动添加 |
| `identity/` | 设备认证 | 重新配对 |
| `auth-profiles.json` | 认证配置 | 可能需要重新配置 |
| `agents/*/sessions/*.jsonl` | 对话历史 | 可选保留 |

### 敏感信息不包含在备份中

以下信息出于安全考虑未包含在备份中，需要在新环境手动添加：
- MiniMax API Key
- 飞书 Webhook Token
- 微信公众号 AppID 和 Secret
- 其他第三方 API 密钥

### 模型配置

如果新环境的API配置不同，需要修改 `openclaw.json` 中的：
```json
{
  "auth": {
    "profiles": {
      "minimax-portal": {
        "apiKey": "你的新密钥"
      }
    }
  }
}
```

---

## 🔄 增量备份（后续更新）

在新设备恢复后，可以设置定期自动备份：

```bash
# 进入 .openclaw 目录
cd %USERPROFILE%\.openclaw

# 添加 remote（如果需要）
git remote add origin https://github.com/janeaaaa/Apple-openclaw.git

# 每次手动备份
git add .
git commit -m "增量备份 - $(date)"
git push origin master
```

---

## 📞 遇到问题？

如果迁移过程中遇到问题，可以：
1. 查看 OpenClaw 文档：https://docs.openclaw.ai
2. 检查日志：%USERPROFILE%\.openclaw\logs\
3. 重新运行配置：openclaw configure

---

**最后更新：2026-03-30**