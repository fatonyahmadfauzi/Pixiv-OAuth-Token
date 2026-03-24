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

from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


# ===== CONFIG =====
DEBUG_MODE = False
MENU_CONSOLE_WIDTH = 90

def debug_print(msg: str, color_on: bool = True):
    if DEBUG_MODE:
        print(f"\033[35m[DEBUG] {msg}\033[0m" if color_on else f"[DEBUG] {msg}")

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
    "debug_current": "Current"
}

MENU_UI_OVERRIDES = {
    "id": {
        "menu_title": "Menu Utama",
        "opt_change_lang": "Ubah Bahasa",
        "opt_tutorial": "Tutorial",
        "opt_resources_docs": "Sumber Daya & Dokumentasi",
        "opt_support": "Dukungan",
        "opt_social": "Sosial",
        "opt_login": "Login",
        "opt_exit": "Keluar",
        "select_option": "Pilih opsi",
        "invalid_option": "Opsi tidak valid.",
        "choose_lang": "Pilih kode bahasa",
        "lang_updated": "Bahasa default diperbarui menjadi",
        "resources_docs_title": "Sumber Daya & Dokumentasi",
        "res_docs_documentation": "Dokumentasi",
        "res_docs_license": "Lisensi",
        "res_docs_pixiv": "Endpoint OAuth Pixiv",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Dijalankan di Vercel",
        "support_title": "Dukungan",
        "sup_contact": "Hubungi Kami",
        "sup_report": "Laporkan Masalah",
        "sup_discussions": "Diskusi",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "Dukungan / Donasi",
        "social_title": "Tautan Sosial",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "back": "Kembali",
        "tutorial_title": "Tutorial CLI",
        "tutorial_desc": "Ikuti langkah berikut untuk mendapatkan token Pixiv OAuth langsung dari CLI ini.",
        "tutorial_step1": "1) Pilih opsi [6] Login.",
        "tutorial_step2": "2) Browser akan terbuka ke halaman login Pixiv.",
        "tutorial_step3": "3) Setelah login, salin URL callback pixiv:// lengkap.",
        "tutorial_step4": "4) Paste URL/code pada prompt CLI.",
        "tutorial_step5": "5) CLI mendeteksi code dan menukar token.",
        "tutorial_step6": "6) access_token dan refresh_token ditampilkan.",
        "tutorial_example": "Contoh output",
        "developer_info": "Informasi Pengembang",
        "opt_debug": "Alihkan Mode Debug",
        "debug_enabled": "Mode debug sekarang DIAKTIFKAN.",
        "debug_disabled": "Mode debug sekarang DINONAKTIFKAN.",
        "debug_current": "Saat ini"
    },
    "jp": {
        "menu_title": "メインメニュー",
        "opt_change_lang": "言語を変更",
        "opt_tutorial": "チュートリアル",
        "opt_resources_docs": "リソースとドキュメント",
        "opt_support": "サポート",
        "opt_social": "ソーシャル",
        "opt_login": "ログイン",
        "opt_exit": "終了",
        "select_option": "オプションを選択",
        "invalid_option": "無効なオプションです。",
        "choose_lang": "言語コードを選択",
        "lang_updated": "デフォルト言語が更新されました",
        "resources_docs_title": "リソースとドキュメント",
        "res_docs_documentation": "ドキュメント",
        "res_docs_license": "ライセンス",
        "res_docs_pixiv": "Pixiv OAuthエンドポイント",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Vercelでデプロイ",
        "support_title": "サポート",
        "sup_contact": "お問い合わせ",
        "sup_report": "問題を報告",
        "sup_discussions": "ディスカッション",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "サポート / 寄付",
        "social_title": "ソーシャルリンク",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "back": "戻る",
        "tutorial_title": "CLIチュートリアル",
        "tutorial_desc": "これらのステップに従って、このCLIから直接Pixiv OAuthトークンを取得します。",
        "tutorial_step1": "1) オプション [6] Loginを選択します。",
        "tutorial_step2": "2) ブラウザがPixivログインページに開きます。",
        "tutorial_step3": "3) ログイン後、完全なpixiv:// URLコールバックをコピーします。",
        "tutorial_step4": "4) URLやコードをCLIプロンプトに貼り付けます。",
        "tutorial_step5": "5) CLIはコードを検出してトークンを交換します。",
        "tutorial_step6": "6) access_tokenおよびrefresh_tokenが表示されます。",
        "tutorial_example": "出力例",
        "developer_info": "開発者情報",
        "opt_debug": "デバッグモードの切り替え",
        "debug_enabled": "デバッグモードが【有効】になりました。",
        "debug_disabled": "デバッグモードが【無効】になりました。",
        "debug_current": "現在"
    },
    "pl": {
        "menu_title": "Menu główne",
        "opt_change_lang": "Zmień język",
        "opt_tutorial": "Samouczek",
        "opt_resources_docs": "Zasoby i dokumentacja",
        "opt_support": "Wsparcie",
        "opt_social": "Społeczne",
        "opt_login": "Zaloguj się",
        "opt_exit": "Wyjście",
        "select_option": "Wybierz opcję",
        "invalid_option": "Nieprawidłowa opcja.",
        "choose_lang": "Wybierz kod języka",
        "lang_updated": "Domyślny język został zaktualizowany na",
        "resources_docs_title": "Zasoby i dokumentacja",
        "res_docs_documentation": "Dokumentacja",
        "res_docs_license": "Licencja",
        "res_docs_pixiv": "Endpoint OAuth Pixiv",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Wdrożone na Vercel",
        "support_title": "Wsparcie",
        "sup_contact": "Skontaktuj się z nami",
        "sup_report": "Zgłoś problem",
        "sup_discussions": "Dyskusje",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "Wsparcie / Darowizna",
        "social_title": "Linki społeczne",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "back": "Powrót",
        "tutorial_title": "Samouczek CLI",
        "tutorial_desc": "Postępuj zgodnie z tymi krokami, aby uzyskać tokeny Pixiv OAuth bezpośrednio z tego CLI.",
        "tutorial_step1": "1) Wybierz opcję [6] Zaloguj się.",
        "tutorial_step2": "2) Przeglądarka otwiera stronę logowania Pixiv.",
        "tutorial_step3": "3) Po zalogowaniu skopiuj pełny adres URL pixiv://.",
        "tutorial_step4": "4) Wklej adres URL/kod w monit CLI.",
        "tutorial_step5": "5) CLI wykrywa kod i wymienia token.",
        "tutorial_step6": "6) Wyświetlane są access_token i refresh_token.",
        "tutorial_example": "Przykład wyniku",
        "developer_info": "Informacje o deweloperze",
        "opt_debug": "Przełącz tryb debugowania",
        "debug_enabled": "Tryb debugowania jest teraz WŁĄCZONY.",
        "debug_disabled": "Tryb debugowania jest teraz WYŁĄCZONY.",
        "debug_current": "Obecny"
    },
    "zh": {
        "menu_title": "主菜单",
        "opt_change_lang": "更改语言",
        "opt_tutorial": "教程",
        "opt_resources_docs": "资源和文档",
        "opt_support": "支持",
        "opt_social": "社交",
        "opt_login": "登录",
        "opt_exit": "退出",
        "select_option": "选择选项",
        "invalid_option": "无效选项。",
        "choose_lang": "选择语言代码",
        "lang_updated": "默认语言已更新为",
        "resources_docs_title": "资源和文档",
        "res_docs_documentation": "文档",
        "res_docs_license": "许可证",
        "res_docs_pixiv": "Pixiv OAuth端点",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "部署在Vercel上",
        "support_title": "支持",
        "sup_contact": "联系我们",
        "sup_report": "报告问题",
        "sup_discussions": "讨论",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "支持 / 捐赠",
        "social_title": "社交链接",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "back": "返回",
        "tutorial_title": "CLI教程",
        "tutorial_desc": "按照以下步骤直接从此CLI获取Pixiv OAuth令牌。",
        "tutorial_step1": "1) 选择选项 [6] 登录。",
        "tutorial_step2": "2) 浏览器打开Pixiv登录页面。",
        "tutorial_step3": "3) 登录后，复制完整的pixiv:// URL回调。",
        "tutorial_step4": "4) 将URL/代码粘贴到CLI提示中。",
        "tutorial_step5": "5) CLI检测代码并交换令牌。",
        "tutorial_step6": "6) 显示access_token和refresh_token。",
        "tutorial_example": "输出示例",
        "developer_info": "开发者信息",
        "opt_debug": "切换调试模式",
        "debug_enabled": "调试模式现在已启用。",
        "debug_disabled": "调试模式现在已禁用。",
        "debug_current": "当前"
    },
    "de": {
        "menu_title": "Hauptmenü",
        "opt_change_lang": "Sprache ändern",
        "opt_tutorial": "Anleitung",
        "opt_resources_docs": "Ressourcen & Dokumentation",
        "opt_support": "Unterstützung",
        "opt_social": "Sozial",
        "opt_login": "Anmelden",
        "opt_exit": "Beenden",
        "select_option": "Option wählen",
        "invalid_option": "Ungültige Option.",
        "choose_lang": "Sprachcode wählen",
        "lang_updated": "Standardsprache wurde aktualisiert auf",
        "resources_docs_title": "Ressourcen & Dokumentation",
        "res_docs_documentation": "Dokumentation",
        "res_docs_license": "Lizenz",
        "res_docs_pixiv": "Pixiv OAuth Endpoint",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Auf Vercel bereitgestellt",
        "support_title": "Unterstützung",
        "sup_contact": "Kontaktieren Sie uns",
        "sup_report": "Problem melden",
        "sup_discussions": "Diskussionen",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "Unterstützung / Spende",
        "social_title": "Soziale Links",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "back": "Zurück",
        "tutorial_title": "CLI-Anleitung",
        "tutorial_desc": "Befolgen Sie diese Schritte, um Pixiv OAuth-Token direkt von dieser CLI zu erhalten.",
        "tutorial_step1": "1) Wählen Sie Option [6] Anmelden.",
        "tutorial_step2": "2) Browser öffnet die Pixiv-Anmeldeseite.",
        "tutorial_step3": "3) Nach der Anmeldung die vollständige pixiv:// URL-Rückruf kopieren.",
        "tutorial_step4": "4) URL/Code in CLI-Eingabeaufforderung einfügen.",
        "tutorial_step5": "5) CLI erkennt den Code und tauscht das Token aus.",
        "tutorial_step6": "6) access_token und refresh_token werden angezeigt.",
        "tutorial_example": "Ausgabebeispiel",
        "developer_info": "Entwicklerinformationen",
        "opt_debug": "Debug-Modus umschalten",
        "debug_enabled": "Debug-Modus ist jetzt AKTIVIERT.",
        "debug_disabled": "Debug-Modus ist jetzt DEAKTIVIERT.",
        "debug_current": "Aktuell"
    },
    "fr": {
        "menu_title": "Menu principal",
        "opt_change_lang": "Changer la langue",
        "opt_tutorial": "Tutoriel",
        "opt_resources_docs": "Ressources et documentation",
        "opt_support": "Soutien",
        "opt_social": "Réseaux sociaux",
        "opt_login": "Connexion",
        "opt_exit": "Quitter",
        "select_option": "Choisir une option",
        "invalid_option": "Option invalide.",
        "choose_lang": "Choisir le code de langue",
        "lang_updated": "La langue par défaut a été mise à jour vers",
        "resources_docs_title": "Ressources et documentation",
        "res_docs_documentation": "Documentation",
        "res_docs_license": "Licence",
        "res_docs_pixiv": "Point de terminaison Pixiv OAuth",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Déployé sur Vercel",
        "support_title": "Soutien",
        "sup_contact": "Contactez-nous",
        "sup_report": "Signaler un problème",
        "sup_discussions": "Discussions",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "Soutien / Donation",
        "social_title": "Liens sociaux",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "back": "Retour",
        "tutorial_title": "Tutoriel CLI",
        "tutorial_desc": "Suivez ces étapes pour obtenir les jetons Pixiv OAuth directement à partir de cette CLI.",
        "tutorial_step1": "1) Choisissez l'option [6] Connexion.",
        "tutorial_step2": "2) Le navigateur ouvre la page de connexion Pixiv.",
        "tutorial_step3": "3) Après la connexion, copiez l'URL de rappel complète pixiv://.",
        "tutorial_step4": "4) Collez l'URL/le code dans l'invite CLI.",
        "tutorial_step5": "5) CLI détecte le code et échange le token.",
        "tutorial_step6": "6) access_token et refresh_token sont affichés.",
        "tutorial_example": "Exemple de sortie",
        "developer_info": "Informations sur le développeur",
        "opt_debug": "Basculer le mode débogage",
        "debug_enabled": "Le mode débogage est maintenant ACTIVÉ.",
        "debug_disabled": "Le mode débogage est maintenant DÉSACTIVÉ.",
        "debug_current": "Actuel"
    },
    "es": {
        "menu_title": "Menú principal",
        "opt_change_lang": "Cambiar idioma",
        "opt_tutorial": "Tutorial",
        "opt_resources_docs": "Recursos y documentación",
        "opt_support": "Apoyo",
        "opt_social": "Social",
        "opt_login": "Iniciar sesión",
        "opt_exit": "Salir",
        "select_option": "Seleccionar opción",
        "invalid_option": "Opción no válida.",
        "choose_lang": "Elige código de idioma",
        "lang_updated": "El idioma predeterminado se ha actualizado a",
        "resources_docs_title": "Recursos y documentación",
        "res_docs_documentation": "Documentación",
        "res_docs_license": "Licencia",
        "res_docs_pixiv": "Endpoint de OAuth de Pixiv",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Implementado en Vercel",
        "support_title": "Apoyo",
        "sup_contact": "Contáctenos",
        "sup_report": "Reportar un problema",
        "sup_discussions": "Discusiones",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "Apoyo / Donación",
        "social_title": "Enlaces sociales",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "back": "Volver",
        "tutorial_title": "Tutorial CLI",
        "tutorial_desc": "Siga estos pasos para obtener tokens de OAuth de Pixiv directamente desde esta CLI.",
        "tutorial_step1": "1) Elija la opción [6] Iniciar sesión.",
        "tutorial_step2": "2) El navegador abre la página de inicio de sesión de Pixiv.",
        "tutorial_step3": "3) Después de iniciar sesión, copie la devolución de llamada de URL pixiv://.",
        "tutorial_step4": "4) Pegue la URL/código en el indicador CLI.",
        "tutorial_step5": "5) CLI detecta el código e intercambia el token.",
        "tutorial_step6": "6) Se muestran access_token y refresh_token.",
        "tutorial_example": "Salida de ejemplo",
        "developer_info": "Información del desarrollador",
        "opt_debug": "Alternar Modo Depuración",
        "debug_enabled": "El modo de depuración ahora está ACTIVADO.",
        "debug_disabled": "El modo de depuración ahora está DESACTIVADO.",
        "debug_current": "Actual"
    },
    "ru": {
        "menu_title": "Главное меню",
        "opt_change_lang": "Изменить язык",
        "opt_tutorial": "Руководство",
        "opt_resources_docs": "Ресурсы и документация",
        "opt_support": "Поддержка",
        "opt_social": "Социальные сети",
        "opt_login": "Вход",
        "opt_exit": "Выход",
        "select_option": "Выберите опцию",
        "invalid_option": "Неверная опция.",
        "choose_lang": "Выберите код языка",
        "lang_updated": "Язык по умолчанию был обновлен на",
        "resources_docs_title": "Ресурсы и документация",
        "res_docs_documentation": "Документация",
        "res_docs_license": "Лицензия",
        "res_docs_pixiv": "Конечная точка OAuth Pixiv",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Развернуто на Vercel",
        "support_title": "Поддержка",
        "sup_contact": "Свяжитесь с нами",
        "sup_report": "Сообщить о проблеме",
        "sup_discussions": "Обсуждения",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "Поддержка / Пожертвование",
        "social_title": "Социальные ссылки",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "back": "Назад",
        "tutorial_title": "Руководство CLI",
        "tutorial_desc": "Следуйте этим шагам, чтобы получить токены Pixiv OAuth прямо из этого CLI.",
        "tutorial_step1": "1) Выберите опцию [6] Вход.",
        "tutorial_step2": "2) Браузер открывает страницу входа Pixiv.",
        "tutorial_step3": "3) После входа скопируйте полный URL обратного вызова pixiv://.",
        "tutorial_step4": "4) Вставьте URL/код в командную строку CLI.",
        "tutorial_step5": "5) CLI обнаруживает код и обменивает токен.",
        "tutorial_step6": "6) Отображаются access_token и refresh_token.",
        "tutorial_example": "Пример вывода",
        "developer_info": "Информация о разработчике",
        "opt_debug": "Переключить режим отладки",
        "debug_enabled": "Режим отладки теперь ВКЛЮЧЕН.",
        "debug_disabled": "Режим отладки теперь ВЫКЛЮЧЕН.",
        "debug_current": "Текущий"
    },
    "pt": {
        "menu_title": "Menu principal",
        "opt_change_lang": "Mudar idioma",
        "opt_tutorial": "Tutorial",
        "opt_resources_docs": "Recursos e documentação",
        "opt_support": "Suporte",
        "opt_social": "Social",
        "opt_login": "Entrar",
        "opt_exit": "Sair",
        "select_option": "Selecione uma opção",
        "invalid_option": "Opção inválida.",
        "choose_lang": "Escolha o código de idioma",
        "lang_updated": "O idioma padrão foi atualizado para",
        "resources_docs_title": "Recursos e documentação",
        "res_docs_documentation": "Documentação",
        "res_docs_license": "Licença",
        "res_docs_pixiv": "Endpoint OAuth Pixiv",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Implantado no Vercel",
        "support_title": "Suporte",
        "sup_contact": "Entre em contato conosco",
        "sup_report": "Relatar um problema",
        "sup_discussions": "Discussões",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "Suporte / Doação",
        "social_title": "Links sociais",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "back": "Voltar",
        "tutorial_title": "Tutorial da CLI",
        "tutorial_desc": "Siga estas etapas para obter tokens Pixiv OAuth diretamente deste CLI.",
        "tutorial_step1": "1) Escolha a opção [6] Entrar.",
        "tutorial_step2": "2) O navegador abre a página de login do Pixiv.",
        "tutorial_step3": "3) Após o login, copie o URL de retorno completo pixiv://.",
        "tutorial_step4": "4) Cole URL/código no prompt da CLI.",
        "tutorial_step5": "5) CLI detecta o código e troca o token.",
        "tutorial_step6": "6) access_token e refresh_token são exibidos.",
        "tutorial_example": "Exemplo de saída",
        "developer_info": "Informações do desenvolvedor",
        "opt_debug": "Alternar Modo de Depuração",
        "debug_enabled": "O modo de depuração agora está ATIVADO.",
        "debug_disabled": "O modo de depuração agora está DESATIVADO.",
        "debug_current": "Atual"
    },
    "kr": {
        "menu_title": "메인 메뉴",
        "opt_change_lang": "언어 변경",
        "opt_tutorial": "튜토리얼",
        "opt_resources_docs": "리소스 및 문서",
        "opt_support": "지원",
        "opt_social": "소셜",
        "opt_login": "로그인",
        "opt_exit": "종료",
        "select_option": "옵션 선택",
        "invalid_option": "잘못된 옵션입니다.",
        "choose_lang": "언어 코드 선택",
        "lang_updated": "기본 언어가 다음으로 업데이트되었습니다",
        "resources_docs_title": "리소스 및 문서",
        "res_docs_documentation": "문서",
        "res_docs_license": "라이센스",
        "res_docs_pixiv": "Pixiv OAuth 엔드포인트",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Vercel에 배포됨",
        "support_title": "지원",
        "sup_contact": "문의하기",
        "sup_report": "문제 보고",
        "sup_discussions": "토론",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "지원 / 기부",
        "social_title": "소셜 링크",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "back": "뒤로",
        "tutorial_title": "CLI 튜토리얼",
        "tutorial_desc": "이 단계를 따라 이 CLI에서 직접 Pixiv OAuth 토큰을 얻으십시오.",
        "tutorial_step1": "1) 옵션 [6] 로그인을 선택합니다.",
        "tutorial_step2": "2) 브라우저가 Pixiv 로그인 페이지를 엽니다.",
        "tutorial_step3": "3) 로그인 후 전체 pixiv:// URL 콜백을 복사합니다.",
        "tutorial_step4": "4) CLI 프롬프트에 URL/코드를 붙여넣습니다.",
        "tutorial_step5": "5) CLI가 코드를 감지하고 토큰을 교환합니다.",
        "tutorial_step6": "6) access_token 및 refresh_token이 표시됩니다.",
        "tutorial_example": "출력 예시",
        "developer_info": "개발자 정보",
        "opt_debug": "디버그 모드 전환",
        "debug_enabled": "디버그 모드가 이제 활성화되었습니다.",
        "debug_disabled": "디버그 모드가 이제 비활성화되었습니다.",
        "debug_current": "현재"
    },
}

MENU_UI = {code: {**MENU_UI_EN, **MENU_UI_OVERRIDES.get(code, {})} for code in SUPPORTED_LANGS}


def mt(key: str, lang: str) -> str:
    return MENU_UI.get(lang, MENU_UI_EN).get(key, MENU_UI_EN.get(key, key))


def _rich_available() -> bool:
    return True


def _menu_console() -> Console:
    return Console(width=MENU_CONSOLE_WIDTH)


def _clear_menu_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def _build_menu_options(lang: str) -> list[tuple[str, str, str]]:
    debug_status = "ON" if DEBUG_MODE else "OFF"
    return [
        ("1", mt("opt_change_lang", lang), "green"),
        ("2", mt("opt_tutorial", lang), "green"),
        ("3", mt("opt_resources_docs", lang), "green"),
        ("4", mt("opt_support", lang), "green"),
        ("5", mt("opt_social", lang), "green"),
        ("6", mt("opt_login", lang), "green"),
        ("7", f"{mt('opt_debug', lang)} ({mt('debug_current', lang)}: {debug_status})", "magenta"),
        ("0", mt("opt_exit", lang), "white"),
    ]


def _render_rich_option_panel(title: str, options: list[tuple[str, str]], prompt: str) -> str:
    console = _menu_console()
    _clear_menu_screen()
    lines = [f"[{key}] {label}" for key, label in options]
    console.print(
        Panel("\n".join(lines), title=title, title_align="left", border_style="cyan", box=box.SQUARE, expand=True)
    )
    return console.input("\n[bold yellow][+][/bold yellow] [bold yellow]" + prompt + ":[/bold yellow] ").strip()


def _render_rich_text_panel(title: str, lines: list[str], prompt: str | None = None) -> str | None:
    console = _menu_console()
    _clear_menu_screen()
    console.print(
        Panel("\n".join(lines), title=title, title_align="left", border_style="cyan", box=box.SQUARE, expand=True)
    )
    if prompt is None:
        return None
    return console.input("\n[bold yellow][+][/bold yellow] [bold yellow]" + prompt + ":[/bold yellow] ").strip()


def _choose_boxed_option(title: str, options: list[tuple[str, str]], lang: str, color_on: bool) -> str:
    return _render_rich_option_panel(title, options, mt("select_option", lang))


def _render_rich_main_menu(lang: str) -> None:
    console = _menu_console()
    _clear_menu_screen()

    header_text = Text()
    header_text.append(f"🔐 {mt('project', lang)}\n", style="bold green")
    header_text.append(f"{mt('developer', lang)}: {DEVELOPER_NAME}", style="green")
    console.print(Panel(Align.center(header_text), border_style="cyan", box=box.SQUARE, expand=True))

    menu_text = Text()
    for key, label, style in _build_menu_options(lang):
        menu_text.append(f"[{key}] {label}\n" if key != "0" else f"[{key}] {label}", style=style)
    console.print(Panel(menu_text, title=mt("menu_title", lang), title_align="left", border_style="cyan", box=box.SQUARE, expand=True))

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
    lines = [f" {LANG_LABELS.get(code, code)}" for code in SUPPORTED_LANGS]
    prompt = mt("choose_lang", current_lang) + " (empty to cancel)"
    new_lang = _render_rich_text_panel(mt("opt_change_lang", current_lang), lines, prompt)
    new_lang = (new_lang or "").strip().lower()
    if new_lang == "":
        return current_lang
    if new_lang not in SUPPORTED_LANGS:
        print(colorize(mt("invalid_option", current_lang), Ansi.RED, color_on))
        return current_lang
    set_default_lang(new_lang)
    print(colorize(f"{mt('lang_updated', new_lang)} {new_lang}", Ansi.GREEN, color_on))
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
        "Opening browser for login...",
        "Paste FULL URL (pixiv://...) or paste code here:",
        "pixiv://account/login?code=eltWz8pQgT-D0foeIPzhHN_y6CwptwjXk8kJ0yzowvw&via=login",
        "Detected code: eltWz8pQgT-D0foeIPzhHN_y6CwptwjXk8kJ0yzowvw",
        "=== LOGIN SUCCESS ===",
        "access_token : uog7p1mdnJ7G3lJl30XbYQZx2otlJFwkfmfsO7gPtDU",
        "refresh_token: zF6DNiG2tvSQgnd3AkTeI6ZaVxbNf1jqU3cQX5MkyI4",
        "expires_in   : 3600",
    ]
    _render_rich_text_panel(mt("tutorial_title", lang), lines, "Enter to main menu")

def show_developer_info_cli(lang: str, color_on: bool) -> None:
    print()
    print(colorize(mt("developer_info", lang), Ansi.BOLD + Ansi.CYAN, color_on))
    print(colorize(f"{mt('developer', lang)}: {DEVELOPER_NAME}", Ansi.BOLD, color_on))
    print(colorize(f"GitHub: {REPO_BASE_URL}", Ansi.BLUE, color_on))
    print(colorize(f"TikTok: {TIKTOK_URL}", Ansi.BLUE, color_on))
    print(colorize(f"Twitter/X: {TWITTER_URL}", Ansi.BLUE, color_on))

def run_interactive_menu(lang: str, color_on: bool) -> None:
    global DEBUG_MODE
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
        debug_print(f"User selected main menu option: {choice}")

        if choice == "7":
            DEBUG_MODE = not DEBUG_MODE
            print(colorize(mt("debug_enabled", current_lang) if DEBUG_MODE else mt("debug_disabled", current_lang), Ansi.GREEN if DEBUG_MODE else Ansi.RED, color_on))
            try:
                input("\nPress Enter to continue...")
            except Exception:
                pass
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
        elif choice == "0":
            print("Exiting...")
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
def load_config() -> dict:
    try:
        if CONFIG_FILE.exists():
            debug_print(f"Loaded config from {CONFIG_FILE}"); return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
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
    debug_print(f"Reading default lang from config: {lang}")
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
    debug_print(f"Resolving language (explicit={explicit_lang})...")
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
    debug_print("Hashing and encoding PKCE challenge via SHA-256")
    return urlsafe_b64encode(sha256(data).digest()).rstrip(b"=").decode("ascii")


def oauth_pkce(transform):
    code_verifier = token_urlsafe(32)
    code_challenge = transform(code_verifier.encode("ascii"))
    debug_print(f"Generated PKCE verifier: {code_verifier[:5]}... challenge: {code_challenge[:5]}...")
    return code_verifier, code_challenge


# ===== PRINT TOKEN =====
def print_auth_token_response(response, lang: str, color_on: bool):
    L = get_lang(lang)
    debug_print(f"Response Status: {response.status_code}")
    debug_print(f"Raw Response Body: {response.text}")
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
    debug_print(f"Generated Login URL: {login_url}")

    open_url(login_url)

    raw_input_value = _render_rich_text_panel(
        mt("opt_login", lang),
        [L["open_browser"], "", L["paste_url"]],
        mt("select_option", lang),
    )
    raw_input_value = (raw_input_value or "").strip()
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

    print_auth_token_response(response, lang, color_on)


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

    # menu
    subparsers.add_parser("menu", help="Open interactive menu")
    config_sub = config_parser.add_subparsers(dest="config_cmd")

    config_sub.add_parser("show", help="Show current config (default)")

    setlang = config_sub.add_parser("set-lang", help="Set default language saved to config")
    setlang.add_argument("language")

    args = parser.parse_args()
    color_on = _supports_color(args.no_color)
    debug_print(f"Parsed arguments: {args}", color_on)
    debug_print(f"Command selected: {args.command}", color_on)

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
