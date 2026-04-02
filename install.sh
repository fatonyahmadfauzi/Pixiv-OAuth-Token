#!/usr/bin/env bash
# =============================================================
#  Pixiv OAuth Token CLI - Quick Installer (Bash)
#  Supports: Bash, Zsh, WSL, Git Bash, macOS Terminal
#  Usage:
#    bash <(curl -sL https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/install.sh)
#    bash <(curl -sL https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/install.sh) --lang jp
#    PIXIV_LANG=jp bash <(curl -sL https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/install.sh)
# =============================================================
#  Supported lang values: en, jp, kr, zh, id, de, fr, es, ru, pt, pl
# =============================================================

set -e

RAW_BASE="https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master"
FILE_URL="$RAW_BASE/app/pixiv_login.py"
OUT_FILE="pixiv_login.py"

# ---- Language detection ----
RESOLVED_LANG="en"
SUPPORTED_LANGS="en jp kr zh id de fr es ru pt pl"

map_locale() {
  local loc
  loc=$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed 's/_/-/g' | cut -d. -f1)
  case "$loc" in
    ja|ja-jp)            printf 'jp' ;;
    ko|ko-kr)            printf 'kr' ;;
    zh|zh-cn|zh-tw|zh-sg|zh-hk) printf 'zh' ;;
    id|in|id-id)         printf 'id' ;;
    de|de-de)            printf 'de' ;;
    fr|fr-fr)            printf 'fr' ;;
    es|es-es)            printf 'es' ;;
    ru|ru-ru)            printf 'ru' ;;
    pt|pt-br|pt-pt)      printf 'pt' ;;
    pl|pl-pl)            printf 'pl' ;;
    en*)                 printf 'en' ;;
    *)                   printf ''  ;;
  esac
}

is_lang() { printf '%s' "$SUPPORTED_LANGS" | grep -qw "$1"; }

# 1. Parse --lang arg
while [ $# -gt 0 ]; do
  case "$1" in
    --lang)   shift; is_lang "$1" && RESOLVED_LANG="$1"; shift ;;
    --lang=*) val="${1#--lang=}"; is_lang "$val" && RESOLVED_LANG="$val"; shift ;;
    *)        shift ;;
  esac
done

# 2. $PIXIV_LANG env var
if [ "$RESOLVED_LANG" = "en" ] && [ -n "$PIXIV_LANG" ] && is_lang "$PIXIV_LANG"; then
  RESOLVED_LANG="$PIXIV_LANG"
fi

# 3. OS locale
if [ "$RESOLVED_LANG" = "en" ]; then
  for lv in "$LC_ALL" "$LANG" "$LANGUAGE"; do
    if [ -n "$lv" ]; then
      d=$(map_locale "$lv")
      [ -n "$d" ] && RESOLVED_LANG="$d" && break
    fi
  done
fi

# ---- Colors ----
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BOLD='\033[1m'
DIM='\033[2m'
RESET='\033[0m'

# ---- Localized messages ----
msg() {
  local key="$1"
  case "$RESOLVED_LANG" in
    en)
      case "$key" in
        banner_title) printf '%s' 'Pixiv OAuth Token CLI - Installer' ;;
        banner_by) printf '%s' 'by Fatony Ahmad Fauzi' ;;
        lang_label) printf '%s' 'Language' ;;
        check_python) printf '%s' 'Checking Python installation...' ;;
        found_python) printf '%s' 'Found' ;;
        py_need) printf '%s' 'Python not found or version < 3.11.' ;;
        py_auto) printf '%s' 'Attempting to install Python via winget...' ;;
        py_ok) printf '%s' 'Python installed. Reloading environment variables...' ;;
        py_fail) printf '%s' 'Auto-install failed. Please install Python 3.11+ manually from https://www.python.org/downloads/' ;;
        downloading) printf '%s' 'Downloading pixiv_login.py from GitHub...' ;;
        downloaded) printf '%s' 'Downloaded:' ;;
        dl_fail) printf '%s' 'Download failed:' ;;
        dl_fail2) printf '%s' 'Check your internet connection or download manually:' ;;
        deps) printf '%s' 'Installing dependencies (requests)...' ;;
        deps_ok) printf '%s' 'requests installed' ;;
        deps_fail) printf '%s' 'pip install failed. Try manually: pip install requests' ;;
        complete) printf '%s' 'Installation complete!' ;;
        run_with) printf '%s' 'Run with:' ;;
        lang_detected) printf '%s' 'Language detected:' ;;
        diff_lang) printf '%s' 'To use a different language:' ;;
        save_perm) printf '%s' 'To save permanently:' ;;
        *) printf '%s' "$(msg_en "$key")" ;;
      esac ;;
    jp)
      case "$key" in
        banner_title) printf '%s' 'Pixiv OAuth Token CLI - インストーラー' ;;
        banner_by) printf '%s' '開発者: Fatony Ahmad Fauzi' ;;
        lang_label) printf '%s' '言語' ;;
        check_python) printf '%s' 'Pythonのインストールを確認中...' ;;
        found_python) printf '%s' '確認済み:' ;;
        py_need) printf '%s' 'Pythonが見つからないか、バージョンが3.11未満です。' ;;
        py_auto) printf '%s' 'wingetでPythonを自動インストール中...' ;;
        py_ok) printf '%s' 'Pythonをインストールしました。環境変数を再読み込み中...' ;;
        py_fail) printf '%s' '自動インストールに失敗しました。https://www.python.org/downloads/ から手動でインストールしてください。' ;;
        downloading) printf '%s' 'GitHubからpixiv_login.pyをダウンロード中...' ;;
        downloaded) printf '%s' 'ダウンロード完了:' ;;
        dl_fail) printf '%s' 'ダウンロード失敗:' ;;
        dl_fail2) printf '%s' 'インターネット接続を確認するか、手動でダウンロードしてください:' ;;
        deps) printf '%s' '依存関係をインストール中 (requests)...' ;;
        deps_ok) printf '%s' 'requests をインストールしました' ;;
        deps_fail) printf '%s' 'pip install に失敗しました。手動で: pip install requests' ;;
        complete) printf '%s' 'インストール完了！' ;;
        run_with) printf '%s' '実行コマンド:' ;;
        lang_detected) printf '%s' '検出された言語:' ;;
        diff_lang) printf '%s' '別の言語を使用するには:' ;;
        save_perm) printf '%s' '永続的に設定するには:' ;;
        *) printf '%s' "$(msg_en "$key")" ;;
      esac ;;
    kr)
      case "$key" in
        banner_title) printf '%s' 'Pixiv OAuth Token CLI - 설치 프로그램' ;;
        banner_by) printf '%s' '개발자: Fatony Ahmad Fauzi' ;;
        lang_label) printf '%s' '언어' ;;
        check_python) printf '%s' 'Python 설치 확인 중...' ;;
        found_python) printf '%s' '확인됨:' ;;
        py_need) printf '%s' 'Python이 없거나 버전이 3.11 미만입니다.' ;;
        py_auto) printf '%s' 'winget으로 Python 자동 설치 중...' ;;
        py_ok) printf '%s' 'Python이 설치되었습니다. 환경 변수 다시 로드 중...' ;;
        py_fail) printf '%s' '자동 설치 실패. https://www.python.org/downloads/ 에서 수동으로 설치하세요.' ;;
        downloading) printf '%s' 'GitHub에서 pixiv_login.py 다운로드 중...' ;;
        downloaded) printf '%s' '다운로드 완료:' ;;
        dl_fail) printf '%s' '다운로드 실패:' ;;
        dl_fail2) printf '%s' '인터넷 연결을 확인하거나 수동으로 다운로드하세요:' ;;
        deps) printf '%s' '종속성 설치 중 (requests)...' ;;
        deps_ok) printf '%s' 'requests 설치 완료' ;;
        deps_fail) printf '%s' 'pip install 실패. 수동으로 시도하세요: pip install requests' ;;
        complete) printf '%s' '설치 완료!' ;;
        run_with) printf '%s' '실행 방법:' ;;
        lang_detected) printf '%s' '감지된 언어:' ;;
        diff_lang) printf '%s' '다른 언어를 사용하려면:' ;;
        save_perm) printf '%s' '영구적으로 저장하려면:' ;;
        *) printf '%s' "$(msg_en "$key")" ;;
      esac ;;
    zh)
      case "$key" in
        banner_title) printf '%s' 'Pixiv OAuth Token CLI - 安装程序' ;;
        banner_by) printf '%s' '开发者: Fatony Ahmad Fauzi' ;;
        lang_label) printf '%s' '语言' ;;
        check_python) printf '%s' '正在检查 Python 安装...' ;;
        found_python) printf '%s' '已找到:' ;;
        py_need) printf '%s' '未找到 Python 或版本低于 3.11。' ;;
        py_auto) printf '%s' '正在通过 winget 自动安装 Python...' ;;
        py_ok) printf '%s' 'Python 已安装。正在重新加载环境变量...' ;;
        py_fail) printf '%s' '自动安装失败。请从 https://www.python.org/downloads/ 手动安装 Python 3.11+。' ;;
        downloading) printf '%s' '正在从 GitHub 下载 pixiv_login.py...' ;;
        downloaded) printf '%s' '已下载:' ;;
        dl_fail) printf '%s' '下载失败:' ;;
        dl_fail2) printf '%s' '请检查网络连接或手动下载:' ;;
        deps) printf '%s' '正在安装依赖 (requests)...' ;;
        deps_ok) printf '%s' 'requests 已安装' ;;
        deps_fail) printf '%s' 'pip install 失败。请手动尝试: pip install requests' ;;
        complete) printf '%s' '安装完成！' ;;
        run_with) printf '%s' '运行方法:' ;;
        lang_detected) printf '%s' '检测到的语言:' ;;
        diff_lang) printf '%s' '使用其他语言:' ;;
        save_perm) printf '%s' '永久保存:' ;;
        *) printf '%s' "$(msg_en "$key")" ;;
      esac ;;
    id)
      case "$key" in
        banner_title) printf '%s' 'Pixiv OAuth Token CLI - Penginstal' ;;
        banner_by) printf '%s' 'Pengembang: Fatony Ahmad Fauzi' ;;
        lang_label) printf '%s' 'Bahasa' ;;
        check_python) printf '%s' 'Memeriksa instalasi Python...' ;;
        found_python) printf '%s' 'Ditemukan:' ;;
        py_need) printf '%s' 'Python tidak ditemukan atau versi < 3.11.' ;;
        py_auto) printf '%s' 'Mencoba menginstal Python via winget...' ;;
        py_ok) printf '%s' 'Python berhasil diinstal. Memuat ulang variabel lingkungan...' ;;
        py_fail) printf '%s' 'Instalasi otomatis gagal. Instal Python 3.11+ secara manual dari https://www.python.org/downloads/' ;;
        downloading) printf '%s' 'Mengunduh pixiv_login.py dari GitHub...' ;;
        downloaded) printf '%s' 'Berhasil diunduh:' ;;
        dl_fail) printf '%s' 'Unduhan gagal:' ;;
        dl_fail2) printf '%s' 'Periksa koneksi internet atau unduh secara manual:' ;;
        deps) printf '%s' 'Menginstal dependensi (requests)...' ;;
        deps_ok) printf '%s' 'requests berhasil diinstal' ;;
        deps_fail) printf '%s' 'pip install gagal. Coba manual: pip install requests' ;;
        complete) printf '%s' 'Instalasi selesai!' ;;
        run_with) printf '%s' 'Jalankan dengan:' ;;
        lang_detected) printf '%s' 'Bahasa terdeteksi:' ;;
        diff_lang) printf '%s' 'Untuk menggunakan bahasa lain:' ;;
        save_perm) printf '%s' 'Untuk menyimpan secara permanen:' ;;
        *) printf '%s' "$(msg_en "$key")" ;;
      esac ;;
    de)
      case "$key" in
        banner_title) printf '%s' 'Pixiv OAuth Token CLI - Installer' ;;
        banner_by) printf '%s' 'Entwickler: Fatony Ahmad Fauzi' ;;
        lang_label) printf '%s' 'Sprache' ;;
        check_python) printf '%s' 'Python-Installation wird geprüft...' ;;
        found_python) printf '%s' 'Gefunden:' ;;
        py_need) printf '%s' 'Python nicht gefunden oder Version < 3.11.' ;;
        py_auto) printf '%s' 'Python wird über winget installiert...' ;;
        py_ok) printf '%s' 'Python installiert. Umgebungsvariablen werden neu geladen...' ;;
        py_fail) printf '%s' 'Automatische Installation fehlgeschlagen. Bitte Python 3.11+ manuell von https://www.python.org/downloads/ installieren.' ;;
        downloading) printf '%s' 'pixiv_login.py wird von GitHub heruntergeladen...' ;;
        downloaded) printf '%s' 'Heruntergeladen:' ;;
        dl_fail) printf '%s' 'Download fehlgeschlagen:' ;;
        dl_fail2) printf '%s' 'Überprüfe Internetverbindung oder lade manuell herunter:' ;;
        deps) printf '%s' 'Abhängigkeiten werden installiert (requests)...' ;;
        deps_ok) printf '%s' 'requests installiert' ;;
        deps_fail) printf '%s' 'pip install fehlgeschlagen. Manuell: pip install requests' ;;
        complete) printf '%s' 'Installation abgeschlossen!' ;;
        run_with) printf '%s' 'Starten mit:' ;;
        lang_detected) printf '%s' 'Erkannte Sprache:' ;;
        diff_lang) printf '%s' 'Um eine andere Sprache zu nutzen:' ;;
        save_perm) printf '%s' 'Dauerhaft speichern:' ;;
        *) printf '%s' "$(msg_en "$key")" ;;
      esac ;;
    fr)
      case "$key" in
        banner_title) printf '%s' 'Pixiv OAuth Token CLI - Installateur' ;;
        banner_by) printf '%s' 'Développeur: Fatony Ahmad Fauzi' ;;
        lang_label) printf '%s' 'Langue' ;;
        check_python) printf '%s' 'Vérification de l'\''installation de Python...' ;;
        found_python) printf '%s' 'Trouvé:' ;;
        py_need) printf '%s' 'Python introuvable ou version < 3.11.' ;;
        py_auto) printf '%s' 'Installation automatique de Python via winget...' ;;
        py_ok) printf '%s' 'Python installé. Rechargement des variables d'\''environnement...' ;;
        py_fail) printf '%s' 'Installation automatique échouée. Installez Python 3.11+ depuis https://www.python.org/downloads/' ;;
        downloading) printf '%s' 'Téléchargement de pixiv_login.py depuis GitHub...' ;;
        downloaded) printf '%s' 'Téléchargé:' ;;
        dl_fail) printf '%s' 'Échec du téléchargement:' ;;
        dl_fail2) printf '%s' 'Vérifiez la connexion Internet ou téléchargez manuellement:' ;;
        deps) printf '%s' 'Installation des dépendances (requests)...' ;;
        deps_ok) printf '%s' 'requests installé' ;;
        deps_fail) printf '%s' 'Échec de pip install. Essayez: pip install requests' ;;
        complete) printf '%s' 'Installation terminée!' ;;
        run_with) printf '%s' 'Lancer avec:' ;;
        lang_detected) printf '%s' 'Langue détectée:' ;;
        diff_lang) printf '%s' 'Pour utiliser une autre langue:' ;;
        save_perm) printf '%s' 'Pour sauvegarder définitivement:' ;;
        *) printf '%s' "$(msg_en "$key")" ;;
      esac ;;
    es)
      case "$key" in
        banner_title) printf '%s' 'Pixiv OAuth Token CLI - Instalador' ;;
        banner_by) printf '%s' 'Desarrollador: Fatony Ahmad Fauzi' ;;
        lang_label) printf '%s' 'Idioma' ;;
        check_python) printf '%s' 'Verificando instalación de Python...' ;;
        found_python) printf '%s' 'Encontrado:' ;;
        py_need) printf '%s' 'Python no encontrado o versión < 3.11.' ;;
        py_auto) printf '%s' 'Intentando instalar Python via winget...' ;;
        py_ok) printf '%s' 'Python instalado. Recargando variables de entorno...' ;;
        py_fail) printf '%s' 'Instalación automática fallida. Instala Python 3.11+ desde https://www.python.org/downloads/' ;;
        downloading) printf '%s' 'Descargando pixiv_login.py desde GitHub...' ;;
        downloaded) printf '%s' 'Descargado:' ;;
        dl_fail) printf '%s' 'Descarga fallida:' ;;
        dl_fail2) printf '%s' 'Verifica la conexión a internet o descarga manualmente:' ;;
        deps) printf '%s' 'Instalando dependencias (requests)...' ;;
        deps_ok) printf '%s' 'requests instalado' ;;
        deps_fail) printf '%s' 'pip install fallido. Intenta: pip install requests' ;;
        complete) printf '%s' '¡Instalación completa!' ;;
        run_with) printf '%s' 'Ejecutar con:' ;;
        lang_detected) printf '%s' 'Idioma detectado:' ;;
        diff_lang) printf '%s' 'Para usar un idioma diferente:' ;;
        save_perm) printf '%s' 'Para guardar permanentemente:' ;;
        *) printf '%s' "$(msg_en "$key")" ;;
      esac ;;
    ru)
      case "$key" in
        banner_title) printf '%s' 'Pixiv OAuth Token CLI - Установщик' ;;
        banner_by) printf '%s' 'Разработчик: Fatony Ahmad Fauzi' ;;
        lang_label) printf '%s' 'Язык' ;;
        check_python) printf '%s' 'Проверка установки Python...' ;;
        found_python) printf '%s' 'Найдено:' ;;
        py_need) printf '%s' 'Python не найден или версия < 3.11.' ;;
        py_auto) printf '%s' 'Автоматическая установка Python через winget...' ;;
        py_ok) printf '%s' 'Python установлен. Перезагрузка переменных среды...' ;;
        py_fail) printf '%s' 'Автоматическая установка не удалась. Установите Python 3.11+ с https://www.python.org/downloads/' ;;
        downloading) printf '%s' 'Загрузка pixiv_login.py с GitHub...' ;;
        downloaded) printf '%s' 'Загружено:' ;;
        dl_fail) printf '%s' 'Ошибка загрузки:' ;;
        dl_fail2) printf '%s' 'Проверьте подключение к интернету или загрузите вручную:' ;;
        deps) printf '%s' 'Установка зависимостей (requests)...' ;;
        deps_ok) printf '%s' 'requests установлено' ;;
        deps_fail) printf '%s' 'pip install не удалось. Попробуйте: pip install requests' ;;
        complete) printf '%s' 'Установка завершена!' ;;
        run_with) printf '%s' 'Запустить с:' ;;
        lang_detected) printf '%s' 'Определённый язык:' ;;
        diff_lang) printf '%s' 'Для другого языка:' ;;
        save_perm) printf '%s' 'Для постоянного сохранения:' ;;
        *) printf '%s' "$(msg_en "$key")" ;;
      esac ;;
    pt)
      case "$key" in
        banner_title) printf '%s' 'Pixiv OAuth Token CLI - Instalador' ;;
        banner_by) printf '%s' 'Desenvolvedor: Fatony Ahmad Fauzi' ;;
        lang_label) printf '%s' 'Idioma' ;;
        check_python) printf '%s' 'Verificando instalação do Python...' ;;
        found_python) printf '%s' 'Encontrado:' ;;
        py_need) printf '%s' 'Python não encontrado ou versão < 3.11.' ;;
        py_auto) printf '%s' 'Tentando instalar Python via winget...' ;;
        py_ok) printf '%s' 'Python instalado. Recarregando variáveis de ambiente...' ;;
        py_fail) printf '%s' 'Instalação automática falhou. Instale o Python 3.11+ em https://www.python.org/downloads/' ;;
        downloading) printf '%s' 'Baixando pixiv_login.py do GitHub...' ;;
        downloaded) printf '%s' 'Baixado:' ;;
        dl_fail) printf '%s' 'Falha no download:' ;;
        dl_fail2) printf '%s' 'Verifique a conexão com a internet ou baixe manualmente:' ;;
        deps) printf '%s' 'Instalando dependências (requests)...' ;;
        deps_ok) printf '%s' 'requests instalado' ;;
        deps_fail) printf '%s' 'pip install falhou. Tente: pip install requests' ;;
        complete) printf '%s' 'Instalação concluída!' ;;
        run_with) printf '%s' 'Executar com:' ;;
        lang_detected) printf '%s' 'Idioma detectado:' ;;
        diff_lang) printf '%s' 'Para usar outro idioma:' ;;
        save_perm) printf '%s' 'Para salvar permanentemente:' ;;
        *) printf '%s' "$(msg_en "$key")" ;;
      esac ;;
    pl)
      case "$key" in
        banner_title) printf '%s' 'Pixiv OAuth Token CLI - Instalator' ;;
        banner_by) printf '%s' 'Deweloper: Fatony Ahmad Fauzi' ;;
        lang_label) printf '%s' 'Język' ;;
        check_python) printf '%s' 'Sprawdzanie instalacji Python...' ;;
        found_python) printf '%s' 'Znaleziono:' ;;
        py_need) printf '%s' 'Python nie znaleziony lub wersja < 3.11.' ;;
        py_auto) printf '%s' 'Automatyczna instalacja Python przez winget...' ;;
        py_ok) printf '%s' 'Python zainstalowany. Przeładowanie zmiennych środowiskowych...' ;;
        py_fail) printf '%s' 'Automatyczna instalacja nie powiodła się. Zainstaluj Python 3.11+ z https://www.python.org/downloads/' ;;
        downloading) printf '%s' 'Pobieranie pixiv_login.py z GitHub...' ;;
        downloaded) printf '%s' 'Pobrano:' ;;
        dl_fail) printf '%s' 'Pobieranie nie powiodło się:' ;;
        dl_fail2) printf '%s' 'Sprawdź połączenie internetowe lub pobierz ręcznie:' ;;
        deps) printf '%s' 'Instalowanie zależności (requests)...' ;;
        deps_ok) printf '%s' 'requests zainstalowano' ;;
        deps_fail) printf '%s' 'pip install nie powiodło się. Spróbuj: pip install requests' ;;
        complete) printf '%s' 'Instalacja zakończona!' ;;
        run_with) printf '%s' 'Uruchom za pomocą:' ;;
        lang_detected) printf '%s' 'Wykryty język:' ;;
        diff_lang) printf '%s' 'Aby użyć innego języka:' ;;
        save_perm) printf '%s' 'Aby zapisać na stałe:' ;;
        *) printf '%s' "$(msg_en "$key")" ;;
      esac ;;
    *)
      msg_en "$key" ;;
  esac
}

msg_en() {
  local key="$1"
  case "$key" in
    banner_title) printf '%s' 'Pixiv OAuth Token CLI - Installer' ;;
    banner_by) printf '%s' 'by Fatony Ahmad Fauzi' ;;
    lang_label) printf '%s' 'Language' ;;
    check_python) printf '%s' 'Checking Python installation...' ;;
    found_python) printf '%s' 'Found' ;;
    py_need) printf '%s' 'Python not found or version < 3.11.' ;;
    py_auto) printf '%s' 'Attempting to install Python via winget...' ;;
    py_ok) printf '%s' 'Python installed. Reloading environment variables...' ;;
    py_fail) printf '%s' 'Auto-install failed. Please install Python 3.11+ manually from https://www.python.org/downloads/' ;;
    downloading) printf '%s' 'Downloading pixiv_login.py from GitHub...' ;;
    downloaded) printf '%s' 'Downloaded:' ;;
    dl_fail) printf '%s' 'Download failed:' ;;
    dl_fail2) printf '%s' 'Check your internet connection or download manually:' ;;
    deps) printf '%s' 'Installing dependencies (requests)...' ;;
    deps_ok) printf '%s' 'requests installed' ;;
    deps_fail) printf '%s' 'pip install failed. Try manually: pip install requests' ;;
    complete) printf '%s' 'Installation complete!' ;;
    run_with) printf '%s' 'Run with:' ;;
    lang_detected) printf '%s' 'Language detected:' ;;
    diff_lang) printf '%s' 'To use a different language:' ;;
    save_perm) printf '%s' 'To save permanently:' ;;
    *) printf '%s' "$key" ;;
  esac
}

banner() {
  echo ""
  echo -e "  ${CYAN}+==========================================+${RESET}"
  echo -e "  ${CYAN}|  $(msg banner_title)${RESET}"
  echo -e "  ${CYAN}|  $(msg banner_by)${RESET}"
  echo -e "  ${CYAN}+==========================================+${RESET}"
  echo ""
}
step() { echo -e "  ${YELLOW}[*]${RESET} $1"; }
ok()   { echo -e "  ${GREEN}[+]${RESET} $1"; }
err()  { echo -e "  ${RED}[!]${RESET} $1" >&2; }
info() { echo -e "  ${DIM}[i]${RESET} $1"; }

banner
info "$(msg lang_label): ${CYAN}${RESOLVED_LANG}${RESET}"

# --- 1. Check Python ---
step "$(msg check_python)"
PYTHON_CMD=""
for cmd in python3 python; do
  if command -v "$cmd" >/dev/null 2>&1; then
    PY_VER=$("$cmd" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
    MAJOR=$(printf '%s' "$PY_VER" | cut -d. -f1)
    MINOR=$(printf '%s' "$PY_VER" | cut -d. -f2)
    if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 11 ]; then
      PYTHON_CMD="$cmd"
      ok "$(msg found_python) $cmd $PY_VER"
      break
    else
      err "$(msg py_need)"
    fi
  fi
done

if [ -z "$PYTHON_CMD" ]; then
  step "$(msg py_need)"
  step "$(msg py_auto)"
  if command -v apt >/dev/null 2>&1; then
    sudo apt update && sudo apt install -y python3 python3-pip python3-venv
    PYTHON_CMD="python3"
  elif command -v dnf >/dev/null 2>&1; then
    sudo dnf install -y python3 python3-pip; PYTHON_CMD="python3"
  elif command -v pacman >/dev/null 2>&1; then
    sudo pacman -Sy --noconfirm python python-pip; PYTHON_CMD="python"
  elif command -v brew >/dev/null 2>&1; then
    brew install python; PYTHON_CMD="python3"
  else
    err "$(msg py_fail)"; exit 1
  fi
  ok "$(msg py_ok)"
fi

# --- 2. Check download tool ---
step "$(msg downloading)"
if command -v curl >/dev/null 2>&1; then
  DOWNLOADER="curl"; curl -fsSL "$FILE_URL" -o "$OUT_FILE"
elif command -v wget >/dev/null 2>&1; then
  DOWNLOADER="wget"; wget -q "$FILE_URL" -O "$OUT_FILE"
else
  err "$(msg dl_fail2)"; exit 1
fi
ok "$(msg downloaded) $OUT_FILE"

# --- 3. Install dependencies ---
step "$(msg deps)"
if "$PYTHON_CMD" -m pip install requests --quiet --disable-pip-version-check 2>/dev/null; then
  ok "$(msg deps_ok)"
else
  err "$(msg deps_fail)"
fi

chmod +x "$OUT_FILE" 2>/dev/null || true

# --- Done ---
echo ""
echo -e "  ${GREEN}${BOLD}+==========================================+${RESET}"
echo -e "  ${GREEN}${BOLD}|  $(msg complete)${RESET}"
echo -e "  ${GREEN}${BOLD}+==========================================+${RESET}"
echo ""
echo -e "  $(msg run_with)"
if [ "$RESOLVED_LANG" != "en" ]; then
  echo -e "    ${CYAN}$PYTHON_CMD pixiv_login.py --lang $RESOLVED_LANG${RESET}"
else
  echo -e "    ${CYAN}$PYTHON_CMD pixiv_login.py${RESET}"
fi
echo ""
echo -e "  ${DIM}[i] $(msg lang_detected) $RESOLVED_LANG${RESET}"
echo -e "  ${DIM}    $(msg diff_lang) $PYTHON_CMD pixiv_login.py --lang jp${RESET}"
echo -e "  ${DIM}    $(msg save_perm)  $PYTHON_CMD pixiv_login.py config set-lang jp${RESET}"
echo ""
