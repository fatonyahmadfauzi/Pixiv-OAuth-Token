# Pixiv OAuth Token


> 🌐 다른 언어로도 사용 가능: [English](../../README.md) | [Polski](README-PL.md) | [中文](README-ZH.md) | [日本語](README-JP.md) | [Deutsch](README-DE.md) | [Français](README-FR.md) | [Español](README-ES.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [Bahasa Indonesia](README-ID.md)

---
세 가지 모드로 Pixiv OAuth 토큰을 생성하는 툴킷:

- CLI(`pixiv_login.py`)
- GUI(`pixiv_login_gui.py`)
- 웹 앱(`public/` + 서버리스 API)

## 요구 사항

- 파이썬 3.11+
- Windows(`.bat` 빌드 스크립트 및 Inno 설치 프로그램에 필요)
- `requirements.txt`의 Python 종속성

## 소스에서 실행

```bash
python -m pip install -r requirements.txt
python pixiv_login.py
```

GUI 실행:

```bash
python pixiv_login_gui.py
```

## 짓다

### 모든 아티팩트 빌드(CLI + GUI + 설치 프로그램 + ZIP)

```bat
build_all_pro.bat patch
```

버전 인수:

- `patch`
- `minor`
- `major`
- `none`

선택적 플래그:

- `noinst`(설치 프로그램 건너뛰기)
- `nosign`(서명 건너뛰기)
- `nozip`(우편번호 건너뛰기)
- `nogui`(GUI 건너뛰기)
- `nopause`(마지막에 일시정지 없음)

예:

```bat
build_all_pro.bat patch noinst nosign
```

### 메인 출력

- 휴대용 CLI: `dist_portable\Pixiv OAuth CLi (Portable).exe`
- 휴대용 GUI: `dist_gui\Pixiv OAuth GUi (Portable).exe`
- 설치 프로그램 CLI: `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe`
- 설치 프로그램 GUI: `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe`
- 출시 우편번호: `PixivOAuthRelease_v<version>.zip`
- 자동 동기화 폴더: `downloads/` (최신 휴대용/설정 + 릴리스 ZIP)

## 서명

`sign_auto.bat` 편집:

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

PFX 파일이 없으면 서명을 건너뜁니다.

## 버전 관리

애플리케이션 버전은 `version.json`에 저장됩니다.

## 웹버전(Vercel)

동적 다국어 지원(자동 감지 기능이 있는 11개 언어) 및 포괄적인 SEO 메타데이터를 특징으로 하는 고도로 최적화된 반응형 웹 앱입니다.

### 주요 웹 기능
- **광범위한 페이지**: 홈페이지, 다운로드, 자습서, 연락처, 문제 및 PR, 토론 추적기, 문서 마크다운 뷰어 및 지원/기부 통합.
- **고급 SEO**: 자동 삽입된 현지화된 `<meta>` 태그, 광범위한 JSON-LD 구조 데이터(사이트링크, 소프트웨어 애플리케이션 등), 자동화된 `hreflang` 생성, `robots.txt` 및 `sitemap.xml`.
- **보안 및 성능**: 자동 JavaScript 난독화(극도의 맹글링), HTML/CSS 축소(`node build_minify.js`를 통해) 및 `escapeHTML`를 통한 깔끔한 `XSS` 방지.
- **GitHub API 프록시**: 서버리스 Vercel 엔드포인트(`/api/github`)는 개인 액세스 토큰(`GITHUB_PAT`)을 사용하여 GitHub API 요청을 프록시하여 공개 속도 제한을 완전히 우회합니다.

### Vercel에 배포

1. 저장소를 GitHub에 푸시합니다.
2. Vercel → **새로 추가...** → **프로젝트** → 이 저장소를 가져옵니다.
3. Vercel에서 환경 변수를 설정합니다.
- `PIXIV_CLIENT_SECRET`: Pixiv OAuth 클라이언트 비밀번호입니다.
- `GITHUB_PAT`: 선택 사항이지만 적극 권장됩니다(리포지토리 문제 및 릴리스에 대한 속도 제한을 피하기 위한 GitHub 개인 액세스 토큰).
4. `vercel.json`은(는) 이미 다음을 구성했습니다.
- URL 정리(`.html` 제거)
- `public/`의 정적 호스팅
- `/api/*`의 서버리스 API
- 내장된 사용자 정의 404 페이지 라우팅
- Edge Cache 헤더를 통한 먼 미래의 캐싱.
5. 배포.

> [!중요]
> HTML, CSS 또는 JS를 변경하는 경우 배포하기 전에 `node build_minify.js`을 실행하여 자동으로 코드를 난독화하고 자산을 압축해야 합니다.

> 보안 참고 사항: 프로덕션의 경우 항상 Vercel 프로젝트 환경 변수에 `PIXIV_CLIENT_SECRET`을 설정하세요.

## 애플리케이션 다운로드(최신 릴리스)

기본 URL:

`https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download`

파일:

- 휴대용 GUI: `Pixiv OAuth GUi (Portable).exe`
- 설정 GUI: `Pixiv OAuth GUi Setup_v<version>.exe`
- 휴대용 CLI: `Pixiv OAuth CLi (Portable).exe`
- CLI 설정: `Pixiv OAuth CLi Setup_v<version>.exe`

### PowerShell(최신 릴리스 자산 자동 감지)

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

### PowerShell(`downloads/`의 고정 URL)

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

**PowerShell**(CMD 아님)에서 실행하세요.

다음만 실행하는 경우:

```powershell
$guiPortable = "..."
```

아무것도 나타나지 않습니다. 예상되는 현상입니다. 변수에만 값을 저장합니다. `Invoke-WebRequest`을 실행하면 다운로드가 시작됩니다.

다운로드가 완료되고 PowerShell은 오류 없이 `PS C:\...>`으로 돌아갑니다.

```powershell
Get-ChildItem "Pixiv OAuth GUi (Portable).exe"
Start-Process ".\Pixiv OAuth GUi (Portable).exe"
```

설치 프로그램 빌드의 경우:

```powershell
Invoke-WebRequest $guiSetup -OutFile "Pixiv OAuth GUi Setup.exe"
Start-Process ".\Pixiv OAuth GUi Setup.exe"
```

TLS 정책이 다운로드를 차단하는 경우:

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

### CMD(최신 릴리스 자산 자동 감지)

```cmd
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi Setup.exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi Setup.exe"
```

## 파이썬 설치

```bash
python -m pip install -r requirements.txt
```

또는 GitHub에서 직접 설치:

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```

## 라이센스

MIT License. `LICENSE`을 참조하세요.
