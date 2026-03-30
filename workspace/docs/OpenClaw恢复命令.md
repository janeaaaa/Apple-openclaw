# OpenClaw 新设备恢复命令清单

> 在新设备上执行以下命令完成迁移
> 仓库：https://github.com/janeaaaa/Apple-openclaw

---

## 🚀 第一步：安装环境

```powershell
# 1. 安装 Node.js（如未安装）
# 下载地址：https://nodejs.org/

# 2. 安装 OpenClaw
npm install -g openclaw

# 3. 验证安装
openclaw --version
```

---

## 📥 第二步：下载备份

```powershell
# 在 PowerShell 中执行

# 克隆仓库到临时目录
git clone https://github.com/janeaaaa/Apple-openclaw.git "$env:TEMP\openclaw-backup"

# 进入备份目录
cd "$env:TEMP\openclaw-backup"
```

---

## 📁 第三步：复制配置

```powershell
# 创建 .openclaw 目录
New-Item -ItemType Directory -Path "$env:USERPROFILE\.openclaw" -Force

# 复制核心配置
Copy-Item "openclaw.json" "$env:USERPROFILE\.openclaw\openclaw.json"
Copy-Item "gateway.cmd" "$env:USERPROFILE\.openclaw\gateway.cmd"
Copy-Item ".gitignore" "$env:USERPROFILE\.openclaw\.gitignore"
Copy-Item "update-check.json" "$env:USERPROFILE\.openclaw\update-check.json"
```

---

## 👥 第四步：复制 agents

```powershell
# 复制 agents 目录
Copy-Item "agents" "$env:USERPROFILE\.openclaw\agents" -Recurse -Force

# 复制 subagents
Copy-Item "subagents" "$env:USERPROFILE\.openclaw\subagents" -Recurse -Force
```

---

## 💼 第五步：复制工作空间

```powershell
# 复制 workspace（包含 skills、memory、docs 等）
Copy-Item "workspace" "$env:USERPROFILE\.openclaw\workspace" -Recurse -Force
```

---

## ⏰ 第六步：复制定时任务

```powershell
# 复制 cron 配置
New-Item -ItemType Directory -Path "$env:USERPROFILE\.openclaw\cron" -Force
Copy-Item "cron\jobs.json" "$env:USERPROFILE\.openclaw\cron\jobs.json"
Copy-Item "cron" "$env:USERPROFILE\.openclaw\cron" -Recurse -Force

# 复制 delivery-queue
Copy-Item "delivery-queue" "$env:USERPROFILE\.openclaw\delivery-queue" -Recurse -Force
```

---

## 📦 第七步：复制其他配置

```powershell
# 复制 completions（shell补全）
Copy-Item "completions" "$env:USERPROFILE\.openclaw\completions" -Recurse -Force

# 复制 canvas
Copy-Item "canvas" "$env:USERPROFILE\.openclaw\canvas" -Recurse -Force

# 复制 devices
Copy-Item "devices" "$env:USERPROFILE\.openclaw\devices" -Recurse -Force

# 复制 feishu 配置
Copy-Item "feishu" "$env:USERPROFILE\.openclaw\feishu" -Recurse -Force
```

---

## 🔑 第八步：手动配置（必须）

```powershell
# 创建 credentials 目录
New-Item -ItemType Directory -Path "$env:USERPROFILE\.openclaw\credentials" -Force

# 创建 identity 目录
New-Item -ItemType Directory -Path "$env:USERPROFILE\.openclaw\identity" -Force
New-Item -ItemType Directory -Path "$env:USERPROFILE\.openclaw\media" -Force
New-Item -ItemType Directory -Path "$env:USERPROFILE\.openclaw\logs" -Force
```

### 需要手动添加的密钥：
1. **MiniMax API Key** → 告诉静静获取
2. **飞书 Bot Token** → 配置飞书连接
3. **微信公众号配置** → 如需发布文章

---

## ✅ 第九步：验证恢复

```powershell
# 检查状态
openclaw status

# 启动 Gateway
openclaw gateway start

# 查看 skills
openclaw skills list

# 测试飞书
openclaw feishu test
```

---

## 🎉 完成！

恢复成功后，你可以：
- 使用所有之前配置的 agents（小苹果、小帅、小美、Zero）
- 使用所有 skills（热点推送、公众号发布等）
- 查看历史对话和记忆

---

## ❓ 遇到问题？

1. **Gateway 启动失败** → 检查 credentials 是否配置
2. **Agent 无法连接** → 检查 API Key 是否正确
3. **飞书无响应** → 检查飞书 Bot Token

---

**有问题联系静静获取帮助** 📞