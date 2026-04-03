# Pixiv OAuth Token


> 🌐 他の言語でも利用可能: [English](../../../../README.md) | [Polski](README-PL.md) | [中文](README-ZH.md) | [Deutsch](README-DE.md) | [Français](README-FR.md) | [Español](README-ES.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [Bahasa Indonesia](README-ID.md) | [한국어](README-KR.md)

---

Pixiv OAuth トークンを 3 つのモードで生成するツールキット:

- CLI (`app/pixiv_login.py`)
- GUI (`app/pixiv_login_gui.py`)
- Web アプリ (`web/public/` + サーバーレス API)

＃＃ 要件

- Python 3.11+
- Windows (`.bat` ビルド スクリプトと Inno Setup インストーラーに必要)
- `app/requirements.txt` からの Python 依存関係

## ソースから実行

```bash
cd app
python -m pip install -r requirements.txt
python pixiv_login.py
```

GUI を実行します。

```bash
cd app
python pixiv_login_gui.py
```

### GUI の機能

|特集 |説明 |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **多言語** | 11 言語 — 設定から自動検出、ドロップダウン経由でライブで切り替え可能 |
| **⚙ デバッグ コンソール** |右上のヘッダーのボタン。 **すべて**のイベント (ボタンのクリック、言語の変更、HTTP リクエスト、PKCE ステップ、クリップボード、設定の保存、警告) をリアルタイムで現在の言語でログに記録するダーク ターミナルを開きます。
| **トークン交換**​​ | pixiv:// URL または生コードを貼り付け → アクセス + リフレッシュトークンと交換 |
| **リフレッシュトークン** |設定から保存したrefresh_tokenを使用してワンクリックで更新 |
| **トークンをコピー** | access_token /fresh_token を即座にクリップボードにコピーします |
| **チュートリアル** |アプリに組み込まれたステップバイステップの画像ガイド |

＃＃ 建てる

### すべてのアーティファクトをビルドする (CLI + GUI + インストーラー + ZIP)

```bat
cd scripts
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
cd scripts
build_all_pro.bat patch noinst nosign
```

### 主な出力

- ポータブル CLI: `dist_portable\Pixiv OAuth CLi (Portable).exe`
- ポータブル GUI: `dist_gui\Pixiv OAuth GUi (Portable).exe`
- 統合インストーラー: `dist_installer\PixivLoginSetup_v<version>.exe` (CLI + GUI の両方をインストールします)
- インストーラー CLI: `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe` (統合インストーラーのコピー)
- インストーラー GUI: `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe` (統合インストーラーのコピー)
- リリース ZIP: `PixivOAuthRelease_v<version>.zip`
- 自動同期フォルダー: `downloads/` (最新のポータブル/セットアップ + リリース ZIP)

## 署名

`scripts/sign_auto.bat`を編集:

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

PFX ファイルが見つからない場合、署名はスキップされます。

## バージョン管理

アプリケーションのバージョン/ビルド ID は `version.json` に保存されます。

- `version`: セマンティック バージョン (`X.Y.Z`)
- `build_code`: 一意のビルド識別子

デフォルトの非リリース フォールバックは (`REL-LOCAL` ではなく) `BUILD-UNKNOWN` になりましたが、リリース バンプでは `scripts/bump_version.py` 経由で Unix スタイルのビルド コードが生成されます。

- `REL-U<unix_ms>`

## Web バージョン (Vercel)

動的多言語サポート (自動検出付き 11 言語) と包括的な SEO メタデータを備えた、高度に最適化された応答性の高い Web アプリです。

### 主要な Web 機能

- **豊富なページ**: ホームページ、ダウンロード、チュートリアル、連絡先、問題と PR、ディスカッション トラッカー、ドキュメント Markdown ビューア、およびサポート/寄付の統合。
- **高度な SEO**: 自動挿入されたローカライズされた `<meta>` タグ、広範な JSON-LD 構造化データ (サイトリンク、ソフトウェア アプリケーションなど)、自動 `hreflang` 生成、`robots.txt`、および `sitemap.xml`。
- **セキュリティとパフォーマンス**: JavaScript の自動難読化 (極端なマングリング)、HTML/CSS の縮小 (`cd web && node build_minify.js` 経由)、および `escapeHTML` 経由のクリーンな `XSS` 防止。
- **GitHub API プロキシ**: サーバーレス Vercel エンドポイント (`/api/github`) プロキシ GitHub API リクエストは、パーソナル アクセス トークン (`GITHUB_PAT`) を使用してパブリック レート制限を完全にバイパスします。

### Vercel にデプロイします

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
> HTML、CSS、または JS に変更を加える場合は、コードを自動的に難読化し、アセットを圧縮するために、展開する前に必ず `cd web && node build_minify.js` を実行してください。

> セキュリティ上の注意: 運用環境では、常に Vercel プロジェクト環境変数に `PIXIV_CLIENT_SECRET` を設定してください。

## アプリケーションをダウンロード (最新リリース)

ベース URL:

`https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download`

ファイル:

- ポータブル GUI: `Pixiv OAuth GUi (Portable).exe`
- GUI: `Pixiv OAuth GUi Setup_v<version>.exe` のセットアップ
- ポータブル CLI: `Pixiv OAuth CLi (Portable).exe`
- CLI: `Pixiv OAuth CLi Setup_v<version>.exe` のセットアップ

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

## Python インストール

```bash
cd app
python -m pip install -r requirements.txt
```

または、GitHub から直接インストールします。

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```

## 🧾 変更履歴

[変更履歴](CHANGELOG-JP.md) ファイル内の各バージョンの注目すべき変更点をすべて参照してください。
📦 [GitHub リリース ページ](https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases). でリリース ノートを直接表示することもできます。

### 最新: v1.0.5 (2026-04-03)

**✨ 追加**

- **インターネット対応 GUI スタートアップ** — GUI を起動する前のスマート接続プリフライト チェック。ライブ ランタイム接続モニタリングを備えています。
- **ネイティブ GUI ドキュメント モーダル** - 利用規約、プライバシー ポリシー、および変更ログが、Web リダイレクトを強制するのではなく、動的なポップアップに直接表示されるようになりました。
- **包括的なターミナル ローカリゼーション** — GitHub CLI トラッカーと法的ページは、サポートされている 11 言語すべてに正しく翻訳されるようになりました。

**✨ 変更および修正**

- **自動デジタル コード署名** - すべての実行可能ファイルは、Windows SmartScreen を抑制するために自己署名 ID をネイティブにバンドルします。
- **インストーラー プロパティのバグ** - セットアップ実行可能ファイルは、デフォルトのゼロではなく、`1.0.5.0` ファイル バージョンを Windows PE ヘッダーに厳密にブロードキャストします。
- **再設計された CLI の美しさ** — 洗練された左揃えの端末ディスプレイのために UI ボックスの境界線が排除されました。

**🔜 次回のアップデートで登場予定**

- モバイル Web サポート — Web アプリはモバイル ブラウザー向けに完全に応答性の高いレイアウトを取得します。

## ライセンス

MIT License。 `LICENSE`を参照してください。
