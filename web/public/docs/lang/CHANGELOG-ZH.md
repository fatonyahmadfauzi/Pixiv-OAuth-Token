# 变更日志

All notable changes to the "Pixiv OAuth Token" toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🔜 Coming Soon

- **Mobile Web Support** — The web app currently only supports desktop browsers. Upcoming update will bring full responsive mobile support, allowing users to generate Pixiv OAuth tokens directly from mobile devices without needing the desktop app.


---

## [1.0.5] - 2026-04-03

### ✨ 添加

- **互联网感知 GUI 启动**
在启动主 GUI 窗口之前，智能 `NetLoadingScreen` 闪屏现在会执行飞行前互联网连接检查。如果未找到连接，它将在后台安全地重试，直到连接为止。此外，如果在使用过程中连接中断，活动的运行时监视器将显示一条警报，返回到加载屏幕。
- **本机 GUI 文档模态**
替换了关键文档的外部浏览器重定向。 **变更日志**、**条款和条件**以及**隐私政策**现在显示在本机、动态且干净的 `tkinter` 对话框窗口中（直接从 GitHub 存储库异步获取）。
- **全面的终端本地化**
交互式 GitHub CLI 界面（问题导航）和所有基于终端的法律/支持布局现在已在所有 11 种支持的语言中进行了真正的本地化。

### ✨ 已更改

- **重新设计的 CLI 美学**
删除了传统的装饰框边框，以获得更加干净、现代化、左对齐的终端显示。
- **自动数字代码签名**
大幅升级 `sign_auto.bat` 管道。该脚本现在动态自动发现 Windows SDK 深处的 `signtool.exe`，轻松地在所有生成的版本中同时应用自签名证书（包括安装程序设置和下载 `_latest` 别名），以抑制基本的 SmartScreen“未知发布者”标志。

### 🐞 已修复

- **安装程序属性错误**
修复了安装程序 `Setup.exe` 在 Windows 属性中显示 `0.0.0.0` 的异常情况。现在，构建器在编译期间正确注入严格的 PE `VersionInfoVersion` 标头，以在渲染后立即反映精确匹配的版本号（e.g.、1.0.5.0）。

---

## [1.0.4] - 2026-03-29

### 🐞 已修复

- **便携式 CLI/GUI — 更新后版本回滚**：`VERSION_FILE` 和 `CONFIG_FILE` 使用 `Path(__file__)` 解析，在冻结（PyInstaller onefile）模式下指向临时 `_MEIPASS` 目录 — 该目录在应用程序关闭时被销毁。现在，这两个文件都使用 `_app_dir()` / `app_dir()` 进行解析，这会正确返回包含实际 `.exe` 的文件夹，确保版本标识在重新启动后保持不变。
- **CLI — 更新覆盖临时 `.py` 而不是 exe**：作为冻结可执行文件运行时，`_self_update()` 覆盖临时目录中提取的 `.py`，而不是替换实际的 `.exe`。该函数现在检测 `is_frozen` 并直接下载新的可执行文件，通过 `.bat` 更新程序脚本替换它（与 GUI 相同的机制）。

### ✨ 添加

- **架构感知自动更新 (CLI + GUI)**：可移植和安装更新流程现在都可以从文件名中检测正在运行的可执行文件（`x64`、`x86`、`ARM64` 或通用）的架构，并从 `downloads/` 文件夹下载精确匹配的变体，从而防止更新期间意外出现架构不匹配。
- **CLI 安装程序更新流程**：CLI 现在镜像安装程序安装的 GUI 行为 — 当从 `Program Files` 运行时，它会下载最新的 `.exe` 安装程序并以静默方式运行它 (`/VERYSILENT /NORESTART`)，而不是尝试就地二进制交换。

---

## [1.0.3] - 2026-03-26

### ✨ 已更改

- 在运行时/版本工具和生成的清单中将默认本地构建标签从 `REL-LOCAL` 替换为 `BUILD-UNKNOWN`。
- GUI 现在包括 **Changelog** 顶部菜单操作和带有显式版本检查条目的 **Version** 下拉列表。
- 在 GUI 中添加了自动启动版本检查和更新弹出操作（**更新** / **稍后**），以及冻结安装/便携式发行版的更新流程处理。
- 在版本升级 (`patch/minor/major`) 上将构建代码生成更新为 Unix 风格 `REL-U<unix_ms>`。

## [1.0.2] - 2026-03-23

### ✨ 添加

- **调试控制台 (GUI)**
GUI 标题右上角的专用 `⚙ Debug` 按钮可打开一个深色主题的终端控制台，该控制台实时记录每个应用程序事件。捕获的事件包括：应用程序启动、语言更改、所有按钮单击（打开登录、交换令牌、刷新令牌、复制访问/刷新令牌、教程）、HTTP 请求状态（发送/成功/失败）、PKCE 流程步骤、剪贴板操作、配置写入和警告。所有调试消息均已完全本地化为所有 11 种受支持的语言。控制台支持在打开时实时传输新消息、从会话开始预填充历史日志、**复制全部**按钮和**清除**按钮。

## [1.0.1] - 2026-03-22

### ✨ 添加

- **用于发布的智能自述文件清理器**
编译可分发的 `.zip` 时，自动从 `` 文件中删除本地化语言部分，用绝对 GitHub 链接替换内部链接。
- **统一双安装程序支持**
InnoSetup 构建器脚本现在生成一个统一的安装程序，提示最终用户选择安装独立的 CLI 或图形化的 GUI。

### 🐞 已修复

- **安装程序构建路径解析**
修复了 `make_installer_iss_dual.py` 中的关键路径不匹配问题，其中 `iscc` 无法通过直接在配置的 `scripts\` 目录中生成构建文件来找到 `app\pixiv_oauth.ico`。

## [1.0.0] - 2026-03-21

### ✨ 添加

- 为 GUI 和 CLI 模式编译的初始独立可执行发行版 (`.exe`)。
- 初始优化的无服务器集成通过自动语言检测同步到 Vercel。
- 为 Web 端点添加了极端 JavaScript 混淆过程。
