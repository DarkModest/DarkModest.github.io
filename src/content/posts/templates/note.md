---
title: Templates
published: 2026-07-03
description: Useful Templates for Writing Notes, Guides, and Troubleshooting Posts.
tags: [Markdown, Blogging]
category: Examples
draft: false
---

# [错误代码/错误现象] 修复记录

## 1. 元数据（Metadata）
> **日期**：2026-07-03 | **环境**：Win11 / Python 3.10 / Docker | **严重级**：P0

## 2. 现象与复现（What）
- **预期结果**：（系统正常应输出什么）
- **实际结果**：（贴报错截图或Log日志，重点用 `[ERROR]` 标出）
- **复现步骤**：
  1. 执行 `npm run build`
  2. 观察控制台...

## 3. 根因分析（Why）—— 对应你的“原因”
- **直接原因**：依赖包 `axios` 版本从 v1.5 升级到 v1.6 导致 API 参数校验失效。
- **深层原因**：（技术债/文档缺失/并发冲突）
- **排查过程**：（简述二分法定位或关键Debug日志）

## 4. 原理剖析（How）—— 对应你的“概念”
> *（此处解释涉及的核心机制，比如HTTP Keep-Alive、JVM内存模型、React Fiber等）*
- 为什么 v1.6 会报错？因为官方修改了默认 `transitional` 配置...

## 5. 解决方案（What）—— 对应你的“解决方法”
- **临时方案**：（回滚版本 / 重启）
- **最终方案**：（修改 `axios.defaults.transitional` 配置，贴Diff代码）
- **验证结果**：（贴测试通过的截图）

## 6. 经验教训与Checklist
- [ ] 后续升级第三方库前，务必阅读 **Breaking Changes**。
- [ ] 增加单元测试覆盖该边界Case。

# [技术名称] 学习笔记：核心特性

## 1. 为什么需要它？（痛点）
- 旧方案（如同步IO）在并发高时阻塞线程。
- 该技术承诺解决：**高吞吐、低延迟**。

## 2. 核心概念（核心理念）
- **定义**：它是什么？（一句话说清）
- **架构图**：
  > ```mermaid
  > graph LR; Client-->Proxy-->Backend
  > ```
- **关键术语表**：（如：持久化、哨兵模式、集群分片）

## 3. 核心原理（深入浅出）
- **工作流程**：数据写入后，底层发生了哪几步？（如：写AOF -> 更新内存 -> 返回ACK）
- **关键源码/配置解读**：（只记最难懂的那个参数，如 `maxmemory-policy`）

## 4. 快速上手（Hello World）
- 环境搭建指令（Docker 一键启动）
- 最常用 API 示例（附输出结果）

## 5. 踩坑指南（Troubleshooting）
- **坑点1**：默认配置不适用于生产环境 -> 解决方法。

# [场景] 常用指令速查

## 场景：日志太大，需要切割
- **命令**：`split -b 100m access.log log_part_`
- **回显解释**：生成 log_part_aa, ab...

## 场景：Git 误提交大文件
- **步骤**：
  1. `git filter-branch ...` （强制改写历史）
  2. `git push --force-with-lease`
- **注意**：团队协作时禁用，除非全员知晓。