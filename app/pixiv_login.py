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

from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.text import Text


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
APP_VERSION = "v1.0.2"
APP_BUILD_CODE = "BUILD-UNKNOWN"
GITHUB_API_LATEST_RELEASE = "https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest"
RAW_MAIN_PY_URL = "https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/app/pixiv_login.py"
LATEST_MANIFEST_URL = "https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/latest.json"
UPDATE_CACHE = {"latest": None, "latest_code": None, "checked_at": 0.0}

CONFIG_FILE = Path(__file__).with_name("pixiv_login_config.json")
VERSION_FILE = Path(__file__).with_name("pixiv_login_version.txt")


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
    "exiting": "Exiting..."
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
        'opt_version': 'Versi'},
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
        'res_docs_pixiv': 'Pixiv OAuthエンドポイント',
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
        'developer': '開発者'},
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
        'exiting': 'Zamykanie...'},
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
        'exiting': '正在退出...'},
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
        'exiting': 'Wird beendet...'},
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
        'exiting': 'Fermeture...'},
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
        'exiting': 'Saliendo...'},
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
        'exiting': 'Выход...'},
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
        'exiting': 'Saindo...'},
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
        'exiting': '종료 중...'}}

MENU_UI = {code: {**MENU_UI_EN, **MENU_UI_OVERRIDES.get(code, {})} for code in SUPPORTED_LANGS}


def mt(key: str, lang: str) -> str:
    return MENU_UI.get(lang, MENU_UI_EN).get(key, MENU_UI_EN.get(key, key))


def _rich_available() -> bool:
    return False


def _menu_console() -> Console:
    return Console(width=MENU_CONSOLE_WIDTH)


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
        ("7", mt("opt_changelog", lang), "green"),
        ("8", version_label, "green"),
        ("9", mt("debug_title", lang), "magenta"),
        ("0", mt("opt_exit", lang), "white"),
    ]


def _render_rich_option_panel(title: str, options: list[tuple[str, str]], prompt: str) -> str:
    _clear_menu_screen()
    print(colorize(f"=== {title} ===", Ansi.CYAN + Ansi.BOLD, True))
    lines = [f"[{key}] {label}" for key, label in options]
    print("\n".join(lines))
    return input(colorize(f"\n[+] {prompt}: ", Ansi.YELLOW, True)).strip()


def _render_rich_text_panel(title: str, lines: list[str], prompt: str | None = None) -> str | None:
    _clear_menu_screen()
    print(colorize(f"=== {title} ===", Ansi.CYAN + Ansi.BOLD, True))
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
    body_lines = [*lines, ""]
    body_lines.extend([f"[{key}] {label}" for key, label in options])
    print(colorize(f"=== {title} ===", Ansi.CYAN + Ansi.BOLD, True))
    print("\n".join(body_lines))
    return input(colorize(f"\n[+] {prompt}: ", Ansi.YELLOW, True)).strip()


def _choose_boxed_option(title: str, options: list[tuple[str, str]], lang: str, color_on: bool) -> str:
    return _render_rich_option_panel(title, options, mt("select_option", lang))


def _render_rich_main_menu(lang: str) -> None:
    _clear_menu_screen()
    print_cli_banner(lang, True)
    print(colorize(f"=== {mt('menu_title', lang)} ===", Ansi.CYAN + Ansi.BOLD, True))
    for key, label, style in _build_menu_options(lang):
        ansi_style = {"green": Ansi.GREEN, "magenta": Ansi.MAGENTA, "white": Ansi.DIM}.get(style, Ansi.GREEN)
        print(colorize(f"[{key}] {label}", ansi_style, True))

def print_cli_banner(lang: str, color_on: bool) -> None:
    title_art = [
        r"  ____  _      _         ____   _   _ _   _ _____ _   _ ",
        r" |  _ \(_)__ _(_)_ __   / __ \ / | | | | |_   _| | | |",
        r" | |_) | / _` | | '_ \ | |  | || | | | | | | | | |_| |",
        r" |  __/| | (_| | | | | || |__| || | | |_| | | | |  _  |",
        r" |_|   |_|\__, |_|_| |_| \____/ |_|  \___/  |_| |_| |_|",
        r"           |___/                                           ",
    ]
    print(colorize("=" * 70, Ansi.CYAN, color_on))
    for line in title_art:
        print(colorize(line, Ansi.BOLD + Ansi.GREEN, color_on))

    print(colorize(f"  {mt('project', lang)}", Ansi.BOLD, color_on))
    print(colorize(f"  {mt('developer', lang)}: {DEVELOPER_NAME}", Ansi.DIM, color_on))
    print(colorize("=" * 70, Ansi.CYAN, color_on))


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


def _open_resources_docs_menu(lang: str, color_on: bool) -> None:
    options = [
        ("1", mt("res_docs_documentation", lang)),
        ("2", mt("res_docs_license", lang)),
        ("3", mt("res_docs_pixiv", lang)),
        ("4", mt("res_docs_python", lang)),
        ("5", mt("res_docs_vercel", lang)),
        ("0", mt("back", lang)),
    ]
    while True:
        choice = _choose_boxed_option(mt("resources_docs_title", lang), options, lang, color_on).lower()
        debug_print(f"Resources menu choice: {choice}", color_on)
        if choice == "1":
            open_url("https://pixiv-o-auth-token.vercel.app/documentation")
        elif choice == "2":
            open_url("https://pixiv-o-auth-token.vercel.app/license")
        elif choice == "3":
            open_url("https://oauth.secure.pixiv.net/auth/token")
        elif choice == "4":
            open_url("https://www.python.org/")
        elif choice == "5":
            open_url("https://vercel.com/")
        elif choice == "0":
            return
        else:
            print(colorize(mt("invalid_option", lang), Ansi.RED, color_on))

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
            open_url("https://pixiv-o-auth-token.vercel.app/contact")
        elif choice == "2":
            open_url("https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/issues")
        elif choice == "3":
            open_url("https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/discussions")
        elif choice == "4":
            open_url("https://github.com/fatonyahmadfauzi")
        elif choice == "5":
            open_url("https://pixiv-o-auth-token.vercel.app/support")
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


def _open_changelog() -> None:
    debug_print("Opening changelog URL")
    open_url("https://pixiv-o-auth-token.vercel.app/changelog")


def _open_debug_menu(lang: str, color_on: bool) -> None:
    while True:
        recent_logs = DEBUG_LOGS[-30:] if DEBUG_LOGS else [mt("debug_empty", lang)]
        _clear_menu_screen()
        print(colorize(f"=== {mt('debug_title', lang)} ===", Ansi.CYAN + Ansi.BOLD, color_on))
        debug_lines = [*recent_logs, "", f"[1] {mt('debug_copy', lang)}", f"[2] {mt('debug_clear', lang)}", f"[0] {mt('debug_exit', lang)}"]
        print("\n".join(debug_lines))
        choice = input(colorize(f"\n[+] {mt('select_option', lang)}: ", Ansi.YELLOW, color_on)).strip()
        if choice == "1":
            payload = "\n".join(DEBUG_LOGS) if DEBUG_LOGS else mt("debug_empty", lang)
            ok = _copy_to_clipboard(payload)
            _render_rich_text_panel(
                mt("debug_title", lang),
                [mt("debug_copied", lang) if ok else mt("debug_copy_failed", lang)],
                mt("enter_continue", lang),
            )
        elif choice == "2":
            DEBUG_LOGS.clear()
            _render_rich_text_panel(mt("debug_title", lang), [mt("debug_cleared", lang)], mt("enter_continue", lang))
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


def _self_update(target_version: str, target_code: str) -> bool:
    _clear_menu_screen()
    print(colorize("Downloading latest update and installing requirements...", Ansi.CYAN, True))
    try:
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
    while True:
        current_version = get_current_app_version()
        current_code = get_current_app_code()
        latest = _fetch_latest_release_tag_cached()
        latest_code = _get_latest_release_code_cached()
        has_update = bool(latest and (latest != current_version or (latest_code and latest_code != current_code)))
        check_label = mt("version_check_update", lang)
        if has_update and latest:
            check_label = f"{mt('version_check_update', lang)} ({mt('version_new_badge', lang)} {latest})"
        _clear_menu_screen()
        print(colorize(f"=== {mt('version_title', lang)} ===", Ansi.CYAN + Ansi.BOLD, color_on))
        lines = [
            f"{mt('version_current', lang)}: {current_version}",
            "",
            f"[1] {check_label}",
            f"[0] {mt('back', lang)}",
        ]
        print("\n".join(lines))
        choice = input(colorize(f"\n[+] {mt('select_option', lang)}: ", Ansi.YELLOW, color_on)).strip()
        debug_print(f"Version menu choice: {choice}", color_on)

        if choice == "1":
            latest = _fetch_latest_release_tag_cached(force=True)
            latest_code = _get_latest_release_code_cached(force=True)
            current_version = get_current_app_version()
            current_code = get_current_app_code()
            debug_print(f"Version check result -> current={current_version}/{current_code}, latest={latest}/{latest_code}", color_on)
            if not latest:
                _render_rich_text_panel(mt("version_title", lang), [mt("version_no_internet_check", lang)], mt("enter_continue", lang))
            elif latest == current_version and (not latest_code or latest_code == current_code):
                _render_rich_text_panel(
                    mt("version_title", lang),
                    [
                        f"{mt('version_current', lang)}: {current_version}",
                        f"{mt('version_current', lang)} {current_version} {mt('version_latest', lang)}",
                    ],
                    mt("enter_continue", lang),
                )
            else:
                decision = _render_rich_combined_panel(
                    mt("version_title", lang),
                    [
                        f"{mt('version_current', lang)}: {current_version}",
                        f"{mt('version_latest_available', lang)}: {latest}",
                    ],
                    [("1", mt("version_update_now", lang)), ("2", mt("version_later", lang))],
                    mt("select_option", lang),
                )
                debug_print(f"Update decision choice: {decision}", color_on)
                if decision == "1":
                    success = _self_update(latest, latest_code or APP_BUILD_CODE)
                    debug_print(f"Self-update execution result: {success}", color_on)
                    if success:
                        _render_rich_text_panel(
                            mt("version_title", lang),
                            [
                                f"{mt('version_update_success', lang)} {get_current_app_version()}.",
                            ],
                            mt("enter_continue", lang),
                        )
                    else:
                        _render_rich_text_panel(mt("version_title", lang), [mt("version_update_failed", lang)], mt("enter_continue", lang))
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

def run_interactive_menu(lang: str, color_on: bool) -> None:
    current_lang = lang
    use_rich_menu = _rich_available()
    while True:
        if use_rich_menu:
            _render_rich_main_menu(current_lang)
            choice = _menu_console().input(
                "\n[bold yellow][+][/bold yellow] [bold yellow]" + mt("select_option", current_lang) + ":[/bold yellow] "
            ).strip()
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

        if choice == "9":
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
            _open_changelog()
        elif choice == "8":
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
    while True:
        _clear_menu_screen()
        lines = [
            L["open_browser"],
            L["paste_url"],
        ]
        if detected_code:
            lines.append(f"{L['code_detected']} {detected_code}")
        lines.extend(
            [
                L["login_success"],
                f"access_token : {tokens.get('access_token', '')}",
                f"refresh_token: {tokens.get('refresh_token', '')}",
                f"expires_in   : {tokens.get('expires_in', 0)}",
                "",
                f"[1] {mt('login_action_refresh', lang)}",
                f"[2] {mt('login_action_copy_access', lang)}",
                f"[3] {mt('login_action_copy_refresh', lang)}",
                f"[0] {mt('debug_exit', lang)}",
            ]
        )
        print(colorize(f"=== {mt('login_actions_title', lang)} ===", Ansi.CYAN + Ansi.BOLD, color_on))
        print("\n".join(lines))
        choice = input(colorize(f"\n[+] {mt('select_option', lang)}: ", Ansi.YELLOW, color_on)).strip()
        debug_print(f"Post-login actions choice: {choice}", color_on)

        if choice == "1":
            refreshed = refresh(tokens.get("refresh_token", ""), lang, color_on)
            if refreshed:
                tokens.update(refreshed)
                _render_rich_text_panel(mt("login_actions_title", lang), [mt("login_action_refresh_success", lang)], mt("enter_continue", lang))
            else:
                _render_rich_text_panel(mt("login_actions_title", lang), [mt("login_action_refresh_failed", lang)], mt("enter_continue", lang))
        elif choice == "2":
            ok = _copy_to_clipboard(tokens.get("access_token", ""))
            msg = mt("login_action_access_copied", lang) if ok else mt("login_action_access_copy_failed", lang)
            _render_rich_text_panel(mt("login_actions_title", lang), [msg], mt("enter_continue", lang))
        elif choice == "3":
            ok = _copy_to_clipboard(tokens.get("refresh_token", ""))
            msg = mt("login_action_refresh_copied", lang) if ok else mt("login_action_refresh_copy_failed", lang)
            _render_rich_text_panel(mt("login_actions_title", lang), [msg], mt("enter_continue", lang))
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

    print("\n" + colorize(L["login_success"], Ansi.GREEN + Ansi.BOLD, color_on))
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
    subparsers.add_parser("menu", help="Open interactive menu")
    config_sub = config_parser.add_subparsers(dest="config_cmd")

    config_sub.add_parser("show", help="Show current config (default)")

    setlang = config_sub.add_parser("set-lang", help="Set default language saved to config")
    setlang.add_argument("language")

    args = parser.parse_args()
    color_on = _supports_color(args.no_color)
    debug_print(_dbg_msg("parsed_arguments", args=args), color_on)
    debug_print(_dbg_msg("command_selected", command=args.command), color_on)

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

    elif args.command == "menu":
        lang = resolve_lang(None)
        run_interactive_menu(lang, color_on)

    else:
        # no subcommand: open interactive menu by default for better UX
        lang = resolve_lang(None)
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
