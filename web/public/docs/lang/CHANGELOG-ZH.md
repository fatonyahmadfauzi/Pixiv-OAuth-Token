# 变更日志

All notable changes to the "Pixiv OAuth Token" toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


---
## [1.0.3] - 2026-03-26 
### ✨ 已更改
- 在运行时/版本工具和生成的清单中将默认本地构建标签从 `REL-LOCAL` 替换为 `BUILD-UNKNOWN`。
- GUI 现在包括 **Changelog** 顶部菜单操作和带有显式版本检查条目的 **Version** 下拉列表。
- 在 GUI 中添加了自动启动版本检查和更新弹出操作（**更新** / **稍后**），以及冻结安装/便携式发行版的更新流程处理。
- 在版本升级 (`patch/minor/major`) 上将构建代码生成更新为 Unix 风格 `REL-U<unix_ms>`。

## [1.0.2] - 2026-03-23 
### ✨ 已添加
- **调试控制台（GUI）**
GUI 标题右上角的专用 `⚙ Debug` 按钮可打开一个深色主题的终端控制台，该控制台实时记录每个应用程序事件。捕获的事件包括：应用程序启动、语言更改、所有按钮单击（打开登录、交换令牌、刷新令牌、复制访问/刷新令牌、教程）、HTTP 请求状态（发送/成功/失败）、PKCE 流程步骤、剪贴板操作、配置写入和警告。所有调试消息均已完全本地化为所有 11 种受支持的语言。控制台支持在打开时实时传输新消息、从会话开始预填充历史日志、**复制全部**按钮和**清除**按钮。

## [1.0.1] - 2026-03-22
### ✨ 已添加
- **用于发布的智能自述文件清理器**
编译可分发的 `.zip` 时，自动从 `` 文件中删除本地化语言部分，用绝对 GitHub 链接替换内部链接。
- **统一双安装程序支持**
InnoSetup 构建器脚本现在生成一个统一的安装程序，提示最终用户选择安装独立 CLI 或图形 GUI。

### 🐞 已修复
- **安装程序构建路径解析**
修复了 `make_installer_iss_dual.py` 中的关键路径不匹配问题，其中 `iscc` 无法通过直接在配置的 `scripts\` 目录中生成构建文件来找到 `app\pixiv_oauth.ico`。

## [1.0.0] - 2026-03-21
### ✨ 已添加
- 为 GUI 和 CLI 模式编译的初始独立可执行发行版 (`.exe`)。
- 初始优化的无服务器集成通过自动语言检测同步到 Vercel。
- 为 Web 端点添加了极端 JavaScript 混淆过程。
