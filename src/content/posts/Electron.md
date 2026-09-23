---
title: Electron 入门
published: 2026-08-19
description: Introduction to Electron.
category: Notes
draft: false
---
# Electron 入门

## 简介

- Electron是一个开源框架，可以写成跨平台的桌面程序。
- 简单地说，Electron = Chromium + Node.js + Native APIs。

## 架构

- Main 进程：Electron的入口，负责创建 `BrowserWindow`、管理应用生命周期和原生 API。
- Renderer 进程：每个 `BrowserWindow` 对应一个 renderer，运行网页，不直接访问 Node。
- Preload 脚本：连接 main 和 renderer 的桥梁。在 renderer 加载网页前进行，通过 contextBridge 安全地暴露 API给 renderer。
- IPC（进程间通信）：通信核心。Preload 脚本通过 IPC 实现连接功能。
|类型|主进程监听|渲染进程发送|
|---|:--|---|
|渲染 → 主|ipcMain.on(channel, handler)|ipcRenderer.send(channel, data)|
|主 → 渲染|event.sender.send(channel, data)|ipcRenderer.on(channel, callback)|