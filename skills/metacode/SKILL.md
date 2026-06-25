---
name: metacode
description: 通过自然语言提示词自动配置、管理 OpenCode 等Agent软件的元编程 skill。覆盖初始化配置、skill/plugin/MCP 创建、更新诊断、自进化等全生命周期管理。用户无需记忆 CLI 命令，用对话即可完成所有运维操作。
category: devops
author: William
tags: [atomcode, meta, automation, self-evolving, mcp]
version: 0.1.0
---

# Metacode —— 用说话的方式驾驭 Agent软件

## 定位

Metacode 是 Agent软件 (OpenCode, OpenClaw等) 的"管理员模式"。
普通 skill 帮你写业务代码，Metacode 帮你管理 AtomCode 本身：
装插件、建 skill、配 MCP、查故障、做升级，甚至让它自己改进自己。

## 能力范围

### 1. 初始化与基础配置
- 一键检测安装状态与环境
- 根据用户技术栈（前端/后端/算法/全栈）自动推荐并写入 `config.yaml`
- 管理模型 provider、API Key、默认模型的增删改查
- 备份与回滚配置

### 2. Skill 生命周期管理
- 从对话描述生成完整的 `SKILL.md`（含 YAML frontmatter + 操作步骤）
- 自动写入 `~/.config/<agent>/skills/` 或项目级 `.<agent>/skills/`
- 支持 skill 的启用、禁用、版本迭代、批量更新
- 提供 skill 质量自检（frontmatter 完整性、步骤可执行性）

### 3. Plugin / MCP 管理
- 解析社区 plugin/MCP 仓库，一键安装、配置、卸载
- 自动处理 MCP server 的 `stdio` / `sse` 接入参数
- 监控 plugin 加载状态，冲突时自动降级或提示

### 4. 更新与诊断
- 检测软件本体、skill、plugin 的更新
- 执行安全升级（先备份再替换）
- 收集运行日志、环境信息，定位常见故障（网络、权限、依赖缺失）
- 生成诊断报告并提供修复建议

### 5. 自进化（Self-Evolving）
- **技能自省**：分析当前对话中 Agent 的表现，识别重复错误、低效模式
- **自动修补**：将修复方案写入对应 skill 的 pitfalls 或新增操作步骤
- **技能合并**：发现功能重叠的 skill，提出合并方案并执行
- **元日志**：记录每次自进化的变更点，支持人工审阅与回退

## 使用示例

### 场景 A：新人上手
> 用户：我刚装好 OpenCode，主要写 Python 后端，帮我配好环境
>
> Opencode：
> 1. 检测安装路径与版本
> 2. 写入推荐配置（模型：qwen-coder；默认 shell：zsh；Python 工具集全开）
> 3. 安装 `python-expert`、`git-workflow` 两个 skill
> 4. 验证配置生效

### 场景 B：创建自定义 skill
> 用户：我需要一个 skill，用来把设计稿转成 Tailwind CSS
>
> Metacode：
> 1. 追问细节（输入格式、输出规范、是否需要截图分析）
> 2. 生成 `design-to-tailwind/SKILL.md`
> 3. 注册到 skill 目录
> 4. 现场测试一个用例，确认可用

### 场景 C：故障排查
> 用户：OpenCode 突然不响应我的 MCP 工具了
>
> Metacode：
> 1. 读取最近 50 行日志
> 2. 检查 MCP server 进程是否存活
> 3. 验证 `config.yaml` 中 mcp_servers 配置格式
> 4. 发现 JSON 语法错误，自动修复并重启服务

### 场景 D：自进化触发
> 用户：（连续 3 次在同一个 skill 上遇到相似错误）
>
> Metacode（后台）：
> 1. 识别重复失败模式
> 2. 在原 skill 的 pitfalls 段追加规避方案
> 3. 向用户汇报："已为你优化了 XX skill，下次不会再踩这个坑"

## 设计原则

1. **对话即接口**：所有操作都通过自然语言完成，零命令记忆负担
2. **安全第一**：修改配置前自动备份，关键操作需确认，支持 undo
3. **透明可审计**：每次变更记录原因、 diff、时间戳，用户随时可查
4. **渐进增强**：基础功能开箱即用，自进化等高级能力默认关闭，需用户授权

## Roadmap

- [x] v0.1 基础配置 + skill 创建
- [ ] v0.2 Plugin / MCP 自动化管理
- [ ] v0.3 诊断中心 + 一键修复
- [ ] v0.4 自进化引擎（技能自省与自动修补）
- [ ] v0.5 社区 skill 市场接入（一键安装他人分享的 metacode 包）
