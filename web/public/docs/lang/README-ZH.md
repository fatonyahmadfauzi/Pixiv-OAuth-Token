# Pixiv OAuth Token


> 🌐 提供其他语言版本： [English](..\..\..\../README.md) | [Polski](README-PL.md) | [日本語](README-JP.md) | [Deutsch](README-DE.md) | [Français](README-FR.md) | [Español](README-ES.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [Bahasa Indonesia](README-ID.md) | [한국어](README-KR.md)

---
> 🌐 其他语言版本：[日语](web/public/docs/lang/README-JP.md)

一个以三种模式生成 Pixiv OAuth 代币的工具包：

- CLI (`app/pixiv_login.py`)
- GUI (`app/pixiv_login_gui.py`)
- Web 应用程序（`web/public/` + 无服务器 API）

＃＃ 要求

- Python 3.11+
- Windows（`.bat` 构建脚本和 Inno Setup 安装程序所需）
- Python 依赖于 `app/requirements.txt`

## 从源代码运行

```bash
cd app
python -m pip install -r requirements.txt
python pixiv_login.py
```

运行GUI：

```bash
cd app
python pixiv_login_gui.py
```

### GUI 特点

|特色 |描述 |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **多语言** | 11 种语言 — 从配置中自动检测，可通过下拉菜单实时切换 |
| **⚙ 调试控制台** |右上角标题中的按钮；打开一个黑暗的终端，以当前语言实时记录**所有**事件（按钮单击、语言更改、HTTP 请求、PKCE 步骤、剪贴板、配置保存、警告）|
| **代币兑换** |粘贴pixiv:// URL 或原始代码→ 交换访问权限+刷新令牌 |
| **刷新令牌** |使用配置中保存的refresh_token一键刷新|
| **复制令牌** |立即将 access_token / refresh_token 复制到剪贴板 |
| **教程** |应用程序内置分步图像指南 |

＃＃ 建造

### 构建所有工件（CLI + GUI + 安装程序 + ZIP）

```bat
cd scripts
build_all_pro.bat patch
```

版本参数：

- `patch`
- `minor`
- `major`
- `none`

可选标志：

- `noinst`（跳过安装程序）
- `nosign`（跳过签名）
- `nozip`（跳过拉链）
- `nogui` （跳过 GUI）
- `nopause` （最后没有停顿）

例子：

```bat
cd scripts
build_all_pro.bat patch noinst nosign
```

### 主要输出

- 便携式CLI：`dist_portable\Pixiv OAuth CLi (Portable).exe`
- 便携式GUI：`dist_gui\Pixiv OAuth GUi (Portable).exe`
- 统一安装程序：`dist_installer\PixivLoginSetup_v<version>.exe`（同时安装 CLI + GUI）
- 安装程序 CLI: `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe` （统一安装程序的副本）
- 安装程序 GUI: `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe` （统一安装程序的副本）
- 发布邮编：`PixivOAuthRelease_v<version>.zip`
- 自动同步文件夹：`downloads/`（最新的便携式/设置+发布ZIP）

## 签名

编辑`scripts/sign_auto.bat`：

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

如果 PFX 文件丢失，则会跳过签名。

## 版本控制

应用程序版本/构建标识存储在 `version.json` 中。

- `version`：语义版本 (`X.Y.Z`)
- `build_code`：唯一的构建标识符

默认的非发布后备现在是 `BUILD-UNKNOWN` （而不是 `REL-LOCAL`），而发布碰撞通过 `scripts/bump_version.py` 生成 unix 风格的构建代码：

- `REL-U<unix_ms>`

## 网页版 (Vercel)

高度优化的响应式 Web 应用程序，具有动态多语言支持（自动检测 11 种语言）和全面的 SEO 元数据。

### 主要网络功能

- **广泛的页面**：主页、下载、教程、联系方式、问题和 PR、讨论跟踪器、文档 Markdown 查看器以及支持/捐赠集成。
- **高级 SEO**：自动注入本地化 `<meta>` 标签、广泛的 JSON-LD 结构化数据（站点链接、软件应用程序等）、自动 `hreflang` 生成、`robots.txt` 和 `sitemap.xml`。
- **安全性和性能**：自动 JavaScript 混淆（极端修改）、HTML/CSS 缩小（通过 `cd web && node build_minify.js`）以及通过 `escapeHTML` 进行干净的 `XSS` 预防。
- **GitHub API 代理**：无服务器 Vercel 端点 (`/api/github`) 代理 GitHub API 使用个人访问令牌 (`GITHUB_PAT`) 请求完全绕过公共速率限制。

### 部署到 Vercel

1. 将存储库推送到 GitHub。
2. Vercel → **添加新...** → **项目** → 导入此存储库。
3. 在 Vercel 中设置环境变量：
- `PIXIV_CLIENT_SECRET`：您的 Pixiv OAuth 客户端机密。
- `GITHUB_PAT`：可选但强烈推荐（您的 GitHub 个人访问令牌以避免回购问题和发布的速率限制）。
4. `vercel.json` 已经配置：
- 干净的 URL（剥离 `.html`）
- 来自 `public/` 的静态托管
- `/api/*` 处的无服务器 APIs
- 内置自定义 404 页面路由
- 通过边缘缓存标头进行远期缓存。
5. 部署。

> [!重要]
> 如果您对 HTML、CSS 或 JS 进行更改，请记住在部署之前运行 `cd web && node build_minify.js` 以自动混淆代码并压缩资源。

> 安全说明：对于生产环境，请始终在 Vercel 项目环境变量中设置 `PIXIV_CLIENT_SECRET`。

## 下载应用程序（最新版本）

基本网址：

`https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download`

文件：

- 便携式GUI：`Pixiv OAuth GUi (Portable).exe`
- 设置 GUI: `Pixiv OAuth GUi Setup_v<version>.exe`
- 便携式CLI：`Pixiv OAuth CLi (Portable).exe`
- 设置 CLI: `Pixiv OAuth CLi Setup_v<version>.exe`

### PowerShell（自动检测最新版本资产）

```powershell
$api = "https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest"
$assets = (Invoke-RestMethod -Uri $api).assets

function Get-AssetUrl([string]$pattern) {
  ($assets | Where-Object { $_.name -match $pattern } | Select-Object -First 1).browser_download_url
}

$guiPortable = Get-AssetUrl "Pixiv OAuth GUi \(Portable\)"
$cliPortable = Get-AssetUrl "Pixiv OAuth CLi \(Portable\)"
$guiSetup    = Get-AssetUrl "Pixiv OAuth GUi Setup"
$cliSetup    = Get-AssetUrl "Pixiv OAuth CLi Setup"

Invoke-WebRequest $guiPortable -OutFile "Pixiv OAuth GUi (Portable).exe"
Invoke-WebRequest $cliPortable -OutFile "Pixiv OAuth CLi (Portable).exe"
Invoke-WebRequest $guiSetup    -OutFile "Pixiv OAuth GUi Setup.exe"
Invoke-WebRequest $cliSetup    -OutFile "Pixiv OAuth CLi Setup.exe"
```

### PowerShell（来自 `downloads/` 的固定 URL）

```powershell
$guiPortable = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads/Pixiv%20OAuth%20GUi%20(Portable)_latest.exe"
$cliPortable = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads/Pixiv%20OAuth%20CLi%20(Portable)_latest.exe"
$guiSetup    = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads/Pixiv%20OAuth%20GUi%20Setup_latest.exe"
$cliSetup    = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads/Pixiv%20OAuth%20CLi%20Setup_latest.exe"

Invoke-WebRequest $guiPortable -OutFile "Pixiv OAuth GUi (Portable).exe"
Invoke-WebRequest $cliPortable -OutFile "Pixiv OAuth CLi (Portable).exe"
Invoke-WebRequest $guiSetup    -OutFile "Pixiv OAuth GUi Setup.exe"
Invoke-WebRequest $cliSetup    -OutFile "Pixiv OAuth CLi Setup.exe"
```

在 **PowerShell** （不是 CMD）中运行它。

如果你只运行：

```powershell
$guiPortable = "..."
```

不出所料，什么也没有出现。它仅将值存储在变量中。当您运行 `Invoke-WebRequest` 时，下载开始。

下载完成后，PowerShell 返回到 `PS C:\...>` 且没有错误：

```powershell
Get-ChildItem "Pixiv OAuth GUi (Portable).exe"
Start-Process ".\Pixiv OAuth GUi (Portable).exe"
```

对于安装程序构建：

```powershell
Invoke-WebRequest $guiSetup -OutFile "Pixiv OAuth GUi Setup.exe"
Start-Process ".\Pixiv OAuth GUi Setup.exe"
```

如果 TLS 策略阻止下载：

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

### CMD（自动检测最新版本资产）

```cmd
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi Setup.exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi Setup.exe"
```

## Python 安装

```bash
cd app
python -m pip install -r requirements.txt
```

或者直接从 GitHub 安装：

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```

## 🧾 变更日志

在 [变更日志](CHANGELOG-ZH.md) 文件中查看每个版本的所有显着更改。
📦 您还可以直接在 [GitHub 发布页面](https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases).

### 最新：v1.0.5 (2026-04-03)

**✨ 添加**

- **互联网感知 GUI 启动** — 在启动 GUI 之前进行智能连接飞行前检查，并完成实时运行时连接监控。
- **原生 GUI 文档模式** — 条款和条件、隐私政策和变更日志现在直接显示在动态弹出窗口中，而不是强制 Web 重定向。
- **全面的终端本地化** — GitHub CLI 跟踪器和法律页面现在已在所有 11 种支持的语言中进行了真实翻译。

**✨ 更改并修复**

- **自动数字代码签名** — 所有可执行文件本机捆绑自签名身份以抑制 Windows SmartScreen。
- **安装程序属性错误** - 安装程序可执行文件正确地将 `1.0.5.0` 文件版本严格广播到 Windows PE 标头中，而不是默认为零。
- **重新设计 CLI 美学** - UI 框边框被消除，以实现时尚的左对齐终端显示。

**🔜 将在下次更新中**

- 移动网络支持——网络应用程序将获得移动浏览器的完全响应式布局。

＃＃ 执照

MIT License。参见 `LICENSE`。
