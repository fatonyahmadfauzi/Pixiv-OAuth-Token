# Pixiv OAuth Token


> 🌐 他の言語でも利用可能: [English](../../README.md)

---
Pixiv OAuth トークンを 3 つのモードで生成するツールキット:

- CLI (`pixiv_login.py`)
- GUI (`pixiv_login_gui.py`)
- Web アプリ (`public/` + サーバーレス API)

＃＃ 要件

- Python 3.11+
- Windows (`.bat` ビルド スクリプトと Inno Setup インストーラーに必要)
- `requirements.txt` からの Python 依存関係

## ソースから実行

```bash
python -m pip install -r requirements.txt
python pixiv_login.py
```

GUI を実行します。

```bash
python pixiv_login_gui.py
```

＃＃ 建てる

### すべてのアーティファクトをビルドする (CLI + GUI + インストーラー + ZIP)

```bat
build_all_pro.bat patch
```

バージョン引数:

- `patch`
- `minor`
- `major`
- `none`

オプションのフラグ:

- `noinst` (インストーラーをスキップ)
- `nosign` (署名をスキップ)
- `nozip` (zipをスキップ)
- `nogui` (GUI をスキップ)
- `nopause` (最後に一時停止なし)

例：

```bat
build_all_pro.bat patch noinst nosign
```

### 主な出力

- ポータブル CLI: `dist_portable\Pixiv OAuth CLi (Portable).exe`
- ポータブル GUI: `dist_gui\Pixiv OAuth GUi (Portable).exe`
- インストーラー CLI: `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe`
- インストーラー GUI: `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe`
- リリース ZIP: `PixivOAuthRelease_v<version>.zip`
- 自動同期フォルダー: `downloads/` (最新のポータブル/セットアップ + リリース ZIP)

## 署名

`sign_auto.bat`を編集:

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

PFX ファイルが見つからない場合、署名はスキップされます。

## バージョン管理

アプリケーションのバージョンは `version.json` に保存されます。

## Web版（Vercel）

動的多言語サポート (自動検出付き 11 言語) と包括的な SEO メタデータを備えた、高度に最適化された応答性の高い Web アプリです。

### 主要な Web 機能
- **豊富なページ**: ホームページ、ダウンロード、チュートリアル、連絡先、問題と PR、ディスカッション トラッカー、ドキュメント Markdown ビューア、およびサポート/寄付の統合。
- **高度な SEO**: 自動挿入されたローカライズされた `<meta>` タグ、広範な JSON-LD 構造化データ (サイトリンク、ソフトウェア アプリケーションなど)、自動 `hreflang` 生成、`robots.txt`、および `sitemap.xml`。
- **セキュリティとパフォーマンス**: JavaScript の自動難読化 (極端なマングリング)、HTML/CSS の縮小 (`node build_minify.js` 経由)、および `escapeHTML` 経由のクリーンな `XSS` 防止。
- **GitHub API プロキシ**: サーバーレス Vercel エンドポイント (`/api/github`) プロキシ GitHub API リクエストは、パーソナル アクセス トークン (`GITHUB_PAT`) を使用してパブリック レート制限を完全にバイパスします。

### Vercel にデプロイする

1. リポジトリを GitHub にプッシュします。
2. Vercel → **新規追加...** → **プロジェクト** → このリポジトリをインポートします。
3. Vercel で環境変数を設定します。
- `PIXIV_CLIENT_SECRET`: Pixiv OAuth クライアント シークレット。
- `GITHUB_PAT`: オプションですが強く推奨されます (リポジトリの問題とリリースのレート制限を回避するための GitHub パーソナル アクセス トークン)。
4. `vercel.json` はすでに以下を構成しています。
- クリーンな URL (`.html` の除去)
- `public/` からの静的ホスティング
- `/api/*` のサーバーレス API
- 組み込みのカスタム 404 ページ ルーティング
- Edge Cache ヘッダーを介した遠い将来のキャッシュ。
5. デプロイします。

> [!重要]
> HTML、CSS、または JS に変更を加える場合は、コードを自動的に難読化し、アセットを圧縮するために、展開する前に必ず `node build_minify.js` を実行してください。

> セキュリティ上の注意: 運用環境では、Vercel プロジェクトの環境変数に常に `PIXIV_CLIENT_SECRET` を設定してください。

## アプリケーションをダウンロード (最新リリース)

ベース URL:

`https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download`

ファイル:

- ポータブル GUI: `Pixiv OAuth GUi (Portable).exe`
- セットアップ GUI: `Pixiv OAuth GUi Setup_v<version>.exe`
- ポータブル CLI: `Pixiv OAuth CLi (Portable).exe`
- CLI のセットアップ: `Pixiv OAuth CLi Setup_v<version>.exe`

### PowerShell (最新リリースの資産を自動検出)

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

### PowerShell (`downloads/` からの修正 URL)

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

これを **PowerShell** (CMD ではなく) で実行します。

実行するだけの場合:

```powershell
$guiPortable = "..."
```

そして何も表示されません、それは予想通りです。変数に値を格納するだけです。 `Invoke-WebRequest` を実行するとダウンロードが開始されます。

ダウンロードが完了し、PowerShell がエラーなしで `PS C:\...>` に戻ると、次のようになります。

```powershell
Get-ChildItem "Pixiv OAuth GUi (Portable).exe"
Start-Process ".\Pixiv OAuth GUi (Portable).exe"
```

インストーラーのビルドの場合:

```powershell
Invoke-WebRequest $guiSetup -OutFile "Pixiv OAuth GUi Setup.exe"
Start-Process ".\Pixiv OAuth GUi Setup.exe"
```

TLS ポリシーがダウンロードをブロックする場合:

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

### CMD (最新リリースのアセットを自動検出)

```cmd
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi Setup.exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi Setup.exe"
```

## Python のインストール

```bash
python -m pip install -r requirements.txt
```

または、GitHub から直接インストールします。

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```

## ライセンス

MIT License。 `LICENSE`を参照してください。
