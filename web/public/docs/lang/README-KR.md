# Pixiv OAuth Token


> 🌐 다른 언어로도 사용 가능: [English](../../README.md) | [Polski](README-PL.md) | [中文](README-ZH.md) | [日本語](README-JP.md) | [Deutsch](README-DE.md) | [Français](README-FR.md) | [Español](README-ES.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [Bahasa Indonesia](README-ID.md)

---
세 가지 모드로 Pixiv OAuth 토큰을 생성하는 툴킷:

- CLI(`app/pixiv_login.py`)
- GUI(`app/pixiv_login_gui.py`)
- 웹 앱(`web/public/` + 서버리스 API)

## 요구 사항

- 파이썬 3.11+
- Windows(`.bat` 빌드 스크립트 및 Inno 설치 프로그램에 필요)
- `app/requirements.txt`의 Python 종속성

## 소스에서 실행

```bash
cd app
python -m pip install -r requirements.txt
python pixiv_login.py
```

GUI 실행:

```bash
cd app
python pixiv_login_gui.py
```

### GUI 기능

| 기능 | 설명 |
|---|---|
| **다국어** | 11개 언어 — 구성에서 자동 감지, 드롭다운을 통해 실시간으로 전환 가능 |
| **⚙ 디버그 콘솔** | 오른쪽 상단 헤더의 버튼; 실시간 및 현재 언어로 **모든** 이벤트(버튼 클릭, 언어 변경, HTTP 요청, PKCE 단계, 클립보드, 구성 저장, 경고)를 기록하는 어두운 터미널을 엽니다 |
| **토큰 교환** | pixiv:// URL 또는 원시 코드 붙여넣기 → 액세스 교환 + 새로 고침 토큰 |
| **새로고침 토큰** | 구성에서 저장된 새로 고침 토큰을 사용하여 원클릭 새로 고침 |
| **토큰 복사** | access_token/refresh_token을 클립보드에 즉시 복사 |
| **튜토리얼** | 앱에 내장된 단계별 이미지 가이드 |

## 짓다

### 모든 아티팩트 빌드(CLI + GUI + 설치 프로그램 + ZIP)

```bat
cd scripts
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
cd scripts
build_all_pro.bat patch noinst nosign
```

### 메인 출력

- 휴대용 CLI: `dist_portable\Pixiv OAuth CLi (Portable).exe`
- 휴대용 GUI: `dist_gui\Pixiv OAuth GUi (Portable).exe`
- 통합 설치 프로그램: `dist_installer\PixivLoginSetup_v<version>.exe`(CLI + GUI 모두 설치)
- 설치 프로그램 CLI: `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe`(통합 설치 프로그램 사본)
- 설치 프로그램 GUI: `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe`(통합 설치 프로그램 사본)
- 출시 우편번호: `PixivOAuthRelease_v<version>.zip`
- 자동 동기화 폴더: `downloads/` (최신 휴대용/설정 + 릴리스 ZIP)

## 서명

`scripts/sign_auto.bat` 편집:

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

PFX 파일이 없으면 서명을 건너뜁니다.

## 버전 관리

애플리케이션 버전/빌드 ID는 `version.json`에 저장됩니다.

- `version`: 의미 버전(`X.Y.Z`)
- `build_code`: 고유한 빌드 식별자

기본 비릴리스 폴백은 이제 `BUILD-UNKNOWN`(`REL-LOCAL` 대신)이며, 릴리스 범프는 `scripts/bump_version.py`를 통해 Unix 스타일 빌드 코드를 생성합니다.

- `REL-U<unix_ms>`

## 웹버전(Vercel)

동적 다국어 지원(자동 감지 기능이 있는 11개 언어) 및 포괄적인 SEO 메타데이터를 특징으로 하는 고도로 최적화된 반응형 웹 앱입니다.

### 주요 웹 기능
- **광범위한 페이지**: 홈페이지, 다운로드, 자습서, 연락처, 문제 및 PR, 토론 추적기, 문서 Markdown 뷰어 및 지원/기부 통합.
- **고급 SEO**: 자동 삽입된 현지화된 `<meta>` 태그, 광범위한 JSON-LD 구조 데이터(사이트링크, 소프트웨어 애플리케이션 등), 자동화된 `hreflang` 생성, `robots.txt` 및 `sitemap.xml`.
- **보안 및 성능**: 자동 JavaScript 난독화(극도의 맹글링), HTML/CSS 축소(`cd web && node build_minify.js`를 통해) 및 `escapeHTML`를 통한 깔끔한 `XSS` 방지.
- **GitHub API 프록시**: 서버리스 Vercel 엔드포인트(`/api/github`) 프록시 GitHub API은 개인 액세스 토큰(`GITHUB_PAT`)을 사용하여 공개 속도 제한을 완전히 우회하도록 요청합니다.

### Vercel에 배포

1. 저장소를 GitHub에 푸시합니다.
2. Vercel → **새로 추가...** → **프로젝트** → 이 저장소를 가져옵니다.
3. Vercel에서 환경 변수를 설정합니다.
- `PIXIV_CLIENT_SECRET`: Pixiv OAuth 클라이언트 비밀번호입니다.
- `GITHUB_PAT`: 선택 사항이지만 적극 권장됩니다(repo 문제 및 릴리스에 대한 속도 제한을 피하기 위한 GitHub 개인 액세스 토큰).
4. `vercel.json`은(는) 이미 다음을 구성했습니다.
- URL 정리(`.html` 제거)
- `public/`의 정적 호스팅
- `/api/*`의 서버리스 APIs
- 내장된 사용자 정의 404 페이지 라우팅
- Edge Cache 헤더를 통한 먼 미래의 캐싱.
5. 배포.

> [!중요]
> HTML, CSS 또는 JS를 변경하는 경우 배포하기 전에 `cd web && node build_minify.js`을 실행하여 자동으로 코드를 난독화하고 자산을 압축해야 합니다.

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
cd app
python -m pip install -r requirements.txt
```

또는 GitHub에서 직접 설치하십시오.

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```

## 🧾 변경 내역

[변경 내역](CHANGELOG-KR.md) 파일에서 각 버전의 주요 변경 사항을 모두 확인하세요.
📦 [GitHub 릴리스 페이지](https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases).에서 직접 릴리스 노트를 볼 수도 있습니다.

## 라이선스

MIT License. `LICENSE`을 참조하세요.
