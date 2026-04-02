# =============================================================
#  Pixiv OAuth Token CLI - Quick Installer (PowerShell)
#  Supports: PowerShell 5.1+, PowerShell 7+
#  Usage:
#    irm https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/install.ps1 | iex
#    $env:PIXIV_LANG="jp"; irm https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/install.ps1 | iex
# =============================================================
#  Supported lang values: en, jp, kr, zh, id, de, fr, es, ru, pt, pl
# =============================================================

$ErrorActionPreference = "Stop"

$RAW_BASE  = "https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master"
$FILE_URL  = "$RAW_BASE/app/pixiv_login.py"
$OUT_FILE  = "pixiv_login.py"

# ---- Language detection ----
# Priority: $env:PIXIV_LANG > OS UI culture > English
$SUPPORTED_LANGS = @("en","jp","kr","zh","id","de","fr","es","ru","pt","pl")
$LANG_MAP = @{
  "ja" = "jp"; "ja-jp" = "jp"
  "ko" = "kr"; "ko-kr" = "kr"
  "zh" = "zh"; "zh-cn" = "zh"; "zh-tw" = "zh"; "zh-sg" = "zh"
  "id" = "id"; "in" = "id"
  "de" = "de"; "de-de" = "de"
  "fr" = "fr"; "fr-fr" = "fr"
  "es" = "es"; "es-es" = "es"
  "ru" = "ru"; "ru-ru" = "ru"
  "pt" = "pt"; "pt-br" = "pt"; "pt-pt" = "pt"
  "pl" = "pl"; "pl-pl" = "pl"
  "en" = "en"
}

$RESOLVED_LANG = "en"
if ($env:PIXIV_LANG -and $SUPPORTED_LANGS -contains $env:PIXIV_LANG.ToLower().Trim()) {
    $RESOLVED_LANG = $env:PIXIV_LANG.ToLower().Trim()
} else {
    try {
        $uiCulture = (Get-Culture).Name.ToLower()
        $baseCulture = $uiCulture.Split('-')[0]
        if ($LANG_MAP.ContainsKey($uiCulture)) {
            $RESOLVED_LANG = $LANG_MAP[$uiCulture]
        } elseif ($LANG_MAP.ContainsKey($baseCulture)) {
            $RESOLVED_LANG = $LANG_MAP[$baseCulture]
        }
    } catch { $RESOLVED_LANG = "en" }
}

# ---- Localized messages ----
$MSGS = @{
  "en" = @{
    "banner_title" = 'Pixiv OAuth Token CLI - Installer'
    "banner_by" = 'by Fatony Ahmad Fauzi'
    "lang_label" = 'Language'
    "check_python" = 'Checking Python installation...'
    "found_python" = 'Found'
    "py_need" = 'Python not found or version < 3.11.'
    "py_auto" = 'Attempting to install Python via winget...'
    "py_ok" = 'Python installed. Reloading environment variables...'
    "py_fail" = 'Auto-install failed. Please install Python 3.11+ manually from https://www.python.org/downloads/'
    "downloading" = 'Downloading pixiv_login.py from GitHub...'
    "downloaded" = 'Downloaded:'
    "dl_fail" = 'Download failed:'
    "dl_fail2" = 'Check your internet connection or download manually:'
    "deps" = 'Installing dependencies (requests)...'
    "deps_ok" = 'requests installed'
    "deps_fail" = 'pip install failed. Try manually: pip install requests'
    "complete" = 'Installation complete!'
    "run_with" = 'Run with:'
    "lang_detected" = 'Language detected:'
    "diff_lang" = 'To use a different language:'
    "save_perm" = 'To save permanently:'
  }
  "jp" = @{
    "banner_title" = 'Pixiv OAuth Token CLI - インストーラー'
    "banner_by" = '開発者: Fatony Ahmad Fauzi'
    "lang_label" = '言語'
    "check_python" = 'Pythonのインストールを確認中...'
    "found_python" = '確認済み:'
    "py_need" = 'Pythonが見つからないか、バージョンが3.11未満です。'
    "py_auto" = 'wingetでPythonを自動インストール中...'
    "py_ok" = 'Pythonをインストールしました。環境変数を再読み込み中...'
    "py_fail" = '自動インストールに失敗しました。https://www.python.org/downloads/ から手動でインストールしてください。'
    "downloading" = 'GitHubからpixiv_login.pyをダウンロード中...'
    "downloaded" = 'ダウンロード完了:'
    "dl_fail" = 'ダウンロード失敗:'
    "dl_fail2" = 'インターネット接続を確認するか、手動でダウンロードしてください:'
    "deps" = '依存関係をインストール中 (requests)...'
    "deps_ok" = 'requests をインストールしました'
    "deps_fail" = 'pip install に失敗しました。手動で: pip install requests'
    "complete" = 'インストール完了！'
    "run_with" = '実行コマンド:'
    "lang_detected" = '検出された言語:'
    "diff_lang" = '別の言語を使用するには:'
    "save_perm" = '永続的に設定するには:'
  }
  "kr" = @{
    "banner_title" = 'Pixiv OAuth Token CLI - 설치 프로그램'
    "banner_by" = '개발자: Fatony Ahmad Fauzi'
    "lang_label" = '언어'
    "check_python" = 'Python 설치 확인 중...'
    "found_python" = '확인됨:'
    "py_need" = 'Python이 없거나 버전이 3.11 미만입니다.'
    "py_auto" = 'winget으로 Python 자동 설치 중...'
    "py_ok" = 'Python이 설치되었습니다. 환경 변수 다시 로드 중...'
    "py_fail" = '자동 설치 실패. https://www.python.org/downloads/ 에서 수동으로 설치하세요.'
    "downloading" = 'GitHub에서 pixiv_login.py 다운로드 중...'
    "downloaded" = '다운로드 완료:'
    "dl_fail" = '다운로드 실패:'
    "dl_fail2" = '인터넷 연결을 확인하거나 수동으로 다운로드하세요:'
    "deps" = '종속성 설치 중 (requests)...'
    "deps_ok" = 'requests 설치 완료'
    "deps_fail" = 'pip install 실패. 수동으로 시도하세요: pip install requests'
    "complete" = '설치 완료!'
    "run_with" = '실행 방법:'
    "lang_detected" = '감지된 언어:'
    "diff_lang" = '다른 언어를 사용하려면:'
    "save_perm" = '영구적으로 저장하려면:'
  }
  "zh" = @{
    "banner_title" = 'Pixiv OAuth Token CLI - 安装程序'
    "banner_by" = '开发者: Fatony Ahmad Fauzi'
    "lang_label" = '语言'
    "check_python" = '正在检查 Python 安装...'
    "found_python" = '已找到:'
    "py_need" = '未找到 Python 或版本低于 3.11。'
    "py_auto" = '正在通过 winget 自动安装 Python...'
    "py_ok" = 'Python 已安装。正在重新加载环境变量...'
    "py_fail" = '自动安装失败。请从 https://www.python.org/downloads/ 手动安装 Python 3.11+。'
    "downloading" = '正在从 GitHub 下载 pixiv_login.py...'
    "downloaded" = '已下载:'
    "dl_fail" = '下载失败:'
    "dl_fail2" = '请检查网络连接或手动下载:'
    "deps" = '正在安装依赖 (requests)...'
    "deps_ok" = 'requests 已安装'
    "deps_fail" = 'pip install 失败。请手动尝试: pip install requests'
    "complete" = '安装完成！'
    "run_with" = '运行方法:'
    "lang_detected" = '检测到的语言:'
    "diff_lang" = '使用其他语言:'
    "save_perm" = '永久保存:'
  }
  "id" = @{
    "banner_title" = 'Pixiv OAuth Token CLI - Penginstal'
    "banner_by" = 'Pengembang: Fatony Ahmad Fauzi'
    "lang_label" = 'Bahasa'
    "check_python" = 'Memeriksa instalasi Python...'
    "found_python" = 'Ditemukan:'
    "py_need" = 'Python tidak ditemukan atau versi < 3.11.'
    "py_auto" = 'Mencoba menginstal Python via winget...'
    "py_ok" = 'Python berhasil diinstal. Memuat ulang variabel lingkungan...'
    "py_fail" = 'Instalasi otomatis gagal. Instal Python 3.11+ secara manual dari https://www.python.org/downloads/'
    "downloading" = 'Mengunduh pixiv_login.py dari GitHub...'
    "downloaded" = 'Berhasil diunduh:'
    "dl_fail" = 'Unduhan gagal:'
    "dl_fail2" = 'Periksa koneksi internet atau unduh secara manual:'
    "deps" = 'Menginstal dependensi (requests)...'
    "deps_ok" = 'requests berhasil diinstal'
    "deps_fail" = 'pip install gagal. Coba manual: pip install requests'
    "complete" = 'Instalasi selesai!'
    "run_with" = 'Jalankan dengan:'
    "lang_detected" = 'Bahasa terdeteksi:'
    "diff_lang" = 'Untuk menggunakan bahasa lain:'
    "save_perm" = 'Untuk menyimpan secara permanen:'
  }
  "de" = @{
    "banner_title" = 'Pixiv OAuth Token CLI - Installer'
    "banner_by" = 'Entwickler: Fatony Ahmad Fauzi'
    "lang_label" = 'Sprache'
    "check_python" = 'Python-Installation wird geprüft...'
    "found_python" = 'Gefunden:'
    "py_need" = 'Python nicht gefunden oder Version < 3.11.'
    "py_auto" = 'Python wird über winget installiert...'
    "py_ok" = 'Python installiert. Umgebungsvariablen werden neu geladen...'
    "py_fail" = 'Automatische Installation fehlgeschlagen. Bitte Python 3.11+ manuell von https://www.python.org/downloads/ installieren.'
    "downloading" = 'pixiv_login.py wird von GitHub heruntergeladen...'
    "downloaded" = 'Heruntergeladen:'
    "dl_fail" = 'Download fehlgeschlagen:'
    "dl_fail2" = 'Überprüfe Internetverbindung oder lade manuell herunter:'
    "deps" = 'Abhängigkeiten werden installiert (requests)...'
    "deps_ok" = 'requests installiert'
    "deps_fail" = 'pip install fehlgeschlagen. Manuell: pip install requests'
    "complete" = 'Installation abgeschlossen!'
    "run_with" = 'Starten mit:'
    "lang_detected" = 'Erkannte Sprache:'
    "diff_lang" = 'Um eine andere Sprache zu nutzen:'
    "save_perm" = 'Dauerhaft speichern:'
  }
  "fr" = @{
    "banner_title" = 'Pixiv OAuth Token CLI - Installateur'
    "banner_by" = 'Développeur: Fatony Ahmad Fauzi'
    "lang_label" = 'Langue'
    "check_python" = 'Vérification de l''installation de Python...'
    "found_python" = 'Trouvé:'
    "py_need" = 'Python introuvable ou version < 3.11.'
    "py_auto" = 'Installation automatique de Python via winget...'
    "py_ok" = 'Python installé. Rechargement des variables d''environnement...'
    "py_fail" = 'Installation automatique échouée. Installez Python 3.11+ depuis https://www.python.org/downloads/'
    "downloading" = 'Téléchargement de pixiv_login.py depuis GitHub...'
    "downloaded" = 'Téléchargé:'
    "dl_fail" = 'Échec du téléchargement:'
    "dl_fail2" = 'Vérifiez la connexion Internet ou téléchargez manuellement:'
    "deps" = 'Installation des dépendances (requests)...'
    "deps_ok" = 'requests installé'
    "deps_fail" = 'Échec de pip install. Essayez: pip install requests'
    "complete" = 'Installation terminée!'
    "run_with" = 'Lancer avec:'
    "lang_detected" = 'Langue détectée:'
    "diff_lang" = 'Pour utiliser une autre langue:'
    "save_perm" = 'Pour sauvegarder définitivement:'
  }
  "es" = @{
    "banner_title" = 'Pixiv OAuth Token CLI - Instalador'
    "banner_by" = 'Desarrollador: Fatony Ahmad Fauzi'
    "lang_label" = 'Idioma'
    "check_python" = 'Verificando instalación de Python...'
    "found_python" = 'Encontrado:'
    "py_need" = 'Python no encontrado o versión < 3.11.'
    "py_auto" = 'Intentando instalar Python via winget...'
    "py_ok" = 'Python instalado. Recargando variables de entorno...'
    "py_fail" = 'Instalación automática fallida. Instala Python 3.11+ desde https://www.python.org/downloads/'
    "downloading" = 'Descargando pixiv_login.py desde GitHub...'
    "downloaded" = 'Descargado:'
    "dl_fail" = 'Descarga fallida:'
    "dl_fail2" = 'Verifica la conexión a internet o descarga manualmente:'
    "deps" = 'Instalando dependencias (requests)...'
    "deps_ok" = 'requests instalado'
    "deps_fail" = 'pip install fallido. Intenta: pip install requests'
    "complete" = '¡Instalación completa!'
    "run_with" = 'Ejecutar con:'
    "lang_detected" = 'Idioma detectado:'
    "diff_lang" = 'Para usar un idioma diferente:'
    "save_perm" = 'Para guardar permanentemente:'
  }
  "ru" = @{
    "banner_title" = 'Pixiv OAuth Token CLI - Установщик'
    "banner_by" = 'Разработчик: Fatony Ahmad Fauzi'
    "lang_label" = 'Язык'
    "check_python" = 'Проверка установки Python...'
    "found_python" = 'Найдено:'
    "py_need" = 'Python не найден или версия < 3.11.'
    "py_auto" = 'Автоматическая установка Python через winget...'
    "py_ok" = 'Python установлен. Перезагрузка переменных среды...'
    "py_fail" = 'Автоматическая установка не удалась. Установите Python 3.11+ с https://www.python.org/downloads/'
    "downloading" = 'Загрузка pixiv_login.py с GitHub...'
    "downloaded" = 'Загружено:'
    "dl_fail" = 'Ошибка загрузки:'
    "dl_fail2" = 'Проверьте подключение к интернету или загрузите вручную:'
    "deps" = 'Установка зависимостей (requests)...'
    "deps_ok" = 'requests установлено'
    "deps_fail" = 'pip install не удалось. Попробуйте: pip install requests'
    "complete" = 'Установка завершена!'
    "run_with" = 'Запустить с:'
    "lang_detected" = 'Определённый язык:'
    "diff_lang" = 'Для другого языка:'
    "save_perm" = 'Для постоянного сохранения:'
  }
  "pt" = @{
    "banner_title" = 'Pixiv OAuth Token CLI - Instalador'
    "banner_by" = 'Desenvolvedor: Fatony Ahmad Fauzi'
    "lang_label" = 'Idioma'
    "check_python" = 'Verificando instalação do Python...'
    "found_python" = 'Encontrado:'
    "py_need" = 'Python não encontrado ou versão < 3.11.'
    "py_auto" = 'Tentando instalar Python via winget...'
    "py_ok" = 'Python instalado. Recarregando variáveis de ambiente...'
    "py_fail" = 'Instalação automática falhou. Instale o Python 3.11+ em https://www.python.org/downloads/'
    "downloading" = 'Baixando pixiv_login.py do GitHub...'
    "downloaded" = 'Baixado:'
    "dl_fail" = 'Falha no download:'
    "dl_fail2" = 'Verifique a conexão com a internet ou baixe manualmente:'
    "deps" = 'Instalando dependências (requests)...'
    "deps_ok" = 'requests instalado'
    "deps_fail" = 'pip install falhou. Tente: pip install requests'
    "complete" = 'Instalação concluída!'
    "run_with" = 'Executar com:'
    "lang_detected" = 'Idioma detectado:'
    "diff_lang" = 'Para usar outro idioma:'
    "save_perm" = 'Para salvar permanentemente:'
  }
  "pl" = @{
    "banner_title" = 'Pixiv OAuth Token CLI - Instalator'
    "banner_by" = 'Deweloper: Fatony Ahmad Fauzi'
    "lang_label" = 'Język'
    "check_python" = 'Sprawdzanie instalacji Python...'
    "found_python" = 'Znaleziono:'
    "py_need" = 'Python nie znaleziony lub wersja < 3.11.'
    "py_auto" = 'Automatyczna instalacja Python przez winget...'
    "py_ok" = 'Python zainstalowany. Przeładowanie zmiennych środowiskowych...'
    "py_fail" = 'Automatyczna instalacja nie powiodła się. Zainstaluj Python 3.11+ z https://www.python.org/downloads/'
    "downloading" = 'Pobieranie pixiv_login.py z GitHub...'
    "downloaded" = 'Pobrano:'
    "dl_fail" = 'Pobieranie nie powiodło się:'
    "dl_fail2" = 'Sprawdź połączenie internetowe lub pobierz ręcznie:'
    "deps" = 'Instalowanie zależności (requests)...'
    "deps_ok" = 'requests zainstalowano'
    "deps_fail" = 'pip install nie powiodło się. Spróbuj: pip install requests'
    "complete" = 'Instalacja zakończona!'
    "run_with" = 'Uruchom za pomocą:'
    "lang_detected" = 'Wykryty język:'
    "diff_lang" = 'Aby użyć innego języka:'
    "save_perm" = 'Aby zapisać na stałe:'
  }
}

function M([string]$key) {
    $lang = $MSGS[$RESOLVED_LANG]
    if ($lang -and $lang.ContainsKey($key)) { return $lang[$key] }
    return $MSGS["en"][$key]
}

function Write-Banner {
    Write-Host ""
    Write-Host "  +==========================================+" -ForegroundColor Cyan
    Write-Host "  |  $(M 'banner_title')" -ForegroundColor Cyan
    Write-Host "  |  $(M 'banner_by')" -ForegroundColor Cyan
    Write-Host "  +==========================================+" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step([string]$msg) { Write-Host "  [*] $msg" -ForegroundColor Yellow }
function Write-Ok([string]$msg)   { Write-Host "  [+] $msg" -ForegroundColor Green }
function Write-Err([string]$msg)  { Write-Host "  [!] $msg" -ForegroundColor Red }

Write-Banner
Write-Host "  [i] $(M 'lang_label'): $RESOLVED_LANG" -ForegroundColor DarkCyan

# --- 1. Check Python ---
Write-Step (M "check_python")
$needsPython = $false
try {
    $pyVer = python --version 2>&1
    if ($pyVer -match "Python (\d+)\.(\d+)") {
        $major = [int]$Matches[1]; $minor = [int]$Matches[2]
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 11)) {
            Write-Err (M "py_need"); $needsPython = $true
        } else { Write-Ok "$(M 'found_python') $pyVer" }
    } else { throw "Cannot parse version" }
} catch { $needsPython = $true }

if ($needsPython) {
    Write-Step (M "py_need")
    Write-Step (M "py_auto")
    try {
        winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
        if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne 2316632065) { throw "winget returned $LASTEXITCODE" }
        Write-Ok (M "py_ok")
        Start-Sleep -Seconds 2
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        $pyVerTest = python --version 2>&1
        Write-Ok "$(M 'found_python') $pyVerTest"
    } catch {
        Write-Err (M "py_fail"); exit 1
    }
}

# --- 2. Download pixiv_login.py ---
Write-Step (M "downloading")
try {
    Invoke-WebRequest -Uri $FILE_URL -OutFile $OUT_FILE -UseBasicParsing
    Write-Ok "$(M 'downloaded') $OUT_FILE"
} catch {
    Write-Err "$(M 'dl_fail') $_"
    Write-Err (M "dl_fail2")
    Write-Err "  $FILE_URL"
    exit 1
}

# --- 3. Install dependencies ---
Write-Step (M "deps")
try {
    python -m pip install requests --quiet --disable-pip-version-check
    Write-Ok (M "deps_ok")
} catch { Write-Err (M "deps_fail") }

# --- 4. Done ---
Write-Host ""
Write-Host "  +==========================================+" -ForegroundColor Green
Write-Host "  |  $(M 'complete')" -ForegroundColor Green
Write-Host "  +==========================================+" -ForegroundColor Green
Write-Host ""
Write-Host "  $(M 'run_with')" -ForegroundColor White
if ($RESOLVED_LANG -ne "en") {
    Write-Host "    python pixiv_login.py --lang $RESOLVED_LANG" -ForegroundColor Cyan
} else {
    Write-Host "    python pixiv_login.py" -ForegroundColor Cyan
}
Write-Host ""
Write-Host "  [i] $(M 'lang_detected') $RESOLVED_LANG" -ForegroundColor DarkGray
Write-Host "      $(M 'diff_lang') python pixiv_login.py --lang jp" -ForegroundColor DarkGray
Write-Host "      $(M 'save_perm')  python pixiv_login.py config set-lang jp" -ForegroundColor DarkGray
Write-Host ""
