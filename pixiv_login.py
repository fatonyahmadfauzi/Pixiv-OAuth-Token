#!/usr/bin/env python3
"""
Pixiv OAuth Login Tool (PKCE)
- Multi-language output with config + system language auto-detect
- Optional colored terminal output (ANSI)
- Windows .exe build instructions (PyInstaller)
"""

from __future__ import annotations

from argparse import ArgumentParser
from base64 import urlsafe_b64encode
from hashlib import sha256
from secrets import token_urlsafe
from urllib.parse import urlencode, urlparse, parse_qs
from webbrowser import open as open_url
from pprint import pprint
from sys import exit, stdout
import sys
import traceback
from pathlib import Path
import json
import os
import locale
import requests


# ===== CONFIG =====
USER_AGENT = "PixivAndroidApp/5.0.234 (Android 11; Pixel 5)"
REDIRECT_URI = "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback"
LOGIN_URL = "https://app-api.pixiv.net/web/v1/login"
AUTH_TOKEN_URL = "https://oauth.secure.pixiv.net/auth/token"

CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT"
CLIENT_SECRET = "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj"

CONFIG_FILE = Path(__file__).with_name("pixiv_login_config.json")


# ===== LANGUAGE CONFIG =====
DEFAULT_LANG = "en"
SUPPORTED_LANGS = ("en", "pl", "zh", "jp", "de", "fr", "es", "ru", "pt", "id", "kr")
LANG_LABELS = {
    "en": "🇬🇧 English",
    "pl": "🇵🇱 Polski",
    "zh": "🇨🇳 中文",
    "jp": "🇯🇵 日本語",
    "de": "🇩🇪 Deutsch",
    "fr": "🇫🇷 Français",
    "es": "🇪🇸 Español",
    "ru": "🇷🇺 Русский",
    "pt": "🇵🇹 Português",
    "id": "🇮🇩 Indonesia",
    "kr": "🇰🇷 한국어",
}

LANGUAGES = {
    "en": {
        "open_browser": "Opening browser for login...",
        "paste_url": "Paste FULL URL (pixiv://...) or paste code here:",
        "code_detected": "Detected code:",
        "login_success": "=== LOGIN SUCCESS ===",
        "error_response": "ERROR RESPONSE:",
        "invalid_code": "Failed to read code from input.",
        "config_title": "=== CONFIG ===",
        "config_path": "Config file:",
        "config_default_lang": "Default language:",
        "config_saved": "Saved.",
        "config_invalid_lang": "Unsupported language. Supported:",
        "config_detected_lang": "System language detected:",
    },
    "id": {
        "open_browser": "Membuka browser untuk login...",
        "paste_url": "Paste FULL URL (pixiv://...) atau langsung code di sini:",
        "code_detected": "Code terdeteksi:",
        "login_success": "=== LOGIN BERHASIL ===",
        "error_response": "ERROR RESPONSE:",
        "invalid_code": "Gagal membaca code dari input.",
        "config_title": "=== KONFIG ===",
        "config_path": "File config:",
        "config_default_lang": "Bahasa default:",
        "config_saved": "Tersimpan.",
        "config_invalid_lang": "Bahasa tidak didukung. Pilihan:",
        "config_detected_lang": "Bahasa sistem terdeteksi:",
    },
    "jp": {
        "open_browser": "ログイン用ブラウザを開いています...",
        "paste_url": "FULL URL (pixiv://...) またはコードを貼り付けてください:",
        "code_detected": "検出されたコード:",
        "login_success": "=== ログイン成功 ===",
        "error_response": "エラーレスポンス:",
        "invalid_code": "コードの読み取りに失敗しました。",
        "config_title": "=== 設定 ===",
        "config_path": "設定ファイル:",
        "config_default_lang": "既定の言語:",
        "config_saved": "保存しました。",
        "config_invalid_lang": "未対応の言語。対応:",
        "config_detected_lang": "検出されたシステム言語:",
    },
    "de": {
        "open_browser": "Browser wird für Login geöffnet...",
        "paste_url": "FULL URL (pixiv://...) oder Code hier einfügen:",
        "code_detected": "Erkannter Code:",
        "login_success": "=== LOGIN ERFOLGREICH ===",
        "error_response": "FEHLERANTWORT:",
        "invalid_code": "Code konnte nicht gelesen werden.",
        "config_title": "=== KONFIGURATION ===",
        "config_path": "Konfigurationsdatei:",
        "config_default_lang": "Standardsprache:",
        "config_saved": "Gespeichert.",
        "config_invalid_lang": "Sprache nicht unterstützt. Unterstützt:",
        "config_detected_lang": "Erkannte Systemsprache:",
    },
    "fr": {
        "open_browser": "Ouverture du navigateur pour la connexion...",
        "paste_url": "Collez l'URL complète (pixiv://...) ou le code ici:",
        "code_detected": "Code détecté:",
        "login_success": "=== CONNEXION RÉUSSIE ===",
        "error_response": "RÉPONSE D'ERREUR:",
        "invalid_code": "Impossible de lire le code.",
        "config_title": "=== CONFIG ===",
        "config_path": "Fichier de config:",
        "config_default_lang": "Langue par défaut:",
        "config_saved": "Enregistré.",
        "config_invalid_lang": "Langue non prise en charge. Supportées:",
        "config_detected_lang": "Langue système détectée:",
    },
    "es": {
        "open_browser": "Abriendo navegador para iniciar sesión...",
        "paste_url": "Pega la URL completa (pixiv://...) o el código aquí:",
        "code_detected": "Código detectado:",
        "login_success": "=== INICIO DE SESIÓN EXITOSO ===",
        "error_response": "RESPUESTA DE ERROR:",
        "invalid_code": "No se pudo leer el código.",
        "config_title": "=== CONFIG ===",
        "config_path": "Archivo de config:",
        "config_default_lang": "Idioma predeterminado:",
        "config_saved": "Guardado.",
        "config_invalid_lang": "Idioma no soportado. Soportados:",
        "config_detected_lang": "Idioma del sistema detectado:",
    },
    "ru": {
        "open_browser": "Открытие браузера для входа...",
        "paste_url": "Вставьте полный URL (pixiv://...) или код здесь:",
        "code_detected": "Обнаружен код:",
        "login_success": "=== ВХОД УСПЕШЕН ===",
        "error_response": "ОШИБКА:",
        "invalid_code": "Не удалось прочитать код.",
        "config_title": "=== КОНФИГ ===",
        "config_path": "Файл конфига:",
        "config_default_lang": "Язык по умолчанию:",
        "config_saved": "Сохранено.",
        "config_invalid_lang": "Язык не поддерживается. Доступны:",
        "config_detected_lang": "Определён язык системы:",
    },
    "pt": {
        "open_browser": "Abrindo navegador para login...",
        "paste_url": "Cole a URL completa (pixiv://...) ou o código aqui:",
        "code_detected": "Código detectado:",
        "login_success": "=== LOGIN BEM-SUCEDIDO ===",
        "error_response": "RESPOSTA DE ERRO:",
        "invalid_code": "Falha ao ler o código.",
        "config_title": "=== CONFIG ===",
        "config_path": "Arquivo de config:",
        "config_default_lang": "Idioma padrão:",
        "config_saved": "Salvo.",
        "config_invalid_lang": "Idioma não suportado. Suportados:",
        "config_detected_lang": "Idioma do sistema detectado:",
    },
    "pl": {
        "open_browser": "Otwieranie przeglądarki do logowania...",
        "paste_url": "Wklej pełny URL (pixiv://...) lub kod tutaj:",
        "code_detected": "Wykryty kod:",
        "login_success": "=== LOGOWANIE UDANE ===",
        "error_response": "ODPOWIEDŹ BŁĘDU:",
        "invalid_code": "Nie udało się odczytać kodu.",
        "config_title": "=== KONFIG ===",
        "config_path": "Plik konfig:",
        "config_default_lang": "Domyślny język:",
        "config_saved": "Zapisano.",
        "config_invalid_lang": "Język nieobsługiwany. Dostępne:",
        "config_detected_lang": "Wykryty język systemu:",
    },
    "kr": {
        "open_browser": "로그인을 위해 브라우저를 여는 중...",
        "paste_url": "FULL URL (pixiv://...) 또는 코드를 입력하세요:",
        "code_detected": "감지된 코드:",
        "login_success": "=== 로그인 성공 ===",
        "error_response": "오류 응답:",
        "invalid_code": "코드를 읽지 못했습니다.",
        "config_title": "=== 설정 ===",
        "config_path": "설정 파일:",
        "config_default_lang": "기본 언어:",
        "config_saved": "저장됨.",
        "config_invalid_lang": "지원하지 않는 언어. 지원:",
        "config_detected_lang": "감지된 시스템 언어:",
    },
    "zh": {
        "open_browser": "正在打开浏览器进行登录...",
        "paste_url": "粘贴完整URL (pixiv://...) 或直接输入代码:",
        "code_detected": "检测到的代码:",
        "login_success": "=== 登录成功 ===",
        "error_response": "错误响应:",
        "invalid_code": "无法读取代码。",
        "config_title": "=== 配置 ===",
        "config_path": "配置文件:",
        "config_default_lang": "默认语言:",
        "config_saved": "已保存。",
        "config_invalid_lang": "不支持的语言。支持:",
        "config_detected_lang": "检测到系统语言:",
    },
}


def supported_langs_display() -> str:
    return ", ".join(f"{code} ({LANG_LABELS.get(code, code)})" for code in SUPPORTED_LANGS)


def get_lang(lang_code: str):
    return LANGUAGES.get(lang_code, LANGUAGES[DEFAULT_LANG])


# ===== TERMINAL COLORS (ANSI) =====
class Ansi:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"


def _supports_color(no_color: bool) -> bool:
    if no_color:
        return False
    if not hasattr(stdout, "isatty") or not stdout.isatty():
        return False
    # Common opt-out envs
    if os.environ.get("NO_COLOR"):
        return False
    # Most modern terminals support ANSI (Windows 10+ typically OK)
    return True


def colorize(text: str, color: str, enabled: bool) -> str:
    if not enabled:
        return text
    return f"{color}{text}{Ansi.RESET}"


# ===== CONFIG FILE =====
def load_config() -> dict:
    try:
        if CONFIG_FILE.exists():
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def save_config(cfg: dict) -> None:
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")


def set_default_lang(lang: str) -> None:
    cfg = load_config()
    cfg["default_lang"] = lang
    save_config(cfg)


def get_default_lang_from_config() -> str | None:
    cfg = load_config()
    lang = cfg.get("default_lang")
    if isinstance(lang, str) and lang in SUPPORTED_LANGS:
        return lang
    return None


# ===== SYSTEM LANGUAGE DETECTION =====
def _normalize_locale(loc: str | None) -> str | None:
    if not loc:
        return None
    # Examples: "id_ID", "en_US", "ja_JP", "zh_CN", "pt_BR"
    loc = loc.strip()
    if not loc:
        return None
    loc = loc.replace("-", "_")
    return loc


def detect_system_lang() -> str | None:
    # Try environment first
    for key in ("LC_ALL", "LC_MESSAGES", "LANG"):
        v = _normalize_locale(os.environ.get(key))
        if v:
            code = v.split(".")[0].split("_")[0].lower()
            mapped = map_locale_to_lang(code)
            if mapped:
                return mapped

    try:
        loc, _enc = locale.getdefaultlocale()  # type: ignore[deprecated]
        loc = _normalize_locale(loc)
        if loc:
            code = loc.split(".")[0].split("_")[0].lower()
            mapped = map_locale_to_lang(code)
            if mapped:
                return mapped
    except Exception:
        pass

    try:
        loc = locale.getlocale()[0]
        loc = _normalize_locale(loc)
        if loc:
            code = loc.split(".")[0].split("_")[0].lower()
            mapped = map_locale_to_lang(code)
            if mapped:
                return mapped
    except Exception:
        pass

    return None


def map_locale_to_lang(two_letter: str) -> str | None:
    # Map OS locale language to our supported codes
    mapping = {
        "en": "en",
        "id": "id",
        "in": "id",   # sometimes Indonesian is "in"
        "ja": "jp",
        "jp": "jp",
        "ko": "kr",
        "kr": "kr",
        "zh": "zh",
        "de": "de",
        "fr": "fr",
        "es": "es",
        "ru": "ru",
        "pt": "pt",
        "pl": "pl",
    }
    lang = mapping.get(two_letter.lower())
    if lang in SUPPORTED_LANGS:
        return lang
    return None


def resolve_lang(explicit_lang: str | None) -> str:
    if explicit_lang and explicit_lang in SUPPORTED_LANGS:
        return explicit_lang
    cfg_lang = get_default_lang_from_config()
    if cfg_lang:
        return cfg_lang
    sys_lang = detect_system_lang()
    if sys_lang:
        return sys_lang
    return DEFAULT_LANG


# ===== PKCE =====
def s256(data: bytes) -> str:
    return urlsafe_b64encode(sha256(data).digest()).rstrip(b"=").decode("ascii")


def oauth_pkce(transform):
    code_verifier = token_urlsafe(32)
    code_challenge = transform(code_verifier.encode("ascii"))
    return code_verifier, code_challenge


# ===== PRINT TOKEN =====
def print_auth_token_response(response, lang: str, color_on: bool):
    L = get_lang(lang)
    data = response.json()

    if "access_token" not in data:
        print("\n" + colorize(L["error_response"], Ansi.RED + Ansi.BOLD, color_on))
        pprint(data)
        exit(1)

    print("\n" + colorize(L["login_success"], Ansi.GREEN + Ansi.BOLD, color_on))
    print(colorize("access_token :", Ansi.BOLD, color_on), data["access_token"])
    print(colorize("refresh_token:", Ansi.BOLD, color_on), data["refresh_token"])
    print(colorize("expires_in   :", Ansi.BOLD, color_on), data.get("expires_in", 0))


# ===== LOGIN FLOW =====
def login(lang: str, color_on: bool):
    L = get_lang(lang)

    code_verifier, code_challenge = oauth_pkce(s256)

    login_params = {
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "client": "pixiv-android",
    }

    login_url = f"{LOGIN_URL}?{urlencode(login_params)}"

    print(colorize(L["open_browser"], Ansi.CYAN, color_on))
    open_url(login_url)

    raw_input_value = input("\n" + colorize(L["paste_url"], Ansi.YELLOW, color_on) + "\n").strip()

    try:
        if raw_input_value.startswith("pixiv://"):
            parsed = urlparse(raw_input_value)
            code = parse_qs(parsed.query)["code"][0]
        else:
            code = raw_input_value
    except Exception:
        print(colorize(L["invalid_code"], Ansi.RED, color_on))
        return

    print(colorize(L["code_detected"], Ansi.BLUE, color_on), code)

    response = requests.post(
        AUTH_TOKEN_URL,
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "code_verifier": code_verifier,
            "grant_type": "authorization_code",
            "include_policy": "true",
            "redirect_uri": REDIRECT_URI,
        },
        headers={"User-Agent": USER_AGENT},
        timeout=30,
    )

    print_auth_token_response(response, lang, color_on)


# ===== REFRESH FLOW =====
def refresh(refresh_token: str, lang: str, color_on: bool):
    response = requests.post(
        AUTH_TOKEN_URL,
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "include_policy": "true",
            "refresh_token": refresh_token,
        },
        headers={"User-Agent": USER_AGENT},
        timeout=30,
    )

    print_auth_token_response(response, lang, color_on)


def print_config(lang: str, color_on: bool):
    L = get_lang(lang)
    cfg_lang = get_default_lang_from_config()
    sys_lang = detect_system_lang()

    print(colorize(L["config_title"], Ansi.BOLD, color_on))
    print(colorize(L["config_path"], Ansi.DIM, color_on), str(CONFIG_FILE))
    print(L["config_default_lang"], cfg_lang if cfg_lang else "(not set)")
    print(L["config_detected_lang"], sys_lang if sys_lang else "(unknown)")
    print("Supported:", supported_langs_display())


def _pause_before_exit_if_frozen() -> None:
    if not getattr(sys, "frozen", False):
        return
    try:
        input("\nPress Enter to exit...")
    except Exception:
        pass


# ===== MAIN =====
def main():
    parser = ArgumentParser(description="Pixiv OAuth Login Tool")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")

    subparsers = parser.add_subparsers(dest="command")

    # login
    login_parser = subparsers.add_parser("login", help="Login flow")
    login_parser.add_argument("--lang", default=None, help="Language code (e.g. en, id, jp)")

    # lang (alias for login with lang positional)
    lang_parser = subparsers.add_parser("lang", help="Login flow with language selection")
    lang_parser.add_argument("language", nargs="?", default=None)

    # refresh
    refresh_parser = subparsers.add_parser("refresh", help="Refresh token flow")
    refresh_parser.add_argument("refresh_token")
    refresh_parser.add_argument("--lang", default=None, help="Language code (e.g. en, id, jp)")

    # config
    config_parser = subparsers.add_parser("config", help="Show or set config")
    config_sub = config_parser.add_subparsers(dest="config_cmd")

    config_sub.add_parser("show", help="Show current config (default)")

    setlang = config_sub.add_parser("set-lang", help="Set default language saved to config")
    setlang.add_argument("language")

    args = parser.parse_args()
    color_on = _supports_color(args.no_color)

    if args.command == "login":
        lang = resolve_lang(args.lang)
        login(lang, color_on)

    elif args.command == "lang":
        lang = resolve_lang(args.language)
        login(lang, color_on)

    elif args.command == "refresh":
        lang = resolve_lang(args.lang)
        refresh(args.refresh_token, lang, color_on)

    elif args.command == "config":
        # pick a language for the config UI as well:
        ui_lang = resolve_lang(None)

        if args.config_cmd in (None, "show"):
            print_config(ui_lang, color_on)
            return

        if args.config_cmd == "set-lang":
            new_lang = args.language
            L = get_lang(ui_lang)

            if new_lang not in SUPPORTED_LANGS:
                print(colorize(L["config_invalid_lang"], Ansi.RED, color_on), supported_langs_display())
                exit(2)

            set_default_lang(new_lang)
            print(colorize(L["config_saved"], Ansi.GREEN, color_on))
            print_config(ui_lang, color_on)
            return

    else:
        parser.print_help()
        _pause_before_exit_if_frozen()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        _pause_before_exit_if_frozen()
        exit(130)
    except Exception as exc:
        print("\nUnexpected error:", exc)
        traceback.print_exc()
        _pause_before_exit_if_frozen()
        exit(1)
