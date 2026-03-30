---
name: Community Manager
description: >
  📱 社群运营工具。社群搭建、活跃度提升、内容规划、用户增长、变现策略、危机处理。
  使用方式：通过 exec 调用 bash 脚本（需通过 PowerShell）
allowed-tools:
  - Read
  - Write
  - exec
---

# Community Manager

社群运营工具。社群搭建、活跃度提升、内容规划、用户增长、变现策略、危机处理。

## 使用方式

在Windows上，需要通过PowerShell调用Git Bash运行脚本：

```powershell
powershell -Command "& 'C:\Program Files\Git\bin\bash.exe' 'skills\community-manager-cn-1.0.4\scripts\community.sh' <command> [args...]"
```

## 命令列表

| 命令 | 功能 | 示例 |
|------|------|------|
| `calendar` | 生成月度运营日历 | calendar 2025-03 "AI学习群" |
| `activity` | 生成活动方案 | activity "抽奖" "春季回馈" |
| `report` | 生成数据分析报告 | report "技术社群" 800 240 50 2000 6 |
| `sop` | 生成运营SOP模板 | sop |

## 功能说明

### calendar - 运营日历
- 生成月度运营日历
- 包含每日安排和KPI目标
- 每周主题规划

### activity - 活动方案
- 完整活动方案
- 包含流程/预算/话术/风险

### report - 数据报告
- 社群健康度评分
- 成员分层分析
- 改进建议

### sop - 运营SOP
- 日/周/月运营模板
- 标准流程文档
