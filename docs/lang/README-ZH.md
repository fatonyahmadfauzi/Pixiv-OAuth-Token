# Pixiv OAuth Token


> 🌐 提供其他语言版本： [English](../../README.md) | [Polski](README-PL.md) | [日本語](README-JP.md) | [Deutsch](README-DE.md) | [Français](README-FR.md) | [Español](README-ES.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [Bahasa Indonesia](README-ID.md) | [한국어](README-KR.md)

---
用于以三种模式生成 Pixiv OAuth 令牌的工具包：

- CLI (`pixiv_login.py`)
- 图形用户界面 (`pixiv_login_gui.py`)
- Web 应用程序（`public/` + 无服务器 API）

＃＃ 要求

- Python 3.11+
- Windows（`.bat` 构建脚本和 Inno Setup 安装程序所需）
- 来自 `requirements.txt` 的 Python 依赖项

## 从源代码运行

```bash
python -m pip install -r requirements.txt
python pixiv_login.py
```

运行图形用户界面：

```bash
python pixiv_login_gui.py
```

＃＃ 建造

### 构建所有工件（CLI + GUI + 安装程序 + ZIP）

```bat
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
- `nogui`（跳过 GUI）
- `nopause` （最后没有停顿）

例子：

```bat
build_all_pro.bat patch noinst nosign
```

### 主要输出

- 便携式 CLI：`dist_portable\Pixiv OAuth CLi (Portable).exe`
- 便携式图形用户界面：`dist_gui\Pixiv OAuth GUi (Portable).exe`
- 安装程序 CLI：`dist_installer\Pixiv OAuth CLi Setup_v<version>.exe`
- 安装程序 GUI：`dist_installer\Pixiv OAuth GUi Setup_v<version>.exe`
- 发布邮编：`PixivOAuthRelease_v<version>.zip`
- 自动同步文件夹：`downloads/`（最新的便携式/设置+发布ZIP）

## 签名

编辑`sign_auto.bat`：

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

如果 PFX 文件丢失，则会跳过签名。

## 版本控制

应用程序版本存储在 `version.json` 中。

## 网页版 (Vercel)

高度优化的响应式 Web 应用程序，具有动态多语言支持（自动检测 11 种语言）和全面的 SEO 元数据。

### 主要网络功能
- **广泛的页面**：主页、下载、教程、联系方式、问题和 PR、讨论跟踪器、文档 Markdown 查看器以及支持/捐赠集成。
- **高级 SEO**：自动注入本地化 `<meta>` 标签、广泛的 JSON-LD 结构化数据（站点链接、软件应用程序等）、自动 `hreflang` 生成、`robots.txt` 和 `sitemap.xml`。
- **安全性和性能**：自动 JavaScript 混淆（极端修改）、HTML/CSS 缩小（通过 `node build_minify.js`）以及通过 `escapeHTML` 进行干净的 `XSS` 预防。
- **GitHub API 代理**：无服务器 Vercel 端点 (`/api/github`) 使用个人访问令牌 (`GITHUB_PAT`) 代理 GitHub API 请求，以完全绕过公共速率限制。

### 部署到 Vercel

1. 将存储库推送到 GitHub。
2. Vercel → **添加新...** → **项目** → 导入此存储库。
3. 在 Vercel 中设置环境变量：
- `PIXIV_CLIENT_SECRET`：您的 Pixiv OAuth 客户端密钥。
- `GITHUB_PAT`：可选但强烈推荐（您的 GitHub 个人访问令牌以避免回购问题和发布的速率限制）。
4. `vercel.json` 已经配置：
- 干净的 URL（剥离 `.html`）
- 来自 `public/` 的静态托管
- 无服务器 API 位于 `/api/*`
- 内置自定义 404 页面路由
- 通过边缘缓存标头进行远期缓存。
5. 部署。

> [!重要]
> 如果您对 HTML、CSS 或 JS 进行更改，请记住在部署之前运行 `node build_minify.js` 以自动混淆代码并压缩资源。

> 安全说明：对于生产，请始终在 Vercel 项目环境变量中设置 `PIXIV_CLIENT_SECRET`。

## 下载应用程序（最新版本）

基本网址：

`https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download`

文件：

- 便携式图形用户界面：`Pixiv OAuth GUi (Portable).exe`
- 设置 GUI：`Pixiv OAuth GUi Setup_v<version>.exe`
- 便携式 CLI：`Pixiv OAuth CLi (Portable).exe`
- 设置 CLI：`Pixiv OAuth CLi Setup_v<version>.exe`

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
python -m pip install -r requirements.txt
```

或者直接从 GitHub 安装：

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```

＃＃ 执照

MIT License。参见 `LICENSE`。
> 🌐 其他语言版本：[Polski](docs/lang/README-PL.md) | [中文](docs/lang/README-ZH.md) | [日本语](docs/lang/README-JP.md) | [德语](docs/lang/README-DE.md) | [法语](docs/lang/README-FR.md) | [西班牙语](docs/lang/README-ES.md) | [Русский](docs/lang/README-RU.md) | [葡萄牙语](docs/lang/README-PT.md) | [印尼语](docs/lang/README-ID.md) | [한국어](docs/lang/README-KR.md)
