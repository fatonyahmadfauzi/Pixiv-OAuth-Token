#!/usr/bin/env python3
"""
Pixiv Login GUI (Tkinter) - FINAL (Extended i18n)
- UI language dropdown shows language NAMES (English, Indonesia, Polski, ...)
- UI strings translated for: EN, ID, PL, JP, ZH, DE, FR, ES, RU, PT, KR
- Pixiv OAuth PKCE login flow (open browser -> paste pixiv:// URL or code -> exchange token)
- Refresh token flow
- Copy buttons for access_token / refresh_token
- Saves config (default language CODE + refresh_token) next to the .exe (PyInstaller-friendly)
"""

from __future__ import annotations

import json
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from base64 import urlsafe_b64encode
from hashlib import sha256
from secrets import token_urlsafe
from urllib.parse import urlencode, urlparse, parse_qs
from webbrowser import open as open_url

import requests


# ===== PIXIV CONFIG =====
USER_AGENT = "PixivAndroidApp/5.0.234 (Android 11; Pixel 5)"
REDIRECT_URI = "https://app-api.pixiv.net/web/v1/users/auth/pixiv/callback"
LOGIN_URL = "https://app-api.pixiv.net/web/v1/login"
AUTH_TOKEN_URL = "https://oauth.secure.pixiv.net/auth/token"

CLIENT_ID = "MOBrBDS8blbauoSck0ZfDbtuzpyT"
CLIENT_SECRET = "lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj"

REPO_BASE_URL = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token"
README_URL = f"{REPO_BASE_URL}/blob/master/README.md"
RELEASES_URL = f"{REPO_BASE_URL}/releases"
TIKTOK_URL = "https://www.tiktok.com/@fatonyahmadfauzi"
TWITTER_URL = "https://x.com/fatonyahmad89"
DEVELOPER_NAME = "Fatony Ahmad Fauzi"

# ===== LANGUAGE =====
SUPPORTED_LANGS = ("en", "pl", "zh", "jp", "de", "fr", "es", "ru", "pt", "id", "kr")

LANG_CHOICES = [
    ("🇬🇧  English", "en"),
    ("🇵🇱  Polski", "pl"),
    ("🇨🇳  中文", "zh"),
    ("🇯🇵  日本語", "jp"),
    ("🇩🇪  Deutsch", "de"),
    ("🇫🇷  Français", "fr"),
    ("🇪🇸  Español", "es"),
    ("🇷🇺  Русский", "ru"),
    ("🇵🇹  Português", "pt"),
    ("🇮🇩  Indonesia", "id"),
    ("🇰🇷  한국어", "kr"),
]

LANG_NAME_TO_CODE = {name: code for name, code in LANG_CHOICES}
LANG_CODE_TO_NAME = {code: name for name, code in LANG_CHOICES}
LANG_LABELS = {code: name for name, code in LANG_CHOICES}


UI = {
    "en": {
        "title": "Pixiv Login (GUI)",
        "language": "Language:",
        "save_default": "Save as default",
        "refresh": "Refresh Token",
        "open_login": "Open Login Page",
        "paste": "Paste URL / Code",
        "exchange": "Exchange Token",
        "copy_access": "Copy access_token",
        "copy_refresh": "Copy refresh_token",
        "output": "Output",
        "next_step_title": "Next Step",
        "next_step_body": "After logging in, copy the FULL pixiv:// URL (or the code) and paste it into the input box, then click 'Exchange Token'.",
        "pkce_warn": "Please click 'Open Login Page' first.",
        "input_warn": "Please paste pixiv:// URL or code.",
        "copied": "Copied",
        "copied_access": "access_token copied to clipboard.",
        "copied_refresh": "refresh_token copied to clipboard.",
        "no_access": "No access_token yet. Do login/refresh first.",
        "no_refresh": "No refresh_token yet. Do login first.",
        "refresh_no_token": "No refresh_token found in config yet. Do login first.",
        "parse_fail": "Failed to parse code.",
        "net_fail": "Network/API error.",
    },
    "id": {
        "title": "Pixiv Login (GUI)",
        "language": "Bahasa:",
        "save_default": "Simpan sebagai default",
        "refresh": "Refresh Token",
        "open_login": "Buka Halaman Login",
        "paste": "Tempel URL / Kode",
        "exchange": "Tukar Token",
        "copy_access": "Salin access_token",
        "copy_refresh": "Salin refresh_token",
        "output": "Output",
        "next_step_title": "Langkah Berikutnya",
        "next_step_body": "Setelah login, salin URL pixiv:// lengkap (atau kodenya) lalu tempel ke kolom input, kemudian klik 'Tukar Token'.",
        "pkce_warn": "Klik 'Buka Halaman Login' dulu.",
        "input_warn": "Tempel URL pixiv:// atau kode dulu.",
        "copied": "Tersalin",
        "copied_access": "access_token tersalin ke clipboard.",
        "copied_refresh": "refresh_token tersalin ke clipboard.",
        "no_access": "Belum ada access_token. Silakan login/refresh dulu.",
        "no_refresh": "Belum ada refresh_token. Silakan login dulu.",
        "refresh_no_token": "Belum ada refresh_token di config. Login dulu.",
        "parse_fail": "Gagal membaca kode.",
        "net_fail": "Error jaringan/API.",
    },
    "pl": {
        "title": "Pixiv Login (GUI)",
        "language": "Język:",
        "save_default": "Zapisz jako domyślne",
        "refresh": "Odśwież token",
        "open_login": "Otwórz logowanie",
        "paste": "Wklej URL / Kod",
        "exchange": "Wymień token",
        "copy_access": "Kopiuj access_token",
        "copy_refresh": "Kopiuj refresh_token",
        "output": "Wyjście",
        "next_step_title": "Następny krok",
        "next_step_body": "Po zalogowaniu skopiuj PEŁNY URL pixiv:// (lub kod), wklej do pola, a następnie kliknij 'Wymień token'.",
        "pkce_warn": "Najpierw kliknij 'Otwórz logowanie'.",
        "input_warn": "Wklej URL pixiv:// lub kod.",
        "copied": "Skopiowano",
        "copied_access": "access_token skopiowano do schowka.",
        "copied_refresh": "refresh_token skopiowano do schowka.",
        "no_access": "Brak access_token. Najpierw zaloguj/odśwież.",
        "no_refresh": "Brak refresh_token. Najpierw zaloguj.",
        "refresh_no_token": "Brak refresh_token w konfiguracji. Najpierw zaloguj.",
        "parse_fail": "Nie udało się odczytać kodu.",
        "net_fail": "Błąd sieci/API.",
    },
    "jp": {
        "title": "Pixiv ログイン (GUI)",
        "language": "言語:",
        "save_default": "デフォルトとして保存",
        "refresh": "トークン更新",
        "open_login": "ログインページを開く",
        "paste": "URL / コードを貼り付け",
        "exchange": "トークン取得",
        "copy_access": "access_token をコピー",
        "copy_refresh": "refresh_token をコピー",
        "output": "出力",
        "next_step_title": "次の手順",
        "next_step_body": "ログイン後、完全な pixiv:// URL（またはコード）をコピーして入力欄に貼り付け、「トークン取得」をクリックしてください。",
        "pkce_warn": "先に「ログインページを開く」をクリックしてください。",
        "input_warn": "pixiv:// URL またはコードを貼り付けてください。",
        "copied": "コピーしました",
        "copied_access": "access_token をクリップボードにコピーしました。",
        "copied_refresh": "refresh_token をクリップボードにコピーしました。",
        "no_access": "access_token がありません。先にログイン/更新してください。",
        "no_refresh": "refresh_token がありません。先にログインしてください。",
        "refresh_no_token": "設定に refresh_token がありません。先にログインしてください。",
        "parse_fail": "コードの解析に失敗しました。",
        "net_fail": "ネットワーク/API エラー。",
    },
    "zh": {
        "title": "Pixiv 登录 (GUI)",
        "language": "语言：",
        "save_default": "设为默认",
        "refresh": "刷新 Token",
        "open_login": "打开登录页面",
        "paste": "粘贴 URL / 代码",
        "exchange": "兑换 Token",
        "copy_access": "复制 access_token",
        "copy_refresh": "复制 refresh_token",
        "output": "输出",
        "next_step_title": "下一步",
        "next_step_body": "登录后，复制完整的 pixiv:// URL（或代码）粘贴到输入框，然后点击“兑换 Token”。",
        "pkce_warn": "请先点击“打开登录页面”。",
        "input_warn": "请粘贴 pixiv:// URL 或代码。",
        "copied": "已复制",
        "copied_access": "已复制 access_token 到剪贴板。",
        "copied_refresh": "已复制 refresh_token 到剪贴板。",
        "no_access": "还没有 access_token，请先登录/刷新。",
        "no_refresh": "还没有 refresh_token，请先登录。",
        "refresh_no_token": "配置中没有 refresh_token，请先登录。",
        "parse_fail": "解析代码失败。",
        "net_fail": "网络/API 错误。",
    },
    "de": {
        "title": "Pixiv Login (GUI)",
        "language": "Sprache:",
        "save_default": "Als Standard speichern",
        "refresh": "Token aktualisieren",
        "open_login": "Login-Seite öffnen",
        "paste": "URL / Code einfügen",
        "exchange": "Token abrufen",
        "copy_access": "access_token kopieren",
        "copy_refresh": "refresh_token kopieren",
        "output": "Ausgabe",
        "next_step_title": "Nächster Schritt",
        "next_step_body": "Nach dem Login die vollständige pixiv:// URL (oder den Code) kopieren, einfügen und dann „Token abrufen“ klicken.",
        "pkce_warn": "Bitte zuerst „Login-Seite öffnen“ klicken.",
        "input_warn": "Bitte pixiv:// URL oder Code einfügen.",
        "copied": "Kopiert",
        "copied_access": "access_token in die Zwischenablage kopiert.",
        "copied_refresh": "refresh_token in die Zwischenablage kopiert.",
        "no_access": "Noch kein access_token. Bitte zuerst Login/Refresh.",
        "no_refresh": "Noch kein refresh_token. Bitte zuerst Login.",
        "refresh_no_token": "Kein refresh_token in der Konfiguration. Bitte zuerst Login.",
        "parse_fail": "Code konnte nicht gelesen werden.",
        "net_fail": "Netzwerk/API-Fehler.",
    },
    "fr": {
        "title": "Pixiv Login (GUI)",
        "language": "Langue :",
        "save_default": "Enregistrer par défaut",
        "refresh": "Rafraîchir le token",
        "open_login": "Ouvrir la page de connexion",
        "paste": "Coller URL / Code",
        "exchange": "Échanger le token",
        "copy_access": "Copier access_token",
        "copy_refresh": "Copier refresh_token",
        "output": "Sortie",
        "next_step_title": "Étape suivante",
        "next_step_body": "Après connexion, copiez l’URL pixiv:// complète (ou le code), collez-la dans le champ puis cliquez sur « Échanger le token ».",
        "pkce_warn": "Veuillez d’abord cliquer sur « Ouvrir la page de connexion ».",
        "input_warn": "Veuillez coller l’URL pixiv:// ou le code.",
        "copied": "Copié",
        "copied_access": "access_token copié dans le presse-papiers.",
        "copied_refresh": "refresh_token copié dans le presse-papiers.",
        "no_access": "Pas encore de access_token. Faites d’abord login/refresh.",
        "no_refresh": "Pas encore de refresh_token. Faites d’abord login.",
        "refresh_no_token": "Aucun refresh_token dans la config. Faites d’abord login.",
        "parse_fail": "Échec de lecture du code.",
        "net_fail": "Erreur réseau/API.",
    },
    "es": {
        "title": "Pixiv Login (GUI)",
        "language": "Idioma:",
        "save_default": "Guardar como predeterminado",
        "refresh": "Actualizar token",
        "open_login": "Abrir página de inicio",
        "paste": "Pegar URL / Código",
        "exchange": "Canjear token",
        "copy_access": "Copiar access_token",
        "copy_refresh": "Copiar refresh_token",
        "output": "Salida",
        "next_step_title": "Siguiente paso",
        "next_step_body": "Después de iniciar sesión, copia la URL pixiv:// completa (o el código), pégala y pulsa “Canjear token”.",
        "pkce_warn": "Primero pulsa “Abrir página de inicio”.",
        "input_warn": "Pega la URL pixiv:// o el código.",
        "copied": "Copiado",
        "copied_access": "access_token copiado al portapapeles.",
        "copied_refresh": "refresh_token copiado al portapapeles.",
        "no_access": "Aún no hay access_token. Inicia sesión/actualiza primero.",
        "no_refresh": "Aún no hay refresh_token. Inicia sesión primero.",
        "refresh_no_token": "No hay refresh_token en la configuración. Inicia sesión primero.",
        "parse_fail": "No se pudo leer el código.",
        "net_fail": "Error de red/API.",
    },
    "ru": {
        "title": "Pixiv Login (GUI)",
        "language": "Язык:",
        "save_default": "Сохранить по умолчанию",
        "refresh": "Обновить токен",
        "open_login": "Открыть страницу входа",
        "paste": "Вставить URL / код",
        "exchange": "Получить токен",
        "copy_access": "Копировать access_token",
        "copy_refresh": "Копировать refresh_token",
        "output": "Вывод",
        "next_step_title": "Следующий шаг",
        "next_step_body": "После входа скопируйте полный pixiv:// URL (или код), вставьте и нажмите «Получить токен».",
        "pkce_warn": "Сначала нажмите «Открыть страницу входа».",
        "input_warn": "Вставьте pixiv:// URL или код.",
        "copied": "Скопировано",
        "copied_access": "access_token скопирован в буфер обмена.",
        "copied_refresh": "refresh_token скопирован в буфер обмена.",
        "no_access": "access_token ещё нет. Сначала вход/обновление.",
        "no_refresh": "refresh_token ещё нет. Сначала войдите.",
        "refresh_no_token": "В конфиге нет refresh_token. Сначала войдите.",
        "parse_fail": "Не удалось разобрать код.",
        "net_fail": "Ошибка сети/API.",
    },
    "pt": {
        "title": "Pixiv Login (GUI)",
        "language": "Idioma:",
        "save_default": "Salvar como padrão",
        "refresh": "Atualizar token",
        "open_login": "Abrir página de login",
        "paste": "Colar URL / Código",
        "exchange": "Trocar token",
        "copy_access": "Copiar access_token",
        "copy_refresh": "Copiar refresh_token",
        "output": "Saída",
        "next_step_title": "Próximo passo",
        "next_step_body": "Após o login, copie a URL pixiv:// completa (ou o código), cole no campo e clique em “Trocar token”.",
        "pkce_warn": "Clique primeiro em “Abrir página de login”.",
        "input_warn": "Cole a URL pixiv:// ou o código.",
        "copied": "Copiado",
        "copied_access": "access_token copiado para a área de transferência.",
        "copied_refresh": "refresh_token copiado para a área de transferência.",
        "no_access": "Sem access_token ainda. Faça login/atualize primeiro.",
        "no_refresh": "Sem refresh_token ainda. Faça login primeiro.",
        "refresh_no_token": "Sem refresh_token no config. Faça login primeiro.",
        "parse_fail": "Falha ao ler o código.",
        "net_fail": "Erro de rede/API.",
    },
    "kr": {
        "title": "Pixiv 로그인 (GUI)",
        "language": "언어:",
        "save_default": "기본값으로 저장",
        "refresh": "토큰 새로고침",
        "open_login": "로그인 페이지 열기",
        "paste": "URL / 코드 붙여넣기",
        "exchange": "토큰 받기",
        "copy_access": "access_token 복사",
        "copy_refresh": "refresh_token 복사",
        "output": "출력",
        "next_step_title": "다음 단계",
        "next_step_body": "로그인 후 전체 pixiv:// URL(또는 코드)을 복사해 입력란에 붙여넣고 ‘토큰 받기’를 클릭하세요.",
        "pkce_warn": "먼저 ‘로그인 페이지 열기’를 클릭하세요.",
        "input_warn": "pixiv:// URL 또는 코드를 붙여넣으세요.",
        "copied": "복사됨",
        "copied_access": "access_token 이(가) 클립보드에 복사되었습니다.",
        "copied_refresh": "refresh_token 이(가) 클립보드에 복사되었습니다.",
        "no_access": "access_token 이 없습니다. 먼저 로그인/새로고침하세요.",
        "no_refresh": "refresh_token 이 없습니다. 먼저 로그인하세요.",
        "refresh_no_token": "설정에 refresh_token 이 없습니다. 먼저 로그인하세요.",
        "parse_fail": "코드 파싱에 실패했습니다.",
        "net_fail": "네트워크/API 오류.",
    },
}

EXTRA_UI_EN = {
    "app_header": "Pixiv OAuth Token",
    "app_subtitle": "Modern login helper with quick token exchange",
    "docs": "Read the Docs",
    "menu_docs": "Docs",
    "menu_tutorial": "Tutorial",
    "menu_resources": "Resources",
    "menu_contact": "Contact",
    "menu_developer": "Developer",
    "tutorial_open": "Open Tutorial",
    "tutorial_title": "Tutorial - Pixiv OAuth Token GUI",
    "tutorial_header": "How to Use",
    "tutorial_desc": "Follow this guided flow to exchange Pixiv OAuth tokens quickly.",
    "tutorial_steps": "Step by step",
    "tutorial_missing": "No tutorial images found. Put ordered PNG files in tutorial_images/.",
    "dev_info_title": "Developer",
    "repo_link": "GitHub Repository",
    "releases_link": "Latest Releases",
    "developer_prefix": "Developer",
}

EXTRA_UI_OVERRIDES = {
    "id": {
        "app_subtitle": "Alat login modern untuk pertukaran token cepat",
        "docs": "Baca Dokumentasi",
        "menu_docs": "Dokumen",
        "menu_resources": "Resource",
        "menu_contact": "Kontak",
        "menu_developer": "Developer",
        "tutorial_open": "Buka Tutorial",
        "tutorial_header": "Cara Penggunaan",
        "tutorial_desc": "Ikuti langkah berikut untuk menukar token Pixiv OAuth dengan cepat.",
        "tutorial_steps": "Langkah-langkah",
        "tutorial_missing": "Gambar tutorial tidak ditemukan. Taruh file PNG berurutan di folder tutorial_images/.",
        "repo_link": "Repositori GitHub",
        "releases_link": "Rilis Terbaru",
    },
    "jp": {
        "app_subtitle": "クイックトークン交換のためのモダンなログインヘルパー",
        "docs": "ドキュメントを読む",
        "menu_docs": "ドキュメント",
        "menu_resources": "リソース",
        "menu_contact": "連絡先",
        "menu_developer": "開発者",
        "tutorial_open": "チュートリアルを開く",
        "tutorial_header": "使い方",
        "tutorial_desc": "このガイドに沿って Pixiv OAuth トークンを素早く取得できます。",
        "tutorial_steps": "手順",
        "dev_info_title": "開発者",
        "repo_link": "GitHub リポジトリ",
        "releases_link": "最新リリース",
        "developer_prefix": "開発者",
    },
    "pl": {"menu_resources": "Zasoby", "menu_contact": "Kontakt", "menu_developer": "Deweloper", "docs": "Czytaj dokumentację", "repo_link": "Repozytorium GitHub", "releases_link": "Najnowsze wydania", "developer_prefix": "Deweloper"},
    "zh": {"menu_resources": "资源", "menu_contact": "联系", "menu_developer": "开发者", "docs": "阅读文档", "repo_link": "GitHub 仓库", "releases_link": "最新发布", "developer_prefix": "开发者"},
    "de": {"menu_resources": "Ressourcen", "menu_contact": "Kontakt", "menu_developer": "Entwickler", "docs": "Dokumentation lesen", "repo_link": "GitHub-Repository", "releases_link": "Neueste Releases", "developer_prefix": "Entwickler"},
    "fr": {"menu_resources": "Ressources", "menu_contact": "Contact", "menu_developer": "Développeur", "docs": "Lire la documentation", "repo_link": "Dépôt GitHub", "releases_link": "Dernières versions", "developer_prefix": "Développeur"},
    "es": {"menu_resources": "Recursos", "menu_contact": "Contacto", "menu_developer": "Desarrollador", "docs": "Leer la documentación", "repo_link": "Repositorio GitHub", "releases_link": "Últimas versiones", "developer_prefix": "Desarrollador"},
    "ru": {"menu_resources": "Ресурсы", "menu_contact": "Контакты", "menu_developer": "Разработчик", "docs": "Читать документацию", "repo_link": "Репозиторий GitHub", "releases_link": "Последние релизы", "developer_prefix": "Разработчик"},
    "pt": {"menu_resources": "Recursos", "menu_contact": "Contato", "menu_developer": "Desenvolvedor", "docs": "Ler a documentação", "repo_link": "Repositório GitHub", "releases_link": "Últimos releases", "developer_prefix": "Desenvolvedor"},
    "kr": {"menu_resources": "리소스", "menu_contact": "연락처", "menu_developer": "개발자", "docs": "문서 읽기", "repo_link": "GitHub 저장소", "releases_link": "최신 릴리스", "developer_prefix": "개발자"},
}

EXTRA_UI = {code: {**EXTRA_UI_EN, **EXTRA_UI_OVERRIDES.get(code, {})} for code in SUPPORTED_LANGS}


TUTORIAL_CAPTIONS = {
    "en": [
        "Step 1: Click Open Login Page in the app.",
        "Step 2: Continue login on Pixiv page.",
        "Step 3: Open browser console (Ctrl+Shift+J).",
        "Step 4: Copy pixiv:// URL/code from console.",
        "Step 5: Paste URL/code into the app input field.",
        "Step 6: Click Exchange Token to finish.",
    ],
    "id": [
        "Langkah 1: Klik Open Login Page di aplikasi.",
        "Langkah 2: Lanjutkan login pada halaman Pixiv.",
        "Langkah 3: Buka console browser (Ctrl+Shift+J).",
        "Langkah 4: Copy URL/kode pixiv:// dari console.",
        "Langkah 5: Paste URL/kode ke kolom input aplikasi.",
        "Langkah 6: Klik Exchange Token untuk selesai.",
    ],
}


EXTRA_UI_EN = {
    "app_header": "Pixiv OAuth Token",
    "app_subtitle": "Modern login helper with quick token exchange",
    "docs": "Read the Docs",
    "menu_docs": "Docs",
    "menu_tutorial": "Tutorial",
    "menu_resources": "Resources",
    "menu_contact": "Contact",
    "menu_developer": "Developer",
    "tutorial_open": "Open Tutorial",
    "tutorial_title": "Tutorial - Pixiv OAuth Token GUI",
    "tutorial_header": "How to Use",
    "tutorial_desc": "Follow this guided flow to exchange Pixiv OAuth tokens quickly.",
    "tutorial_steps": "Step by step",
    "tutorial_missing": "No tutorial images found. Put ordered PNG files in tutorial_images/.",
    "dev_info_title": "Developer",
    "repo_link": "GitHub Repository",
    "releases_link": "Latest Releases",
    "developer_prefix": "Developer",
}

EXTRA_UI_OVERRIDES = {
    "id": {
        "app_subtitle": "Alat login modern untuk pertukaran token cepat",
        "docs": "Baca Dokumentasi",
        "menu_docs": "Dokumen",
        "menu_resources": "Resource",
        "menu_contact": "Kontak",
        "menu_developer": "Developer",
        "tutorial_open": "Buka Tutorial",
        "tutorial_header": "Cara Penggunaan",
        "tutorial_desc": "Ikuti langkah berikut untuk menukar token Pixiv OAuth dengan cepat.",
        "tutorial_steps": "Langkah-langkah",
        "tutorial_missing": "Gambar tutorial tidak ditemukan. Taruh file PNG berurutan di folder tutorial_images/.",
        "repo_link": "Repositori GitHub",
        "releases_link": "Rilis Terbaru",
    },
    "jp": {
        "app_subtitle": "クイックトークン交換のためのモダンなログインヘルパー",
        "docs": "ドキュメントを読む",
        "menu_docs": "ドキュメント",
        "menu_resources": "リソース",
        "menu_contact": "連絡先",
        "menu_developer": "開発者",
        "tutorial_open": "チュートリアルを開く",
        "tutorial_header": "使い方",
        "tutorial_desc": "このガイドに沿って Pixiv OAuth トークンを素早く取得できます。",
        "tutorial_steps": "手順",
        "dev_info_title": "開発者",
        "repo_link": "GitHub リポジトリ",
        "releases_link": "最新リリース",
        "developer_prefix": "開発者",
    },
    "pl": {"menu_resources": "Zasoby", "menu_contact": "Kontakt", "menu_developer": "Deweloper", "docs": "Czytaj dokumentację", "repo_link": "Repozytorium GitHub", "releases_link": "Najnowsze wydania", "developer_prefix": "Deweloper"},
    "zh": {"menu_resources": "资源", "menu_contact": "联系", "menu_developer": "开发者", "docs": "阅读文档", "repo_link": "GitHub 仓库", "releases_link": "最新发布", "developer_prefix": "开发者"},
    "de": {"menu_resources": "Ressourcen", "menu_contact": "Kontakt", "menu_developer": "Entwickler", "docs": "Dokumentation lesen", "repo_link": "GitHub-Repository", "releases_link": "Neueste Releases", "developer_prefix": "Entwickler"},
    "fr": {"menu_resources": "Ressources", "menu_contact": "Contact", "menu_developer": "Développeur", "docs": "Lire la documentation", "repo_link": "Dépôt GitHub", "releases_link": "Dernières versions", "developer_prefix": "Développeur"},
    "es": {"menu_resources": "Recursos", "menu_contact": "Contacto", "menu_developer": "Desarrollador", "docs": "Leer la documentación", "repo_link": "Repositorio GitHub", "releases_link": "Últimas versiones", "developer_prefix": "Desarrollador"},
    "ru": {"menu_resources": "Ресурсы", "menu_contact": "Контакты", "menu_developer": "Разработчик", "docs": "Читать документацию", "repo_link": "Репозиторий GitHub", "releases_link": "Последние релизы", "developer_prefix": "Разработчик"},
    "pt": {"menu_resources": "Recursos", "menu_contact": "Contato", "menu_developer": "Desenvolvedor", "docs": "Ler a documentação", "repo_link": "Repositório GitHub", "releases_link": "Últimos releases", "developer_prefix": "Desenvolvedor"},
    "kr": {"menu_resources": "리소스", "menu_contact": "연락처", "menu_developer": "개발자", "docs": "문서 읽기", "repo_link": "GitHub 저장소", "releases_link": "최신 릴리스", "developer_prefix": "개발자"},
}

EXTRA_UI = {code: {**EXTRA_UI_EN, **EXTRA_UI_OVERRIDES.get(code, {})} for code in SUPPORTED_LANGS}


TUTORIAL_CAPTIONS = {
    "en": [
        "Step 1: Click Open Login Page in the app.",
        "Step 2: Continue login on Pixiv page.",
        "Step 3: Open browser console (Ctrl+Shift+J).",
        "Step 4: Copy pixiv:// URL/code from console.",
        "Step 5: Paste URL/code into the app input field.",
        "Step 6: Click Exchange Token to finish.",
    ],
    "id": [
        "Langkah 1: Klik Open Login Page di aplikasi.",
        "Langkah 2: Lanjutkan login pada halaman Pixiv.",
        "Langkah 3: Buka console browser (Ctrl+Shift+J).",
        "Langkah 4: Copy URL/kode pixiv:// dari console.",
        "Langkah 5: Paste URL/kode ke kolom input aplikasi.",
        "Langkah 6: Klik Exchange Token untuk selesai.",
    ],
}


EXTRA_UI_EN = {
    "app_header": "Pixiv OAuth Token",
    "app_subtitle": "Modern login helper with quick token exchange",
    "docs": "Read the Docs",
    "menu_docs": "Docs",
    "menu_tutorial": "Tutorial",
    "menu_resources": "Resources",
    "menu_contact": "Contact",
    "menu_developer": "Developer",
    "tutorial_open": "Open Tutorial",
    "tutorial_title": "Tutorial - Pixiv OAuth Token GUI",
    "tutorial_header": "How to Use",
    "tutorial_desc": "Follow this guided flow to exchange Pixiv OAuth tokens quickly.",
    "tutorial_steps": "Step by step",
    "tutorial_missing": "No tutorial images found. Put ordered PNG files in tutorial_images/.",
    "dev_info_title": "Developer",
    "repo_link": "GitHub Repository",
    "releases_link": "Latest Releases",
    "developer_prefix": "Developer",
}

EXTRA_UI_OVERRIDES = {
    "id": {
        "app_subtitle": "Alat login modern untuk pertukaran token cepat",
        "docs": "Baca Dokumentasi",
        "menu_docs": "Dokumen",
        "menu_resources": "Resource",
        "menu_contact": "Kontak",
        "menu_developer": "Developer",
        "tutorial_open": "Buka Tutorial",
        "tutorial_header": "Cara Penggunaan",
        "tutorial_desc": "Ikuti langkah berikut untuk menukar token Pixiv OAuth dengan cepat.",
        "tutorial_steps": "Langkah-langkah",
        "tutorial_missing": "Gambar tutorial tidak ditemukan. Taruh file PNG berurutan di folder tutorial_images/.",
        "repo_link": "Repositori GitHub",
        "releases_link": "Rilis Terbaru",
    },
    "jp": {
        "app_subtitle": "クイックトークン交換のためのモダンなログインヘルパー",
        "docs": "ドキュメントを読む",
        "menu_docs": "ドキュメント",
        "menu_resources": "リソース",
        "menu_contact": "連絡先",
        "menu_developer": "開発者",
        "tutorial_open": "チュートリアルを開く",
        "tutorial_header": "使い方",
        "tutorial_desc": "このガイドに沿って Pixiv OAuth トークンを素早く取得できます。",
        "tutorial_steps": "手順",
        "dev_info_title": "開発者",
        "repo_link": "GitHub リポジトリ",
        "releases_link": "最新リリース",
        "developer_prefix": "開発者",
    },
    "pl": {"menu_resources": "Zasoby", "menu_contact": "Kontakt", "menu_developer": "Deweloper", "docs": "Czytaj dokumentację", "repo_link": "Repozytorium GitHub", "releases_link": "Najnowsze wydania", "developer_prefix": "Deweloper"},
    "zh": {"menu_resources": "资源", "menu_contact": "联系", "menu_developer": "开发者", "docs": "阅读文档", "repo_link": "GitHub 仓库", "releases_link": "最新发布", "developer_prefix": "开发者"},
    "de": {"menu_resources": "Ressourcen", "menu_contact": "Kontakt", "menu_developer": "Entwickler", "docs": "Dokumentation lesen", "repo_link": "GitHub-Repository", "releases_link": "Neueste Releases", "developer_prefix": "Entwickler"},
    "fr": {"menu_resources": "Ressources", "menu_contact": "Contact", "menu_developer": "Développeur", "docs": "Lire la documentation", "repo_link": "Dépôt GitHub", "releases_link": "Dernières versions", "developer_prefix": "Développeur"},
    "es": {"menu_resources": "Recursos", "menu_contact": "Contacto", "menu_developer": "Desarrollador", "docs": "Leer la documentación", "repo_link": "Repositorio GitHub", "releases_link": "Últimas versiones", "developer_prefix": "Desarrollador"},
    "ru": {"menu_resources": "Ресурсы", "menu_contact": "Контакты", "menu_developer": "Разработчик", "docs": "Читать документацию", "repo_link": "Репозиторий GitHub", "releases_link": "Последние релизы", "developer_prefix": "Разработчик"},
    "pt": {"menu_resources": "Recursos", "menu_contact": "Contato", "menu_developer": "Desenvolvedor", "docs": "Ler a documentação", "repo_link": "Repositório GitHub", "releases_link": "Últimos releases", "developer_prefix": "Desenvolvedor"},
    "kr": {"menu_resources": "리소스", "menu_contact": "연락처", "menu_developer": "개발자", "docs": "문서 읽기", "repo_link": "GitHub 저장소", "releases_link": "최신 릴리스", "developer_prefix": "개발자"},
}

EXTRA_UI = {code: {**EXTRA_UI_EN, **EXTRA_UI_OVERRIDES.get(code, {})} for code in SUPPORTED_LANGS}


TUTORIAL_CAPTIONS = {
    "en": [
        "Step 1: Click Open Login Page in the app.",
        "Step 2: Continue login on Pixiv page.",
        "Step 3: Open browser console (Ctrl+Shift+J).",
        "Step 4: Copy pixiv:// URL/code from console.",
        "Step 5: Paste URL/code into the app input field.",
        "Step 6: Click Exchange Token to finish.",
    ],
    "id": [
        "Langkah 1: Klik Open Login Page di aplikasi.",
        "Langkah 2: Lanjutkan login pada halaman Pixiv.",
        "Langkah 3: Buka console browser (Ctrl+Shift+J).",
        "Langkah 4: Copy URL/kode pixiv:// dari console.",
        "Langkah 5: Paste URL/kode ke kolom input aplikasi.",
        "Langkah 6: Klik Exchange Token untuk selesai.",
    ],
}


EXTRA_UI_EN = {
    "app_header": "Pixiv OAuth Token",
    "app_subtitle": "Modern login helper with quick token exchange",
    "docs": "Read the Docs",
    "menu_docs": "Docs",
    "menu_tutorial": "Tutorial",
    "menu_resources": "Resources",
    "menu_contact": "Contact",
    "menu_developer": "Developer",
    "tutorial_open": "Open Tutorial",
    "tutorial_title": "Tutorial - Pixiv OAuth Token GUI",
    "tutorial_header": "How to Use",
    "tutorial_desc": "Follow this guided flow to exchange Pixiv OAuth tokens quickly.",
    "tutorial_steps": "Step by step",
    "tutorial_missing": "No tutorial images found. Put ordered PNG files in tutorial_images/.",
    "dev_info_title": "Developer",
    "repo_link": "GitHub Repository",
    "releases_link": "Latest Releases",
    "developer_prefix": "Developer",
}

EXTRA_UI_OVERRIDES = {
    "id": {
        "app_subtitle": "Alat login modern untuk pertukaran token cepat",
        "docs": "Baca Dokumentasi",
        "menu_docs": "Dokumen",
        "menu_resources": "Resource",
        "menu_contact": "Kontak",
        "menu_developer": "Developer",
        "tutorial_open": "Buka Tutorial",
        "tutorial_header": "Cara Penggunaan",
        "tutorial_desc": "Ikuti langkah berikut untuk menukar token Pixiv OAuth dengan cepat.",
        "tutorial_steps": "Langkah-langkah",
        "tutorial_missing": "Gambar tutorial tidak ditemukan. Taruh file PNG berurutan di folder tutorial_images/.",
        "repo_link": "Repositori GitHub",
        "releases_link": "Rilis Terbaru",
    },
    "jp": {
        "app_subtitle": "クイックトークン交換のためのモダンなログインヘルパー",
        "docs": "ドキュメントを読む",
        "menu_docs": "ドキュメント",
        "menu_resources": "リソース",
        "menu_contact": "連絡先",
        "menu_developer": "開発者",
        "tutorial_open": "チュートリアルを開く",
        "tutorial_header": "使い方",
        "tutorial_desc": "このガイドに沿って Pixiv OAuth トークンを素早く取得できます。",
        "tutorial_steps": "手順",
        "dev_info_title": "開発者",
        "repo_link": "GitHub リポジトリ",
        "releases_link": "最新リリース",
        "developer_prefix": "開発者",
    },
    "pl": {"menu_resources": "Zasoby", "menu_contact": "Kontakt", "menu_developer": "Deweloper", "docs": "Czytaj dokumentację", "repo_link": "Repozytorium GitHub", "releases_link": "Najnowsze wydania", "developer_prefix": "Deweloper"},
    "zh": {"menu_resources": "资源", "menu_contact": "联系", "menu_developer": "开发者", "docs": "阅读文档", "repo_link": "GitHub 仓库", "releases_link": "最新发布", "developer_prefix": "开发者"},
    "de": {"menu_resources": "Ressourcen", "menu_contact": "Kontakt", "menu_developer": "Entwickler", "docs": "Dokumentation lesen", "repo_link": "GitHub-Repository", "releases_link": "Neueste Releases", "developer_prefix": "Entwickler"},
    "fr": {"menu_resources": "Ressources", "menu_contact": "Contact", "menu_developer": "Développeur", "docs": "Lire la documentation", "repo_link": "Dépôt GitHub", "releases_link": "Dernières versions", "developer_prefix": "Développeur"},
    "es": {"menu_resources": "Recursos", "menu_contact": "Contacto", "menu_developer": "Desarrollador", "docs": "Leer la documentación", "repo_link": "Repositorio GitHub", "releases_link": "Últimas versiones", "developer_prefix": "Desarrollador"},
    "ru": {"menu_resources": "Ресурсы", "menu_contact": "Контакты", "menu_developer": "Разработчик", "docs": "Читать документацию", "repo_link": "Репозиторий GitHub", "releases_link": "Последние релизы", "developer_prefix": "Разработчик"},
    "pt": {"menu_resources": "Recursos", "menu_contact": "Contato", "menu_developer": "Desenvolvedor", "docs": "Ler a documentação", "repo_link": "Repositório GitHub", "releases_link": "Últimos releases", "developer_prefix": "Desenvolvedor"},
    "kr": {"menu_resources": "리소스", "menu_contact": "연락처", "menu_developer": "개발자", "docs": "문서 읽기", "repo_link": "GitHub 저장소", "releases_link": "최신 릴리스", "developer_prefix": "개발자"},
}

EXTRA_UI = {code: {**EXTRA_UI_EN, **EXTRA_UI_OVERRIDES.get(code, {})} for code in SUPPORTED_LANGS}


TUTORIAL_CAPTIONS = {
    "en": [
        "Step 1: Click Open Login Page in the app.",
        "Step 2: Continue login on Pixiv page.",
        "Step 3: Open browser console (Ctrl+Shift+J).",
        "Step 4: Copy pixiv:// URL/code from console.",
        "Step 5: Paste URL/code into the app input field.",
        "Step 6: Click Exchange Token to finish.",
    ],
    "id": [
        "Langkah 1: Klik Open Login Page di aplikasi.",
        "Langkah 2: Lanjutkan login pada halaman Pixiv.",
        "Langkah 3: Buka console browser (Ctrl+Shift+J).",
        "Langkah 4: Copy URL/kode pixiv:// dari console.",
        "Langkah 5: Paste URL/kode ke kolom input aplikasi.",
        "Langkah 6: Klik Exchange Token untuk selesai.",
    ],
}


def app_dir() -> Path:
    """Store config next to the executable when frozen (PyInstaller onefile), otherwise next to the script."""
    try:
        import sys
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent
    except Exception:
        pass
    return Path(__file__).resolve().parent


CONFIG_FILE = app_dir() / "pixiv_login_config.json"


def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_config(cfg: dict) -> None:
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")


def s256(data: bytes) -> str:
    return urlsafe_b64encode(sha256(data).digest()).rstrip(b"=").decode("ascii")


def oauth_pkce() -> tuple[str, str]:
    code_verifier = token_urlsafe(32)
    code_challenge = s256(code_verifier.encode("ascii"))
    return code_verifier, code_challenge


def extract_code(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("pixiv://"):
        parsed = urlparse(raw)
        qs = parse_qs(parsed.query)
        if "code" not in qs or not qs["code"]:
            raise ValueError("code missing")
        return qs["code"][0]
    return raw


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.cfg = load_config()
        default_code = self.cfg.get("default_lang", "en")
        if default_code not in SUPPORTED_LANGS:
            default_code = "en"
        default_name = LANG_CODE_TO_NAME.get(default_code, "🇬🇧  English")

        self.code_verifier: str | None = None
        self.last_access_token: str | None = None
        self.last_refresh_token: str | None = self.cfg.get("refresh_token")
        self.tutorial_dirs = self._resolve_tutorial_dirs()
        self._tutorial_images: list[Path] = []
        self._tutorial_index = 0
        self._tutorial_photo = None

        self.lang_var = tk.StringVar(value=default_name)
        self.save_lang_var = tk.BooleanVar(value=True)

        self._build_ui()
        self.apply_ui_language()
        self._update_copy_buttons()

        self.log(f"Config file: {CONFIG_FILE}")

    # ---------- i18n ----------
    def current_lang_code(self) -> str:
        name = self.lang_var.get().strip()
        return LANG_NAME_TO_CODE.get(name, "en")

    def t(self, key: str) -> str:
        code = self.current_lang_code()
        return UI.get(code, UI["en"]).get(key, UI["en"].get(key, key))

    def tx(self, key: str) -> str:
        code = self.current_lang_code()
        return EXTRA_UI.get(code, EXTRA_UI["en"]).get(key, EXTRA_UI["en"].get(key, key))

    def apply_ui_language(self):
        self.title(self.t("title"))
        self.lang_label.config(text=self.t("language"))
        self.save_lang_check.config(text=self.t("save_default"))
        self.refresh_btn.config(text=self.t("refresh"))
        self.open_login_btn.config(text=self.t("open_login"))
        self.paste_frame.config(text=self.t("paste"))
        self.exchange_btn.config(text=self.t("exchange"))
        self.copy_access_btn.config(text=self.t("copy_access"))
        self.copy_refresh_btn.config(text=self.t("copy_refresh"))
        self.output_frame.config(text=self.t("output"))
        self.docs_btn.config(text=self.tx("docs"))
        self.header_title_label.config(text=self.tx("app_header"))
        self.header_subtitle_label.config(text=self.tx("app_subtitle"))
        self._build_menu()

        if self.save_lang_var.get():
            self.cfg["default_lang"] = self.current_lang_code()
            save_config(self.cfg)

    def _set_default_lang_if_needed(self):
        if self.save_lang_var.get():
            self.cfg["default_lang"] = self.current_lang_code()
            save_config(self.cfg)

    # ---------- UI ----------
    def _resolve_tutorial_dirs(self):
        dirs = []

        # 1) Preferred: beside executable/script (persistent app folder)
        dirs.append(app_dir() / "tutorial_images")

        # 2) Source checkout location (when running from repo)
        dirs.append(Path(__file__).resolve().parent / "tutorial_images")

        # 3) PyInstaller temp extraction folder (onefile runtime)
        meipass = getattr(__import__("sys"), "_MEIPASS", None)
        if meipass:
            dirs.append(Path(meipass) / "tutorial_images")

        # unique order-preserving
        uniq = []
        seen = set()
        for d in dirs:
            key = str(d)
            if key not in seen:
                seen.add(key)
                uniq.append(d)
        return uniq

    def _build_ui(self):
        self.configure(bg="#f3f5f9")

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        self._build_menu()

        style.configure("App.TFrame", background="#f3f5f9")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("TLabel", background="#f3f5f9", foreground="#1f2937", font=("Segoe UI", 10))
        style.configure("Header.TLabel", background="#f3f5f9", foreground="#111827", font=("Segoe UI Semibold", 14))
        style.configure("Sub.TLabel", background="#f3f5f9", foreground="#6b7280", font=("Segoe UI", 9))
        style.configure("TCheckbutton", background="#ffffff", foreground="#374151", font=("Segoe UI", 10))
        style.configure("TLabelframe", background="#ffffff", foreground="#111827", borderwidth=1, relief="solid")
        style.configure("TLabelframe.Label", background="#ffffff", foreground="#111827", font=("Segoe UI Semibold", 10))
        style.configure("Primary.TButton", font=("Segoe UI Semibold", 10), padding=(14, 8), foreground="#ffffff", background="#2563eb", borderwidth=0)
        style.map("Primary.TButton", background=[("active", "#1d4ed8")])
        style.configure("Secondary.TButton", font=("Segoe UI", 10), padding=(12, 8), foreground="#1f2937", background="#e5e7eb", borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#d1d5db")])
        style.configure("Lang.TCombobox", font=("Segoe UI Emoji", 10), padding=6)

        root = ttk.Frame(self, style="App.TFrame", padding=14)
        root.pack(fill="both", expand=True)

        header = ttk.Frame(root, style="App.TFrame")
        header.pack(fill="x", pady=(0, 10))

        self.header_title_label = ttk.Label(header, text=self.tx("app_header"), style="Header.TLabel")
        self.header_title_label.pack(anchor="w")
        self.header_subtitle_label = ttk.Label(header, text=self.tx("app_subtitle"), style="Sub.TLabel")
        self.header_subtitle_label.pack(anchor="w")

        top = ttk.Frame(root, style="Card.TFrame", padding=12)
        top.pack(fill="x", pady=(0, 10))

        self.lang_label = ttk.Label(top, text="Language:")
        self.lang_label.pack(side="left")

        self.lang_combo = ttk.Combobox(
            top,
            style="Lang.TCombobox",
            textvariable=self.lang_var,
            values=[name for name, _ in LANG_CHOICES],
            width=22,
            state="readonly",
        )
        self.lang_combo.pack(side="left", padx=(6, 16))
        self.lang_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_ui_language())

        self.save_lang_check = ttk.Checkbutton(top, text="Save as default", variable=self.save_lang_var, command=self.apply_ui_language)
        self.save_lang_check.pack(side="left")

        self.open_login_btn = ttk.Button(top, text="Open Login Page", style="Primary.TButton", command=self.open_login)
        self.open_login_btn.pack(side="right")

        self.docs_btn = ttk.Button(top, text="Read the Docs", style="Secondary.TButton", command=lambda: open_url(README_URL))
        self.docs_btn.pack(side="right", padx=(0, 8))

        self.refresh_btn = ttk.Button(top, text="Refresh Token", style="Secondary.TButton", command=self.refresh_token)
        self.refresh_btn.pack(side="right", padx=(0, 8))

        self.paste_frame = ttk.LabelFrame(root, text="Paste URL / Code", padding=12)
        self.paste_frame.pack(fill="x", pady=(0, 10))

        self.code_entry = ttk.Entry(self.paste_frame, font=("Segoe UI", 10))
        self.code_entry.pack(fill="x", expand=True)

        btn_row = ttk.Frame(self.paste_frame)
        btn_row.pack(fill="x", pady=(8, 0))

        self.exchange_btn = ttk.Button(btn_row, text="Exchange Token", style="Primary.TButton", command=self.exchange_token)
        self.exchange_btn.pack(side="right")

        copy_row = ttk.Frame(root, style="App.TFrame", padding=(0, 0, 0, 10))
        copy_row.pack(fill="x")

        self.copy_access_btn = ttk.Button(copy_row, text="Copy access_token", style="Secondary.TButton", command=self.copy_access_token)
        self.copy_access_btn.pack(side="left")

        self.copy_refresh_btn = ttk.Button(copy_row, text="Copy refresh_token", style="Secondary.TButton", command=self.copy_refresh_token)
        self.copy_refresh_btn.pack(side="left", padx=(8, 0))

        self.output_frame = ttk.LabelFrame(root, text="Output", padding=12)
        self.output_frame.pack(fill="both", expand=True)

        self.output = tk.Text(
            self.output_frame,
            wrap="word",
            bg="#0f172a",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
            relief="flat",
            font=("Cascadia Mono", 10),
            padx=10,
            pady=10,
        )
        self.output.pack(fill="both", expand=True)

        self.geometry("860x620")
        self.minsize(860, 620)

    def _build_menu(self):
        menubar = tk.Menu(self)

        docs_menu = tk.Menu(menubar, tearoff=0)
        docs_menu.add_command(label=f"📘 {self.tx('docs')} (GitHub README)", command=lambda: open_url(README_URL))
        menubar.add_cascade(label=self.tx("menu_docs"), menu=docs_menu)

        tutorial_menu = tk.Menu(menubar, tearoff=0)
        tutorial_menu.add_command(label=f"🧭 {self.tx('tutorial_open')}", command=self.show_tutorial)
        menubar.add_cascade(label=self.tx("menu_tutorial"), menu=tutorial_menu)

        resource_menu = tk.Menu(menubar, tearoff=0)
        resource_menu.add_command(label=self.tx("repo_link"), command=lambda: open_url(REPO_BASE_URL))
        resource_menu.add_command(label=self.tx("releases_link"), command=lambda: open_url(RELEASES_URL))
        menubar.add_cascade(label=self.tx("menu_resources"), menu=resource_menu)

        contact_menu = tk.Menu(menubar, tearoff=0)
        contact_menu.add_command(label="TikTok", command=lambda: open_url(TIKTOK_URL))
        contact_menu.add_command(label="Twitter / X", command=lambda: open_url(TWITTER_URL))
        menubar.add_cascade(label=self.tx("menu_contact"), menu=contact_menu)

        developer_menu = tk.Menu(menubar, tearoff=0)
        developer_menu.add_command(label=f"{self.tx('developer_prefix')}: {DEVELOPER_NAME}", command=self.show_developer_info)
        menubar.add_cascade(label=self.tx("menu_developer"), menu=developer_menu)

        self.config(menu=menubar)

    def show_developer_info(self):
        messagebox.showinfo(
            self.tx("dev_info_title"),
            f"{DEVELOPER_NAME}\n\nGitHub: {REPO_BASE_URL}\nTikTok: {TIKTOK_URL}\nTwitter/X: {TWITTER_URL}",
        )

    def _load_tutorial_images(self):
        images = []
        for d in self.tutorial_dirs:
            if not d.exists():
                continue
            images.extend(sorted(d.glob("*.png")))
            images.extend(sorted(d.glob("*.gif")))

        # unique by filename first occurrence to avoid duplicates from multiple dirs
        seen = set()
        uniq = []
        for img in images:
            k = img.name.lower()
            if k in seen:
                continue
            seen.add(k)
            uniq.append(img)
        self._tutorial_images = uniq

    def _scaled_tutorial_photo(self, image_path: Path, max_width: int = 860):
        photo = tk.PhotoImage(file=str(image_path))
        w = max(photo.width(), 1)
        factor = max(1, (w + max_width - 1) // max_width)
        if factor > 1:
            photo = photo.subsample(factor, factor)
        return photo

    def show_tutorial(self):
        self._load_tutorial_images()

        tutorial = tk.Toplevel(self)
        tutorial.title(self.tx("tutorial_title"))
        tutorial.geometry("980x740")
        tutorial.minsize(860, 620)
        tutorial.configure(bg="#f3f5f9")

        container = ttk.Frame(tutorial, style="App.TFrame", padding=16)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text=self.tx("tutorial_header"), style="Header.TLabel").pack(anchor="w")
        ttk.Label(container, text=self.tx("tutorial_desc"), style="Sub.TLabel").pack(anchor="w", pady=(0, 12))

        card = ttk.LabelFrame(container, text=self.tx("tutorial_steps"), padding=12)
        card.pack(fill="both", expand=True)

        canvas = tk.Canvas(card, bg="#ffffff", highlightthickness=0)
        vscroll = ttk.Scrollbar(card, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)

        vscroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        content = ttk.Frame(canvas, style="Card.TFrame")
        window_id = canvas.create_window((0, 0), window=content, anchor="nw")

        def on_content_configure(_event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_canvas_configure(event):
            canvas.itemconfigure(window_id, width=event.width)

        content.bind("<Configure>", on_content_configure)
        canvas.bind("<Configure>", on_canvas_configure)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        tutorial.bind("<Destroy>", lambda _e: canvas.unbind_all("<MouseWheel>"))

        self._tutorial_photos = []

        if not self._tutorial_images:
            ttk.Label(content, text=self.tx("tutorial_missing"), style="TLabel").pack(anchor="w", pady=8)
        else:
            code = self.current_lang_code()
            captions = TUTORIAL_CAPTIONS.get(code, TUTORIAL_CAPTIONS["en"])

            for i, image_path in enumerate(self._tutorial_images, start=1):
                caption = captions[i - 1] if i - 1 < len(captions) else image_path.name

                section = ttk.Frame(content, style="Card.TFrame", padding=(8, 8, 8, 16))
                section.pack(fill="x", expand=True)

                ttk.Label(section, text=f"{i}. {caption}", style="TLabelframe.Label").pack(anchor="w", pady=(0, 8))

                try:
                    photo = self._scaled_tutorial_photo(image_path)
                    self._tutorial_photos.append(photo)
                    img_label = ttk.Label(section, image=photo)
                    img_label.pack(anchor="center", fill="x", expand=True)
                except tk.TclError:
                    ttk.Label(section, text=f"Cannot open image: {image_path.name}", style="TLabel").pack(anchor="w")

                ttk.Separator(content, orient="horizontal").pack(fill="x", pady=(2, 10))

        footer = ttk.Frame(container, style="App.TFrame")
        footer.pack(fill="x", pady=(10, 0))
        ttk.Button(footer, text=self.tx("docs"), style="Primary.TButton", command=lambda: open_url(README_URL)).pack(side="right")



    def log(self, msg: str):
        self.output.insert("end", msg + "\n")
        self.output.see("end")

    def _update_copy_buttons(self):
        self.copy_access_btn.state(["!disabled"] if self.last_access_token else ["disabled"])
        self.copy_refresh_btn.state(["!disabled"] if self.last_refresh_token else ["disabled"])

    def _copy_to_clipboard(self, value: str, success_key: str):
        try:
            self.clipboard_clear()
            self.clipboard_append(value)
            self.update()
            messagebox.showinfo(self.t("copied"), self.t(success_key))
        except Exception as e:
            messagebox.showerror("Clipboard Error", str(e))

    def copy_access_token(self):
        if not self.last_access_token:
            messagebox.showinfo("Copy", self.t("no_access"))
            return
        self._copy_to_clipboard(self.last_access_token, "copied_access")

    def copy_refresh_token(self):
        if not self.last_refresh_token:
            messagebox.showinfo("Copy", self.t("no_refresh"))
            return
        self._copy_to_clipboard(self.last_refresh_token, "copied_refresh")

    # ---------- Actions ----------
    def open_login(self):
        self._set_default_lang_if_needed()

        self.code_verifier, code_challenge = oauth_pkce()

        login_params = {
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "client": "pixiv-android",
        }
        login_url = f"{LOGIN_URL}?{urlencode(login_params)}"
        self.log("Opening browser for login...")
        open_url(login_url)

        messagebox.showinfo(self.t("next_step_title"), self.t("next_step_body"))

    def exchange_token(self):
        if not self.code_verifier:
            messagebox.showwarning("PKCE", self.t("pkce_warn"))
            return

        raw = self.code_entry.get().strip()
        if not raw:
            messagebox.showwarning("Input", self.t("input_warn"))
            return

        try:
            code = extract_code(raw)
        except Exception:
            messagebox.showerror("Error", self.t("parse_fail"))
            return

        self._set_default_lang_if_needed()

        def worker():
            try:
                resp = requests.post(
                    AUTH_TOKEN_URL,
                    data={
                        "client_id": CLIENT_ID,
                        "client_secret": CLIENT_SECRET,
                        "code": code,
                        "code_verifier": self.code_verifier,
                        "grant_type": "authorization_code",
                        "include_policy": "true",
                        "redirect_uri": REDIRECT_URI,
                    },
                    headers={"User-Agent": USER_AGENT},
                    timeout=30,
                )
                data = resp.json()
            except Exception as e:
                self.after(0, lambda: self.log(f"[ERROR] {self.t('net_fail')} {e}"))
                return

            def ui():
                if "access_token" not in data:
                    self.log("ERROR RESPONSE:")
                    self.log(json.dumps(data, indent=2, ensure_ascii=False))
                    return

                self.last_access_token = data.get("access_token")
                self.last_refresh_token = data.get("refresh_token")
                self._update_copy_buttons()

                self.log("=== LOGIN SUCCESS ===")
                self.log(f"access_token : {self.last_access_token}")
                self.log(f"refresh_token: {self.last_refresh_token}")
                self.log(f"expires_in   : {data.get('expires_in')}")

                self.cfg["refresh_token"] = self.last_refresh_token
                save_config(self.cfg)

            self.after(0, ui)

        threading.Thread(target=worker, daemon=True).start()

    def refresh_token(self):
        self.cfg = load_config()
        rt = self.cfg.get("refresh_token")
        if not rt:
            messagebox.showinfo("Refresh", self.t("refresh_no_token"))
            return

        def worker():
            try:
                resp = requests.post(
                    AUTH_TOKEN_URL,
                    data={
                        "client_id": CLIENT_ID,
                        "client_secret": CLIENT_SECRET,
                        "refresh_token": rt,
                        "grant_type": "refresh_token",
                        "include_policy": "true",
                    },
                    headers={"User-Agent": USER_AGENT},
                    timeout=30,
                )
                data = resp.json()
            except Exception as e:
                self.after(0, lambda: self.log(f"[ERROR] {self.t('net_fail')} {e}"))
                return

            def ui():
                if "access_token" not in data:
                    self.log("ERROR RESPONSE:")
                    self.log(json.dumps(data, indent=2, ensure_ascii=False))
                    return

                self.last_access_token = data.get("access_token")
                self.last_refresh_token = data.get("refresh_token")
                self._update_copy_buttons()

                self.log("=== REFRESH SUCCESS ===")
                self.log(f"access_token : {self.last_access_token}")
                self.log(f"refresh_token: {self.last_refresh_token}")
                self.log(f"expires_in   : {data.get('expires_in')}")

                self.cfg["refresh_token"] = self.last_refresh_token
                save_config(self.cfg)

            self.after(0, ui)

        threading.Thread(target=worker, daemon=True).start()


if __name__ == "__main__":
    App().mainloop()
