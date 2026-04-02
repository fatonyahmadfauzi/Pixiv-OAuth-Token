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
import subprocess
import time
import requests

# rich library removed — using plain ANSI output only


# ===== CONFIG =====
DEBUG_MODE = False
DEBUG_LOGS: list[str] = []
DEBUG_MAX_LINES = 1000
MENU_CONSOLE_WIDTH = 90
DEBUG_LANG = "en"

DEBUG_MSGS = {
    "en": {
        "parsed_arguments": "Parsed arguments: {args}",
        "command_selected": "Command selected: {command}",
        "resolving_language": "Resolving language (explicit={explicit})...",
        "loaded_config": "Loaded config from {path}",
        "read_default_lang": "Reading default lang from config: {lang}",
        "menu_option_selected": "User selected main menu option: {choice}",
        "open_language_selector": "Opening language selector (current={lang})",
        "language_selector_input": "Language selector input: '{value}'",
        "language_change_canceled": "Language change canceled by user",
        "language_updated": "Language updated to: {lang}",
    },
    "jp": {
        "parsed_arguments": "引数を解析しました: {args}",
        "command_selected": "選択されたコマンド: {command}",
        "resolving_language": "言語を解決中 (explicit={explicit})...",
        "loaded_config": "設定を読み込みました: {path}",
        "read_default_lang": "設定のデフォルト言語を読み込みました: {lang}",
        "menu_option_selected": "メインメニューで選択されたオプション: {choice}",
        "open_language_selector": "言語選択を開いています (current={lang})",
        "language_selector_input": "言語選択の入力: '{value}'",
        "language_change_canceled": "ユーザーが言語変更をキャンセルしました",
        "language_updated": "言語が更新されました: {lang}",
    },
}

CANCEL_HINT = {
    "en": "empty to cancel",
    "id": "kosongkan untuk batal",
    "jp": "空欄でキャンセル",
    "pl": "puste aby anulować",
    "zh": "留空以取消",
    "de": "leer zum Abbrechen",
    "fr": "laisser vide pour annuler",
    "es": "vacío para cancelar",
    "ru": "пусто для отмены",
    "pt": "vazio para cancelar",
    "kr": "비워두면 취소",
}

def _dbg_msg(key: str, **kwargs) -> str:
    template = DEBUG_MSGS.get(DEBUG_LANG, {}).get(key) or DEBUG_MSGS["en"].get(key, key)
    try:
        return template.format(**kwargs)
    except Exception:
        return template

def debug_print(msg: str, color_on: bool = True):
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    DEBUG_LOGS.append(f"{stamp} | {msg}")
    if len(DEBUG_LOGS) > DEBUG_MAX_LINES:
        del DEBUG_LOGS[:-DEBUG_MAX_LINES]

USER_AGENT = "PixivAndroidApp/5.0.234 (Android 11; Pixel 5)"
REDIRECT_URI = "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback"
LOGIN_URL = "https://app-api.pixiv.net/web/v1/login"
AUTH_TOKEN_URL = "https://oauth.secure.pixiv.net/auth/token"

CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT"
CLIENT_SECRET = "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj"

REPO_BASE_URL = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token"
README_URL = f"{REPO_BASE_URL}/blob/master/README.md"
RELEASES_URL = f"{REPO_BASE_URL}/releases"
TUTORIAL_URL = README_URL
TIKTOK_URL = "https://www.tiktok.com/@fatonyahmadfauzi"
TWITTER_URL = "https://x.com/fatonyahmad89"
DEVELOPER_NAME = "Fatony Ahmad Fauzi"
APP_VERSION = "v1.0.5"
APP_BUILD_CODE = "REL-U1775122868915"
GITHUB_API_LATEST_RELEASE = "https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest"
RAW_MAIN_PY_URL = "https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/app/pixiv_login.py"
LATEST_MANIFEST_URL = "https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/latest.json"
UPDATE_CACHE = {"latest": None, "latest_code": None, "checked_at": 0.0}


def _app_dir() -> Path:
    """Return the persistent app folder (next to exe when frozen, next to script otherwise)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


CONFIG_FILE = _app_dir() / "pixiv_login_config.json"
VERSION_FILE = _app_dir() / "pixiv_login_version.txt"


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
LANG_NAMES = {
    "en": "English",
    "pl": "Polski",
    "zh": "中文",
    "jp": "日本語",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
    "ru": "Русский",
    "pt": "Português",
    "id": "Indonesia",
    "kr": "한국어",
}

LANGUAGES = {
    "en": {
        "open_browser": "Opening browser for login...",
        "paste_url": "Paste FULL URL (pixiv://...) or paste code here:",
        "code_detected": "Detected code:",
        "login_success": "LOGIN SUCCESS",
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
        "login_success": "LOGIN BERHASIL",
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
        "login_success": "ログイン成功",
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
        "login_success": "LOGIN ERFOLGREICH",
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
        "login_success": "CONNEXION RÉUSSIE",
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
        "login_success": "INICIO DE SESIÓN EXITOSO",
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
        "login_success": "ВХОД УСПЕШЕН",
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
        "login_success": "LOGIN BEM-SUCEDIDO",
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
        "login_success": "LOGOWANIE UDANE",
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
        "login_success": "로그인 성공",
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
        "login_success": "登录成功",
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




MENU_UI_EN = {
    "project": "Pixiv OAuth Token",
    "developer": "Developer",
    "menu_title": "Main Menu",
    "opt_change_lang": "Change Language",
    "opt_tutorial": "Tutorial",
    "opt_resources_docs": "Resources & Docs",
    "opt_support": "Support",
    "opt_social": "Social",
    "opt_login": "Login",
    "opt_changelog": "Changelog",
    "opt_version": "Version",
    "opt_exit": "Exit",
    "select_option": "Select option",
    "invalid_option": "Invalid option.",
    "choose_lang": "Choose language code",
    "lang_updated": "Default language updated to",
    "resources_docs_title": "Resources & Docs",
    "res_docs_documentation": "Documentation",
    "res_docs_license": "License",
    "res_docs_pixiv": "Pixiv OAuth Endpoint",
    "res_docs_python": "Python 3.11+",
    "res_docs_vercel": "Deployed on Vercel",
    "support_title": "Support",
    "sup_contact": "Contact Us",
    "sup_report": "Report an Issue",
    "sup_discussions": "Discussions",
    "sup_fatony": "Fatony Ahmad Fauzi",
    "sup_donate": "Support / Donate",
    "social_title": "Social Links",
    "social_github": "GitHub",
    "social_linkedin": "LinkedIn",
    "back": "Back",
    "tutorial_title": "CLI Tutorial",
    "tutorial_desc": "Follow these steps to get Pixiv OAuth tokens directly from this CLI.",
    "tutorial_step1": "1) Choose option [6] Login.",
    "tutorial_step2": "2) Browser opens to Pixiv login page.",
    "tutorial_step3": "3) After login, copy full pixiv:// URL callback.",
    "tutorial_step4": "4) Paste URL/code in CLI prompt.",
    "tutorial_step5": "5) CLI detects code and exchanges token.",
    "tutorial_step6": "6) access_token and refresh_token are shown.",
    "tutorial_example": "Example output",
    "developer_info": "Developer Information",
    "opt_debug": "Toggle Debug Mode",
    "debug_enabled": "Debug mode is now ENABLED.",
    "debug_disabled": "Debug mode is now DISABLED.",
    "debug_current": "Current",
    "debug_title": "Debug",
    "debug_copy": "Copy debug",
    "debug_clear": "Clear debug",
    "debug_exit": "Exit",
    "debug_copied": "Debug copied.",
    "debug_copy_failed": "Failed to copy debug.",
    "debug_cleared": "Debug logs cleared.",
    "debug_empty": "(no debug logs yet)",
    "version_title": "Version",
    "version_check_update": "Check update",
    "version_update_now": "Update now",
    "version_later": "Later",
    "version_new_badge": "New Version Available",
    "version_current": "Current version",
    "version_latest_available": "Latest version available",
    "version_latest": "Current version is already latest.",
    "version_no_internet_check": "No internet connection. Cannot check update.",
    "version_no_internet_update": "No internet connection. Update canceled.",
    "version_update_success": "Updated successfully. Current version",
    "version_update_failed": "Update failed. Please try again.",
    "enter_main_menu": "Enter to main menu",
    "enter_continue": "Enter to continue",
    "login_paste_prompt": "Paste link/code (Enter to cancel)",
    "login_canceled": "Login canceled.",
    "login_actions_title": "Login Actions",
    "login_action_refresh": "Refresh token",
    "login_action_copy_access": "Copy access token",
    "login_action_copy_refresh": "Copy refresh token",
    "login_action_refresh_success": "Refresh token success.",
    "login_action_refresh_failed": "Refresh token failed.",
    "login_action_access_copied": "Access token copied.",
    "login_action_access_copy_failed": "Failed to copy access token.",
    "login_action_refresh_copied": "Refresh token copied.",
    "login_action_refresh_copy_failed": "Failed to copy refresh token.",
    "exiting": "Exiting...",
    "res_docs_privacy": "Privacy Policy",
    "res_docs_terms": "Terms & Conditions",
    "privacy_title": "Privacy Policy",
    "terms_title": "Terms & Conditions",
    "policy_last_updated": "Last updated",
}


# ===== POLICY TEXTS =====
PRIVACY_POLICY_TEXT = {
    "en": [
        "Last updated: April 1, 2026",
        "",
        "This website is an independent open-source utility for Pixiv",
        "OAuth token workflows.",
        "",
        "Independent Project",
        "Pixiv OAuth Token is developed independently and is not an",
        "official Pixiv product or service.",
        "",
        "How Token Data Is Processed",
        "This tool helps you submit authorization data to official Pixiv",
        "OAuth endpoints to exchange or refresh tokens. Token values may",
        "be processed in your browser and API flow only as needed.",
        "",
        "Data Collection & Misuse",
        "The developer does not intentionally collect, sell, or misuse",
        "your Pixiv credentials or OAuth tokens.",
        "",
        "Third-Party Services",
        "This project may link to or rely on services such as GitHub,",
        "Vercel, Pixiv endpoints, and related documentation. Those",
        "services have separate privacy practices.",
        "",
        "Your Responsibility",
        "You are responsible for securing your own device, browser,",
        "network environment, and account credentials.",
        "",
        "Contact",
        "For support or privacy-related questions, please use the",
        "Contact page or the project's GitHub repository.",
    ],
    "id": [
        "Terakhir diperbarui: 1 April 2026",
        "",
        "Situs ini adalah utilitas open-source independen untuk alur",
        "kerja token OAuth Pixiv.",
        "",
        "Proyek Independen",
        "Pixiv OAuth Token dikembangkan secara independen dan bukan",
        "produk atau layanan resmi Pixiv.",
        "",
        "Cara Data Token Diproses",
        "Alat ini membantu Anda mengirimkan data otorisasi ke endpoint",
        "OAuth resmi Pixiv untuk menukar atau memperbarui token.",
        "",
        "Pengumpulan & Penyalahgunaan Data",
        "Pengembang tidak dengan sengaja mengumpulkan, menjual, atau",
        "menyalahgunakan kredensial Pixiv atau token OAuth Anda.",
        "",
        "Layanan Pihak Ketiga",
        "Proyek ini dapat menautkan ke layanan seperti GitHub, Vercel,",
        "endpoint Pixiv, dan dokumentasi terkait.",
        "",
        "Tanggung Jawab Anda",
        "Anda bertanggung jawab untuk mengamankan perangkat, browser,",
        "lingkungan jaringan, dan kredensial akun Anda sendiri.",
        "",
        "Kontak",
        "Untuk pertanyaan dukungan atau privasi, gunakan halaman Kontak",
        "atau repositori GitHub proyek.",
    ],
    "jp": [
        "最終更新日: 2026年4月1日",
        "",
        "このサイトはPixiv OAuthトークンのための",
        "独立したオープンソースユーティリティです。",
        "",
        "独立プロジェクト",
        "Pixiv OAuth Tokenは独立して開発されており、Pixivの",
        "公式製品またはサービスではありません。",
        "",
        "トークンデータの処理方法",
        "このツールはPixivの公式OAuthエンドポイントに認証データを",
        "送信してトークンを交換または更新します。",
        "",
        "データ収集と不正使用",
        "開発者はあなたのPixiv認証情報やOAuthトークンを",
        "意図的に収集、販売、または悪用しません。",
        "",
        "サードパーティサービス",
        "このプロジェクトはGitHub、Vercel、Pixivエンドポイントなどの",
        "サービスに依存する場合があります。",
        "",
        "お客様の責任",
        "ご自身のデバイス、ブラウザ、ネットワーク環境、",
        "アカウント認証情報の保護はお客様の責任です。",
        "",
        "お問い合わせ",
        "サポートやプライバシーに関するご質問は、",
        "お問い合わせページまたはGitHubリポジトリをご利用ください。",
    ],
}

TERMS_CONDITIONS_TEXT = {
    "en": [
        "Last updated: April 1, 2026",
        "",
        "By using this tool, you agree to these terms.",
        "",
        "Open-Source License",
        "This project is released under the MIT License. You are free",
        "to use, modify, and distribute it under those terms.",
        "",
        "No Warranty",
        "This tool is provided 'as is' without any warranty. The",
        "developer makes no guarantees about reliability, accuracy,",
        "or fitness for a particular purpose.",
        "",
        "Acceptable Use",
        "You agree to use this tool only for lawful purposes and in",
        "compliance with Pixiv's own Terms of Service.",
        "",
        "Third-Party Services",
        "Use of third-party services (GitHub, Vercel, Pixiv) is",
        "governed by their respective terms.",
        "",
        "Changes",
        "These terms may be updated at any time. Continued use",
        "implies acceptance of updated terms.",
        "",
        "Contact",
        "For questions, use the Contact page or the project's",
        "GitHub repository.",
    ],
    "id": [
        "Terakhir diperbarui: 1 April 2026",
        "",
        "Dengan menggunakan alat ini, Anda menyetujui syarat-syarat ini.",
        "",
        "Lisensi Open-Source",
        "Proyek ini dirilis di bawah Lisensi MIT. Anda bebas",
        "menggunakan, memodifikasi, dan mendistribusikannya.",
        "",
        "Tanpa Garansi",
        "Alat ini disediakan 'sebagaimana adanya' tanpa jaminan apa pun.",
        "Pengembang tidak memberikan jaminan keandalan atau akurasi.",
        "",
        "Penggunaan yang Diterima",
        "Anda setuju untuk menggunakan alat ini hanya untuk tujuan",
        "yang sah dan sesuai dengan Syarat Layanan Pixiv.",
        "",
        "Layanan Pihak Ketiga",
        "Penggunaan layanan pihak ketiga (GitHub, Vercel, Pixiv)",
        "diatur oleh ketentuan masing-masing layanan.",
        "",
        "Perubahan",
        "Syarat ini dapat diperbarui kapan saja. Penggunaan",
        "berkelanjutan berarti penerimaan syarat yang diperbarui.",
        "",
        "Kontak",
        "Untuk pertanyaan, gunakan halaman Kontak atau repositori",
        "GitHub proyek.",
    ],
    "jp": [
        "最終更新日: 2026年4月1日",
        "",
        "このツールを使用することで、これらの条件に同意したことになります。",
        "",
        "オープンソースライセンス",
        "このプロジェクトはMITライセンスの下でリリースされています。",
        "その条件の下で自由に使用、変更、配布できます。",
        "",
        "無保証",
        "このツールは保証なしで'現状のまま'提供されます。",
        "開発者は信頼性や正確性について保証しません。",
        "",
        "許容される使用",
        "このツールは合法的な目的のみに使用し、",
        "PixivのサービスのTerms of Serviceに準拠してください。",
        "",
        "サードパーティサービス",
        "サードパーティサービス(GitHub、Vercel、Pixiv)の使用は",
        "それぞれの利用規約に従います。",
        "",
        "変更",
        "これらの条件はいつでも更新される場合があります。",
        "継続的な使用は更新された条件の承認を意味します。",
        "",
        "お問い合わせ",
        "ご質問はお問い合わせページまたは",
        "GitHubリポジトリをご利用ください。",
    ],
    "de": [
        "Zuletzt aktualisiert: 1. April 2026",
        "",
        "Diese Website ist ein unabhängiges Open-Source-Hilfsprogramm",
        "für Pixiv OAuth-Token-Workflows.",
        "",
        "Unabhängiges Projekt",
        "Pixiv OAuth Token wird unabhängig entwickelt und ist kein",
        "offizielles Pixiv-Produkt oder -Service.",
        "",
        "Verarbeitung der Token-Daten",
        "Dieses Tool hilft beim Senden von Autorisierungsdaten an die",
        "offiziellen Pixiv-OAuth-Endpunkte zum Austauschen oder Aktualisieren.",
        "",
        "Datenerfassung & Missbrauch",
        "Der Entwickler sammelt, verkauft oder missbraucht Ihre Pixiv-",
        "Anmeldedaten oder OAuth-Token nicht absichtlich.",
        "",
        "Drittanbieterdienste",
        "Dieses Projekt kann auf Dienste wie GitHub, Vercel und Pixiv-",
        "Endpunkte verlinken oder sich auf diese verlassen.",
        "",
        "Ihre Verantwortung",
        "Sie sind für die Sicherung Ihres Geräts, Browsers,",
        "Netzwerks und Ihrer Anmeldedaten verantwortlich.",
        "",
        "Kontakt",
        "Für Support oder Datenschutzfragen nutzen Sie die Kontaktseite",
        "oder das GitHub-Repository des Projekts.",
    ],
    "fr": [
        "Dernière mise à jour: 1er avril 2026",
        "",
        "Ce site est un utilitaire open-source indépendant pour les",
        "flux de travail de jetons OAuth Pixiv.",
        "",
        "Projet indépendant",
        "Pixiv OAuth Token est développé indépendamment et n'est pas",
        "un produit ou service officiel de Pixiv.",
        "",
        "Traitement des données de jeton",
        "Cet outil soumet des données d'autorisation aux points de",
        "terminaison OAuth officiels de Pixiv pour échanger des jetons.",
        "",
        "Collecte de données & utilisation abusive",
        "Le développeur ne collecte pas, ne vend pas et n'utilise pas",
        "abusivement vos identifiants Pixiv ou jetons OAuth.",
        "",
        "Services tiers",
        "Ce projet peut utiliser des services comme GitHub, Vercel et",
        "les points de terminaison Pixiv.",
        "",
        "Votre responsabilité",
        "Vous êtes responsable de la sécurité de votre appareil,",
        "navigateur, réseau et de vos identifiants.",
        "",
        "Contact",
        "Pour toute question, utilisez la page de contact ou le",
        "dépôt GitHub du projet.",
    ],
    "es": [
        "Última actualización: 1 de abril de 2026",
        "",
        "Este sitio es una utilidad open-source independiente para",
        "flujos de trabajo de tokens OAuth de Pixiv.",
        "",
        "Proyecto independiente",
        "Pixiv OAuth Token se desarrolla de forma independiente y no",
        "es un producto ni servicio oficial de Pixiv.",
        "",
        "Procesamiento de datos de token",
        "Esta herramienta ayuda a enviar datos de autorización a los",
        "endpoints OAuth oficiales de Pixiv para intercambiar tokens.",
        "",
        "Recopilación de datos y uso indebido",
        "El desarrollador no recopila, vende ni usa indebidamente sus",
        "credenciales de Pixiv o tokens OAuth.",
        "",
        "Servicios de terceros",
        "Este proyecto puede depender de servicios como GitHub, Vercel",
        "y los endpoints de Pixiv.",
        "",
        "Su responsabilidad",
        "Usted es responsable de proteger su dispositivo, navegador,",
        "entorno de red y credenciales de cuenta.",
        "",
        "Contacto",
        "Para soporte o consultas de privacidad, use la página de",
        "contacto o el repositorio GitHub del proyecto.",
    ],
    "ru": [
        "Последнее обновление: 1 апреля 2026 г.",
        "",
        "Этот сайт — независимая утилита с открытым исходным кодом",
        "для работы с токенами Pixiv OAuth.",
        "",
        "Независимый проект",
        "Pixiv OAuth Token разрабатывается независимо и не является",
        "официальным продуктом или сервисом Pixiv.",
        "",
        "Обработка данных токена",
        "Этот инструмент отправляет данные авторизации к официальным",
        "OAuth-эндпоинтам Pixiv для обмена или обновления токенов.",
        "",
        "Сбор данных и злоупотребление",
        "Разработчик не собирает намеренно, не продаёт и не злоупотребляет",
        "вашими учётными данными Pixiv или OAuth-токенами.",
        "",
        "Сторонние сервисы",
        "Проект может использовать сервисы GitHub, Vercel, Pixiv.",
        "Эти сервисы имеют собственную политику конфиденциальности.",
        "",
        "Ваша ответственность",
        "Вы несёте ответственность за защиту своего устройства,",
        "браузера, сети и учётных данных.",
        "",
        "Контакт",
        "По вопросам поддержки или конфиденциальности используйте",
        "страницу контактов или репозиторий GitHub.",
    ],
    "pt": [
        "Última atualização: 1 de abril de 2026",
        "",
        "Este site é um utilitário open-source independente para",
        "fluxos de trabalho de tokens OAuth do Pixiv.",
        "",
        "Projeto Independente",
        "O Pixiv OAuth Token é desenvolvido independentemente e não é",
        "um produto ou serviço oficial do Pixiv.",
        "",
        "Processamento de Dados de Token",
        "Esta ferramenta envia dados de autorização para os endpoints",
        "OAuth oficiais do Pixiv para trocar ou atualizar tokens.",
        "",
        "Coleta de Dados e Uso Indevido",
        "O desenvolvedor não coleta, vende ou usa indevidamente suas",
        "credenciais Pixiv ou tokens OAuth.",
        "",
        "Serviços de Terceiros",
        "Este projeto pode depender de serviços como GitHub, Vercel",
        "e endpoints do Pixiv.",
        "",
        "Sua Responsabilidade",
        "Você é responsável por proteger seu dispositivo, navegador,",
        "rede e credenciais de conta.",
        "",
        "Contato",
        "Para suporte ou dúvidas de privacidade, use a página de",
        "contato ou o repositório GitHub do projeto.",
    ],
    "pl": [
        "Ostatnia aktualizacja: 1 kwietnia 2026",
        "",
        "Ta strona to niezależne narzędzie open-source do obsługi",
        "przepływów tokenów OAuth Pixiv.",
        "",
        "Niezależny projekt",
        "Pixiv OAuth Token jest rozwijany niezależnie i nie jest",
        "oficjalnym produktem ani usługą Pixiv.",
        "",
        "Przetwarzanie danych tokenów",
        "To narzędzie wysyła dane autoryzacyjne do oficjalnych",
        "punktów końcowych OAuth Pixiv w celu wymiany tokenów.",
        "",
        "Zbieranie danych i nadużycia",
        "Deweloper nie gromadzi, nie sprzedaje ani nie nadużywa",
        "Twoich danych uwierzytelniających Pixiv ani tokenów OAuth.",
        "",
        "Usługi stron trzecich",
        "Projekt może korzystać z usług takich jak GitHub, Vercel",
        "i punkty końcowe Pixiv.",
        "",
        "Twoja odpowiedzialność",
        "Jesteś odpowiedzialny za zabezpieczenie swojego urządzenia,",
        "przeglądarki, sieci i danych uwierzytelniających.",
        "",
        "Kontakt",
        "W sprawie wsparcia lub prywatności skorzystaj ze strony kontaktowej",
        "lub repozytorium GitHub projektu.",
    ],
    "zh": [
        "最后更新：2026年4月1日",
        "",
        "本网站是用于Pixiv OAuth令牌工作流程的独立开源工具。",
        "",
        "独立项目",
        "Pixiv OAuth Token是独立开发的，不是Pixiv的官方产品或服务。",
        "",
        "令牌数据处理方式",
        "此工具将授权数据提交到Pixiv官方OAuth端点",
        "以交换或刷新令牌。",
        "",
        "数据收集与滥用",
        "开发者不会故意收集、出售或滥用您的Pixiv",
        "凭据或OAuth令牌。",
        "",
        "第三方服务",
        "本项目可能使用GitHub、Vercel、Pixiv端点等服务。",
        "这些服务有各自的隐私政策。",
        "",
        "您的责任",
        "您负责保护自己的设备、浏览器、网络环境和账户凭据。",
        "",
        "联系方式",
        "如有支持或隐私问题，请使用联系页面或项目的GitHub仓库。",
    ],
    "kr": [
        "마지막 업데이트: 2026년 4월 1일",
        "",
        "이 사이트는 Pixiv OAuth 토큰 워크플로를 위한",
        "독립적인 오픈소스 유틸리티입니다.",
        "",
        "독립 프로젝트",
        "Pixiv OAuth Token은 독립적으로 개발되었으며 Pixiv의",
        "공식 제품이나 서비스가 아닙니다.",
        "",
        "토큰 데이터 처리 방법",
        "이 도구는 공식 Pixiv OAuth 엔드포인트에 인증 데이터를",
        "전송하여 토큰을 교환하거나 갱신합니다.",
        "",
        "데이터 수집 및 악용",
        "개발자는 귀하의 Pixiv 자격 증명이나 OAuth 토큰을",
        "의도적으로 수집, 판매 또는 악용하지 않습니다.",
        "",
        "타사 서비스",
        "이 프로젝트는 GitHub, Vercel, Pixiv 엔드포인트 등의",
        "서비스를 사용할 수 있습니다.",
        "",
        "귀하의 책임",
        "귀하의 기기, 브라우저, 네트워크 환경 및 계정 자격 증명의",
        "보안은 귀하의 책임입니다.",
        "",
        "문의",
        "지원이나 개인정보 관련 문의는 연락처 페이지 또는",
        "프로젝트의 GitHub 저장소를 이용하세요.",
    ],
}

TERMS_CONDITIONS_TEXT = {
    "en": [
        "Last updated: April 1, 2026",
        "",
        "By using this tool, you agree to these terms.",
        "",
        "Open-Source License",
        "This project is released under the MIT License. You are free",
        "to use, modify, and distribute it under those terms.",
        "",
        "No Warranty",
        "This tool is provided 'as is' without any warranty. The",
        "developer makes no guarantees about reliability, accuracy,",
        "or fitness for a particular purpose.",
        "",
        "Acceptable Use",
        "You agree to use this tool only for lawful purposes and in",
        "compliance with Pixiv's own Terms of Service.",
        "",
        "Third-Party Services",
        "Use of third-party services (GitHub, Vercel, Pixiv) is",
        "governed by their respective terms.",
        "",
        "Changes",
        "These terms may be updated at any time. Continued use",
        "implies acceptance of updated terms.",
        "",
        "Contact",
        "For questions, use the Contact page or the project's",
        "GitHub repository.",
    ],
    "id": [
        "Terakhir diperbarui: 1 April 2026",
        "",
        "Dengan menggunakan alat ini, Anda menyetujui syarat-syarat ini.",
        "",
        "Lisensi Open-Source",
        "Proyek ini dirilis di bawah Lisensi MIT. Anda bebas",
        "menggunakan, memodifikasi, dan mendistribusikannya.",
        "",
        "Tanpa Garansi",
        "Alat ini disediakan 'sebagaimana adanya' tanpa jaminan apa pun.",
        "Pengembang tidak memberikan jaminan keandalan atau akurasi.",
        "",
        "Penggunaan yang Diterima",
        "Anda setuju untuk menggunakan alat ini hanya untuk tujuan",
        "yang sah dan sesuai dengan Syarat Layanan Pixiv.",
        "",
        "Layanan Pihak Ketiga",
        "Penggunaan layanan pihak ketiga (GitHub, Vercel, Pixiv)",
        "diatur oleh ketentuan masing-masing layanan.",
        "",
        "Perubahan",
        "Syarat ini dapat diperbarui kapan saja. Penggunaan",
        "berkelanjutan berarti penerimaan syarat yang diperbarui.",
        "",
        "Kontak",
        "Untuk pertanyaan, gunakan halaman Kontak atau repositori",
        "GitHub proyek.",
    ],
    "jp": [
        "最終更新日: 2026年4月1日",
        "",
        "このツールを使用することで、これらの条件に同意したことになります。",
        "",
        "オープンソースライセンス",
        "このプロジェクトはMITライセンスの下でリリースされています。",
        "その条件の下で自由に使用、変更、配布できます。",
        "",
        "無保証",
        "このツールは保証なしで'現状のまま'提供されます。",
        "開発者は信頼性や正確性について保証しません。",
        "",
        "許容される使用",
        "このツールは合法的な目的のみに使用し、",
        "PixivのサービスのTerms of Serviceに準拠してください。",
        "",
        "サードパーティサービス",
        "サードパーティサービス(GitHub、Vercel、Pixiv)の使用は",
        "それぞれの利用規約に従います。",
        "",
        "変更",
        "これらの条件はいつでも更新される場合があります。",
        "継続的な使用は更新された条件の承認を意味します。",
        "",
        "お問い合わせ",
        "ご質問はお問い合わせページまたは",
        "GitHubリポジトリをご利用ください。",
    ],
    "de": [
        "Zuletzt aktualisiert: 1. April 2026",
        "",
        "Durch die Nutzung dieses Tools stimmen Sie diesen Bedingungen zu.",
        "",
        "Open-Source-Lizenz",
        "Dieses Projekt wird unter der MIT-Lizenz veröffentlicht.",
        "Sie können es frei verwenden, ändern und verteilen.",
        "",
        "Keine Gewährleistung",
        "Dieses Tool wird 'wie besehen' ohne jegliche Gewährleistung",
        "bereitgestellt. Keine Garantie für Zuverlässigkeit oder Genauigkeit.",
        "",
        "Akzeptable Nutzung",
        "Sie verpflichten sich, dieses Tool nur für rechtmäßige Zwecke",
        "und gemäß den Nutzungsbedingungen von Pixiv zu verwenden.",
        "",
        "Drittanbieterdienste",
        "Die Nutzung von Diensten wie GitHub, Vercel und Pixiv",
        "unterliegt deren jeweiligen Bedingungen.",
        "",
        "Änderungen",
        "Diese Bedingungen können jederzeit aktualisiert werden.",
        "Die weitere Nutzung bedeutet die Annahme der aktualisierten Bedingungen.",
        "",
        "Kontakt",
        "Bei Fragen nutzen Sie die Kontaktseite oder das",
        "GitHub-Repository des Projekts.",
    ],
    "fr": [
        "Dernière mise à jour: 1er avril 2026",
        "",
        "En utilisant cet outil, vous acceptez ces conditions.",
        "",
        "Licence open-source",
        "Ce projet est publié sous la licence MIT. Vous êtes libre",
        "de l'utiliser, le modifier et le distribuer.",
        "",
        "Aucune garantie",
        "Cet outil est fourni 'tel quel' sans aucune garantie.",
        "Aucune garantie sur la fiabilité ou la précision.",
        "",
        "Utilisation acceptable",
        "Vous acceptez d'utiliser cet outil uniquement à des fins",
        "légales et conformes aux Conditions d'utilisation de Pixiv.",
        "",
        "Services tiers",
        "L'utilisation des services tiers (GitHub, Vercel, Pixiv)",
        "est régie par leurs conditions respectives.",
        "",
        "Modifications",
        "Ces conditions peuvent être mises à jour à tout moment.",
        "L'utilisation continue implique l'acceptation des conditions mises à jour.",
        "",
        "Contact",
        "Pour toute question, utilisez la page de contact ou le",
        "dépôt GitHub du projet.",
    ],
    "es": [
        "Última actualización: 1 de abril de 2026",
        "",
        "Al usar esta herramienta, acepta estos términos.",
        "",
        "Licencia open-source",
        "Este proyecto se publica bajo la Licencia MIT. Puede usarlo,",
        "modificarlo y distribuirlo libremente.",
        "",
        "Sin garantía",
        "Esta herramienta se proporciona 'tal cual' sin ninguna garantía.",
        "No se garantiza fiabilidad ni precisión.",
        "",
        "Uso aceptable",
        "Acepta usar esta herramienta solo con fines legales y en",
        "conformidad con los Términos de Servicio de Pixiv.",
        "",
        "Servicios de terceros",
        "El uso de servicios de terceros (GitHub, Vercel, Pixiv)",
        "se rige por sus respectivos términos.",
        "",
        "Cambios",
        "Estos términos pueden actualizarse en cualquier momento.",
        "El uso continuo implica la aceptación de los términos actualizados.",
        "",
        "Contacto",
        "Para preguntas, use la página de contacto o el repositorio",
        "GitHub del proyecto.",
    ],
    "ru": [
        "Последнее обновление: 1 апреля 2026 г.",
        "",
        "Используя этот инструмент, вы соглашаетесь с данными условиями.",
        "",
        "Лицензия с открытым исходным кодом",
        "Этот проект выпущен под лицензией MIT. Вы можете свободно",
        "использовать, изменять и распространять его.",
        "",
        "Без гарантий",
        "Инструмент предоставляется 'как есть' без каких-либо гарантий.",
        "Нет гарантий надёжности или точности.",
        "",
        "Допустимое использование",
        "Вы соглашаетесь использовать инструмент только в законных целях",
        "и в соответствии с Условиями использования Pixiv.",
        "",
        "Сторонние сервисы",
        "Использование сторонних сервисов (GitHub, Vercel, Pixiv)",
        "регулируется их условиями.",
        "",
        "Изменения",
        "Эти условия могут обновляться в любое время.",
        "Продолжение использования означает принятие обновлённых условий.",
        "",
        "Контакт",
        "По вопросам используйте страницу контактов или",
        "репозиторий GitHub проекта.",
    ],
    "pt": [
        "Última atualização: 1 de abril de 2026",
        "",
        "Ao usar esta ferramenta, você concorda com estes termos.",
        "",
        "Licença open-source",
        "Este projeto é lançado sob a Licença MIT. Você pode",
        "usá-lo, modificá-lo e distribuí-lo livremente.",
        "",
        "Sem garantia",
        "Esta ferramenta é fornecida 'como está' sem qualquer garantia.",
        "Sem garantias de confiabilidade ou precisão.",
        "",
        "Uso aceitável",
        "Você concorda em usar esta ferramenta apenas para fins legais",
        "e em conformidade com os Termos de Serviço do Pixiv.",
        "",
        "Serviços de terceiros",
        "O uso de serviços de terceiros (GitHub, Vercel, Pixiv)",
        "é regido por seus respectivos termos.",
        "",
        "Alterações",
        "Estes termos podem ser atualizados a qualquer momento.",
        "O uso contínuo implica aceitação dos termos atualizados.",
        "",
        "Contato",
        "Para dúvidas, use a página de contato ou o repositório",
        "GitHub do projeto.",
    ],
    "pl": [
        "Ostatnia aktualizacja: 1 kwietnia 2026",
        "",
        "Korzystając z tego narzędzia, zgadzasz się na te warunki.",
        "",
        "Licencja open-source",
        "Ten projekt jest wydany na licencji MIT. Możesz go swobodnie",
        "używać, modyfikować i dystrybuować.",
        "",
        "Brak gwarancji",
        "Narzędzie jest dostarczane 'tak jak jest' bez żadnej gwarancji.",
        "Brak gwarancji niezawodności ani dokładności.",
        "",
        "Dopuszczalne użytkowanie",
        "Zgadzasz się używać narzędzia wyłącznie w celach zgodnych z prawem",
        "i zgodnie z Warunkami Korzystania z Serwisu Pixiv.",
        "",
        "Usługi stron trzecich",
        "Korzystanie z usług stron trzecich (GitHub, Vercel, Pixiv)",
        "podlega ich odpowiednim warunkom.",
        "",
        "Zmiany",
        "Warunki te mogą być aktualizowane w dowolnym czasie.",
        "Dalsze korzystanie oznacza akceptację zaktualizowanych warunków.",
        "",
        "Kontakt",
        "W przypadku pytań skorzystaj ze strony kontaktowej lub",
        "repozytorium GitHub projektu.",
    ],
    "zh": [
        "最后更新：2026年4月1日",
        "",
        "使用本工具即表示您同意这些条款。",
        "",
        "开源许可证",
        "本项目在MIT许可证下发布。您可以自由地使用、",
        "修改和分发它。",
        "",
        "无保证",
        "本工具按'原样'提供，不附带任何保证。",
        "不保证可靠性或准确性。",
        "",
        "可接受的使用",
        "您同意仅出于合法目的使用本工具，并遵守",
        "Pixiv的服务条款。",
        "",
        "第三方服务",
        "使用第三方服务（GitHub、Vercel、Pixiv）",
        "须遵守各自的条款。",
        "",
        "变更",
        "这些条款可能随时更新。继续使用即表示接受更新后的条款。",
        "",
        "联系方式",
        "如有问题，请使用联系页面或项目的GitHub仓库。",
    ],
    "kr": [
        "마지막 업데이트: 2026년 4월 1일",
        "",
        "이 도구를 사용함으로써 이 약관에 동의하게 됩니다.",
        "",
        "오픈소스 라이선스",
        "이 프로젝트는 MIT 라이선스로 출시됩니다. 해당 조건",
        "하에 자유롭게 사용, 수정 및 배포할 수 있습니다.",
        "",
        "무보증",
        "이 도구는 어떠한 보증도 없이 '있는 그대로' 제공됩니다.",
        "신뢰성이나 정확성에 대한 보증이 없습니다.",
        "",
        "허용 가능한 사용",
        "합법적인 목적으로만 이 도구를 사용하고 Pixiv의",
        "서비스 약관을 준수할 것에 동의합니다.",
        "",
        "타사 서비스",
        "타사 서비스(GitHub, Vercel, Pixiv) 사용은",
        "각각의 약관에 따릅니다.",
        "",
        "변경 사항",
        "이 약관은 언제든지 업데이트될 수 있습니다.",
        "계속 사용하면 업데이트된 약관에 동의하는 것으로 간주됩니다.",
        "",
        "문의",
        "질문이 있으시면 연락처 페이지 또는 프로젝트의",
        "GitHub 저장소를 이용하세요.",
    ],
}

MENU_UI_OVERRIDES = {'id': {'menu_title': 'Menu Utama',
        'opt_change_lang': 'Ubah Bahasa',
        'opt_tutorial': 'Tutorial',
        'opt_resources_docs': 'Sumber Daya & Dokumentasi',
        'opt_support': 'Dukungan',
        'opt_social': 'Sosial',
        'opt_login': 'Login',
        'opt_exit': 'Keluar',
        'select_option': 'Pilih opsi',
        'invalid_option': 'Opsi tidak valid.',
        'choose_lang': 'Pilih kode bahasa',
        'lang_updated': 'Bahasa default diperbarui menjadi',
        'resources_docs_title': 'Sumber Daya & Dokumentasi',
        'res_docs_documentation': 'Dokumentasi',
        'res_docs_license': 'Lisensi',
        'res_docs_pixiv': 'Endpoint OAuth Pixiv',
        'res_docs_python': 'Python 3.11+',
        'res_docs_vercel': 'Dijalankan di Vercel',
        'support_title': 'Dukungan',
        'sup_contact': 'Hubungi Kami',
        'sup_report': 'Laporkan Masalah',
        'sup_discussions': 'Diskusi',
        'sup_fatony': 'Fatony Ahmad Fauzi',
        'sup_donate': 'Dukungan / Donasi',
        'social_title': 'Tautan Sosial',
        'social_github': 'GitHub',
        'social_linkedin': 'LinkedIn',
        'back': 'Kembali',
        'tutorial_title': 'Tutorial CLI',
        'tutorial_desc': 'Ikuti langkah berikut untuk mendapatkan token Pixiv OAuth langsung dari CLI ini.',
        'tutorial_step1': '1) Pilih opsi [6] Login.',
        'tutorial_step2': '2) Browser akan terbuka ke halaman login Pixiv.',
        'tutorial_step3': '3) Setelah login, salin URL callback pixiv:// lengkap.',
        'tutorial_step4': '4) Paste URL/code pada prompt CLI.',
        'tutorial_step5': '5) CLI mendeteksi code dan menukar token.',
        'tutorial_step6': '6) access_token dan refresh_token ditampilkan.',
        'tutorial_example': 'Contoh output',
        'developer_info': 'Informasi Pengembang',
        'opt_debug': 'Alihkan Mode Debug',
        'debug_enabled': 'Mode debug sekarang DIAKTIFKAN.',
        'debug_disabled': 'Mode debug sekarang DINONAKTIFKAN.',
        'debug_current': 'Saat ini',
        'debug_title': 'Debug',
        'debug_copy': 'Salin debug',
        'debug_clear': 'Hapus debug',
        'debug_exit': 'Keluar',
        'debug_copied': 'Debug berhasil disalin.',
        'debug_copy_failed': 'Gagal menyalin debug.',
        'debug_cleared': 'Log debug berhasil dihapus.',
        'debug_empty': '(belum ada log debug)',
        'version_title': 'Versi',
        'version_check_update': 'Cek update',
        'version_update_now': 'Perbarui sekarang',
        'version_later': 'Nanti',
        'version_new_badge': 'Tersedia Versi Baru',
        'version_current': 'Versi saat ini',
        'version_latest_available': 'Versi terbaru tersedia',
        'version_latest': 'Versi saat ini sudah terbaru.',
        'version_no_internet_check': 'Tidak ada internet. Tidak bisa cek update.',
        'version_no_internet_update': 'Tidak ada internet. Update dibatalkan.',
        'version_update_success': 'Berhasil diperbarui. Versi saat ini',
        'version_update_failed': 'Update gagal. Silakan coba lagi.',
        'enter_main_menu': 'Enter untuk ke menu utama',
        'enter_continue': 'Enter untuk lanjut',
        'login_paste_prompt': 'Tempel link/code (Enter untuk batal)',
        'login_canceled': 'Login dibatalkan.',
        'login_actions_title': 'Aksi Login',
        'login_action_refresh': 'Refresh token',
        'login_action_copy_access': 'Salin access token',
        'login_action_copy_refresh': 'Salin refresh token',
        'login_action_refresh_success': 'Refresh token berhasil.',
        'login_action_refresh_failed': 'Refresh token gagal.',
        'login_action_access_copied': 'Access token berhasil disalin.',
        'login_action_access_copy_failed': 'Gagal menyalin access token.',
        'login_action_refresh_copied': 'Refresh token berhasil disalin.',
        'login_action_refresh_copy_failed': 'Gagal menyalin refresh token.',
        'exiting': 'Keluar...',
        'project': 'Pixiv OAuth Token',
        'developer': 'Pengembang',
        'opt_changelog': 'Catatan Perubahan',
        'opt_version': 'Versi',
        'res_docs_privacy': 'Kebijakan Privasi',
        'res_docs_terms': 'Syarat & Ketentuan',
        'privacy_title': 'Kebijakan Privasi',
        'terms_title': 'Syarat & Ketentuan'},
 'jp': {'menu_title': 'メインメニュー',
        'opt_change_lang': '言語を変更',
        'opt_tutorial': 'チュートリアル',
        'opt_resources_docs': 'リソースとドキュメント',
        'opt_support': 'サポート',
        'opt_social': 'ソーシャル',
        'opt_login': 'ログイン',
        'opt_changelog': '変更履歴',
        'opt_version': 'バージョン',
        'opt_exit': '終了',
        'select_option': 'オプションを選択',
        'invalid_option': '無効なオプションです。',
        'choose_lang': '言語コードを選択',
        'lang_updated': 'デフォルト言語が更新されました',
        'resources_docs_title': 'リソースとドキュメント',
        'res_docs_documentation': 'ドキュメント',
        'res_docs_license': 'ライセンス',
        'res_docs_pixiv': 'Pixiv OAuth エンドポイント',
        'res_docs_python': 'Python 3.11+',
        'res_docs_vercel': 'Vercelでデプロイ',
        'support_title': 'サポート',
        'sup_contact': 'お問い合わせ',
        'sup_report': '問題を報告',
        'sup_discussions': 'ディスカッション',
        'sup_fatony': 'Fatony Ahmad Fauzi',
        'sup_donate': 'サポート / 寄付',
        'social_title': 'ソーシャルリンク',
        'social_github': 'GitHub',
        'social_linkedin': 'LinkedIn',
        'back': '戻る',
        'tutorial_title': 'CLIチュートリアル',
        'tutorial_desc': 'これらのステップに従って、このCLIから直接Pixiv OAuthトークンを取得します。',
        'tutorial_step1': '1) オプション [6] Loginを選択します。',
        'tutorial_step2': '2) ブラウザがPixivログインページに開きます。',
        'tutorial_step3': '3) ログイン後、完全なpixiv:// URLコールバックをコピーします。',
        'tutorial_step4': '4) URLやコードをCLIプロンプトに貼り付けます。',
        'tutorial_step5': '5) CLIはコードを検出してトークンを交換します。',
        'tutorial_step6': '6) access_tokenおよびrefresh_tokenが表示されます。',
        'tutorial_example': '出力例',
        'developer_info': '開発者情報',
        'opt_debug': 'デバッグモードの切り替え',
        'debug_enabled': 'デバッグモードが【有効】になりました。',
        'debug_disabled': 'デバッグモードが【無効】になりました。',
        'debug_current': '現在',
        'debug_title': 'デバッグ',
        'debug_copy': 'デバッグをコピー',
        'debug_clear': 'デバッグをクリア',
        'debug_exit': '終了',
        'debug_copied': 'デバッグをコピーしました。',
        'debug_copy_failed': 'デバッグのコピーに失敗しました。',
        'debug_cleared': 'デバッグログを削除しました。',
        'debug_empty': '（デバッグログはまだありません）',
        'version_title': 'バージョン',
        'version_check_update': '更新を確認',
        'version_update_now': '今すぐ更新',
        'version_later': '後で',
        'version_new_badge': '新しいバージョンがあります',
        'version_current': '現在のバージョン',
        'version_latest_available': '最新バージョン',
        'version_latest': '現在のバージョンは最新です。',
        'version_no_internet_check': 'インターネット接続がありません。更新を確認できません。',
        'version_no_internet_update': 'インターネット接続がありません。更新を中止しました。',
        'version_update_success': '更新が完了しました。現在のバージョン',
        'version_update_failed': '更新に失敗しました。もう一度お試しください。',
        'enter_main_menu': 'Enterキーでメインメニューへ',
        'enter_continue': 'Enterキーで続行',
        'login_paste_prompt': 'リンクまたはコードを貼り付けてください（Enterでキャンセル）',
        'login_canceled': 'ログインをキャンセルしました。',
        'login_actions_title': 'ログイン操作',
        'login_action_refresh': 'トークンを更新',
        'login_action_copy_access': 'アクセストークンをコピー',
        'login_action_copy_refresh': 'リフレッシュトークンをコピー',
        'login_action_refresh_success': 'トークンの更新に成功しました。',
        'login_action_refresh_failed': 'トークンの更新に失敗しました。',
        'login_action_access_copied': 'アクセストークンをコピーしました。',
        'login_action_access_copy_failed': 'アクセストークンのコピーに失敗しました。',
        'login_action_refresh_copied': 'リフレッシュトークンをコピーしました。',
        'login_action_refresh_copy_failed': 'リフレッシュトークンのコピーに失敗しました。',
        'exiting': '終了しています...',
        'project': 'Pixiv OAuth Token',
        'developer': '開発者',
        'res_docs_privacy': 'プライバシーポリシー',
        'res_docs_terms': '利用規約',
        'privacy_title': 'プライバシーポリシー',
        'terms_title': '利用規約'},
 'pl': {'menu_title': 'Menu główne',
        'opt_change_lang': 'Zmień język',
        'opt_tutorial': 'Samouczek',
        'opt_resources_docs': 'Zasoby i dokumentacja',
        'opt_support': 'Wsparcie',
        'opt_social': 'Społeczne',
        'opt_login': 'Zaloguj się',
        'opt_exit': 'Wyjście',
        'select_option': 'Wybierz opcję',
        'invalid_option': 'Nieprawidłowa opcja.',
        'choose_lang': 'Wybierz kod języka',
        'lang_updated': 'Domyślny język został zaktualizowany na',
        'resources_docs_title': 'Zasoby i dokumentacja',
        'res_docs_documentation': 'Dokumentacja',
        'res_docs_license': 'Licencja',
        'res_docs_pixiv': 'Endpoint OAuth Pixiv',
        'res_docs_python': 'Python 3.11+',
        'res_docs_vercel': 'Wdrożone na Vercel',
        'support_title': 'Wsparcie',
        'sup_contact': 'Skontaktuj się z nami',
        'sup_report': 'Zgłoś problem',
        'sup_discussions': 'Dyskusje',
        'sup_fatony': 'Fatony Ahmad Fauzi',
        'sup_donate': 'Wsparcie / Darowizna',
        'social_title': 'Linki społeczne',
        'social_github': 'GitHub',
        'social_linkedin': 'LinkedIn',
        'back': 'Powrót',
        'tutorial_title': 'Samouczek CLI',
        'tutorial_desc': 'Postępuj zgodnie z tymi krokami, aby uzyskać tokeny Pixiv OAuth bezpośrednio z tego CLI.',
        'tutorial_step1': '1) Wybierz opcję [6] Zaloguj się.',
        'tutorial_step2': '2) Przeglądarka otwiera stronę logowania Pixiv.',
        'tutorial_step3': '3) Po zalogowaniu skopiuj pełny adres URL pixiv://.',
        'tutorial_step4': '4) Wklej adres URL/kod w monit CLI.',
        'tutorial_step5': '5) CLI wykrywa kod i wymienia token.',
        'tutorial_step6': '6) Wyświetlane są access_token i refresh_token.',
        'tutorial_example': 'Przykład wyniku',
        'developer_info': 'Informacje o deweloperze',
        'opt_debug': 'Przełącz tryb debugowania',
        'debug_enabled': 'Tryb debugowania jest teraz WŁĄCZONY.',
        'debug_disabled': 'Tryb debugowania jest teraz WYŁĄCZONY.',
        'debug_current': 'Obecny',
        'project': 'Pixiv OAuth Token',
        'developer': 'Deweloper',
        'opt_changelog': 'Dziennik zmian',
        'opt_version': 'Wersja',
        'debug_title': 'Debugowanie',
        'debug_copy': 'Kopiuj debug',
        'debug_clear': 'Wyczyść debug',
        'debug_exit': 'Wyjście',
        'debug_copied': 'Skopiowano log debug.',
        'debug_copy_failed': 'Nie udało się skopiować logu debug.',
        'debug_cleared': 'Wyczyszczono logi debug.',
        'debug_empty': '(brak logów debug)',
        'version_title': 'Wersja',
        'version_check_update': 'Sprawdź aktualizację',
        'version_update_now': 'Aktualizuj teraz',
        'version_later': 'Później',
        'version_new_badge': 'Dostępna nowa wersja',
        'version_current': 'Aktualna wersja',
        'version_latest_available': 'Najnowsza dostępna wersja',
        'version_latest': 'Aktualna wersja jest już najnowsza.',
        'version_no_internet_check': 'Brak połączenia z internetem. Nie można sprawdzić aktualizacji.',
        'version_no_internet_update': 'Brak połączenia z internetem. Aktualizacja anulowana.',
        'version_update_success': 'Aktualizacja zakończona sukcesem. Aktualna wersja',
        'version_update_failed': 'Aktualizacja nie powiodła się. Spróbuj ponownie.',
        'enter_main_menu': 'Enter, aby wrócić do menu głównego',
        'enter_continue': 'Enter, aby kontynuować',
        'login_paste_prompt': 'Wklej link/kod (Enter, aby anulować)',
        'login_canceled': 'Logowanie anulowane.',
        'login_actions_title': 'Akcje logowania',
        'login_action_refresh': 'Odśwież token',
        'login_action_copy_access': 'Kopiuj access token',
        'login_action_copy_refresh': 'Kopiuj refresh token',
        'login_action_refresh_success': 'Odświeżenie tokena zakończone sukcesem.',
        'login_action_refresh_failed': 'Odświeżenie tokena nie powiodło się.',
        'login_action_access_copied': 'Skopiowano access token.',
        'login_action_access_copy_failed': 'Nie udało się skopiować access token.',
        'login_action_refresh_copied': 'Skopiowano refresh token.',
        'login_action_refresh_copy_failed': 'Nie udało się skopiować refresh token.',
        'exiting': 'Zamykanie...',
        'res_docs_privacy': 'Polityka prywatności',
        'res_docs_terms': 'Regulamin',
        'privacy_title': 'Polityka prywatności',
        'terms_title': 'Regulamin'},
 'zh': {'menu_title': '主菜单',
        'opt_change_lang': '更改语言',
        'opt_tutorial': '教程',
        'opt_resources_docs': '资源和文档',
        'opt_support': '支持',
        'opt_social': '社交',
        'opt_login': '登录',
        'opt_exit': '退出',
        'select_option': '选择选项',
        'invalid_option': '无效选项。',
        'choose_lang': '选择语言代码',
        'lang_updated': '默认语言已更新为',
        'resources_docs_title': '资源和文档',
        'res_docs_documentation': '文档',
        'res_docs_license': '许可证',
        'res_docs_pixiv': 'Pixiv OAuth端点',
        'res_docs_python': 'Python 3.11+',
        'res_docs_vercel': '部署在Vercel上',
        'support_title': '支持',
        'sup_contact': '联系我们',
        'sup_report': '报告问题',
        'sup_discussions': '讨论',
        'sup_fatony': 'Fatony Ahmad Fauzi',
        'sup_donate': '支持 / 捐赠',
        'social_title': '社交链接',
        'social_github': 'GitHub',
        'social_linkedin': 'LinkedIn',
        'back': '返回',
        'tutorial_title': 'CLI教程',
        'tutorial_desc': '按照以下步骤直接从此CLI获取Pixiv OAuth令牌。',
        'tutorial_step1': '1) 选择选项 [6] 登录。',
        'tutorial_step2': '2) 浏览器打开Pixiv登录页面。',
        'tutorial_step3': '3) 登录后，复制完整的pixiv:// URL回调。',
        'tutorial_step4': '4) 将URL/代码粘贴到CLI提示中。',
        'tutorial_step5': '5) CLI检测代码并交换令牌。',
        'tutorial_step6': '6) 显示access_token和refresh_token。',
        'tutorial_example': '输出示例',
        'developer_info': '开发者信息',
        'opt_debug': '切换调试模式',
        'debug_enabled': '调试模式现在已启用。',
        'debug_disabled': '调试模式现在已禁用。',
        'debug_current': '当前',
        'project': 'Pixiv OAuth Token',
        'developer': '开发者',
        'opt_changelog': '更新日志',
        'opt_version': '版本',
        'debug_title': '调试',
        'debug_copy': '复制调试日志',
        'debug_clear': '清空调试日志',
        'debug_exit': '退出',
        'debug_copied': '调试日志已复制。',
        'debug_copy_failed': '复制调试日志失败。',
        'debug_cleared': '调试日志已清空。',
        'debug_empty': '（暂无调试日志）',
        'version_title': '版本',
        'version_check_update': '检查更新',
        'version_update_now': '立即更新',
        'version_later': '稍后',
        'version_new_badge': '有新版本可用',
        'version_current': '当前版本',
        'version_latest_available': '最新可用版本',
        'version_latest': '当前版本已是最新。',
        'version_no_internet_check': '无网络连接，无法检查更新。',
        'version_no_internet_update': '无网络连接，已取消更新。',
        'version_update_success': '更新成功。当前版本',
        'version_update_failed': '更新失败。请重试。',
        'enter_main_menu': '按 Enter 返回主菜单',
        'enter_continue': '按 Enter 继续',
        'login_paste_prompt': '粘贴链接/代码（按 Enter 取消）',
        'login_canceled': '已取消登录。',
        'login_actions_title': '登录操作',
        'login_action_refresh': '刷新令牌',
        'login_action_copy_access': '复制访问令牌',
        'login_action_copy_refresh': '复制刷新令牌',
        'login_action_refresh_success': '刷新令牌成功。',
        'login_action_refresh_failed': '刷新令牌失败。',
        'login_action_access_copied': '访问令牌已复制。',
        'login_action_access_copy_failed': '复制访问令牌失败。',
        'login_action_refresh_copied': '刷新令牌已复制。',
        'login_action_refresh_copy_failed': '复制刷新令牌失败。',
        'exiting': '正在退出...',
        'res_docs_privacy': '隐私政策',
        'res_docs_terms': '条款与条件',
        'privacy_title': '隐私政策',
        'terms_title': '条款与条件'},
 'de': {'menu_title': 'Hauptmenü',
        'opt_change_lang': 'Sprache ändern',
        'opt_tutorial': 'Anleitung',
        'opt_resources_docs': 'Ressourcen & Dokumentation',
        'opt_support': 'Unterstützung',
        'opt_social': 'Sozial',
        'opt_login': 'Anmelden',
        'opt_exit': 'Beenden',
        'select_option': 'Option wählen',
        'invalid_option': 'Ungültige Option.',
        'choose_lang': 'Sprachcode wählen',
        'lang_updated': 'Standardsprache wurde aktualisiert auf',
        'resources_docs_title': 'Ressourcen & Dokumentation',
        'res_docs_documentation': 'Dokumentation',
        'res_docs_license': 'Lizenz',
        'res_docs_pixiv': 'Pixiv OAuth Endpoint',
        'res_docs_python': 'Python 3.11+',
        'res_docs_vercel': 'Auf Vercel bereitgestellt',
        'support_title': 'Unterstützung',
        'sup_contact': 'Kontaktieren Sie uns',
        'sup_report': 'Problem melden',
        'sup_discussions': 'Diskussionen',
        'sup_fatony': 'Fatony Ahmad Fauzi',
        'sup_donate': 'Unterstützung / Spende',
        'social_title': 'Soziale Links',
        'social_github': 'GitHub',
        'social_linkedin': 'LinkedIn',
        'back': 'Zurück',
        'tutorial_title': 'CLI-Anleitung',
        'tutorial_desc': 'Befolgen Sie diese Schritte, um Pixiv OAuth-Token direkt von dieser CLI zu erhalten.',
        'tutorial_step1': '1) Wählen Sie Option [6] Anmelden.',
        'tutorial_step2': '2) Browser öffnet die Pixiv-Anmeldeseite.',
        'tutorial_step3': '3) Nach der Anmeldung die vollständige pixiv:// URL-Rückruf kopieren.',
        'tutorial_step4': '4) URL/Code in CLI-Eingabeaufforderung einfügen.',
        'tutorial_step5': '5) CLI erkennt den Code und tauscht das Token aus.',
        'tutorial_step6': '6) access_token und refresh_token werden angezeigt.',
        'tutorial_example': 'Ausgabebeispiel',
        'developer_info': 'Entwicklerinformationen',
        'opt_debug': 'Debug-Modus umschalten',
        'debug_enabled': 'Debug-Modus ist jetzt AKTIVIERT.',
        'debug_disabled': 'Debug-Modus ist jetzt DEAKTIVIERT.',
        'debug_current': 'Aktuell',
        'project': 'Pixiv OAuth Token',
        'developer': 'Entwickler',
        'opt_changelog': 'Änderungsprotokoll',
        'opt_version': 'Version',
        'debug_title': 'Debug',
        'debug_copy': 'Debug kopieren',
        'debug_clear': 'Debug leeren',
        'debug_exit': 'Beenden',
        'debug_copied': 'Debug wurde kopiert.',
        'debug_copy_failed': 'Debug konnte nicht kopiert werden.',
        'debug_cleared': 'Debug-Logs wurden gelöscht.',
        'debug_empty': '(noch keine Debug-Logs)',
        'version_title': 'Version',
        'version_check_update': 'Update prüfen',
        'version_update_now': 'Jetzt aktualisieren',
        'version_later': 'Später',
        'version_new_badge': 'Neue Version verfügbar',
        'version_current': 'Aktuelle Version',
        'version_latest_available': 'Neueste verfügbare Version',
        'version_latest': 'Die aktuelle Version ist bereits die neueste.',
        'version_no_internet_check': 'Keine Internetverbindung. Updateprüfung nicht möglich.',
        'version_no_internet_update': 'Keine Internetverbindung. Update abgebrochen.',
        'version_update_success': 'Update erfolgreich. Aktuelle Version',
        'version_update_failed': 'Update fehlgeschlagen. Bitte erneut versuchen.',
        'enter_main_menu': 'Enter für Hauptmenü',
        'enter_continue': 'Enter zum Fortfahren',
        'login_paste_prompt': 'Link/Code einfügen (Enter zum Abbrechen)',
        'login_canceled': 'Login abgebrochen.',
        'login_actions_title': 'Login-Aktionen',
        'login_action_refresh': 'Token aktualisieren',
        'login_action_copy_access': 'Access Token kopieren',
        'login_action_copy_refresh': 'Refresh Token kopieren',
        'login_action_refresh_success': 'Token erfolgreich aktualisiert.',
        'login_action_refresh_failed': 'Token-Aktualisierung fehlgeschlagen.',
        'login_action_access_copied': 'Access Token kopiert.',
        'login_action_access_copy_failed': 'Access Token konnte nicht kopiert werden.',
        'login_action_refresh_copied': 'Refresh Token kopiert.',
        'login_action_refresh_copy_failed': 'Refresh Token konnte nicht kopiert werden.',
        'exiting': 'Wird beendet...',
        'res_docs_privacy': 'Datenschutzrichtlinie',
        'res_docs_terms': 'Nutzungsbedingungen',
        'privacy_title': 'Datenschutzrichtlinie',
        'terms_title': 'Nutzungsbedingungen'},
 'fr': {'menu_title': 'Menu principal',
        'opt_change_lang': 'Changer la langue',
        'opt_tutorial': 'Tutoriel',
        'opt_resources_docs': 'Ressources et documentation',
        'opt_support': 'Soutien',
        'opt_social': 'Réseaux sociaux',
        'opt_login': 'Connexion',
        'opt_exit': 'Quitter',
        'select_option': 'Choisir une option',
        'invalid_option': 'Option invalide.',
        'choose_lang': 'Choisir le code de langue',
        'lang_updated': 'La langue par défaut a été mise à jour vers',
        'resources_docs_title': 'Ressources et documentation',
        'res_docs_documentation': 'Documentation',
        'res_docs_license': 'Licence',
        'res_docs_pixiv': 'Point de terminaison Pixiv OAuth',
        'res_docs_python': 'Python 3.11+',
        'res_docs_vercel': 'Déployé sur Vercel',
        'support_title': 'Soutien',
        'sup_contact': 'Contactez-nous',
        'sup_report': 'Signaler un problème',
        'sup_discussions': 'Discussions',
        'sup_fatony': 'Fatony Ahmad Fauzi',
        'sup_donate': 'Soutien / Donation',
        'social_title': 'Liens sociaux',
        'social_github': 'GitHub',
        'social_linkedin': 'LinkedIn',
        'back': 'Retour',
        'tutorial_title': 'Tutoriel CLI',
        'tutorial_desc': 'Suivez ces étapes pour obtenir les jetons Pixiv OAuth directement à partir de cette CLI.',
        'tutorial_step1': "1) Choisissez l'option [6] Connexion.",
        'tutorial_step2': '2) Le navigateur ouvre la page de connexion Pixiv.',
        'tutorial_step3': "3) Après la connexion, copiez l'URL de rappel complète pixiv://.",
        'tutorial_step4': "4) Collez l'URL/le code dans l'invite CLI.",
        'tutorial_step5': '5) CLI détecte le code et échange le token.',
        'tutorial_step6': '6) access_token et refresh_token sont affichés.',
        'tutorial_example': 'Exemple de sortie',
        'developer_info': 'Informations sur le développeur',
        'opt_debug': 'Basculer le mode débogage',
        'debug_enabled': 'Le mode débogage est maintenant ACTIVÉ.',
        'debug_disabled': 'Le mode débogage est maintenant DÉSACTIVÉ.',
        'debug_current': 'Actuel',
        'project': 'Pixiv OAuth Token',
        'developer': 'Développeur',
        'opt_changelog': 'Journal des modifications',
        'opt_version': 'Version',
        'debug_title': 'Debug',
        'debug_copy': 'Copier le debug',
        'debug_clear': 'Effacer le debug',
        'debug_exit': 'Quitter',
        'debug_copied': 'Debug copié.',
        'debug_copy_failed': 'Échec de la copie du debug.',
        'debug_cleared': 'Logs de debug effacés.',
        'debug_empty': '(pas encore de logs de debug)',
        'version_title': 'Version',
        'version_check_update': 'Vérifier la mise à jour',
        'version_update_now': 'Mettre à jour maintenant',
        'version_later': 'Plus tard',
        'version_new_badge': 'Nouvelle version disponible',
        'version_current': 'Version actuelle',
        'version_latest_available': 'Dernière version disponible',
        'version_latest': 'La version actuelle est déjà la dernière.',
        'version_no_internet_check': 'Pas de connexion internet. Impossible de vérifier la mise à jour.',
        'version_no_internet_update': 'Pas de connexion internet. Mise à jour annulée.',
        'version_update_success': 'Mise à jour réussie. Version actuelle',
        'version_update_failed': 'Échec de la mise à jour. Veuillez réessayer.',
        'enter_main_menu': 'Entrée pour revenir au menu principal',
        'enter_continue': 'Entrée pour continuer',
        'login_paste_prompt': 'Collez le lien/code (Entrée pour annuler)',
        'login_canceled': 'Connexion annulée.',
        'login_actions_title': 'Actions de connexion',
        'login_action_refresh': 'Rafraîchir le token',
        'login_action_copy_access': "Copier l'access token",
        'login_action_copy_refresh': 'Copier le refresh token',
        'login_action_refresh_success': 'Rafraîchissement du token réussi.',
        'login_action_refresh_failed': 'Échec du rafraîchissement du token.',
        'login_action_access_copied': 'Access token copié.',
        'login_action_access_copy_failed': "Échec de la copie de l'access token.",
        'login_action_refresh_copied': 'Refresh token copié.',
        'login_action_refresh_copy_failed': 'Échec de la copie du refresh token.',
        'exiting': 'Fermeture...',
        'res_docs_privacy': 'Politique de confidentialité',
        'res_docs_terms': 'Conditions générales',
        'privacy_title': 'Politique de confidentialité',
        'terms_title': 'Conditions générales'},
 'es': {'menu_title': 'Menú principal',
        'opt_change_lang': 'Cambiar idioma',
        'opt_tutorial': 'Tutorial',
        'opt_resources_docs': 'Recursos y documentación',
        'opt_support': 'Apoyo',
        'opt_social': 'Social',
        'opt_login': 'Iniciar sesión',
        'opt_exit': 'Salir',
        'select_option': 'Seleccionar opción',
        'invalid_option': 'Opción no válida.',
        'choose_lang': 'Elige código de idioma',
        'lang_updated': 'El idioma predeterminado se ha actualizado a',
        'resources_docs_title': 'Recursos y documentación',
        'res_docs_documentation': 'Documentación',
        'res_docs_license': 'Licencia',
        'res_docs_pixiv': 'Endpoint de OAuth de Pixiv',
        'res_docs_python': 'Python 3.11+',
        'res_docs_vercel': 'Implementado en Vercel',
        'support_title': 'Apoyo',
        'sup_contact': 'Contáctenos',
        'sup_report': 'Reportar un problema',
        'sup_discussions': 'Discusiones',
        'sup_fatony': 'Fatony Ahmad Fauzi',
        'sup_donate': 'Apoyo / Donación',
        'social_title': 'Enlaces sociales',
        'social_github': 'GitHub',
        'social_linkedin': 'LinkedIn',
        'back': 'Volver',
        'tutorial_title': 'Tutorial CLI',
        'tutorial_desc': 'Siga estos pasos para obtener tokens de OAuth de Pixiv directamente desde esta CLI.',
        'tutorial_step1': '1) Elija la opción [6] Iniciar sesión.',
        'tutorial_step2': '2) El navegador abre la página de inicio de sesión de Pixiv.',
        'tutorial_step3': '3) Después de iniciar sesión, copie la devolución de llamada de URL pixiv://.',
        'tutorial_step4': '4) Pegue la URL/código en el indicador CLI.',
        'tutorial_step5': '5) CLI detecta el código e intercambia el token.',
        'tutorial_step6': '6) Se muestran access_token y refresh_token.',
        'tutorial_example': 'Salida de ejemplo',
        'developer_info': 'Información del desarrollador',
        'opt_debug': 'Alternar Modo Depuración',
        'debug_enabled': 'El modo de depuración ahora está ACTIVADO.',
        'debug_disabled': 'El modo de depuración ahora está DESACTIVADO.',
        'debug_current': 'Actual',
        'project': 'Pixiv OAuth Token',
        'developer': 'Desarrollador',
        'opt_changelog': 'Registro de cambios',
        'opt_version': 'Versión',
        'debug_title': 'Debug',
        'debug_copy': 'Copiar debug',
        'debug_clear': 'Limpiar debug',
        'debug_exit': 'Salir',
        'debug_copied': 'Debug copiado.',
        'debug_copy_failed': 'No se pudo copiar el debug.',
        'debug_cleared': 'Registros de debug borrados.',
        'debug_empty': '(aún no hay registros de debug)',
        'version_title': 'Versión',
        'version_check_update': 'Buscar actualización',
        'version_update_now': 'Actualizar ahora',
        'version_later': 'Más tarde',
        'version_new_badge': 'Nueva versión disponible',
        'version_current': 'Versión actual',
        'version_latest_available': 'Última versión disponible',
        'version_latest': 'La versión actual ya es la más reciente.',
        'version_no_internet_check': 'Sin conexión a internet. No se puede buscar actualización.',
        'version_no_internet_update': 'Sin conexión a internet. Actualización cancelada.',
        'version_update_success': 'Actualizado correctamente. Versión actual',
        'version_update_failed': 'La actualización falló. Inténtalo de nuevo.',
        'enter_main_menu': 'Enter para volver al menú principal',
        'enter_continue': 'Enter para continuar',
        'login_paste_prompt': 'Pega enlace/código (Enter para cancelar)',
        'login_canceled': 'Inicio de sesión cancelado.',
        'login_actions_title': 'Acciones de inicio de sesión',
        'login_action_refresh': 'Actualizar token',
        'login_action_copy_access': 'Copiar access token',
        'login_action_copy_refresh': 'Copiar refresh token',
        'login_action_refresh_success': 'Token actualizado correctamente.',
        'login_action_refresh_failed': 'Error al actualizar el token.',
        'login_action_access_copied': 'Access token copiado.',
        'login_action_access_copy_failed': 'Error al copiar el access token.',
        'login_action_refresh_copied': 'Refresh token copiado.',
        'login_action_refresh_copy_failed': 'Error al copiar el refresh token.',
        'exiting': 'Saliendo...',
        'res_docs_privacy': 'Política de privacidad',
        'res_docs_terms': 'Términos y condiciones',
        'privacy_title': 'Política de privacidad',
        'terms_title': 'Términos y condiciones'},
 'ru': {'menu_title': 'Главное меню',
        'opt_change_lang': 'Изменить язык',
        'opt_tutorial': 'Руководство',
        'opt_resources_docs': 'Ресурсы и документация',
        'opt_support': 'Поддержка',
        'opt_social': 'Социальные сети',
        'opt_login': 'Вход',
        'opt_exit': 'Выход',
        'select_option': 'Выберите опцию',
        'invalid_option': 'Неверная опция.',
        'choose_lang': 'Выберите код языка',
        'lang_updated': 'Язык по умолчанию был обновлен на',
        'resources_docs_title': 'Ресурсы и документация',
        'res_docs_documentation': 'Документация',
        'res_docs_license': 'Лицензия',
        'res_docs_pixiv': 'Конечная точка OAuth Pixiv',
        'res_docs_python': 'Python 3.11+',
        'res_docs_vercel': 'Развернуто на Vercel',
        'support_title': 'Поддержка',
        'sup_contact': 'Свяжитесь с нами',
        'sup_report': 'Сообщить о проблеме',
        'sup_discussions': 'Обсуждения',
        'sup_fatony': 'Fatony Ahmad Fauzi',
        'sup_donate': 'Поддержка / Пожертвование',
        'social_title': 'Социальные ссылки',
        'social_github': 'GitHub',
        'social_linkedin': 'LinkedIn',
        'back': 'Назад',
        'tutorial_title': 'Руководство CLI',
        'tutorial_desc': 'Следуйте этим шагам, чтобы получить токены Pixiv OAuth прямо из этого CLI.',
        'tutorial_step1': '1) Выберите опцию [6] Вход.',
        'tutorial_step2': '2) Браузер открывает страницу входа Pixiv.',
        'tutorial_step3': '3) После входа скопируйте полный URL обратного вызова pixiv://.',
        'tutorial_step4': '4) Вставьте URL/код в командную строку CLI.',
        'tutorial_step5': '5) CLI обнаруживает код и обменивает токен.',
        'tutorial_step6': '6) Отображаются access_token и refresh_token.',
        'tutorial_example': 'Пример вывода',
        'developer_info': 'Информация о разработчике',
        'opt_debug': 'Переключить режим отладки',
        'debug_enabled': 'Режим отладки теперь ВКЛЮЧЕН.',
        'debug_disabled': 'Режим отладки теперь ВЫКЛЮЧЕН.',
        'debug_current': 'Текущий',
        'project': 'Pixiv OAuth Token',
        'developer': 'Разработчик',
        'opt_changelog': 'Список изменений',
        'opt_version': 'Версия',
        'debug_title': 'Отладка',
        'debug_copy': 'Копировать отладку',
        'debug_clear': 'Очистить отладку',
        'debug_exit': 'Выход',
        'debug_copied': 'Отладочные данные скопированы.',
        'debug_copy_failed': 'Не удалось скопировать отладочные данные.',
        'debug_cleared': 'Журнал отладки очищен.',
        'debug_empty': '(пока нет отладочных записей)',
        'version_title': 'Версия',
        'version_check_update': 'Проверить обновление',
        'version_update_now': 'Обновить сейчас',
        'version_later': 'Позже',
        'version_new_badge': 'Доступна новая версия',
        'version_current': 'Текущая версия',
        'version_latest_available': 'Последняя доступная версия',
        'version_latest': 'Текущая версия уже самая новая.',
        'version_no_internet_check': 'Нет подключения к интернету. Невозможно проверить обновление.',
        'version_no_internet_update': 'Нет подключения к интернету. Обновление отменено.',
        'version_update_success': 'Обновление успешно завершено. Текущая версия',
        'version_update_failed': 'Не удалось обновить. Попробуйте снова.',
        'enter_main_menu': 'Enter для перехода в главное меню',
        'enter_continue': 'Enter для продолжения',
        'login_paste_prompt': 'Вставьте ссылку/код (Enter для отмены)',
        'login_canceled': 'Вход отменен.',
        'login_actions_title': 'Действия входа',
        'login_action_refresh': 'Обновить токен',
        'login_action_copy_access': 'Копировать access token',
        'login_action_copy_refresh': 'Копировать refresh token',
        'login_action_refresh_success': 'Токен успешно обновлен.',
        'login_action_refresh_failed': 'Не удалось обновить токен.',
        'login_action_access_copied': 'Access token скопирован.',
        'login_action_access_copy_failed': 'Не удалось скопировать access token.',
        'login_action_refresh_copied': 'Refresh token скопирован.',
        'login_action_refresh_copy_failed': 'Не удалось скопировать refresh token.',
        'exiting': 'Выход...',
        'res_docs_privacy': 'Политика конфиденциальности',
        'res_docs_terms': 'Условия использования',
        'privacy_title': 'Политика конфиденциальности',
        'terms_title': 'Условия использования'},
 'pt': {'menu_title': 'Menu principal',
        'opt_change_lang': 'Mudar idioma',
        'opt_tutorial': 'Tutorial',
        'opt_resources_docs': 'Recursos e documentação',
        'opt_support': 'Suporte',
        'opt_social': 'Social',
        'opt_login': 'Entrar',
        'opt_exit': 'Sair',
        'select_option': 'Selecione uma opção',
        'invalid_option': 'Opção inválida.',
        'choose_lang': 'Escolha o código de idioma',
        'lang_updated': 'O idioma padrão foi atualizado para',
        'resources_docs_title': 'Recursos e documentação',
        'res_docs_documentation': 'Documentação',
        'res_docs_license': 'Licença',
        'res_docs_pixiv': 'Endpoint OAuth Pixiv',
        'res_docs_python': 'Python 3.11+',
        'res_docs_vercel': 'Implantado no Vercel',
        'support_title': 'Suporte',
        'sup_contact': 'Entre em contato conosco',
        'sup_report': 'Relatar um problema',
        'sup_discussions': 'Discussões',
        'sup_fatony': 'Fatony Ahmad Fauzi',
        'sup_donate': 'Suporte / Doação',
        'social_title': 'Links sociais',
        'social_github': 'GitHub',
        'social_linkedin': 'LinkedIn',
        'back': 'Voltar',
        'tutorial_title': 'Tutorial da CLI',
        'tutorial_desc': 'Siga estas etapas para obter tokens Pixiv OAuth diretamente deste CLI.',
        'tutorial_step1': '1) Escolha a opção [6] Entrar.',
        'tutorial_step2': '2) O navegador abre a página de login do Pixiv.',
        'tutorial_step3': '3) Após o login, copie o URL de retorno completo pixiv://.',
        'tutorial_step4': '4) Cole URL/código no prompt da CLI.',
        'tutorial_step5': '5) CLI detecta o código e troca o token.',
        'tutorial_step6': '6) access_token e refresh_token são exibidos.',
        'tutorial_example': 'Exemplo de saída',
        'developer_info': 'Informações do desenvolvedor',
        'opt_debug': 'Alternar Modo de Depuração',
        'debug_enabled': 'O modo de depuração agora está ATIVADO.',
        'debug_disabled': 'O modo de depuração agora está DESATIVADO.',
        'debug_current': 'Atual',
        'project': 'Pixiv OAuth Token',
        'developer': 'Desenvolvedor',
        'opt_changelog': 'Registro de alterações',
        'opt_version': 'Versão',
        'debug_title': 'Debug',
        'debug_copy': 'Copiar debug',
        'debug_clear': 'Limpar debug',
        'debug_exit': 'Sair',
        'debug_copied': 'Debug copiado.',
        'debug_copy_failed': 'Falha ao copiar debug.',
        'debug_cleared': 'Logs de debug limpos.',
        'debug_empty': '(ainda não há logs de debug)',
        'version_title': 'Versão',
        'version_check_update': 'Verificar atualização',
        'version_update_now': 'Atualizar agora',
        'version_later': 'Depois',
        'version_new_badge': 'Nova versão disponível',
        'version_current': 'Versão atual',
        'version_latest_available': 'Última versão disponível',
        'version_latest': 'A versão atual já é a mais recente.',
        'version_no_internet_check': 'Sem conexão com a internet. Não é possível verificar atualização.',
        'version_no_internet_update': 'Sem conexão com a internet. Atualização cancelada.',
        'version_update_success': 'Atualizado com sucesso. Versão atual',
        'version_update_failed': 'Falha na atualização. Tente novamente.',
        'enter_main_menu': 'Enter para voltar ao menu principal',
        'enter_continue': 'Enter para continuar',
        'login_paste_prompt': 'Cole o link/código (Enter para cancelar)',
        'login_canceled': 'Login cancelado.',
        'login_actions_title': 'Ações de login',
        'login_action_refresh': 'Atualizar token',
        'login_action_copy_access': 'Copiar access token',
        'login_action_copy_refresh': 'Copiar refresh token',
        'login_action_refresh_success': 'Token atualizado com sucesso.',
        'login_action_refresh_failed': 'Falha ao atualizar token.',
        'login_action_access_copied': 'Access token copiado.',
        'login_action_access_copy_failed': 'Falha ao copiar access token.',
        'login_action_refresh_copied': 'Refresh token copiado.',
        'login_action_refresh_copy_failed': 'Falha ao copiar refresh token.',
        'exiting': 'Saindo...',
        'res_docs_privacy': 'Política de Privacidade',
        'res_docs_terms': 'Termos e Condições',
        'privacy_title': 'Política de Privacidade',
        'terms_title': 'Termos e Condições'},
 'kr': {'menu_title': '메인 메뉴',
        'opt_change_lang': '언어 변경',
        'opt_tutorial': '튜토리얼',
        'opt_resources_docs': '리소스 및 문서',
        'opt_support': '지원',
        'opt_social': '소셜',
        'opt_login': '로그인',
        'opt_exit': '종료',
        'select_option': '옵션 선택',
        'invalid_option': '잘못된 옵션입니다.',
        'choose_lang': '언어 코드 선택',
        'lang_updated': '기본 언어가 다음으로 업데이트되었습니다',
        'resources_docs_title': '리소스 및 문서',
        'res_docs_documentation': '문서',
        'res_docs_license': '라이센스',
        'res_docs_pixiv': 'Pixiv OAuth 엔드포인트',
        'res_docs_python': 'Python 3.11+',
        'res_docs_vercel': 'Vercel에 배포됨',
        'support_title': '지원',
        'sup_contact': '문의하기',
        'sup_report': '문제 보고',
        'sup_discussions': '토론',
        'sup_fatony': 'Fatony Ahmad Fauzi',
        'sup_donate': '지원 / 기부',
        'social_title': '소셜 링크',
        'social_github': 'GitHub',
        'social_linkedin': 'LinkedIn',
        'back': '뒤로',
        'tutorial_title': 'CLI 튜토리얼',
        'tutorial_desc': '이 단계를 따라 이 CLI에서 직접 Pixiv OAuth 토큰을 얻으십시오.',
        'tutorial_step1': '1) 옵션 [6] 로그인을 선택합니다.',
        'tutorial_step2': '2) 브라우저가 Pixiv 로그인 페이지를 엽니다.',
        'tutorial_step3': '3) 로그인 후 전체 pixiv:// URL 콜백을 복사합니다.',
        'tutorial_step4': '4) CLI 프롬프트에 URL/코드를 붙여넣습니다.',
        'tutorial_step5': '5) CLI가 코드를 감지하고 토큰을 교환합니다.',
        'tutorial_step6': '6) access_token 및 refresh_token이 표시됩니다.',
        'tutorial_example': '출력 예시',
        'developer_info': '개발자 정보',
        'opt_debug': '디버그 모드 전환',
        'debug_enabled': '디버그 모드가 이제 활성화되었습니다.',
        'debug_disabled': '디버그 모드가 이제 비활성화되었습니다.',
        'debug_current': '현재',
        'project': 'Pixiv OAuth Token',
        'developer': '개발자',
        'opt_changelog': '변경 로그',
        'opt_version': '버전',
        'debug_title': '디버그',
        'debug_copy': '디버그 복사',
        'debug_clear': '디버그 지우기',
        'debug_exit': '종료',
        'debug_copied': '디버그가 복사되었습니다.',
        'debug_copy_failed': '디버그 복사에 실패했습니다.',
        'debug_cleared': '디버그 로그를 지웠습니다.',
        'debug_empty': '(아직 디버그 로그가 없습니다)',
        'version_title': '버전',
        'version_check_update': '업데이트 확인',
        'version_update_now': '지금 업데이트',
        'version_later': '나중에',
        'version_new_badge': '새 버전 사용 가능',
        'version_current': '현재 버전',
        'version_latest_available': '최신 버전',
        'version_latest': '현재 버전이 이미 최신입니다.',
        'version_no_internet_check': '인터넷 연결이 없어 업데이트를 확인할 수 없습니다.',
        'version_no_internet_update': '인터넷 연결이 없어 업데이트를 취소했습니다.',
        'version_update_success': '업데이트 성공. 현재 버전',
        'version_update_failed': '업데이트 실패. 다시 시도하세요.',
        'enter_main_menu': 'Enter를 눌러 메인 메뉴로',
        'enter_continue': 'Enter를 눌러 계속',
        'login_paste_prompt': '링크/코드를 붙여넣으세요 (Enter로 취소)',
        'login_canceled': '로그인이 취소되었습니다.',
        'login_actions_title': '로그인 작업',
        'login_action_refresh': '토큰 갱신',
        'login_action_copy_access': '액세스 토큰 복사',
        'login_action_copy_refresh': '리프레시 토큰 복사',
        'login_action_refresh_success': '토큰 갱신 성공.',
        'login_action_refresh_failed': '토큰 갱신 실패.',
        'login_action_access_copied': '액세스 토큰이 복사되었습니다.',
        'login_action_access_copy_failed': '액세스 토큰 복사 실패.',
        'login_action_refresh_copied': '리프레시 토큰이 복사되었습니다.',
        'login_action_refresh_copy_failed': '리프레시 토큰 복사 실패.',
        'exiting': '종료 중...',
        'res_docs_privacy': '개인정보 처리방침',
        'res_docs_terms': '이용 약관',
        'privacy_title': '개인정보 처리방침',
        'terms_title': '이용 약관'}}

MENU_UI = {code: {**MENU_UI_EN, **MENU_UI_OVERRIDES.get(code, {})} for code in SUPPORTED_LANGS}


def mt(key: str, lang: str) -> str:
    return MENU_UI.get(lang, MENU_UI_EN).get(key, MENU_UI_EN.get(key, key))


def _rich_available() -> bool:
    return False


def _menu_console() -> None:
    pass  # rich removed; no-op


def _clear_menu_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def _build_menu_options(lang: str) -> list[tuple[str, str, str]]:
    latest = _fetch_latest_release_tag_cached()
    latest_code = _get_latest_release_code_cached()
    version_label = mt("opt_version", lang)
    if latest and (latest != get_current_app_version() or (latest_code and latest_code != get_current_app_code())):
        version_label = f"{version_label} ({mt('version_new_badge', lang)} {latest})"
    return [
        ("1", mt("opt_change_lang", lang), "green"),
        ("2", mt("opt_tutorial", lang), "green"),
        ("3", mt("opt_resources_docs", lang), "green"),
        ("4", mt("opt_support", lang), "green"),
        ("5", mt("opt_social", lang), "green"),
        ("6", mt("opt_login", lang), "green"),
        ("7", version_label, "green"),
        ("8", mt("debug_title", lang), "magenta"),
        ("0", mt("opt_exit", lang), "white"),
    ]


def _render_rich_option_panel(title: str, options: list[tuple[str, str]], prompt: str) -> str:
    _clear_menu_screen()
    print(colorize(f"{title}", Ansi.CYAN + Ansi.BOLD, True))
    print()
    for key, label in options:
        color = Ansi.DIM if key == "0" else Ansi.GREEN
        print(colorize(f"[{key}] {label}", color, True))
    return input(colorize(f"\n[+] {prompt}: ", Ansi.YELLOW, True)).strip()


def _render_rich_text_panel(title: str, lines: list[str], prompt: str | None = None) -> str | None:
    _clear_menu_screen()
    print(colorize(f"{title}", Ansi.CYAN + Ansi.BOLD, True))
    print()
    print("\n".join(lines))
    if prompt is None:
        return None
    return input(colorize(f"\n[+] {prompt}: ", Ansi.YELLOW, True)).strip()


def _render_rich_combined_panel(
    title: str,
    lines: list[str],
    options: list[tuple[str, str]],
    prompt: str,
) -> str:
    _clear_menu_screen()
    print(colorize(f"{title}", Ansi.CYAN + Ansi.BOLD, True))
    print()
    if lines:
        print("\n".join(lines))
        print()
    for key, label in options:
        color = Ansi.DIM if key == "0" else Ansi.GREEN
        print(colorize(f"[{key}] {label}", color, True))
    return input(colorize(f"\n[+] {prompt}: ", Ansi.YELLOW, True)).strip()


def _choose_boxed_option(title: str, options: list[tuple[str, str]], lang: str, color_on: bool) -> str:
    return _render_rich_option_panel(title, options, mt("select_option", lang))


def _render_rich_main_menu(lang: str) -> None:
    _clear_menu_screen()
    print_cli_banner(lang, True)
    print(colorize(mt('menu_title', lang), Ansi.CYAN + Ansi.BOLD, True))
    print()
    for key, label, style in _build_menu_options(lang):
        ansi_style = {"green": Ansi.GREEN, "magenta": Ansi.MAGENTA, "white": Ansi.DIM}.get(style, Ansi.GREEN)
        print(colorize(f"[{key}] {label}", ansi_style, True))

def print_cli_banner(lang: str, color_on: bool) -> None:
    print(colorize(f"{mt('project', lang)}", Ansi.BOLD, color_on))
    print(colorize(f"{mt('developer', lang)}: {DEVELOPER_NAME}", Ansi.DIM, color_on))
    print()


def _choose_language_interactive(current_lang: str, color_on: bool) -> str:
    global DEBUG_LANG
    debug_print(_dbg_msg("open_language_selector", lang=current_lang), color_on)
    lines = [f"[{code}] {LANG_NAMES.get(code, LANG_LABELS.get(code, code))}" for code in SUPPORTED_LANGS]
    prompt = f"{mt('choose_lang', current_lang)} ({CANCEL_HINT.get(current_lang, CANCEL_HINT['en'])})"
    new_lang = _render_rich_text_panel(mt("opt_change_lang", current_lang), lines, prompt)
    new_lang = (new_lang or "").strip().lower()
    debug_print(_dbg_msg("language_selector_input", value=new_lang), color_on)
    if new_lang == "":
        debug_print(_dbg_msg("language_change_canceled"), color_on)
        return current_lang
    if new_lang not in SUPPORTED_LANGS:
        print(colorize(mt("invalid_option", current_lang), Ansi.RED, color_on))
        debug_print(f"Invalid language selection: {new_lang}", color_on)
        return current_lang
    set_default_lang(new_lang)
    DEBUG_LANG = new_lang
    print(colorize(f"{mt('lang_updated', new_lang)} {new_lang}", Ansi.GREEN, color_on))
    debug_print(_dbg_msg("language_updated", lang=new_lang), color_on)
    return new_lang


def _open_privacy_policy_cli(lang: str, color_on: bool) -> None:
    debug_print(f"Opening privacy policy CLI view (lang={lang})", color_on)
    lines = PRIVACY_POLICY_TEXT.get(lang) or PRIVACY_POLICY_TEXT["en"]
    _render_rich_text_panel(mt("privacy_title", lang), lines, mt("enter_main_menu", lang))


def _open_terms_conditions_cli(lang: str, color_on: bool) -> None:
    debug_print(f"Opening terms & conditions CLI view (lang={lang})", color_on)
    lines = TERMS_CONDITIONS_TEXT.get(lang) or TERMS_CONDITIONS_TEXT["en"]
    _render_rich_text_panel(mt("terms_title", lang), lines, mt("enter_main_menu", lang))


# ===== GITHUB RAW CONTENT VIEWER =====
_GITHUB_RAW_BASE = "https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master"
_GITHUB_LANG_DOCS_PATH = "web/public/docs/lang"

# Languages that have localized doc files (suffix = LANG-CODE uppercased)
_GITHUB_LANG_DOC_SUFFIX: dict[str, str] = {
    "id": "ID",
    "jp": "JP",
    "de": "DE",
    "fr": "FR",
    "es": "ES",
    "ru": "RU",
    "pt": "PT",
    "pl": "PL",
    "zh": "ZH",
    "kr": "KR",
}


def _get_localized_doc_url(file_name: str, lang: str) -> tuple[str, str]:
    """Return (localized_url, default_english_url) for a doc file."""
    suffix = _GITHUB_LANG_DOC_SUFFIX.get(lang)
    base = _GITHUB_RAW_BASE
    path = _GITHUB_LANG_DOCS_PATH
    default_url = f"{base}/{path}/{file_name}"
    if suffix:
        localized_url = f"{base}/{path}/{file_name}-{suffix}"
    else:
        localized_url = default_url
    return localized_url, default_url

_FETCH_LABELS = {
    "en": {
        "fetching": "Fetching content from GitHub...",
        "fetch_failed": "Failed to fetch content. Check your internet connection.",
        "page_prompt": "[Enter] Next page  [q] Quit  [t] Top",
        "end_of_doc": "-- End of document --",
    },
    "id": {
        "fetching": "Mengambil konten dari GitHub...",
        "fetch_failed": "Gagal mengambil konten. Periksa koneksi internet Anda.",
        "page_prompt": "[Enter] Halaman berikutnya  [q] Keluar  [t] Atas",
        "end_of_doc": "-- Akhir dokumen --",
    },
    "jp": {
        "fetching": "GitHubからコンテンツを取得中...",
        "fetch_failed": "コンテンツの取得に失敗しました。インターネット接続を確認してください。",
        "page_prompt": "[Enter] 次のページ  [q] 終了  [t] 先頭",
        "end_of_doc": "-- ドキュメントの終わり --",
    },
    "de": {
        "fetching": "Inhalt von GitHub wird abgerufen...",
        "fetch_failed": "Inhalt konnte nicht abgerufen werden. Internetverbindung prüfen.",
        "page_prompt": "[Enter] Nächste Seite  [q] Beenden  [t] Anfang",
        "end_of_doc": "-- Ende des Dokuments --",
    },
    "fr": {
        "fetching": "Récupération du contenu depuis GitHub...",
        "fetch_failed": "Échec de la récupération. Vérifiez votre connexion internet.",
        "page_prompt": "[Enter] Page suivante  [q] Quitter  [t] Début",
        "end_of_doc": "-- Fin du document --",
    },
    "es": {
        "fetching": "Obteniendo contenido de GitHub...",
        "fetch_failed": "Error al obtener el contenido. Verifique su conexión.",
        "page_prompt": "[Enter] Siguiente página  [q] Salir  [t] Inicio",
        "end_of_doc": "-- Fin del documento --",
    },
    "ru": {
        "fetching": "Загрузка содержимого с GitHub...",
        "fetch_failed": "Не удалось загрузить содержимое. Проверьте подключение к интернету.",
        "page_prompt": "[Enter] Следующая страница  [q] Выход  [t] Начало",
        "end_of_doc": "-- Конец документа --",
    },
    "pt": {
        "fetching": "Buscando conteúdo do GitHub...",
        "fetch_failed": "Falha ao buscar conteúdo. Verifique sua conexão.",
        "page_prompt": "[Enter] Próxima página  [q] Sair  [t] Início",
        "end_of_doc": "-- Fim do documento --",
    },
    "pl": {
        "fetching": "Pobieranie treści z GitHub...",
        "fetch_failed": "Nie udało się pobrać treści. Sprawdź połączenie z internetem.",
        "page_prompt": "[Enter] Następna strona  [q] Wyjdź  [t] Góra",
        "end_of_doc": "-- Koniec dokumentu --",
    },
    "zh": {
        "fetching": "正在从GitHub获取内容...",
        "fetch_failed": "获取内容失败。请检查您的网络连接。",
        "page_prompt": "[Enter] 下一页  [q] 退出  [t] 顶部",
        "end_of_doc": "-- 文档结尾 --",
    },
    "kr": {
        "fetching": "GitHub에서 콘텐츠를 가져오는 중...",
        "fetch_failed": "콘텐츠를 가져오는 데 실패했습니다. 인터넷 연결을 확인하세요.",
        "page_prompt": "[Enter] 다음 페이지  [q] 종료  [t] 처음",
        "end_of_doc": "-- 문서 끝 --",
    },
}


def _fl(key: str, lang: str) -> str:
    """Get fetch label string for given lang."""
    return _FETCH_LABELS.get(lang, _FETCH_LABELS["en"]).get(key, _FETCH_LABELS["en"][key])


def _fetch_github_raw(url: str, lang: str, color_on: bool, fallback_url: str | None = None) -> str | None:
    """Fetch raw text from URL, return content string or None on failure.
    If the primary URL returns 404, try fallback_url before giving up.
    """
    _clear_menu_screen()
    print(colorize(_fl("fetching", lang), Ansi.CYAN, color_on))
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 404 and fallback_url:
            debug_print(f"404 for {url}, trying fallback: {fallback_url}")
            resp = requests.get(fallback_url, timeout=15)
        resp.raise_for_status()
        return resp.text
    except Exception as exc:
        debug_print(f"Fetch failed for {url}: {exc}")
        print(colorize(_fl("fetch_failed", lang), Ansi.RED, color_on))
        input(colorize(f"\n[+] {mt('enter_continue', lang)}: ", Ansi.YELLOW, color_on))
        return None


def _display_paged_github_content(title: str, content: str, lang: str, color_on: bool) -> None:
    """Display fetched text content with paged navigation."""
    lines = content.splitlines()
    total = len(lines)
    page_size = 30
    pos = 0
    while True:
        _clear_menu_screen()
        print(colorize(f"{title}", Ansi.CYAN + Ansi.BOLD, color_on))
        print()
        chunk = lines[pos:pos + page_size]
        print("\n".join(chunk))
        print()
        at_end = (pos + page_size >= total)
        if at_end:
            print(colorize(_fl("end_of_doc", lang), Ansi.DIM, color_on))
            print(colorize(_fl("page_prompt", lang), Ansi.YELLOW, color_on))
        else:
            remaining = total - pos - page_size
            print(colorize(f"{_fl('page_prompt', lang)}  [{remaining} lines left]", Ansi.YELLOW, color_on))
        try:
            key = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return
        if key == "q":
            return
        elif key == "t":
            pos = 0
        elif at_end:
            return
        else:
            pos = min(pos + page_size, max(0, total - page_size))


def _open_resources_docs_menu(lang: str, color_on: bool) -> None:
    options = [
        ("1", mt("res_docs_documentation", lang)),
        ("2", mt("opt_changelog", lang)),
        ("3", mt("res_docs_license", lang)),
        ("4", mt("res_docs_privacy", lang)),
        ("5", mt("res_docs_terms", lang)),
        ("6", mt("res_docs_pixiv", lang)),
        ("7", mt("res_docs_python", lang)),
        ("8", mt("res_docs_vercel", lang)),
        ("0", mt("back", lang)),
    ]
    while True:
        choice = _choose_boxed_option(mt("resources_docs_title", lang), options, lang, color_on).lower()
        debug_print(f"Resources menu choice: {choice}", color_on)
        if choice == "1":
            url, fallback = _get_localized_doc_url("documentation", lang)
            content = _fetch_github_raw(url, lang, color_on, fallback_url=fallback)
            if content:
                _display_paged_github_content(mt("res_docs_documentation", lang), content, lang, color_on)
        elif choice == "2":
            _open_changelog(lang, color_on)
        elif choice == "3":
            url, fallback = _get_localized_doc_url("license", lang)
            content = _fetch_github_raw(url, lang, color_on, fallback_url=fallback)
            if content:
                _display_paged_github_content(mt("res_docs_license", lang), content, lang, color_on)
        elif choice == "4":
            _open_privacy_policy_cli(lang, color_on)
        elif choice == "5":
            _open_terms_conditions_cli(lang, color_on)
        elif choice == "6":
            open_url("https://oauth.secure.pixiv.net/auth/token")
        elif choice == "7":
            open_url("https://www.python.org/")
        elif choice == "8":
            open_url("https://vercel.com/")
        elif choice == "0":
            return
        else:
            print(colorize(mt("invalid_option", lang), Ansi.RED, color_on))

def _gh_time_ago(iso_str: str) -> str:
    """Format ISO 8601 GitHub timestamp as relative time string."""
    try:
        import datetime
        dt = datetime.datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        now = datetime.datetime.now(datetime.timezone.utc)
        delta = now - dt
        d = delta.days
        s = delta.seconds
        if d >= 365: return f"{d // 365}y ago"
        if d >= 30:  return f"{d // 30}mo ago"
        if d >= 1:   return f"{d}d ago"
        if s >= 3600: return f"{s // 3600}h ago"
        if s >= 60:   return f"{s // 60}m ago"
        return "just now"
    except Exception:
        return iso_str[:10]


def _open_issues_cli(lang: str, color_on: bool) -> None:
    """Fetch and display GitHub Issues with Open/Closed/PR tabs, like the GitHub website."""
    REPO    = "fatonyahmadfauzi/Pixiv-OAuth-Token"
    HEADERS = {"Accept": "application/vnd.github+json"}
    NEW_URL = f"https://github.com/{REPO}/issues/new/choose"
    _L: dict[str, dict[str, str]] = {
        "en": {"title": "Issues", "tab_open": "Open", "tab_closed": "Closed",
               "tab_pr": "Pull Requests", "loading": "Fetching from GitHub...",
               "none_open": "No open issues.\nGreat job! \U0001f389",
               "none_closed": "No closed issues.", "none_pr": "No open pull requests.",
               "err": "Could not fetch issues.", "by": "by", "comments": "comments",
               "hint_o": "[o] Open  [c] Closed  [p] Pull Requests  [n] New Issue  [0] Back",
               "hint_c": "[o] Open  [c] Closed  [p] Pull Requests  [n] New Issue  [0] Back",
               "hint_p": "[o] Open  [c] Closed  [p] Pull Requests  [0] Back",
               "prompt_oc": "o / c / p / n / 0: ", "prompt_p": "o / c / p / 0: "},
        "id": {"title": "Isu", "tab_open": "Terbuka", "tab_closed": "Tertutup",
               "tab_pr": "Pull Requests", "loading": "Mengambil dari GitHub...",
               "none_open": "Tidak ada isu terbuka.\nKerja bagus! \U0001f389",
               "none_closed": "Tidak ada isu tertutup.", "none_pr": "Tidak ada PR terbuka.",
               "err": "Gagal mengambil isu.", "by": "oleh", "comments": "komentar",
               "hint_o": "[o] Terbuka  [c] Tertutup  [p] PR  [n] Buat Isu  [0] Kembali",
               "hint_c": "[o] Terbuka  [c] Tertutup  [p] PR  [n] Buat Isu  [0] Kembali",
               "hint_p": "[o] Terbuka  [c] Tertutup  [p] PR  [0] Kembali",
               "prompt_oc": "o / c / p / n / 0: ", "prompt_p": "o / c / p / 0: "},
        "jp": {"title": "Issue一覧", "tab_open": "オープン", "tab_closed": "クローズ",
               "tab_pr": "プルリク", "loading": "GitHubから取得中...",
               "none_open": "未解決のIssueはありません。\n素晴らしい！\U0001f389",
               "none_closed": "クローズ済みIssueはありません。",
               "none_pr": "オープンなプルリクはありません。",
               "err": "Issueの取得に失敗しました。",
               "by": "投稿者", "comments": "コメント",
               "hint_o": "[o] オープン  [c] クローズ  [p] プルリク  [n] 新規Issue  [0] 戻る",
               "hint_c": "[o] オープン  [c] クローズ  [p] プルリク  [n] 新規Issue  [0] 戻る",
               "hint_p": "[o] オープン  [c] クローズ  [p] プルリク  [0] 戻る",
               "prompt_oc": "o / c / p / n / 0: ", "prompt_p": "o / c / p / 0: "},
        "kr": {"title": "\uc774\uc288", "tab_open": "\uc5f4\ub9b0", "tab_closed": "\ub2eb\ud78c",
               "tab_pr": "\ud480 \ub9ac\ud034\uc2a4\ud2b8", "loading": "GitHub\uc5d0\uc11c \uac00\uc838\uc624\ub294 \uc911...",
               "none_open": "\uc5f4\ub9b0 \uc774\uc288\uac00 \uc5c6\uc2b5\ub2c8\ub2e4.\n\ud6c4\ub96d\ud558\uc2b5\ub2c8\ub2e4! \U0001f389",
               "none_closed": "\ub2eb\ud78c \uc774\uc288\uac00 \uc5c6\uc2b5\ub2c8\ub2e4.",
               "none_pr": "\uc5f4\ub9b0 PR\uc774 \uc5c6\uc2b5\ub2c8\ub2e4.",
               "err": "\uc774\uc288\ub97c \uac00\uc838\uc62c \uc218 \uc5c6\uc2b5\ub2c8\ub2e4.",
               "by": "", "comments": "\ub313\uae00",
               "hint_o": "[o] \uc5f4\ub9b0  [c] \ub2eb\ud78c  [p] PR  [n] \uc0c8 \uc774\uc288  [0] \ub4a4\ub85c",
               "hint_c": "[o] \uc5f4\ub9b0  [c] \ub2eb\ud78c  [p] PR  [n] \uc0c8 \uc774\uc288  [0] \ub4a4\ub85c",
               "hint_p": "[o] \uc5f4\ub9b0  [c] \ub2eb\ud78c  [p] PR  [0] \ub4a4\ub85c",
               "prompt_oc": "o / c / p / n / 0: ", "prompt_p": "o / c / p / 0: "},
        "zh": {"title": "\u8bae\u9898", "tab_open": "\u5f00\u542f", "tab_closed": "\u5df2\u5173\u95ed",
               "tab_pr": "\u62c9\u53d6\u8bf7\u6c42", "loading": "\u6b63\u5728\u4ece GitHub \u83b7\u53d6...",
               "none_open": "\u6ca1\u6709\u5f00\u653e\u7684\u8bae\u9898\u3002\n\u5e72\u5f97\u597d\uff01\U0001f389",
               "none_closed": "\u6ca1\u6709\u5df2\u5173\u95ed\u7684\u8bae\u9898\u3002",
               "none_pr": "\u6ca1\u6709\u5f00\u653e\u7684\u62c9\u53d6\u8bf7\u6c42\u3002",
               "err": "\u65e0\u6cd5\u83b7\u53d6\u8bae\u9898\u3002",
               "by": "", "comments": "\u6761\u8bc4\u8bba",
               "hint_o": "[o] \u5f00\u542f  [c] \u5df2\u5173\u95ed  [p] PR  [n] \u65b0\u5efa  [0] \u8fd4\u56de",
               "hint_c": "[o] \u5f00\u542f  [c] \u5df2\u5173\u95ed  [p] PR  [n] \u65b0\u5efa  [0] \u8fd4\u56de",
               "hint_p": "[o] \u5f00\u542f  [c] \u5df2\u5173\u95ed  [p] PR  [0] \u8fd4\u56de",
               "prompt_oc": "o / c / p / n / 0: ", "prompt_p": "o / c / p / 0: "},
        "de": {"title": "Issues", "tab_open": "Offen", "tab_closed": "Geschlossen",
               "tab_pr": "Pull-Anfragen", "loading": "Von GitHub laden...",
               "none_open": "Keine offenen Issues.\nGute Arbeit! \U0001f389",
               "none_closed": "Keine geschlossenen Issues.", "none_pr": "Keine offenen PRs.",
               "err": "Issues konnten nicht geladen werden.", "by": "von", "comments": "Kommentare",
               "hint_o": "[o] Offen  [c] Geschlossen  [p] PR  [n] Neu  [0] Zur\u00fcck",
               "hint_c": "[o] Offen  [c] Geschlossen  [p] PR  [n] Neu  [0] Zur\u00fcck",
               "hint_p": "[o] Offen  [c] Geschlossen  [p] PR  [0] Zur\u00fcck",
               "prompt_oc": "o / c / p / n / 0: ", "prompt_p": "o / c / p / 0: "},
        "fr": {"title": "Issues", "tab_open": "Ouvertes", "tab_closed": "Ferm\u00e9es",
               "tab_pr": "Demandes de fusion", "loading": "Chargement depuis GitHub...",
               "none_open": "Aucune issue ouverte.\nContinuez comme \u00e7a ! \U0001f389",
               "none_closed": "Aucune issue fermée.", "none_pr": "Aucune demande de fusion ouverte.",
               "err": "Impossible de charger les issues.", "by": "par", "comments": "commentaires",
               "hint_o": "[o] Ouvertes  [c] Fermées  [p] Fusions  [n] Nouvelle  [0] Retour",
               "hint_c": "[o] Ouvertes  [c] Fermées  [p] Fusions  [n] Nouvelle  [0] Retour",
               "hint_p": "[o] Ouvertes  [c] Fermées  [p] Fusions  [0] Retour",
               "prompt_oc": "o / c / p / n / 0 : ", "prompt_p": "o / c / p / 0 : "},
        "es": {"title": "Issues", "tab_open": "Abiertas", "tab_closed": "Cerradas",
               "tab_pr": "Solicitudes de fusión", "loading": "Cargando desde GitHub...",
               "none_open": "No hay issues abiertas.\n\u00a1Buen trabajo! \U0001f389",
               "none_closed": "No hay issues cerradas.", "none_pr": "No hay solicitudes de fusión abiertas.",
               "err": "No se pudieron cargar las issues.", "by": "por", "comments": "comentarios",
               "hint_o": "[o] Abiertas  [c] Cerradas  [p] Fusiones  [n] Nueva  [0] Volver",
               "hint_c": "[o] Abiertas  [c] Cerradas  [p] Fusiones  [n] Nueva  [0] Volver",
               "hint_p": "[o] Abiertas  [c] Cerradas  [p] Fusiones  [0] Volver",
               "prompt_oc": "o / c / p / n / 0: ", "prompt_p": "o / c / p / 0: "},
        "ru": {"title": "\u0417\u0430\u0434\u0430\u0447\u0438", "tab_open": "\u041e\u0442\u043a\u0440\u044b\u0442\u044b\u0435",
               "tab_closed": "\u0417\u0430\u043a\u0440\u044b\u0442\u044b\u0435",
               "tab_pr": "Запросы на слияние", "loading": "Загрузка с GitHub...",
               "none_open": "\u041d\u0435\u0442 \u043e\u0442\u043a\u0440\u044b\u0442\u044b\u0445 \u0437\u0430\u0434\u0430\u0447.\n\u041e\u0442\u043b\u0438\u0447\u043d\u0430\u044f \u0440\u0430\u0431\u043e\u0442\u0430! \U0001f389",
               "none_closed": "\u041d\u0435\u0442 \u0437\u0430\u043a\u0440\u044b\u0442\u044b\u0445 \u0437\u0430\u0434\u0430\u0447.",
               "none_pr": "Нет открытых запросов.",
               "err": "Не удалось загрузить задачи.",
               "by": "автор", "comments": "комментариев",
               "hint_o": "[o] Открытые  [c] Закрытые  [p] Запросы  [n] Создать  [0] Назад",
               "hint_c": "[o] Открытые  [c] Закрытые  [p] Запросы  [n] Создать  [0] Назад",
               "hint_p": "[o] Открытые  [c] Закрытые  [p] Запросы  [0] Назад",
               "prompt_oc": "o / c / p / n / 0: ", "prompt_p": "o / c / p / 0: "},
        "pt": {"title": "Issues", "tab_open": "Abertas", "tab_closed": "Fechadas",
               "tab_pr": "Pedidos de fusão", "loading": "Carregando do GitHub...",
               "none_open": "Nenhuma issue aberta.\n\u00d3timo trabalho! \U0001f389",
               "none_closed": "Nenhuma issue fechada.", "none_pr": "Nenhum pedido de fusão aberto.",
               "err": "Não foi possível carregar as issues.", "by": "por", "comments": "comentários",
               "hint_o": "[o] Abertas  [c] Fechadas  [p] Fusões  [n] Nova  [0] Voltar",
               "hint_c": "[o] Abertas  [c] Fechadas  [p] Fusões  [n] Nova  [0] Voltar",
               "hint_p": "[o] Abertas  [c] Fechadas  [p] Fusões  [0] Voltar",
               "prompt_oc": "o / c / p / n / 0: ", "prompt_p": "o / c / p / 0: "},
        "pl": {"title": "Zg\u0142oszenia", "tab_open": "Otwarte", "tab_closed": "Zamkni\u0119te",
               "tab_pr": "Żądania scalenia", "loading": "Pobieranie z GitHub...",
               "none_open": "Brak otwartych zgłoszeń.\nŚwietna robota! \U0001f389",
               "none_closed": "Brak zamkniętych zgłoszeń.", "none_pr": "Brak otwartych żądań scalenia.",
               "err": "Nie można pobrać zgłoszeń.", "by": "przez", "comments": "komentarzy",
               "hint_o": "[o] Otwarte  [c] Zamknięte  [p] Scalenia  [n] Nowe  [0] Wróć",
               "hint_c": "[o] Otwarte  [c] Zamknięte  [p] Scalenia  [n] Nowe  [0] Wróć",
               "hint_p": "[o] Otwarte  [c] Zamknięte  [p] Scalenia  [0] Wróć",
               "prompt_oc": "o / c / p / n / 0: ", "prompt_p": "o / c / p / 0: "},
    }
    L = _L.get(lang, _L["en"])
    width = 60
    bar   = "\u2550" * width

    # ── Fetch all data upfront (with per-endpoint retry) ───────────────
    def _gh_fetch(url: str, max_retries: int = 3) -> list:
        """Fetch a GitHub API endpoint; retry up to max_retries times on 5xx."""
        delay = 1.5
        last_exc: Exception = Exception("unknown")
        for attempt in range(max_retries):
            try:
                resp = requests.get(url, headers=HEADERS, timeout=12)
                if resp.status_code in (502, 503, 504) and attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                    continue
                resp.raise_for_status()
                return resp.json()
            except Exception as exc:
                last_exc = exc
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
        raise last_exc

    _clear_menu_screen()
    print(colorize(f"  {L['loading']}", Ansi.DIM, color_on))

    fetch_errors: list[str] = []
    open_issues: list = []
    closed_issues: list = []
    pull_requests: list = []

    for label, url, dest in [
        ("open",   f"https://api.github.com/repos/{REPO}/issues?state=open&per_page=50&sort=updated",   "open"),
        ("closed", f"https://api.github.com/repos/{REPO}/issues?state=closed&per_page=50&sort=updated", "closed"),
        ("pr",     f"https://api.github.com/repos/{REPO}/pulls?state=open&per_page=50&sort=updated",    "pr"),
    ]:
        try:
            data = _gh_fetch(url)
            if dest == "open":
                open_issues   = [i for i in data if "pull_request" not in i]
            elif dest == "closed":
                closed_issues = [i for i in data if "pull_request" not in i]
            else:
                pull_requests = data
        except Exception as exc:
            fetch_errors.append(f"{label}: {exc}")

    if fetch_errors and not (open_issues or closed_issues or pull_requests):
        # All endpoints failed — nothing useful to show
        _clear_menu_screen()
        print(colorize(f"  [!] {L['err']}", Ansi.RED, color_on))
        for fe in fetch_errors:
            print(colorize(f"      {fe}", Ansi.DIM, color_on))
        input(colorize(f"\n  {mt('enter_continue', lang)}", Ansi.YELLOW, color_on))
        return

    item_map: dict[int, str] = {}
    tab = "o"  # current tab: o=open, c=closed, p=pr

    while True:
        _clear_menu_screen()
        # Header
        print(colorize(L['title'], Ansi.CYAN + Ansi.BOLD, color_on))
        print()
        # Tab bar
        def _tab_label(label: str, count: int, active: bool) -> str:
            s = f"{label} ({count})"
            return colorize(s, Ansi.GREEN + Ansi.BOLD if active else Ansi.DIM, color_on)
        tabs = (
            _tab_label(L["tab_open"],   len(open_issues),   tab == "o") + "    " +
            _tab_label(L["tab_closed"], len(closed_issues), tab == "c") + "    " +
            _tab_label(L["tab_pr"],     len(pull_requests), tab == "p")
        )
        print(tabs)
        print()
        # List for current tab
        item_map.clear()
        if tab == "o":
            items, none_msg, hint = open_issues, L["none_open"], L["hint_o"]
            prompt = L["prompt_oc"]
        elif tab == "c":
            items, none_msg, hint = closed_issues, L["none_closed"], L["hint_c"]
            prompt = L["prompt_oc"]
        else:
            items, none_msg, hint = pull_requests, L["none_pr"], L["hint_p"]
            prompt = L["prompt_p"]
        if not items:
            for line in none_msg.splitlines():
                clr = Ansi.GREEN if "\U0001f389" in line else Ansi.DIM
                print(colorize(line, clr, color_on))
            print()
        else:
            for item in items:
                num      = item["number"]
                title    = item["title"]
                user     = item.get("user", {}).get("login", "?")
                updated  = _gh_time_ago(item.get("updated_at", ""))
                comments = item.get("comments", 0)
                labels   = ", ".join(lb["name"] for lb in item.get("labels", [])[:3])
                label_str = f"  [{labels}]" if labels else ""
                item_map[num] = item["html_url"]
                title_disp = title if len(title) <= 50 else title[:47] + "..."
                clr = Ansi.MAGENTA if tab == "p" else Ansi.GREEN
                print(colorize(f"#{num:<5} {title_disp}{label_str}", clr, color_on))
                meta = f"       {L['by']} {user} \u00b7 {updated}"
                if comments:
                    meta += f" \u00b7 {comments} {L['comments']}"
                print(colorize(meta, Ansi.DIM, color_on))
                print()
        print(colorize(hint, Ansi.YELLOW, color_on))
        try:
            choice = input(colorize(f"\n{prompt}", Ansi.YELLOW, color_on)).strip().lower()
        except (EOFError, KeyboardInterrupt):
            return
        if choice == "0":
            return
        elif choice in ("o", "c", "p"):
            tab = choice
        elif choice == "n" and tab != "p":
            open_url(NEW_URL)
        elif choice.isdigit():
            url = item_map.get(int(choice))
            if url:
                open_url(url)
            else:
                print(colorize(f"#{choice} not found.", Ansi.RED, color_on))
        else:
            print(colorize(mt("invalid_option", lang), Ansi.RED, color_on))


def _open_discussions_cli(lang: str, color_on: bool) -> None:
    """Display GitHub Discussions page (static, no API call — avoids GraphQL 403 rate-limit)."""
    REPO     = "fatonyahmadfauzi/Pixiv-OAuth-Token"
    DISC_URL = f"https://github.com/{REPO}/discussions"
    NEW_URL  = f"https://github.com/{REPO}/discussions/new/choose"
    Q_URL    = f"https://github.com/{REPO}/discussions/categories/q-a"
    IDEA_URL = f"https://github.com/{REPO}/discussions/categories/ideas"
    SHOW_URL = f"https://github.com/{REPO}/discussions/categories/show-and-tell"
    BUG_URL  = f"https://github.com/{REPO}/issues/new?template=bug_report.md"

    _L: dict[str, dict] = {
        "en": {
            "title":        "Discussions",
            "subtitle":     "Ask questions, share ideas, and connect with the community.",
            "hosted":       "Discussions are hosted on GitHub",
            "desc":         "Join the conversation, ask questions, or share your ideas\n"
                            "  directly on the GitHub Discussions page.\n"
                            "  GitHub account required to post.",
            "open_btn":     "Open Discussions on GitHub",
            "quick_title":  "Quick Links",
            "q_label":      "Ask a Question",
            "q_sub":        "Get help from the community",
            "idea_label":   "Share an Idea",
            "idea_sub":     "Suggest features or improvements",
            "show_label":   "Show & Tell",
            "show_sub":     "Share what you built with this tool",
            "bug_label":    "Report a Bug",
            "bug_sub":      "Found something broken?",
            "hint":         "[1] Open Discussions  [2] Ask a Question  [3] Share an Idea\n"
                            "  [4] Show & Tell  [5] Report a Bug  [0] Back",
            "prompt":       "Select: ",
        },
        "id": {
            "title":        "Diskusi",
            "subtitle":     "Ajukan pertanyaan, bagikan ide, dan terhubung dengan komunitas.",
            "hosted":       "Diskusi di-host di GitHub",
            "desc":         "Bergabunglah, ajukan pertanyaan, atau bagikan ide kamu\n"
                            "  langsung di halaman GitHub Discussions.\n"
                            "  Akun GitHub diperlukan untuk memposting.",
            "open_btn":     "Buka Diskusi di GitHub",
            "quick_title":  "Tautan Cepat",
            "q_label":      "Ajukan Pertanyaan",
            "q_sub":        "Dapatkan bantuan dari komunitas",
            "idea_label":   "Bagikan Ide",
            "idea_sub":     "Sarankan fitur atau perbaikan",
            "show_label":   "Pamer Karya",
            "show_sub":     "Bagikan apa yang kamu buat",
            "bug_label":    "Laporkan Bug",
            "bug_sub":      "Menemukan sesuatu yang rusak?",
            "hint":         "[1] Buka Diskusi  [2] Pertanyaan  [3] Bagikan Ide\n"
                            "  [4] Pamer Karya  [5] Laporkan Bug  [0] Kembali",
            "prompt":       "Pilih: ",
        },
        "jp": {
            "title":        "ディスカッション",
            "subtitle":     "質問したり、アイデアを共有したり、コミュニティとつながりましょう。",
            "hosted":       "ディスカッションはGitHubでホストされています",
            "desc":         "GitHubのディスカッションページで会話に参加し、\n"
                            "  質問したり、アイデアを共有したりしましょう。\n"
                            "  投稿にはGitHubアカウントが必要です。",
            "open_btn":     "GitHubでディスカッションを開く",
            "quick_title":  "クイックリンク",
            "q_label":      "質問する",
            "q_sub":        "コミュニティからサポートを受ける",
            "idea_label":   "アイデアを共有",
            "idea_sub":     "機能や改善点を提案する",
            "show_label":   "作品を披露",
            "show_sub":     "このツールで作ったものを共有する",
            "bug_label":    "バグを報告",
            "bug_sub":      "不具合を見つけましたか？",
            "hint":         "[1] ディスカッションを開く  [2] 質問  [3] アイデア\n"
                            "  [4] 作品を披露  [5] バグ報告  [0] 戻る",
            "prompt":       "選択: ",
        },
        "kr": {
            "title":        "토론",
            "subtitle":     "질문하고, 아이디어를 공유하고, 커뮤니티와 소통하세요.",
            "hosted":       "토론은 GitHub에서 호스팅됩니다",
            "desc":         "GitHub Discussions 페이지에서 대화에 참여하고,\n"
                            "  질문하거나 아이디어를 공유하세요.\n"
                            "  게시하려면 GitHub 계정이 필요합니다.",
            "open_btn":     "GitHub에서 토론 열기",
            "quick_title":  "빠른 링크",
            "q_label":      "질문하기",
            "q_sub":        "커뮤니티에서 도움받기",
            "idea_label":   "아이디어 공유",
            "idea_sub":     "기능이나 개선 사항 제안",
            "show_label":   "작품 공유",
            "show_sub":     "이 도구로 만든 것 공유",
            "bug_label":    "버그 신고",
            "bug_sub":      "문제를 발견했나요?",
            "hint":         "[1] 토론 열기  [2] 질문  [3] 아이디어\n"
                            "  [4] 작품 공유  [5] 버그 신고  [0] 뒤로",
            "prompt":       "선택: ",
        },
        "zh": {
            "title":        "讨论区",
            "subtitle":     "提问、分享想法，与社区建立联系。",
            "hosted":       "讨论托管在 GitHub 上",
            "desc":         "直接在 GitHub Discussions 页面加入对话，\n"
                            "  提问或分享你的想法。\n"
                            "  发帖需要 GitHub 账号。",
            "open_btn":     "在 GitHub 上打开讨论",
            "quick_title":  "快速链接",
            "q_label":      "提问",
            "q_sub":        "向社区寻求帮助",
            "idea_label":   "分享想法",
            "idea_sub":     "建议功能或改进",
            "show_label":   "展示作品",
            "show_sub":     "分享你用此工具制作的内容",
            "bug_label":    "报告错误",
            "bug_sub":      "发现了问题？",
            "hint":         "[1] 打开讨论  [2] 提问  [3] 分享想法\n"
                            "  [4] 展示作品  [5] 报告错误  [0] 返回",
            "prompt":       "选择: ",
        },
        "de": {
            "title":        "Diskussionen",
            "subtitle":     "Fragen stellen, Ideen teilen und mit der Community verbinden.",
            "hosted":       "Diskussionen werden auf GitHub gehostet",
            "desc":         "Nehmen Sie an Gesprächen teil, stellen Sie Fragen oder teilen\n"
                            "  Sie Ihre Ideen direkt auf der GitHub Discussions-Seite.\n"
                            "  Zum Posten ist ein GitHub-Konto erforderlich.",
            "open_btn":     "Diskussionen auf GitHub öffnen",
            "quick_title":  "Schnelllinks",
            "q_label":      "Frage stellen",
            "q_sub":        "Hilfe von der Community erhalten",
            "idea_label":   "Idee teilen",
            "idea_sub":     "Funktionen oder Verbesserungen vorschlagen",
            "show_label":   "Zeigen & Erzählen",
            "show_sub":     "Teilen Sie, was Sie mit diesem Tool erstellt haben",
            "bug_label":    "Fehler melden",
            "bug_sub":      "Etwas Defektes gefunden?",
            "hint":         "[1] Diskussionen öffnen  [2] Fragen  [3] Idee\n"
                            "  [4] Zeigen & Erzählen  [5] Fehler melden  [0] Zurück",
            "prompt":       "Auswählen: ",
        },
        "fr": {
            "title":        "Discussions",
            "subtitle":     "Posez des questions, partagez des idées et connectez-vous avec la communauté.",
            "hosted":       "Les discussions sont hébergées sur GitHub",
            "desc":         "Rejoignez la conversation, posez des questions ou partagez\n"
                            "  vos idées directement sur la page GitHub Discussions.\n"
                            "  Un compte GitHub est requis pour publier.",
            "open_btn":     "Ouvrir les discussions sur GitHub",
            "quick_title":  "Liens rapides",
            "q_label":      "Poser une question",
            "q_sub":        "Obtenir de l'aide de la communauté",
            "idea_label":   "Partager une idée",
            "idea_sub":     "Suggérer des fonctionnalités ou améliorations",
            "show_label":   "Montrer & Raconter",
            "show_sub":     "Partagez ce que vous avez créé",
            "bug_label":    "Signaler un bug",
            "bug_sub":      "Quelque chose de cassé ?",
            "hint":         "[1] Ouvrir discussions  [2] Questions  [3] Idée\n"
                            "  [4] Montrer & Raconter  [5] Signaler bug  [0] Retour",
            "prompt":       "Sélectionner : ",
        },
        "es": {
            "title":        "Discusiones",
            "subtitle":     "Haz preguntas, comparte ideas y conecta con la comunidad.",
            "hosted":       "Las discusiones están alojadas en GitHub",
            "desc":         "Únete a la conversación, haz preguntas o comparte tus ideas\n"
                            "  directamente en la página de GitHub Discussions.\n"
                            "  Se requiere cuenta de GitHub para publicar.",
            "open_btn":     "Abrir Discussions en GitHub",
            "quick_title":  "Enlaces rápidos",
            "q_label":      "Hacer una pregunta",
            "q_sub":        "Obtener ayuda de la comunidad",
            "idea_label":   "Compartir una Idea",
            "idea_sub":     "Sugerir funciones o mejoras",
            "show_label":   "Mostrar & Contar",
            "show_sub":     "Comparte lo que construiste",
            "bug_label":    "Reportar un Bug",
            "bug_sub":      "¿Encontraste algo roto?",
            "hint":         "[1] Abrir discusiones  [2] Preguntas  [3] Idea\n"
                            "  [4] Mostrar & Contar  [5] Reportar bug  [0] Volver",
            "prompt":       "Seleccionar: ",
        },
        "ru": {
            "title":        "Обсуждения",
            "subtitle":     "Задавайте вопросы, делитесь идеями и общайтесь с сообществом.",
            "hosted":       "Обсуждения размещены на GitHub",
            "desc":         "Присоединяйтесь к разговору, задавайте вопросы или делитесь\n"
                            "  идеями прямо на странице GitHub Discussions.\n"
                            "  Для публикации требуется аккаунт GitHub.",
            "open_btn":     "Открыть обсуждения на GitHub",
            "quick_title":  "Быстрые ссылки",
            "q_label":      "Задать вопрос",
            "q_sub":        "Получить помощь от сообщества",
            "idea_label":   "Поделиться идеей",
            "idea_sub":     "Предложить функции или улучшения",
            "show_label":   "Показать & Рассказать",
            "show_sub":     "Поделитесь тем, что вы создали",
            "bug_label":    "Сообщить об ошибке",
            "bug_sub":      "Нашли что-то сломанное?",
            "hint":         "[1] Открыть обсуждения  [2] Вопрос  [3] Идея\n"
                            "  [4] Показать & Рассказать  [5] Сообщить об ошибке  [0] Назад",
            "prompt":       "Выбрать: ",
        },
        "pt": {
            "title":        "Discussões",
            "subtitle":     "Faça perguntas, compartilhe ideias e conecte-se com a comunidade.",
            "hosted":       "As discussões são hospedadas no GitHub",
            "desc":         "Junte-se à conversa, faça perguntas ou compartilhe suas ideias\n"
                            "  diretamente na página do GitHub Discussions.\n"
                            "  Conta GitHub necessária para publicar.",
            "open_btn":     "Abrir Discussions no GitHub",
            "quick_title":  "Links Rápidos",
            "q_label":      "Fazer uma Pergunta",
            "q_sub":        "Obtenha ajuda da comunidade",
            "idea_label":   "Compartilhar uma Ideia",
            "idea_sub":     "Sugira recursos ou melhorias",
            "show_label":   "Mostrar & Contar",
            "show_sub":     "Compartilhe o que você criou",
            "bug_label":    "Reportar um Bug",
            "bug_sub":      "Encontrou algo quebrado?",
            "hint":         "[1] Abrir discussões  [2] Pergunta  [3] Ideia\n"
                            "  [4] Mostrar & Contar  [5] Reportar bug  [0] Voltar",
            "prompt":       "Selecionar: ",
        },
        "pl": {
            "title":        "Dyskusje",
            "subtitle":     "Zadawaj pytania, dziel się pomysłami i łącz się ze społecznością.",
            "hosted":       "Dyskusje są hostowane na GitHub",
            "desc":         "Dołącz do rozmowy, zadawaj pytania lub dziel się pomysłami\n"
                            "  bezpośrednio na stronie GitHub Discussions.\n"
                            "  Do publikowania wymagane jest konto GitHub.",
            "open_btn":     "Otwórz Discussions na GitHub",
            "quick_title":  "Szybkie linki",
            "q_label":      "Zadaj pytanie",
            "q_sub":        "Uzyskaj pomoc od społeczności",
            "idea_label":   "Udostępnij pomysł",
            "idea_sub":     "Zaproponuj funkcje lub ulepszenia",
            "show_label":   "Pokaż & Powiedz",
            "show_sub":     "Podziel się tym, co stworzyłeś",
            "bug_label":    "Zgłoś błąd",
            "bug_sub":      "Znalazłeś coś zepsutego?",
            "hint":         "[1] Otwórz dyskusje  [2] Pytanie  [3] Pomysł\n"
                            "  [4] Pokaż & Powiedz  [5] Zgłoś błąd  [0] Wróć",
            "prompt":       "Wybierz: ",
        },
    }
    L = _L.get(lang, _L["en"])
    sep   = "─" * 58

    _ACTIONS = [
        (DISC_URL, L["open_btn"]),
        (Q_URL,    L["q_label"]),
        (IDEA_URL, L["idea_label"]),
        (SHOW_URL, L["show_label"]),
        (BUG_URL,  L["bug_label"]),
    ]

    while True:
        _clear_menu_screen()

        # ── Header ────────────────────────────────────────────────────────
        print(colorize(L['title'], Ansi.CYAN + Ansi.BOLD, color_on))
        print(colorize(L['subtitle'], Ansi.DIM, color_on))
        print()

        # ── GitHub banner ─────────────────────────────────────────────────
        print(colorize(f"🐙 {L['hosted']}", Ansi.BOLD, color_on))
        print(colorize(sep, Ansi.DIM, color_on))
        for line in L["desc"].splitlines():
            print(colorize(line.strip(), Ansi.DIM, color_on))
        print()
        print(colorize(f"▶  [1] {L['open_btn']}", Ansi.GREEN + Ansi.BOLD, color_on))
        print()

        # ── Quick Links ───────────────────────────────────────────────────
        print(colorize(sep, Ansi.DIM, color_on))
        print(colorize(L['quick_title'], Ansi.BOLD, color_on))
        print(colorize(sep, Ansi.DIM, color_on))
        print()

        cards = [
            ("2", L["q_label"],    L["q_sub"],    Ansi.CYAN),
            ("3", L["idea_label"], L["idea_sub"],  Ansi.MAGENTA),
            ("4", L["show_label"], L["show_sub"],  Ansi.YELLOW),
            ("5", L["bug_label"],  L["bug_sub"],   Ansi.RED),
        ]
        for key, label, sub, clr in cards:
            print(colorize(f"[{key}] {label}", clr + Ansi.BOLD, color_on))
            print(colorize(f"    {sub}", Ansi.DIM, color_on))
            print()

        # ── Hint + Prompt ─────────────────────────────────────────────────
        for hint_line in L["hint"].splitlines():
            print(colorize(hint_line.strip(), Ansi.YELLOW, color_on))
        try:
            choice = input(colorize(f"\n{L['prompt']}", Ansi.YELLOW, color_on)).strip()
        except (EOFError, KeyboardInterrupt):
            return
        if choice == "0":
            return
        elif choice.isdigit() and 1 <= int(choice) <= 5:
            open_url(_ACTIONS[int(choice) - 1][0])
        elif choice == "":
            pass
        else:
            print(colorize(mt("invalid_option", lang), Ansi.RED, color_on))


def _open_donate_screen(lang: str, color_on: bool) -> None:
    """Display QRIS donate screen with QR code rendered in terminal."""
    # Localized strings per language
    _DONATE_MSGS: dict[str, dict[str, str]] = {
        "en": {
            "title":   "Support / Donate",
            "thanks":  "Thank you for supporting this project!",
            "scan":    "Scan the QRIS code below to donate.",
            "wallet":  "Scan with your supported e-wallet or banking app.",
            "name":    "FATONY AHMAD FAUZI, DIGITAL & KREATIF",
            "nmid":    "NMID: ID1026489430243",
            "back":    "Press Enter to go back...",
        },
        "id": {
            "title":   "Dukungan / Donasi",
            "thanks":  "Terima kasih telah mendukung proyek ini!",
            "scan":    "Pindai kode QRIS di bawah ini untuk berdonasi.",
            "wallet":  "Gunakan aplikasi e-wallet atau mobile banking yang mendukung QRIS.",
            "name":    "FATONY AHMAD FAUZI, DIGITAL & KREATIF",
            "nmid":    "NMID: ID1026489430243",
            "back":    "Tekan Enter untuk kembali...",
        },
        "jp": {
            "title":   "サポート / 寄付",
            "thanks":  "このプロジェクトをご支援いただきありがとうございます！",
            "scan":    "以下の QRIS コードをスキャンして寄付してください。",
            "wallet":  "QRIS 対応のe-wallet または銀行アプリで読み取ってください。",
            "name":    "FATONY AHMAD FAUZI, DIGITAL & KREATIF",
            "nmid":    "NMID: ID1026489430243",
            "back":    "Enterキーを押して戻る...",
        },
        "kr": {
            "title":   "지원 / 기부",
            "thanks":  "이 프로젝트를 지원해 주셔서 감사합니다!",
            "scan":    "기부하려면 아래 QRIS 코드를 스캔하세요.",
            "wallet":  "QRIS를 지원하는 e-wallet 또는 뱅킹 앱으로 스캔하세요.",
            "name":    "FATONY AHMAD FAUZI, DIGITAL & KREATIF",
            "nmid":    "NMID: ID1026489430243",
            "back":    "Enter 키를 눌러 뒤로 가세요...",
        },
        "zh": {
            "title":   "支持 / 捐赠",
            "thanks":  "感谢您支持此项目！",
            "scan":    "扫描下方 QRIS 二维码进行捐赠。",
            "wallet":  "请使用支持 QRIS 的 e-wallet 或银行应用扫描。",
            "name":    "FATONY AHMAD FAUZI, DIGITAL & KREATIF",
            "nmid":    "NMID: ID1026489430243",
            "back":    "按 Enter 返回...",
        },
        "de": {
            "title":   "Unterstützung / Spende",
            "thanks":  "Vielen Dank für die Unterstützung dieses Projekts!",
            "scan":    "Scannen Sie den folgenden QRIS-Code, um zu spenden.",
            "wallet":  "Scannen Sie mit einer QRIS-kompatiblen E-Wallet oder Banking-App.",
            "name":    "FATONY AHMAD FAUZI, DIGITAL & KREATIF",
            "nmid":    "NMID: ID1026489430243",
            "back":    "Drücken Sie Enter, um zurückzugehen...",
        },
        "fr": {
            "title":   "Soutien / Don",
            "thanks":  "Merci de soutenir ce projet !",
            "scan":    "Scannez le code QRIS ci-dessous pour faire un don.",
            "wallet":  "Utilisez un e-wallet ou une appli bancaire compatible QRIS.",
            "name":    "FATONY AHMAD FAUZI, DIGITAL & KREATIF",
            "nmid":    "NMID: ID1026489430243",
            "back":    "Appuyez sur Entrée pour revenir...",
        },
        "es": {
            "title":   "Soporte / Donación",
            "thanks":  "¡Gracias por apoyar este proyecto!",
            "scan":    "Escanea el código QRIS a continuación para donar.",
            "wallet":  "Escanea con tu e-wallet o app de banca compatible con QRIS.",
            "name":    "FATONY AHMAD FAUZI, DIGITAL & KREATIF",
            "nmid":    "NMID: ID1026489430243",
            "back":    "Presiona Enter para volver...",
        },
        "ru": {
            "title":   "Поддержка / Донат",
            "thanks":  "Спасибо за поддержку этого проекта!",
            "scan":    "Отсканируйте код QRIS ниже, чтобы сделать пожертвование.",
            "wallet":  "Используйте совместимый e-wallet или банковское приложение.",
            "name":    "FATONY AHMAD FAUZI, DIGITAL & KREATIF",
            "nmid":    "NMID: ID1026489430243",
            "back":    "Нажмите Enter для возврата...",
        },
        "pt": {
            "title":   "Suporte / Doação",
            "thanks":  "Obrigado por apoiar este projeto!",
            "scan":    "Escaneie o código QRIS abaixo para doar.",
            "wallet":  "Use um e-wallet ou app bancário compatível com QRIS.",
            "name":    "FATONY AHMAD FAUZI, DIGITAL & KREATIF",
            "nmid":    "NMID: ID1026489430243",
            "back":    "Pressione Enter para voltar...",
        },
        "pl": {
            "title":   "Wsparcie / Darowizna",
            "thanks":  "Dziękujemy za wsparcie tego projektu!",
            "scan":    "Zeskanuj poniższy kod QRIS, aby przekazać darowiznę.",
            "wallet":  "Użyj obsługiwanego e-portfela lub aplikacji bankowej QRIS.",
            "name":    "FATONY AHMAD FAUZI, DIGITAL & KREATIF",
            "nmid":    "NMID: ID1026489430243",
            "back":    "Naciśnij Enter, aby wrócić...",
        },
    }
    msgs = _DONATE_MSGS.get(lang, _DONATE_MSGS["en"])

    # QRIS string decoded from qris.png
    QRIS_DATA = (
        "00020101021126610014COM.GO-JEK.WWW01189360091434985457910210G4985457910303UMI"
        "51440014ID.CO.QRIS.WWW0215ID10264894302430303UMI5204899953033605802ID"
        "5925FATONY AHMAD FAUZI, Digit6005BOGOR61051671062070703A0163041836"
    )

    def _render_qr_ascii() -> str:
        try:
            import qrcode  # type: ignore
            import io
            qr = qrcode.QRCode(border=1, error_correction=qrcode.constants.ERROR_CORRECT_M)
            qr.add_data(QRIS_DATA)
            qr.make(fit=True)
            buf = io.StringIO()
            qr.print_ascii(out=buf, invert=True)
            buf.seek(0)
            return buf.read().strip()
        except ImportError:
            return "  [!] Install 'qrcode' to display QR: pip install qrcode"

    _clear_menu_screen()
    qr_str = _render_qr_ascii()

    print(colorize(msgs["title"], Ansi.CYAN + Ansi.BOLD, color_on))
    print()
    print(colorize(msgs['thanks'], Ansi.GREEN + Ansi.BOLD, color_on))
    print(colorize(msgs['scan'], Ansi.GREEN, color_on))
    print()

    # Print QR code
    for line in qr_str.splitlines():
        print(line)

    print()
    print(colorize(f"♦  {msgs['name']}", Ansi.YELLOW + Ansi.BOLD, color_on))
    print(colorize(f"   {msgs['nmid']}", Ansi.DIM, color_on))
    print()
    print(colorize(f"── {msgs['wallet']}", Ansi.CYAN, color_on))
    print()
    try:
        input(colorize(msgs['back'], Ansi.YELLOW, color_on))
    except (EOFError, KeyboardInterrupt):
        pass


def _open_contact_us_cli(lang: str, color_on: bool) -> None:
    """Terminal contact-us form — collects input then POSTs to FormSubmit."""
    _L: dict[str, dict[str, str]] = {
        "en": {
            "title":      "Contact Us",
            "subtitle":   "Have questions, suggestions, or need help? Send us a message.",
            "first":      "First Name",
            "last":       "Last Name",
            "email":      "Email Address",
            "attach":     "Attachment path (optional, press Enter to skip)",
            "msg":        "Message",
            "sending":    "Sending...",
            "ok":         "Message sent! We'll get back to you soon.",
            "err":        "Failed to send message",
            "required":   "This field is required.",
            "bad_email":  "Invalid email address.",
            "back":       "Press Enter to go back...",
            "cancel":     "(leave blank to cancel)",
            "err_exe":    "Error: Executable files ({ext}) are not allowed for security reasons.",
            "type_zero":  "(0 to cancel)",
        },
        "id": {
            "title":      "Hubungi Kami",
            "subtitle":   "Ada pertanyaan, saran, atau butuh bantuan? Kirim pesan ke kami.",
            "first":      "Nama Depan",
            "last":       "Nama Belakang",
            "email":      "Alamat Email",
            "attach":     "Path lampiran (opsional, tekan Enter untuk lewati)",
            "msg":        "Pesan",
            "sending":    "Mengirim...",
            "ok":         "Pesan terkirim! Kami akan segera menghubungi Anda.",
            "err":        "Gagal mengirim pesan",
            "required":   "Kolom ini wajib diisi.",
            "bad_email":  "Alamat email tidak valid.",
            "back":       "Tekan Enter untuk kembali...",
            "cancel":     "(kosongkan untuk batal)",
            "err_exe":    "Error: File aplikasi ({ext}) tidak diizinkan demi keamanan.",
            "type_zero":  "(0 untuk batal)",
        },
        "jp": {
            "title":      "お問い合わせ",
            "subtitle":   "ご質問・ご提案・お困りのことがあればメッセージをお送りください。",
            "first":      "名",
            "last":       "姓",
            "email":      "メールアドレス",
            "attach":     "添付ファイルのパス（任意、スキップはEnter）",
            "msg":        "メッセージ",
            "sending":    "送信中...",
            "ok":         "送信完了！近日中にご連絡いたします。",
            "err":        "送信に失敗しました",
            "required":   "このフィールドは必須です。",
            "bad_email":  "メールアドレスの形式が正しくありません。",
            "back":       "Enterキーで戻る...",
            "cancel":     "（空白でキャンセル）",
            "err_exe":    "エラー: セキュリティ上の理由から、実行可能ファイル ({ext}) は許可されていません。",
            "type_zero":  "(0でキャンセル)",
        },
        "kr": {
            "title":      "문의하기",
            "subtitle":   "질문, 제안 또는 도움이 필요하신가요? 메시지를 보내세요.",
            "first":      "이름",
            "last":       "성",
            "email":      "이메일 주소",
            "attach":     "첨부 파일 경로 (선택 사항, 건너뛰려면 Enter)",
            "msg":        "메시지",
            "sending":    "전송 중...",
            "ok":         "메시지가 전송되었습니다! 곧 연락드리겠습니다.",
            "err":        "메시지 전송 실패",
            "required":   "이 필드는 필수입니다.",
            "bad_email":  "이메일 주소가 올바르지 않습니다.",
            "back":       "Enter 키를 눌러 뒤로 가기...",
            "cancel":     "(취소하려면 비워 두세요)",
            "err_exe":    "오류: 보안상의 이유로 실행 파일({ext})은 허용되지 않습니다.",
            "type_zero":  "(0으로 취소)",
        },
        "zh": {
            "title":      "联系我们",
            "subtitle":   "有问题、建议或需要帮助？给我们发消息吧。",
            "first":      "名字",
            "last":       "姓氏",
            "email":      "电子邮件地址",
            "attach":     "附件路径（可选，按 Enter 跳过）",
            "msg":        "消息",
            "sending":    "发送中...",
            "ok":         "消息已发送！我们会尽快回复您。",
            "err":        "发送失败",
            "required":   "此字段为必填项。",
            "bad_email":  "电子邮件地址无效。",
            "back":       "按 Enter 返回...",
            "cancel":     "（留空取消）",
            "err_exe":    "错误：出于安全原因，不允许使用可执行文件 ({ext})。",
            "type_zero":  "(0 取消)",
        },
        "de": {
            "title":      "Kontaktiere uns",
            "subtitle":   "Fragen, Anregungen oder Hilfe nötig? Schreib uns eine Nachricht.",
            "first":      "Vorname",
            "last":       "Nachname",
            "email":      "E-Mail-Adresse",
            "attach":     "Anhangpfad (optional, Enter zum Überspringen)",
            "msg":        "Nachricht",
            "sending":    "Senden...",
            "ok":         "Nachricht gesendet! Wir melden uns bald.",
            "err":        "Nachricht konnte nicht gesendet werden",
            "required":   "Dieses Feld ist erforderlich.",
            "bad_email":  "Ungültige E-Mail-Adresse.",
            "back":       "Enter drücken zum Zurückgehen...",
            "cancel":     "(leer lassen zum Abbrechen)",
            "err_exe":    "Fehler: Ausführbare Dateien ({ext}) sind aus Sicherheitsgründen nicht zulässig.",
            "type_zero":  "(0 zum Abbrechen)",
        },
        "fr": {
            "title":      "Contactez-nous",
            "subtitle":   "Des questions, suggestions, ou besoin d'aide ? Envoyez-nous un message.",
            "first":      "Prénom",
            "last":       "Nom",
            "email":      "Adresse e-mail",
            "attach":     "Chemin de la pièce jointe (optionnel, Enter pour ignorer)",
            "msg":        "Message",
            "sending":    "Envoi en cours...",
            "ok":         "Message envoyé ! Nous vous répondrons bientôt.",
            "err":        "Échec de l'envoi du message",
            "required":   "Ce champ est obligatoire.",
            "bad_email":  "Adresse e-mail invalide.",
            "back":       "Appuyez sur Entrée pour revenir...",
            "cancel":     "(laisser vide pour annuler)",
            "err_exe":    "Erreur : Les fichiers exécutables ({ext}) ne sont pas autorisés pour des raisons de sécurité.",
            "type_zero":  "(0 pour annuler)",
        },
        "es": {
            "title":      "Contáctanos",
            "subtitle":   "¿Preguntas, sugerencias o necesitas ayuda? Envíanos un mensaje.",
            "first":      "Nombre",
            "last":       "Apellido",
            "email":      "Correo electrónico",
            "attach":     "Ruta del archivo adjunto (opcional, Enter para omitir)",
            "msg":        "Mensaje",
            "sending":    "Enviando...",
            "ok":         "¡Mensaje enviado! Nos pondremos en contacto pronto.",
            "err":        "Error al enviar el mensaje",
            "required":   "Este campo es obligatorio.",
            "bad_email":  "Dirección de correo inválida.",
            "back":       "Presiona Enter para volver...",
            "cancel":     "(dejar en blanco para cancelar)",
            "err_exe":    "Error: No se permiten archivos ejecutables ({ext}) por razones de seguridad.",
            "type_zero":  "(0 para cancelar)",
        },
        "ru": {
            "title":      "Связаться с нами",
            "subtitle":   "Есть вопросы, предложения или нужна помощь? Отправьте нам сообщение.",
            "first":      "Имя",
            "last":       "Фамилия",
            "email":      "Адрес электронной почты",
            "attach":     "Путь к вложению (необязательно, Enter для пропуска)",
            "msg":        "Сообщение",
            "sending":    "Отправка...",
            "ok":         "Сообщение отправлено! Мы скоро свяжемся с вами.",
            "err":        "Не удалось отправить сообщение",
            "required":   "Это поле обязательно.",
            "bad_email":  "Неверный адрес электронной почты.",
            "back":       "Нажмите Enter для возврата...",
            "cancel":     "(оставьте пустым для отмены)",
            "err_exe":    "Ошибка: Исполняемые файлы ({ext}) не разрешены по соображениям безопасности.",
            "type_zero":  "(0 для отмены)",
        },
        "pt": {
            "title":      "Fale Conosco",
            "subtitle":   "Tem dúvidas, sugestões ou precisa de ajuda? Envie uma mensagem.",
            "first":      "Nome",
            "last":       "Sobrenome",
            "email":      "Endereço de e-mail",
            "attach":     "Caminho do anexo (opcional, Enter para ignorar)",
            "msg":        "Mensagem",
            "sending":    "Enviando...",
            "ok":         "Mensagem enviada! Entraremos em contato em breve.",
            "err":        "Falha ao enviar mensagem",
            "required":   "Este campo é obrigatório.",
            "bad_email":  "Endereço de e-mail inválido.",
            "back":       "Pressione Enter para voltar...",
            "cancel":     "(deixe em branco para cancelar)",
            "err_exe":    "Erro: Arquivos executáveis ({ext}) não são permitidos por motivos de segurança.",
            "type_zero":  "(0 para cancelar)",
        },
        "pl": {
            "title":      "Skontaktuj się z nami",
            "subtitle":   "Masz pytania, sugestie lub potrzebujesz pomocy? Wyślij wiadomość.",
            "first":      "Imię",
            "last":       "Nazwisko",
            "email":      "Adres e-mail",
            "attach":     "Ścieżka załącznika (opcjonalnie, Enter aby pominąć)",
            "msg":        "Wiadomość",
            "sending":    "Wysyłanie...",
            "ok":         "Wiadomość wysłana! Odezwiemy się wkrótce.",
            "err":        "Nie udało się wysłać wiadomości",
            "required":   "To pole jest wymagane.",
            "bad_email":  "Nieprawidłowy adres e-mail.",
            "back":       "Naciśnij Enter, aby wrócić...",
            "cancel":     "(pozostaw puste, aby anulować)",
            "err_exe":    "Błąd: Pliki wykonywalne ({ext}) są niedozwolone ze względów bezpieczeństwa.",
            "type_zero":  "(0 aby anulować)",
        },
    }
    L = _L.get(lang, _L["en"])
    FORMSUBMIT_URL = "https://formsubmit.co/ajax/fatonyahmadfauzi@gmail.com"

    def _ask(field: str, required: bool = True) -> str | None:
        """Prompt user for a field value, re-ask if required and blank."""
        marker = colorize(" *", Ansi.RED, color_on) if required else ""
        while True:
            val = input(colorize(f"{field}{marker} {L['type_zero']}: ", Ansi.CYAN, color_on)).strip()
            if val == "0":
                return None
            if not val and required:
                print(colorize(L["required"], Ansi.RED, color_on))
                continue
            return val

    import re as _re

    _clear_menu_screen()
    print(colorize(L["title"], Ansi.CYAN + Ansi.BOLD, color_on))
    print(colorize(L["subtitle"], Ansi.DIM, color_on))
    print()

    # First Name
    first = _ask(L["first"])
    if first is None:
        return

    # Last Name
    last = _ask(L["last"])
    if last is None:
        return

    # Email
    while True:
        email = _ask(L["email"])
        if email is None:
            return
        if not _re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            print(colorize(L["bad_email"], Ansi.RED, color_on))
            continue
        break

    # Attachment (optional)
    attach_path = input(colorize(f"{L['attach']} {L['type_zero']}: ", Ansi.CYAN, color_on)).strip()
    if attach_path == "0":
        return

    # Message
    print(colorize(f"{L['msg']} * ({L['cancel']})", Ansi.CYAN, color_on))
    msg_lines: list[str] = []
    while True:
        line = input()
        if line == "" and not msg_lines:
            return  # Cancel if first line is blank
        if line == "" and msg_lines:
            break
        msg_lines.append(line)
    message = "\n".join(msg_lines)
    if not message.strip():
        return

    # Send
    print()
    print(colorize(L["sending"], Ansi.YELLOW, color_on))
    try:
        import mimetypes
        from pathlib import Path as _Path

        form_data: dict = {
            "_subject":  f"[CLI Contact] {first} {last}",
            "name":      f"{first} {last}",
            "email":     email,
            "message":   message,
            "_template": "table",
            "_captcha":  "false",
        }
        files = None
        if attach_path:
            ap = _Path(attach_path.strip('"').strip("'"))
            if ap.is_file():
                if ap.suffix.lower() in [".exe", ".bat", ".cmd", ".sh", ".vbs", ".msi"]:
                    print(colorize(L["err_exe"].format(ext=ap.suffix), Ansi.RED, color_on))
                    print()
                    try:
                        input(colorize(L["back"], Ansi.YELLOW, color_on))
                    except (EOFError, KeyboardInterrupt):
                        pass
                    return

                mime = mimetypes.guess_type(str(ap))[0] or "application/octet-stream"
                files = {"attachment": (ap.name, ap.read_bytes(), mime)}

        headers = {
            "Accept": "application/json",
            "Origin": "https://pixiv-o-auth-token.vercel.app",
            "Referer": "https://pixiv-o-auth-token.vercel.app/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        if files:
            # The FormSubmit /ajax/ endpoint discards attachments.
            # We must use the standard HTML endpoint for form submissions with files.
            submit_url = FORMSUBMIT_URL.replace("/ajax/", "/")
            resp = requests.post(submit_url, data=form_data, files=files, headers=headers, timeout=30)
        else:
            resp = requests.post(FORMSUBMIT_URL, data=form_data, headers=headers, timeout=20)

        if resp.status_code == 200:
            try:
                result = resp.json()
                if result.get("success") == "true" or result.get("success") is True:
                    print(colorize(L["ok"], Ansi.GREEN + Ansi.BOLD, color_on))
                else:
                    print(colorize(f"{L['err']}: {result}", Ansi.RED, color_on))
            except Exception:
                print(colorize(L["ok"], Ansi.GREEN + Ansi.BOLD, color_on))
        else:
            print(colorize(f"{L['err']}: HTTP {resp.status_code}", Ansi.RED, color_on))
    except Exception as exc:
        print(colorize(f"{L['err']}: {exc}", Ansi.RED, color_on))

    print()
    try:
        input(colorize(L["back"], Ansi.YELLOW, color_on))
    except (EOFError, KeyboardInterrupt):
        pass


def _open_support_menu(lang: str, color_on: bool) -> None:
    options = [
        ("1", mt("sup_contact", lang)),
        ("2", mt("sup_report", lang)),
        ("3", mt("sup_discussions", lang)),
        ("4", mt("sup_fatony", lang)),
        ("5", mt("sup_donate", lang)),
        ("0", mt("back", lang)),
    ]
    while True:
        choice = _choose_boxed_option(mt("support_title", lang), options, lang, color_on).lower()
        debug_print(f"Support menu choice: {choice}", color_on)
        if choice == "1":
            _open_contact_us_cli(lang, color_on)
        elif choice == "2":
            _open_issues_cli(lang, color_on)
        elif choice == "3":
            _open_discussions_cli(lang, color_on)
        elif choice == "4":
            open_url("https://github.com/fatonyahmadfauzi")
        elif choice == "5":
            _open_donate_screen(lang, color_on)
        elif choice == "0":
            return
        else:
            print(colorize(mt("invalid_option", lang), Ansi.RED, color_on))

def _open_social_menu(lang: str, color_on: bool) -> None:
    options = [
        ("1", mt("social_github", lang)),
        ("2", mt("social_linkedin", lang)),
        ("0", mt("back", lang)),
    ]
    while True:
        choice = _choose_boxed_option(mt("social_title", lang), options, lang, color_on).lower()
        debug_print(f"Social menu choice: {choice}", color_on)
        if choice == "1":
            open_url("https://github.com/fatonyahmadfauzi")
        elif choice == "2":
            open_url("https://www.linkedin.com/in/fatonyahmadfauzi")
        elif choice == "0":
            return
        else:
            print(colorize(mt("invalid_option", lang), Ansi.RED, color_on))

def _open_resources_menu(lang: str, color_on: bool) -> None:
    while True:
        print()
        print(colorize(f"[1] {mt('res_repo', lang)}", Ansi.BLUE, color_on))
        print(colorize(f"[2] {mt('res_release', lang)}", Ansi.BLUE, color_on))
        print(colorize(f"[0] {mt('back', lang)}", Ansi.DIM, color_on))
        choice = input(colorize(f"[+] {mt('select_option', lang)}: ", Ansi.YELLOW, color_on)).strip()
        if choice == "1":
            open_url(REPO_BASE_URL)
        elif choice == "2":
            open_url(RELEASES_URL)
        elif choice == "0":
            return
        else:
            print(colorize(mt("invalid_option", lang), Ansi.RED, color_on))

def _open_contact_menu(lang: str, color_on: bool) -> None:
    while True:
        print()
        print(colorize(f"[1] {mt('contact_tiktok', lang)}", Ansi.BLUE, color_on))
        print(colorize(f"[2] {mt('contact_twitter', lang)}", Ansi.BLUE, color_on))
        print(colorize(f"[0] {mt('back', lang)}", Ansi.DIM, color_on))
        choice = input(colorize(f"[+] {mt('select_option', lang)}: ", Ansi.YELLOW, color_on)).strip()
        if choice == "1":
            open_url(TIKTOK_URL)
        elif choice == "2":
            open_url(TWITTER_URL)
        elif choice == "0":
            return
        else:
            print(colorize(mt("invalid_option", lang), Ansi.RED, color_on))

def show_cli_tutorial(lang: str, color_on: bool) -> None:
    debug_print(f"Showing tutorial panel (lang={lang})", color_on)
    L = get_lang(lang)
    lines = [
        mt("tutorial_desc", lang),
        "",
        mt("tutorial_step1", lang),
        mt("tutorial_step2", lang),
        mt("tutorial_step3", lang),
        mt("tutorial_step4", lang),
        mt("tutorial_step5", lang),
        mt("tutorial_step6", lang),
        "",
        mt("tutorial_example", lang) + ":",
        L["open_browser"],
        L["paste_url"],
        "pixiv://account/login?code=eltWz8pQgT-D0foeIPzhHN_y6CwptwjXk8kJ0yzowvw&via=login",
        f"{L['code_detected']} eltWz8pQgT-D0foeIPzhHN_y6CwptwjXk8kJ0yzowvw",
        L["login_success"],
        "access_token : uog7p1mdnJ7G3lJl30XbYQZx2otlJFwkfmfsO7gPtDU",
        "refresh_token: zF6DNiG2tvSQgnd3AkTeI6ZaVxbNf1jqU3cQX5MkyI4",
        "expires_in   : 3600",
    ]
    _render_rich_text_panel(mt("tutorial_title", lang), lines, mt("enter_main_menu", lang))


def _open_changelog(lang: str = "en", color_on: bool = True) -> None:
    debug_print("Fetching changelog from GitHub")
    url, fallback = _get_localized_doc_url("changelog", lang)
    content = _fetch_github_raw(url, lang, color_on, fallback_url=fallback)
    if content:
        _display_paged_github_content(mt("opt_changelog", lang), content, lang, color_on)


def _open_debug_menu(lang: str, color_on: bool) -> None:
    while True:
        recent_logs = DEBUG_LOGS[-30:] if DEBUG_LOGS else [mt("debug_empty", lang)]
        _clear_menu_screen()
        print(colorize(mt("debug_title", lang), Ansi.CYAN + Ansi.BOLD, color_on))
        print()
        print("\n".join(recent_logs))
        print()
        print(colorize(f"[1] {mt('debug_copy', lang)}", Ansi.GREEN, color_on))
        print(colorize(f"[2] {mt('debug_clear', lang)}", Ansi.GREEN, color_on))
        print(colorize(f"[0] {mt('debug_exit', lang)}", Ansi.DIM, color_on))
        choice = input(colorize(f"\n[+] {mt('select_option', lang)}: ", Ansi.YELLOW, color_on)).strip()
        if choice == "1":
            payload = "\n".join(DEBUG_LOGS) if DEBUG_LOGS else mt("debug_empty", lang)
            ok = _copy_to_clipboard(payload)
            msg = mt("debug_copied", lang) if ok else mt("debug_copy_failed", lang)
            debug_print(msg, color_on)
        elif choice == "2":
            DEBUG_LOGS.clear()
            debug_print(mt("debug_cleared", lang), color_on)
        elif choice == "0":
            return
        else:
            print(colorize(mt("invalid_option", lang), Ansi.RED, color_on))


def _normalize_version_tag(version: str | None) -> str | None:
    if not version:
        return None
    v = str(version).strip()
    if not v:
        return None
    return v if v.startswith("v") else f"v{v}"


def _version_key(version: str | None) -> tuple[int, ...]:
    if not version:
        return (0, 0, 0)
    cleaned = str(version).strip().lstrip("vV")
    parts: list[int] = []
    for token in cleaned.split("."):
        try:
            parts.append(int(token))
        except ValueError:
            parts.append(0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


def _fetch_latest_manifest_meta() -> tuple[str | None, str | None]:
    try:
        response = requests.get(LATEST_MANIFEST_URL, timeout=15)
        response.raise_for_status()
        payload = response.json()
        tag = _normalize_version_tag(payload.get("version"))
        code = str(payload.get("build_code", "")).strip() or None
        return tag, code
    except Exception:
        return None, None


def _fetch_latest_release_meta() -> tuple[str | None, str | None]:
    manifest_tag, manifest_code = _fetch_latest_manifest_meta()
    if manifest_tag:
        return manifest_tag, manifest_code
    try:
        response = requests.get(GITHUB_API_LATEST_RELEASE, timeout=15)
        response.raise_for_status()
        payload = response.json()
        tag = _normalize_version_tag(payload.get("tag_name"))
        release_id = payload.get("id")
        code = f"REL-{release_id}" if release_id else None
        return tag, code
    except Exception:
        return None, None


def _fetch_latest_release_tag() -> str | None:
    tag, _ = _fetch_latest_release_meta()
    return tag


def _fetch_latest_release_tag_cached(force: bool = False) -> str | None:
    now = time.time()
    if not force and UPDATE_CACHE["checked_at"] and now - float(UPDATE_CACHE["checked_at"]) < 300:
        return UPDATE_CACHE["latest"]
    latest, latest_code = _fetch_latest_release_meta()
    UPDATE_CACHE["latest"] = latest
    UPDATE_CACHE["latest_code"] = latest_code
    UPDATE_CACHE["checked_at"] = now
    return latest


def _get_latest_release_code_cached(force: bool = False) -> str | None:
    _fetch_latest_release_tag_cached(force=force)
    return UPDATE_CACHE["latest_code"]

DOWNLOADS_BASE_URL = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads"


def _detect_arch_suffix(exe_path: Path) -> str:
    """Detect architecture suffix from exe filename (e.g. ' x64', ' ARM64', ' x86', or '' for generic)."""
    name_lower = exe_path.stem.lower()
    if "arm64" in name_lower:
        return " ARM64"
    if "x64" in name_lower:
        return " x64"
    if "x86" in name_lower:
        return " x86"
    return ""  # generic (no arch suffix)


def _get_cli_portable_url(exe_path: Path) -> str:
    arch = _detect_arch_suffix(exe_path)
    from urllib.parse import quote
    filename = f"Pixiv OAuth CLi (Portable){arch}_latest.exe"
    return f"{DOWNLOADS_BASE_URL}/{quote(filename)}"


def _get_cli_setup_url(exe_path: Path) -> str:
    arch = _detect_arch_suffix(exe_path)
    from urllib.parse import quote
    filename = f"Pixiv OAuth CLi Setup{arch}_latest.exe"
    return f"{DOWNLOADS_BASE_URL}/{quote(filename)}"

def _self_update(target_version: str, target_code: str) -> bool:
    _clear_menu_screen()
    print(colorize("Downloading latest update and installing requirements...", Ansi.CYAN, True))
    is_frozen = getattr(sys, "frozen", False)
    try:
        if is_frozen:
            exe_path = Path(sys.executable).resolve()
            is_setup = "program files" in str(exe_path).lower() or "setup" in exe_path.name.lower()
            if is_setup:
                import tempfile
                print(" - Download latest setup installer...")
                setup_file = Path(tempfile.gettempdir()) / "pixiv_cli_setup_latest.exe"
                resp_s = requests.get(_get_cli_setup_url(exe_path), timeout=60, stream=True)
                resp_s.raise_for_status()
                with setup_file.open("wb") as fh:
                    for chunk in resp_s.iter_content(chunk_size=1024 * 128):
                        if chunk:
                            fh.write(chunk)
                print(" - Running installer silently...")
                subprocess.Popen([str(setup_file), "/SP-", "/VERYSILENT", "/NORESTART"], shell=False)
                set_current_app_identity(target_version, target_code)
                return True
            # Portable — download new exe and replace via bat
            new_exe = exe_path.with_name(exe_path.stem + "_new.exe")
            print(" - Download latest portable exe...")
            resp = requests.get(_get_cli_portable_url(exe_path), timeout=60, stream=True)
            resp.raise_for_status()
            with new_exe.open("wb") as fh:
                for chunk in resp.iter_content(chunk_size=1024 * 128):
                    if chunk:
                        fh.write(chunk)
            print(" - Preparing updater...")
            bat = exe_path.with_name("pixiv_cli_updater.bat")
            bat.write_text(
                "@echo off\n"
                "timeout /t 2 /nobreak >nul\n"
                f'if exist "{exe_path}.old" del /f /q "{exe_path}.old" >nul 2>nul\n'
                f'move /y "{exe_path}" "{exe_path}.old" >nul\n'
                f'move /y "{new_exe}" "{exe_path}" >nul\n'
                "del \"%~f0\"\n",
                encoding="utf-8",
            )
            set_current_app_identity(target_version, target_code)
            subprocess.Popen(
                ["cmd", "/c", str(bat)],
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            return True
        else:
            # Running as plain .py — overwrite script and reinstall deps
            print(" - Download latest app...")
            response = requests.get(RAW_MAIN_PY_URL, timeout=30)
            response.raise_for_status()
            print(" - Install dependencies...")
            Path(__file__).write_text(response.text, encoding="utf-8")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(Path(__file__).with_name("requirements.txt"))],
                check=False,
            )
            set_current_app_identity(target_version, target_code)
            return True
    except requests.RequestException:
        _render_rich_text_panel(mt("version_title", "en"), [mt("version_no_internet_update", "en")], mt("enter_continue", "en"))
    except Exception as exc:
        _render_rich_text_panel(mt("version_title", "en"), [f"{mt('version_update_failed', 'en')}: {exc}"], mt("enter_continue", "en"))
    return False


def _open_version_menu(lang: str, color_on: bool) -> None:
    debug_print(f"Opening version menu (lang={lang})", color_on)
    status_line: str = ""
    checked: bool = False
    while True:
        current_version = get_current_app_version()
        current_code = get_current_app_code()
        latest = _fetch_latest_release_tag_cached()
        latest_code = _get_latest_release_code_cached()
        has_update = bool(latest and _version_key(latest) > _version_key(current_version))
        if not has_update and latest and _version_key(latest) == _version_key(current_version):
            has_update = bool(latest_code and latest_code != current_code)

        _clear_menu_screen()
        print(colorize(mt("version_title", lang), Ansi.CYAN + Ansi.BOLD, color_on))
        print()
        print(f"{mt('version_current', lang)}: {current_version}", end="")
        if status_line:
            print(f"  {status_line}", end="")
        print()
        print()

        if checked:
            input(colorize("[+] Ok: ", Ansi.YELLOW, color_on))
            return

        if has_update and latest:
            print(colorize(f"[1] {mt('version_update_now', lang)} ({mt('version_new_badge', lang)} {latest})", Ansi.GREEN, color_on))
            print(colorize(f"[0] {mt('version_later', lang)}", Ansi.DIM, color_on))
        else:
            print(colorize(f"[1] {mt('version_check_update', lang)}", Ansi.GREEN, color_on))
            print(colorize(f"[0] {mt('back', lang)}", Ansi.DIM, color_on))
        choice = input(colorize(f"\n[+] {mt('select_option', lang)}: ", Ansi.YELLOW, color_on)).strip()
        debug_print(f"Version menu choice: {choice}", color_on)

        if choice == "1":
            if has_update and latest:
                # Do the update immediately
                success = _self_update(latest, latest_code or APP_BUILD_CODE)
                debug_print(f"Self-update execution result: {success}", color_on)
                if success:
                    status_line = f"{mt('version_update_success', lang)} {get_current_app_version()}."
                else:
                    status_line = mt("version_update_failed", lang)
                checked = True
            else:
                latest = _fetch_latest_release_tag_cached(force=True)
                latest_code = _get_latest_release_code_cached(force=True)
                current_version = get_current_app_version()
                current_code = get_current_app_code()
                debug_print(f"Version check result -> current={current_version}/{current_code}, latest={latest}/{latest_code}", color_on)
                if not latest:
                    status_line = mt("version_no_internet_check", lang)
                    checked = True
                elif _version_key(latest) <= _version_key(current_version) and (not latest_code or latest_code == current_code):
                    status_line = mt("version_latest", lang)
                    checked = True
                elif _version_key(latest) < _version_key(current_version):
                    status_line = f"{mt('version_latest_available', lang)}: {latest}"
                    checked = True
                else:
                    # Update now available — loop will redraw with Update/Later
                    pass
        elif choice == "0":
            return
        else:
            print(colorize(mt("invalid_option", lang), Ansi.RED, color_on))



def show_developer_info_cli(lang: str, color_on: bool) -> None:
    print()
    print(colorize(mt("developer_info", lang), Ansi.BOLD + Ansi.CYAN, color_on))
    print(colorize(f"{mt('developer', lang)}: {DEVELOPER_NAME}", Ansi.BOLD, color_on))
    print(colorize(f"GitHub: {REPO_BASE_URL}", Ansi.BLUE, color_on))
    print(colorize(f"TikTok: {TIKTOK_URL}", Ansi.BLUE, color_on))
    print(colorize(f"Twitter/X: {TWITTER_URL}", Ansi.BLUE, color_on))


# ===== STARTUP INTERNET CHECK =====
_NET_CHECK_LABELS: dict[str, dict[str, str]] = {
    "en": {
        "checking": "Checking internet connection",
        "connected": "Connected",
        "no_internet": "No internet connection. Retrying",
        "tip": "Press Ctrl+C to exit",
    },
    "id": {
        "checking": "Memeriksa koneksi internet",
        "connected": "Terhubung",
        "no_internet": "Tidak ada koneksi internet. Mencoba lagi",
        "tip": "Tekan Ctrl+C untuk keluar",
    },
    "jp": {
        "checking": "インターネット接続を確認中",
        "connected": "接続済み",
        "no_internet": "インターネット接続なし。再試行中",
        "tip": "Ctrl+C で終了",
    },
    "de": {
        "checking": "Internetverbindung wird geprüft",
        "connected": "Verbunden",
        "no_internet": "Keine Internetverbindung. Erneuter Versuch",
        "tip": "Strg+C zum Beenden",
    },
    "fr": {
        "checking": "Vérification de la connexion internet",
        "connected": "Connecté",
        "no_internet": "Pas de connexion internet. Nouvelle tentative",
        "tip": "Ctrl+C pour quitter",
    },
    "es": {
        "checking": "Verificando conexión a internet",
        "connected": "Conectado",
        "no_internet": "Sin conexión a internet. Reintentando",
        "tip": "Ctrl+C para salir",
    },
    "ru": {
        "checking": "Проверка интернет-соединения",
        "connected": "Подключено",
        "no_internet": "Нет соединения с интернетом. Повторная попытка",
        "tip": "Ctrl+C для выхода",
    },
    "pt": {
        "checking": "Verificando conexão com a internet",
        "connected": "Conectado",
        "no_internet": "Sem conexão com a internet. Tentando novamente",
        "tip": "Ctrl+C para sair",
    },
    "pl": {
        "checking": "Sprawdzanie połączenia z internetem",
        "connected": "Połączono",
        "no_internet": "Brak połączenia z internetem. Ponowna próba",
        "tip": "Ctrl+C aby wyjść",
    },
    "zh": {
        "checking": "正在检查网络连接",
        "connected": "已连接",
        "no_internet": "没有网络连接。正在重试",
        "tip": "Ctrl+C 退出",
    },
    "kr": {
        "checking": "인터넷 연결 확인 중",
        "connected": "연결됨",
        "no_internet": "인터넷 연결 없음. 재시도 중",
        "tip": "Ctrl+C로 종료",
    },
}


def _nl(key: str, lang: str) -> str:
    return _NET_CHECK_LABELS.get(lang, _NET_CHECK_LABELS["en"]).get(
        key, _NET_CHECK_LABELS["en"][key]
    )


def _check_internet(timeout: int = 4) -> bool:
    """Try to reach GitHub (used for docs) and Pixiv OAuth endpoint."""
    try:
        resp = requests.get(
            "https://raw.githubusercontent.com", timeout=timeout, stream=False
        )
        return resp.status_code < 500
    except Exception:
        return False


def _startup_internet_check(lang: str, color_on: bool) -> None:
    """Block until internet is available, displaying a spinner."""
    import itertools
    import sys
    import threading

    SPINNER = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    spin_iter = itertools.cycle(SPINNER)
    _stop_event = threading.Event()
    _result: list[bool] = [False]

    def _checker() -> None:
        _result[0] = _check_internet()
        _stop_event.set()

    RETRY_DELAY = 3  # seconds between retries

    while True:
        _stop_event.clear()
        _result[0] = False
        t = threading.Thread(target=_checker, daemon=True)
        t.start()

        # Animate while checking
        checking_label = _nl("checking", lang)
        while not _stop_event.is_set():
            frame = next(spin_iter)
            sys.stdout.write(
                f"\r  {colorize(frame, Ansi.CYAN, color_on)} "
                f"{colorize(checking_label + '...', Ansi.DIM, color_on)}    "
            )
            sys.stdout.flush()
            time.sleep(0.08)

        t.join()

        if _result[0]:
            # Connected!
            sys.stdout.write(
                f"\r  {colorize('[+]', Ansi.GREEN, color_on)} "
                f"{colorize(_nl('connected', lang), Ansi.GREEN + Ansi.BOLD, color_on)}          \n"
            )
            sys.stdout.flush()
            time.sleep(0.8)
            return
        else:
            # No internet — show message and keep retrying
            no_int_label = _nl("no_internet", lang)
            tip_label = _nl("tip", lang)
            for i in range(RETRY_DELAY * 12):  # count down in 1/12s steps
                frame = next(spin_iter)
                elapsed = RETRY_DELAY - (i // 12)
                sys.stdout.write(
                    f"\r  {colorize(frame, Ansi.RED, color_on)} "
                    f"{colorize(no_int_label + f' ({elapsed}s)...', Ansi.RED, color_on)}  "
                    f"{colorize(f'  [{tip_label}]', Ansi.DIM, color_on)}    "
                )
                sys.stdout.flush()
                time.sleep(1 / 12)


def run_interactive_menu(lang: str, color_on: bool) -> None:
    current_lang = lang
    _startup_internet_check(current_lang, color_on)
    while True:
        if False:  # rich removed, always use plain ANSI
            pass
        else:
            _clear_menu_screen()
            print_cli_banner(current_lang, color_on)
            for key, label, style in _build_menu_options(current_lang):
                ansi_style = {
                    "green": Ansi.GREEN,
                    "magenta": Ansi.MAGENTA,
                    "white": Ansi.DIM,
                }.get(style, Ansi.GREEN)
                print(colorize(f"[{key}] {label}", ansi_style, color_on))
            choice = input(colorize(f"\n[+] {mt('select_option', current_lang)}: ", Ansi.YELLOW, color_on)).strip()
        debug_print(_dbg_msg("menu_option_selected", choice=choice))

        if choice == "8":
            _open_debug_menu(current_lang, color_on)
            continue
        elif choice == "1":
            current_lang = _choose_language_interactive(current_lang, color_on)
        elif choice == "2":
            show_cli_tutorial(current_lang, color_on)
        elif choice == "3":
            _open_resources_docs_menu(current_lang, color_on)
        elif choice == "4":
            _open_support_menu(current_lang, color_on)
        elif choice == "5":
            _open_social_menu(current_lang, color_on)
        elif choice == "6":
            login(current_lang, color_on)
        elif choice == "7":
            _open_version_menu(current_lang, color_on)
        elif choice == "0":
            print(colorize(mt("exiting", current_lang), Ansi.GREEN, color_on))
            return
        else:
            print(colorize(mt("invalid_option", current_lang), Ansi.RED, color_on))


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
    MAGENTA = "\033[35m"
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
def get_current_app_version() -> str:
    try:
        if VERSION_FILE.exists():
            raw = VERSION_FILE.read_text(encoding="utf-8").strip()
            if raw:
                if raw.startswith("{"):
                    data = json.loads(raw)
                    version = data.get("version")
                    if isinstance(version, str) and version.strip():
                        return version.strip()
                return raw.split("|")[0].strip()
    except Exception:
        pass

    cfg = load_config()
    v = cfg.get("app_version")
    if isinstance(v, str) and v.strip():
        return v.strip()
    return APP_VERSION


def get_current_app_code() -> str:
    try:
        if VERSION_FILE.exists():
            raw = VERSION_FILE.read_text(encoding="utf-8").strip()
            if raw:
                if raw.startswith("{"):
                    data = json.loads(raw)
                    code = data.get("build_code")
                    if isinstance(code, str) and code.strip():
                        return code.strip()
                parts = raw.split("|", 1)
                if len(parts) == 2 and parts[1].strip():
                    return parts[1].strip()
    except Exception:
        pass

    cfg = load_config()
    code = cfg.get("app_build_code")
    if isinstance(code, str) and code.strip():
        return code.strip()
    return APP_BUILD_CODE


def set_current_app_identity(version: str, build_code: str) -> None:
    identity = {
        "version": version.strip(),
        "build_code": build_code.strip(),
    }
    try:
        VERSION_FILE.write_text(json.dumps(identity, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

    cfg = load_config()
    cfg["app_version"] = identity["version"]
    cfg["app_build_code"] = identity["build_code"]
    save_config(cfg)


def load_config() -> dict:
    try:
        if CONFIG_FILE.exists():
            debug_print(_dbg_msg("loaded_config", path=CONFIG_FILE)); return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        debug_print(f"Failed to load config: {e}")
    return {}


def save_config(cfg: dict) -> None:
    debug_print(f"Saving config: {cfg}")
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    debug_print(f"Config successfully written to disk")


def set_default_lang(lang: str) -> None:
    debug_print(f"Setting default lang to: {lang}")
    cfg = load_config()
    cfg["default_lang"] = lang
    save_config(cfg)


def get_default_lang_from_config() -> str | None:
    cfg = load_config()
    lang = cfg.get("default_lang")
    debug_print(_dbg_msg("read_default_lang", lang=lang))
    if isinstance(lang, str) and lang in SUPPORTED_LANGS:
        return lang
    return None


# ===== SYSTEM LANGUAGE DETECTION =====
def _normalize_locale(loc: str | None) -> str | None:
    debug_print(f"Normalizing locale: {loc}")
    if not loc:
        return None
    # Examples: "id_ID", "en_US", "ja_JP", "zh_CN", "pt_BR"
    loc = loc.strip()
    if not loc:
        return None
    loc = loc.replace("-", "_")
    return loc


def detect_system_lang() -> str | None:
    debug_print("Detecting system language...")
    # Try environment first
    for key in ("LC_ALL", "LC_MESSAGES", "LANG"):
        v = _normalize_locale(os.environ.get(key))
        if v:
            code = v.split(".")[0].split("_")[0].lower()
            mapped = map_locale_to_lang(code)
            if mapped:
                return mapped

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
    debug_print(f"Mapping OS locale {two_letter} to {lang}")
    if lang in SUPPORTED_LANGS:
        return lang
    return None


def resolve_lang(explicit_lang: str | None) -> str:
    global DEBUG_LANG
    debug_print(_dbg_msg("resolving_language", explicit=explicit_lang))
    if explicit_lang and explicit_lang in SUPPORTED_LANGS:
        DEBUG_LANG = explicit_lang
        return explicit_lang
    cfg_lang = get_default_lang_from_config()
    if cfg_lang:
        DEBUG_LANG = cfg_lang
        return cfg_lang
    sys_lang = detect_system_lang()
    if sys_lang:
        DEBUG_LANG = sys_lang
        return sys_lang
    DEBUG_LANG = DEFAULT_LANG
    return DEFAULT_LANG


# ===== PKCE =====
def s256(data: bytes) -> str:
    debug_print("Hashing and encoding PKCE challenge via SHA-256")
    return urlsafe_b64encode(sha256(data).digest()).rstrip(b"=").decode("ascii")


def oauth_pkce(transform):
    code_verifier = token_urlsafe(32)
    code_challenge = transform(code_verifier.encode("ascii"))
    debug_print(f"Generated PKCE verifier: {code_verifier[:5]}... challenge: {code_challenge[:5]}...")
    return code_verifier, code_challenge


# ===== CLIPBOARD =====
def _copy_to_clipboard(value: str) -> bool:
    if not value:
        return False
    try:
        if os.name == "nt":
            proc = subprocess.run(["clip"], input=value, text=True, check=False)
            return proc.returncode == 0
        if sys.platform == "darwin":
            proc = subprocess.run(["pbcopy"], input=value, text=True, check=False)
            return proc.returncode == 0
        proc = subprocess.run(["xclip", "-selection", "clipboard"], input=value, text=True, check=False)
        return proc.returncode == 0
    except Exception:
        return False


def _post_login_actions(tokens: dict, lang: str, color_on: bool, detected_code: str = "") -> None:
    L = get_lang(lang)
    status_msg: str = ""
    status_opt: str = ""  # "1", "2", or "3"
    while True:
        _clear_menu_screen()
        print(colorize(mt("login_actions_title", lang), Ansi.CYAN + Ansi.BOLD, color_on))
        print()
        print(L["open_browser"])
        print(L["paste_url"])
        if detected_code:
            print(f"{L['code_detected']} {detected_code}")
        print(colorize(mt("login_success", lang), Ansi.GREEN + Ansi.BOLD, color_on))
        print(f"access_token : {tokens.get('access_token', '')}")
        print(f"refresh_token: {tokens.get('refresh_token', '')}")
        print(f"expires_in   : {tokens.get('expires_in', 0)}")
        print()

        def _opt_line(num: str, label: str) -> str:
            base = f"[{num}] {label}"
            if status_opt == num and status_msg:
                return base + colorize(f"  ({status_msg})", Ansi.DIM, color_on)
            return base

        print(colorize(_opt_line("1", mt("login_action_refresh", lang)), Ansi.GREEN, color_on))
        print(colorize(_opt_line("2", mt("login_action_copy_access", lang)), Ansi.GREEN, color_on))
        print(colorize(_opt_line("3", mt("login_action_copy_refresh", lang)), Ansi.GREEN, color_on))
        print(colorize(f"[0] {mt('debug_exit', lang)}", Ansi.DIM, color_on))

        if status_msg:
            # Auto-clear after 2 seconds without waiting for input
            time.sleep(2)
            status_msg = ""
            status_opt = ""
            continue

        choice = input(colorize(f"\n[+] {mt('select_option', lang)}: ", Ansi.YELLOW, color_on)).strip()
        debug_print(f"Post-login actions choice: {choice}", color_on)

        if choice == "1":
            refreshed = refresh(tokens.get("refresh_token", ""), lang, color_on)
            if refreshed:
                tokens.update(refreshed)
                status_msg = mt("login_action_refresh_success", lang)
            else:
                status_msg = mt("login_action_refresh_failed", lang)
            status_opt = "1"
        elif choice == "2":
            ok = _copy_to_clipboard(tokens.get("access_token", ""))
            status_msg = mt("login_action_access_copied", lang) if ok else mt("login_action_access_copy_failed", lang)
            status_opt = "2"
        elif choice == "3":
            ok = _copy_to_clipboard(tokens.get("refresh_token", ""))
            status_msg = mt("login_action_refresh_copied", lang) if ok else mt("login_action_refresh_copy_failed", lang)
            status_opt = "3"
        elif choice == "0":
            print(colorize(mt("exiting", lang), Ansi.GREEN, color_on))
            return
        else:
            print(colorize(mt("invalid_option", lang), Ansi.RED, color_on))


# ===== PRINT TOKEN =====
def print_auth_token_response(response, lang: str, color_on: bool) -> dict | None:
    L = get_lang(lang)
    debug_print(f"Response Status: {response.status_code}")
    debug_print(f"Raw Response Body: {response.text}")
    data = response.json()

    if "access_token" not in data:
        print("\n" + colorize(L["error_response"], Ansi.RED + Ansi.BOLD, color_on))
        pprint(data)
        return None

    print()
    print(colorize(mt("login_success", lang), Ansi.GREEN + Ansi.BOLD, color_on))
    print()
    print(colorize("access_token :", Ansi.BOLD, color_on), data["access_token"])
    print(colorize("refresh_token:", Ansi.BOLD, color_on), data["refresh_token"])
    print(colorize("expires_in   :", Ansi.BOLD, color_on), data.get("expires_in", 0))
    return data


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
    debug_print(f"Generated Login URL: {login_url}")

    open_url(login_url)

    raw_input_value = _render_rich_text_panel(
        mt("opt_login", lang),
        [L["open_browser"], "", L["paste_url"]],
        mt("login_paste_prompt", lang),
    )
    raw_input_value = (raw_input_value or "").strip()
    if raw_input_value == "":
        print(colorize(mt("login_canceled", lang), Ansi.YELLOW, color_on))
        return
    debug_print(f"User inputted raw value: {raw_input_value}")

    try:
        if raw_input_value.startswith("pixiv://"):
            parsed = urlparse(raw_input_value)
            code = parse_qs(parsed.query)["code"][0]
            debug_print(f"Parsed code from pixiv:// URL: {code}")
        else:
            code = raw_input_value
    except Exception as e:
        debug_print(f"Failed to parse pixiv code: {e}")
        print(colorize(L["invalid_code"], Ansi.RED, color_on))
        return

    print(colorize(L["code_detected"], Ansi.BLUE, color_on), code)

    debug_print(f"Sending POST request to {AUTH_TOKEN_URL} for token exchange")
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

    tokens = print_auth_token_response(response, lang, color_on)
    if not tokens:
        return
    _post_login_actions(tokens, lang, color_on, code)


# ===== REFRESH FLOW =====
def refresh(refresh_token: str, lang: str, color_on: bool):
    debug_print("User selected refresh flow...")
    debug_print(f"Refresh Token used: {refresh_token[:10]}...")
    debug_print(f"Sending POST request to {AUTH_TOKEN_URL} for token exchange")
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

    return print_auth_token_response(response, lang, color_on)


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
    parser.add_argument(
        "--lang",
        default=None,
        metavar="CODE",
        help=(
            "Set language for this session (e.g. jp, id, zh, kr, de, fr, es, ru, pt, pl, en). "
            "Overrides saved config and OS detection. "
            "Use 'config set-lang <code>' to save permanently."
        )
    )

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

    # menu
    menu_parser = subparsers.add_parser("menu", help="Open interactive menu")
    menu_parser.add_argument("--lang", default=None, help="Language code (e.g. en, id, jp)")
    config_sub = config_parser.add_subparsers(dest="config_cmd")

    config_sub.add_parser("show", help="Show current config (default)")

    setlang = config_sub.add_parser("set-lang", help="Set default language saved to config")
    setlang.add_argument("language")

    args = parser.parse_args()
    color_on = _supports_color(args.no_color)
    debug_print(_dbg_msg("parsed_arguments", args=args), color_on)
    debug_print(_dbg_msg("command_selected", command=args.command), color_on)

    # Determine effective lang: subcommand --lang takes priority over top-level --lang
    top_lang = getattr(args, "lang", None)

    if args.command == "login":
        # subcommand --lang overrides top-level --lang
        sub_lang = getattr(args, "lang", None)
        lang = resolve_lang(sub_lang or top_lang)
        login(lang, color_on)

    elif args.command == "lang":
        lang = resolve_lang(getattr(args, "language", None) or top_lang)
        login(lang, color_on)

    elif args.command == "refresh":
        sub_lang = getattr(args, "lang", None)
        lang = resolve_lang(sub_lang or top_lang)
        refresh(args.refresh_token, lang, color_on)

    elif args.command == "config":
        ui_lang = resolve_lang(top_lang)

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

    elif args.command == "menu":
        sub_lang = getattr(args, "lang", None)
        lang = resolve_lang(sub_lang or top_lang)
        run_interactive_menu(lang, color_on)

    else:
        # no subcommand: open interactive menu — use --lang if provided
        lang = resolve_lang(top_lang)
        run_interactive_menu(lang, color_on)


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
