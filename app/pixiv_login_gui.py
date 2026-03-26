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
import re
import datetime
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import tempfile
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
APP_VERSION = "v1.0.3"
APP_BUILD_CODE = "BUILD-UNKNOWN"
LATEST_MANIFEST_URL = "https://raw.githubusercontent.com/fatonyahmadfauzi/Pixiv-OAuth-Token/master/latest.json"
GITHUB_API_LATEST_RELEASE = "https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest"
DOWNLOADS_RAW_BASE = f"{REPO_BASE_URL}/raw/HEAD/downloads"
PORTABLE_LATEST_URL = f"{DOWNLOADS_RAW_BASE}/Pixiv%20OAuth%20GUi%20(Portable)_latest.exe"
SETUP_LATEST_URL = f"{DOWNLOADS_RAW_BASE}/Pixiv%20OAuth%20GUi%20Setup_latest.exe"
VERSION_FILE = Path(__file__).with_name("pixiv_login_version.txt")
# ===== LANGUAGE =====
SUPPORTED_LANGS = ("en", "pl", "zh", "jp", "de", "fr", "es", "ru", "pt", "id", "kr")

LANG_CHOICES = [
    ("English", "en"),
    ("Polski", "pl"),
    ("中文", "zh"),
    ("日本語", "jp"),
    ("Deutsch", "de"),
    ("Français", "fr"),
    ("Español", "es"),
    ("Русский", "ru"),
    ("Português", "pt"),
    ("Indonesia", "id"),
    ("한국어", "kr"),
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
        "dbg_app_start": "[APP] Application started",
        "dbg_lang_changed": "[LANG] Language changed to: {}",
        "dbg_lang_saved": "[CONFIG] Default language saved: {}",
        "dbg_open_login": "[BTN] Open Login Page clicked",
        "dbg_browser_open": "[BROWSER] Login URL opened in browser",
        "dbg_exchange_click": "[BTN] Exchange Token clicked",
        "dbg_code_parsed": "[PKCE] Code parsed successfully",
        "dbg_token_request": "[HTTP] Sending token exchange request...",
        "dbg_token_success": "[HTTP] Token exchange SUCCESS",
        "dbg_token_fail": "[HTTP] Token exchange FAILED",
        "dbg_refresh_click": "[BTN] Refresh Token clicked",
        "dbg_refresh_request": "[HTTP] Sending token refresh request...",
        "dbg_refresh_success": "[HTTP] Token refresh SUCCESS",
        "dbg_refresh_fail": "[HTTP] Token refresh FAILED",
        "dbg_copy_access": "[BTN] Copy access_token clicked",
        "dbg_copy_refresh": "[BTN] Copy refresh_token clicked",
        "dbg_copied_ok": "[CLIPBOARD] Copied to clipboard: {}",
        "dbg_tutorial_open": "[BTN] Tutorial opened",
        "dbg_debug_open": "[DEBUG] Debug Console opened",
        "dbg_config_saved": "[CONFIG] Config saved to: {}",
        "dbg_no_rt": "[WARN] No refresh_token in config",
        "dbg_no_pkce": "[WARN] PKCE code_verifier not set",
        "dbg_no_input": "[WARN] Input field is empty",
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
        "dbg_app_start": "[APP] Aplikasi dimulai",
        "dbg_lang_changed": "[BAHASA] Bahasa diubah ke: {}",
        "dbg_lang_saved": "[CONFIG] Bahasa default disimpan: {}",
        "dbg_open_login": "[BTN] Tombol Buka Halaman Login diklik",
        "dbg_browser_open": "[BROWSER] URL login dibuka di browser",
        "dbg_exchange_click": "[BTN] Tombol Tukar Token diklik",
        "dbg_code_parsed": "[PKCE] Kode berhasil diurai",
        "dbg_token_request": "[HTTP] Mengirim permintaan tukar token...",
        "dbg_token_success": "[HTTP] Tukar token BERHASIL",
        "dbg_token_fail": "[HTTP] Tukar token GAGAL",
        "dbg_refresh_click": "[BTN] Tombol Refresh Token diklik",
        "dbg_refresh_request": "[HTTP] Mengirim permintaan refresh token...",
        "dbg_refresh_success": "[HTTP] Refresh token BERHASIL",
        "dbg_refresh_fail": "[HTTP] Refresh token GAGAL",
        "dbg_copy_access": "[BTN] Salin access_token diklik",
        "dbg_copy_refresh": "[BTN] Salin refresh_token diklik",
        "dbg_copied_ok": "[CLIPBOARD] Disalin ke clipboard: {}",
        "dbg_tutorial_open": "[BTN] Tutorial dibuka",
        "dbg_debug_open": "[DEBUG] Debug Console dibuka",
        "dbg_config_saved": "[CONFIG] Config disimpan ke: {}",
        "dbg_no_rt": "[WARN] Tidak ada refresh_token di config",
        "dbg_no_pkce": "[WARN] PKCE code_verifier belum di-set",
        "dbg_no_input": "[WARN] Kolom input kosong",
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
        "dbg_app_start": "[APP] Aplikacja uruchomiona",
        "dbg_lang_changed": "[JĘZYK] Język zmieniony na: {}",
        "dbg_lang_saved": "[CONFIG] Domyślny język zapisany: {}",
        "dbg_open_login": "[BTN] Kliknięto Otwórz logowanie",
        "dbg_browser_open": "[BROWSER] URL logowania otwarto w przeglądarce",
        "dbg_exchange_click": "[BTN] Kliknięto Wymień token",
        "dbg_code_parsed": "[PKCE] Kod odczytano pomyślnie",
        "dbg_token_request": "[HTTP] Wysyłanie żądania wymiany tokenu...",
        "dbg_token_success": "[HTTP] Wymiana tokenu SUKCES",
        "dbg_token_fail": "[HTTP] Wymiana tokenu BŁĄD",
        "dbg_refresh_click": "[BTN] Kliknięto Odśwież token",
        "dbg_refresh_request": "[HTTP] Wysyłanie żądania odświeżenia tokenu...",
        "dbg_refresh_success": "[HTTP] Odświeżenie tokenu SUKCES",
        "dbg_refresh_fail": "[HTTP] Odświeżenie tokenu BŁĄD",
        "dbg_copy_access": "[BTN] Kliknięto Kopiuj access_token",
        "dbg_copy_refresh": "[BTN] Kliknięto Kopiuj refresh_token",
        "dbg_copied_ok": "[CLIPBOARD] Skopiowano do schowka: {}",
        "dbg_tutorial_open": "[BTN] Otwarto tutorial",
        "dbg_debug_open": "[DEBUG] Otwarto Debug Console",
        "dbg_config_saved": "[CONFIG] Config zapisano do: {}",
        "dbg_no_rt": "[WARN] Brak refresh_token w konfiguracji",
        "dbg_no_pkce": "[WARN] PKCE code_verifier nie ustawiony",
        "dbg_no_input": "[WARN] Pole wejściowe jest puste",
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
        "dbg_app_start": "[APP] アプリ起動",
        "dbg_lang_changed": "[言語] 言語変更: {}",
        "dbg_lang_saved": "[CONFIG] デフォルト言語保存: {}",
        "dbg_open_login": "[BTN] ログインページを開くをクリック",
        "dbg_browser_open": "[BROWSER] ブラウザでログインURLを開きました",
        "dbg_exchange_click": "[BTN] トークン取得をクリック",
        "dbg_code_parsed": "[PKCE] コード解析成功",
        "dbg_token_request": "[HTTP] トークン交換リクエスト送信中...",
        "dbg_token_success": "[HTTP] トークン交換 成功",
        "dbg_token_fail": "[HTTP] トークン交換 失敗",
        "dbg_refresh_click": "[BTN] トークン更新をクリック",
        "dbg_refresh_request": "[HTTP] トークン更新リクエスト送信中...",
        "dbg_refresh_success": "[HTTP] トークン更新 成功",
        "dbg_refresh_fail": "[HTTP] トークン更新 失敗",
        "dbg_copy_access": "[BTN] access_tokenをコピーをクリック",
        "dbg_copy_refresh": "[BTN] refresh_tokenをコピーをクリック",
        "dbg_copied_ok": "[CLIPBOARD] クリップボードにコピー: {}",
        "dbg_tutorial_open": "[BTN] チュートリアルを開きました",
        "dbg_debug_open": "[DEBUG] デバッグコンソールを開きました",
        "dbg_config_saved": "[CONFIG] Configを保存しました: {}",
        "dbg_no_rt": "[WARN] configにrefresh_tokenがありません",
        "dbg_no_pkce": "[WARN] PKCE code_verifierが未設定",
        "dbg_no_input": "[WARN] 入力欄が空です",
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
        "dbg_app_start": "[APP] 应用已启动",
        "dbg_lang_changed": "[语言] 语言已切换: {}",
        "dbg_lang_saved": "[CONFIG] 已保存默认语言: {}",
        "dbg_open_login": "[BTN] 点击了打开登录页面",
        "dbg_browser_open": "[BROWSER] 已在浏览器中打开登录URL",
        "dbg_exchange_click": "[BTN] 点击了兑换Token",
        "dbg_code_parsed": "[PKCE] 代码解析成功",
        "dbg_token_request": "[HTTP] 正在发送兑换令牌请求...",
        "dbg_token_success": "[HTTP] 令牌兑换成功",
        "dbg_token_fail": "[HTTP] 令牌兑换失败",
        "dbg_refresh_click": "[BTN] 点击了刷新Token",
        "dbg_refresh_request": "[HTTP] 正在发送刷新令牌请求...",
        "dbg_refresh_success": "[HTTP] 令牌刷新成功",
        "dbg_refresh_fail": "[HTTP] 令牌刷新失败",
        "dbg_copy_access": "[BTN] 点击了复制access_token",
        "dbg_copy_refresh": "[BTN] 点击了复制refresh_token",
        "dbg_copied_ok": "[CLIPBOARD] 已复制到剪贴板: {}",
        "dbg_tutorial_open": "[BTN] 已打开教程",
        "dbg_debug_open": "[DEBUG] 已打开调试控制台",
        "dbg_config_saved": "[CONFIG] 配置已保存至: {}",
        "dbg_no_rt": "[WARN] 配置中无refresh_token",
        "dbg_no_pkce": "[WARN] PKCE code_verifier未设置",
        "dbg_no_input": "[WARN] 输入框为空",
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
        "dbg_app_start": "[APP] Anwendung gestartet",
        "dbg_lang_changed": "[SPRACHE] Sprache geändert auf: {}",
        "dbg_lang_saved": "[CONFIG] Standardsprache gespeichert: {}",
        "dbg_open_login": "[BTN] Login-Seite öffnen geklickt",
        "dbg_browser_open": "[BROWSER] Login-URL im Browser geöffnet",
        "dbg_exchange_click": "[BTN] Token abrufen geklickt",
        "dbg_code_parsed": "[PKCE] Code erfolgreich gelesen",
        "dbg_token_request": "[HTTP] Token-Anfrage wird gesendet...",
        "dbg_token_success": "[HTTP] Token-Austausch ERFOLGREICH",
        "dbg_token_fail": "[HTTP] Token-Austausch FEHLGESCHLAGEN",
        "dbg_refresh_click": "[BTN] Token aktualisieren geklickt",
        "dbg_refresh_request": "[HTTP] Token-Aktualisierungsanfrage wird gesendet...",
        "dbg_refresh_success": "[HTTP] Token-Aktualisierung ERFOLGREICH",
        "dbg_refresh_fail": "[HTTP] Token-Aktualisierung FEHLGESCHLAGEN",
        "dbg_copy_access": "[BTN] access_token kopieren geklickt",
        "dbg_copy_refresh": "[BTN] refresh_token kopieren geklickt",
        "dbg_copied_ok": "[CLIPBOARD] In Zwischenablage kopiert: {}",
        "dbg_tutorial_open": "[BTN] Tutorial geöffnet",
        "dbg_debug_open": "[DEBUG] Debug-Konsole geöffnet",
        "dbg_config_saved": "[CONFIG] Config gespeichert unter: {}",
        "dbg_no_rt": "[WARN] Kein refresh_token in der Konfiguration",
        "dbg_no_pkce": "[WARN] PKCE code_verifier nicht gesetzt",
        "dbg_no_input": "[WARN] Eingabefeld ist leer",
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
        "dbg_app_start": "[APP] Application démarrée",
        "dbg_lang_changed": "[LANGUE] Langue changée en: {}",
        "dbg_lang_saved": "[CONFIG] Langue par défaut enregistrée: {}",
        "dbg_open_login": "[BTN] Ouvrir la page de connexion cliqué",
        "dbg_browser_open": "[BROWSER] URL de connexion ouverte dans le navigateur",
        "dbg_exchange_click": "[BTN] Échanger le token cliqué",
        "dbg_code_parsed": "[PKCE] Code lu avec succès",
        "dbg_token_request": "[HTTP] Envoi de la requête d'échange de token...",
        "dbg_token_success": "[HTTP] Échange de token RÉUSSI",
        "dbg_token_fail": "[HTTP] Échange de token ÉCHOUÉ",
        "dbg_refresh_click": "[BTN] Rafraîchir le token cliqué",
        "dbg_refresh_request": "[HTTP] Envoi de la requête de rafraîchissement...",
        "dbg_refresh_success": "[HTTP] Rafraîchissement du token RÉUSSI",
        "dbg_refresh_fail": "[HTTP] Rafraîchissement du token ÉCHOUÉ",
        "dbg_copy_access": "[BTN] Copier access_token cliqué",
        "dbg_copy_refresh": "[BTN] Copier refresh_token cliqué",
        "dbg_copied_ok": "[CLIPBOARD] Copié dans le presse-papiers: {}",
        "dbg_tutorial_open": "[BTN] Tutoriel ouvert",
        "dbg_debug_open": "[DEBUG] Console de débogage ouverte",
        "dbg_config_saved": "[CONFIG] Config enregistrée dans: {}",
        "dbg_no_rt": "[WARN] Pas de refresh_token dans la config",
        "dbg_no_pkce": "[WARN] PKCE code_verifier non défini",
        "dbg_no_input": "[WARN] Champ de saisie vide",
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
        "dbg_app_start": "[APP] Aplicación iniciada",
        "dbg_lang_changed": "[IDIOMA] Idioma cambiado a: {}",
        "dbg_lang_saved": "[CONFIG] Idioma predeterminado guardado: {}",
        "dbg_open_login": "[BTN] Abrir página de inicio pulsado",
        "dbg_browser_open": "[BROWSER] URL de inicio de sesión abierta en el navegador",
        "dbg_exchange_click": "[BTN] Canjear token pulsado",
        "dbg_code_parsed": "[PKCE] Código leído correctamente",
        "dbg_token_request": "[HTTP] Enviando solicitud de canje de token...",
        "dbg_token_success": "[HTTP] Canje de token EXITOSO",
        "dbg_token_fail": "[HTTP] Canje de token FALLIDO",
        "dbg_refresh_click": "[BTN] Actualizar token pulsado",
        "dbg_refresh_request": "[HTTP] Enviando solicitud de actualización de token...",
        "dbg_refresh_success": "[HTTP] Actualización de token EXITOSA",
        "dbg_refresh_fail": "[HTTP] Actualización de token FALLIDA",
        "dbg_copy_access": "[BTN] Copiar access_token pulsado",
        "dbg_copy_refresh": "[BTN] Copiar refresh_token pulsado",
        "dbg_copied_ok": "[CLIPBOARD] Copiado al portapapeles: {}",
        "dbg_tutorial_open": "[BTN] Tutorial abierto",
        "dbg_debug_open": "[DEBUG] Consola de depuración abierta",
        "dbg_config_saved": "[CONFIG] Config guardado en: {}",
        "dbg_no_rt": "[WARN] No hay refresh_token en la configuración",
        "dbg_no_pkce": "[WARN] PKCE code_verifier no establecido",
        "dbg_no_input": "[WARN] Campo de entrada vacío",
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
        "dbg_app_start": "[APP] Приложение запущено",
        "dbg_lang_changed": "[ЯЗЫК] Язык изменён на: {}",
        "dbg_lang_saved": "[CONFIG] Язык по умолчанию сохранён: {}",
        "dbg_open_login": "[BTN] Нажато «Открыть страницу входа»",
        "dbg_browser_open": "[BROWSER] URL входа открыт в браузере",
        "dbg_exchange_click": "[BTN] Нажато «Получить токен»",
        "dbg_code_parsed": "[PKCE] Код успешно разобран",
        "dbg_token_request": "[HTTP] Отправка запроса обмена токена...",
        "dbg_token_success": "[HTTP] Обмен токена УСПЕШНО",
        "dbg_token_fail": "[HTTP] Обмен токена НЕУДАЧНО",
        "dbg_refresh_click": "[BTN] Нажато «Обновить токен»",
        "dbg_refresh_request": "[HTTP] Отправка запроса обновления токена...",
        "dbg_refresh_success": "[HTTP] Обновление токена УСПЕШНО",
        "dbg_refresh_fail": "[HTTP] Обновление токена НЕУДАЧНО",
        "dbg_copy_access": "[BTN] Нажато «Копировать access_token»",
        "dbg_copy_refresh": "[BTN] Нажато «Копировать refresh_token»",
        "dbg_copied_ok": "[CLIPBOARD] Скопировано в буфер: {}",
        "dbg_tutorial_open": "[BTN] Руководство открыто",
        "dbg_debug_open": "[DEBUG] Консоль отладки открыта",
        "dbg_config_saved": "[CONFIG] Config сохранён в: {}",
        "dbg_no_rt": "[WARN] В конфиге нет refresh_token",
        "dbg_no_pkce": "[WARN] PKCE code_verifier не задан",
        "dbg_no_input": "[WARN] Поле ввода пусто",
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
        "dbg_app_start": "[APP] Aplicativo iniciado",
        "dbg_lang_changed": "[IDIOMA] Idioma alterado para: {}",
        "dbg_lang_saved": "[CONFIG] Idioma padrão salvo: {}",
        "dbg_open_login": "[BTN] Abrir página de login clicado",
        "dbg_browser_open": "[BROWSER] URL de login aberta no navegador",
        "dbg_exchange_click": "[BTN] Trocar token clicado",
        "dbg_code_parsed": "[PKCE] Código lido com sucesso",
        "dbg_token_request": "[HTTP] Enviando solicitação de troca de token...",
        "dbg_token_success": "[HTTP] Troca de token BEM-SUCEDIDA",
        "dbg_token_fail": "[HTTP] Troca de token FALHOU",
        "dbg_refresh_click": "[BTN] Atualizar token clicado",
        "dbg_refresh_request": "[HTTP] Enviando solicitação de atualização de token...",
        "dbg_refresh_success": "[HTTP] Atualização de token BEM-SUCEDIDA",
        "dbg_refresh_fail": "[HTTP] Atualização de token FALHOU",
        "dbg_copy_access": "[BTN] Copiar access_token clicado",
        "dbg_copy_refresh": "[BTN] Copiar refresh_token clicado",
        "dbg_copied_ok": "[CLIPBOARD] Copiado para a área de transferência: {}",
        "dbg_tutorial_open": "[BTN] Tutorial aberto",
        "dbg_debug_open": "[DEBUG] Console de depuração aberta",
        "dbg_config_saved": "[CONFIG] Config salvo em: {}",
        "dbg_no_rt": "[WARN] Sem refresh_token no config",
        "dbg_no_pkce": "[WARN] PKCE code_verifier não definido",
        "dbg_no_input": "[WARN] Campo de entrada vazio",
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
        "dbg_app_start": "[APP] 애플리케이션 시작됨",
        "dbg_lang_changed": "[언어] 언어 변경: {}",
        "dbg_lang_saved": "[CONFIG] 기본 언어 저장됨: {}",
        "dbg_open_login": "[BTN] 로그인 페이지 열기 클릭됨",
        "dbg_browser_open": "[BROWSER] 브라우저에서 로그인 URL 열림",
        "dbg_exchange_click": "[BTN] 토큰 받기 클릭됨",
        "dbg_code_parsed": "[PKCE] 코드 성공적으로 읽힐",
        "dbg_token_request": "[HTTP] 토큰 교환 요청 전송 중...",
        "dbg_token_success": "[HTTP] 토큰 교환 성공",
        "dbg_token_fail": "[HTTP] 토큰 교환 실패",
        "dbg_refresh_click": "[BTN] 토큰 새로고침 클릭됨",
        "dbg_refresh_request": "[HTTP] 토큰 갱신 요청 전송 중...",
        "dbg_refresh_success": "[HTTP] 토큰 갱신 성공",
        "dbg_refresh_fail": "[HTTP] 토큰 갱신 실패",
        "dbg_copy_access": "[BTN] access_token 복사 클릭됨",
        "dbg_copy_refresh": "[BTN] refresh_token 복사 클릭됨",
        "dbg_copied_ok": "[CLIPBOARD] 클립보드에 복사됨: {}",
        "dbg_tutorial_open": "[BTN] 튜토리얼 열림",
        "dbg_debug_open": "[DEBUG] 디버그 콘솔 열림",
        "dbg_config_saved": "[CONFIG] Config 저장됨: {}",
        "dbg_no_rt": "[WARN] 설정에 refresh_token 없음",
        "dbg_no_pkce": "[WARN] PKCE code_verifier 미설정",
        "dbg_no_input": "[WARN] 입력 입력란이 비어 있음",
    },
}

EXTRA_UI_EN = {
    "app_header": "Pixiv OAuth Token",
    "app_subtitle": "Modern login helper with quick token exchange",
    "docs": "Read the Docs",
    "menu_changelog": "Changelog",
    "menu_version": "Version",
    "version_current": "Current Version",
    "version_check_now": "Check Version",
    "version_title": "Version Information",
    "version_latest": "Latest Version",
    "version_up_to_date": "You are using the latest version.",
    "version_update_available": "A newer version is available.",
    "version_check_failed": "Could not check the latest version.",
    "version_btn_update": "Update",
    "version_btn_later": "Later",
    "version_updating": "Updating application...",
    "version_update_done": "Update started. The app will close if replacement is required.",
    "version_update_failed": "Automatic update failed",
    "menu_tutorial": "Tutorial",
    "menu_resources_docs": "Resources & Docs",
    "menu_support": "Support",
    "menu_social": "Social",
    "menu_developer": "Developer",
    "tutorial_open": "Open Tutorial",
    "tutorial_title": "Tutorial - Pixiv OAuth Token GUI",
    "tutorial_header": "How to Use",
    "tutorial_desc": "Follow this guided flow to exchange Pixiv OAuth tokens quickly.",
    "tutorial_steps": "Step by step",
    "tutorial_missing": "No tutorial images found. Put ordered PNG files in tutorial_images/.",
    "dev_info_title": "Developer",
    "res_docs_documentation": "Documentation",
    "res_docs_license": "License",
    "res_docs_pixiv": "Pixiv OAuth Endpoint",
    "res_docs_python": "Python 3.11+",
    "res_docs_vercel": "Deployed on Vercel",
    "sup_contact": "Contact Us",
    "sup_report": "Report an Issue",
    "sup_discussions": "Discussions",
    "sup_fatony": "Fatony Ahmad Fauzi",
    "sup_donate": "Support / Donate",
    "social_github": "GitHub",
    "social_linkedin": "LinkedIn",
    "developer_prefix": "Developer",
}

EXTRA_UI_OVERRIDES = {
    "id": {
        "app_subtitle": "Alat login modern untuk pertukaran token cepat",
        "docs": "Baca Dokumentasi",
        "menu_changelog": "Changelog",
        "menu_version": "Versi",
        "version_current": "Versi Saat Ini",
        "version_check_now": "Cek Versi",
        "version_title": "Informasi Versi",
        "version_latest": "Versi Terbaru",
        "version_up_to_date": "Kamu sudah memakai versi terbaru.",
        "version_update_available": "Ada versi terbaru tersedia.",
        "version_check_failed": "Gagal mengecek versi terbaru.",
        "version_btn_update": "Update",
        "version_btn_later": "Nanti",
        "version_updating": "Sedang memperbarui aplikasi...",
        "version_update_done": "Proses update dimulai. Aplikasi akan ditutup jika perlu penggantian file.",
        "version_update_failed": "Update otomatis gagal",
        "menu_resources_docs": "Resource & Dokumen",
        "menu_support": "Dukungan",
        "menu_social": "Media Sosial",
        "menu_developer": "Developer",
        "tutorial_open": "Buka Tutorial",
        "tutorial_header": "Cara Penggunaan",
        "tutorial_desc": "Ikuti langkah berikut untuk menukar token Pixiv OAuth dengan cepat.",
        "tutorial_steps": "Langkah-langkah",
        "tutorial_missing": "Gambar tutorial tidak ditemukan. Taruh file PNG berurutan di folder tutorial_images/.",
        "res_docs_documentation": "Dokumentasi",
        "res_docs_license": "Lisensi",
        "res_docs_pixiv": "Endpoint Pixiv OAuth",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Deployed on Vercel",
        "sup_contact": "Hubungi Kami",
        "sup_report": "Laporkan Masalah",
        "sup_discussions": "Diskusi",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "Dukung / Donasi",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "developer_prefix": "Developer",
    },
    "jp": {
        "app_subtitle": "クイックトークン交換のためのモダンなログインヘルパー",
        "docs": "ドキュメントを読む",
        "menu_resources_docs": "リソース & ドキュメント",
        "menu_support": "サポート",
        "menu_social": "ソーシャル",
        "menu_developer": "開発者",
        "tutorial_open": "チュートリアルを開く",
        "tutorial_header": "使い方",
        "tutorial_desc": "このガイドに沿って Pixiv OAuth トークンを素早く取得できます。",
        "tutorial_steps": "手順",
        "dev_info_title": "開発者",
        "res_docs_documentation": "ドキュメント",
        "res_docs_license": "ライセンス",
        "res_docs_pixiv": "Pixiv OAuth エンドポイント",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Vercel にデプロイ",
        "sup_contact": "お問い合わせ",
        "sup_report": "問題を報告",
        "sup_discussions": "ディスカッション",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "サポート / 寄付",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "developer_prefix": "開発者",
    },
    "pl": {
        "menu_resources_docs": "Zasoby & Dokumentacja",
        "menu_support": "Wsparcie",
        "menu_social": "Media społeczne",
        "menu_developer": "Deweloper",
        "docs": "Czytaj dokumentację",
        "res_docs_documentation": "Dokumentacja",
        "res_docs_license": "Licencja",
        "res_docs_pixiv": "Punkt końcowy Pixiv OAuth",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Wdrożone na Vercel",
        "sup_contact": "Skontaktuj się z nami",
        "sup_report": "Zgłoś problem",
        "sup_discussions": "Dyskusje",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "Wspomóż / Podaruj",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "developer_prefix": "Deweloper"
    },
    "zh": {
        "menu_resources_docs": "资源 & 文档",
        "menu_support": "支持",
        "menu_social": "社交媒体",
        "menu_developer": "开发者",
        "docs": "阅读文档",
        "res_docs_documentation": "文档",
        "res_docs_license": "许可证",
        "res_docs_pixiv": "Pixiv OAuth 端点",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "部署在 Vercel 上",
        "sup_contact": "联系我们",
        "sup_report": "报告问题",
        "sup_discussions": "讨论",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "支持 / 捐赠",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "developer_prefix": "开发者"
    },
    "de": {
        "menu_resources_docs": "Ressourcen & Dokumentation",
        "menu_support": "Support",
        "menu_social": "Soziale Medien",
        "menu_developer": "Entwickler",
        "docs": "Dokumentation lesen",
        "res_docs_documentation": "Dokumentation",
        "res_docs_license": "Lizenz",
        "res_docs_pixiv": "Pixiv OAuth Endpunkt",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Auf Vercel bereitgestellt",
        "sup_contact": "Kontaktieren Sie uns",
        "sup_report": "Problem melden",
        "sup_discussions": "Diskussionen",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "Unterstützung / Spende",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "developer_prefix": "Entwickler"
    },
    "fr": {
        "menu_resources_docs": "Ressources & Documentation",
        "menu_support": "Support",
        "menu_social": "Réseaux sociaux",
        "menu_developer": "Développeur",
        "docs": "Lire la documentation",
        "res_docs_documentation": "Documentation",
        "res_docs_license": "Licence",
        "res_docs_pixiv": "Point de terminaison Pixiv OAuth",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Déployé sur Vercel",
        "sup_contact": "Nous contacter",
        "sup_report": "Signaler un problème",
        "sup_discussions": "Discussions",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "Support / Donation",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "developer_prefix": "Développeur"
    },
    "es": {
        "menu_resources_docs": "Recursos & Documentación",
        "menu_support": "Soporte",
        "menu_social": "Redes sociales",
        "menu_developer": "Desarrollador",
        "docs": "Leer la documentación",
        "res_docs_documentation": "Documentación",
        "res_docs_license": "Licencia",
        "res_docs_pixiv": "Endpoint de Pixiv OAuth",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Implementado en Vercel",
        "sup_contact": "Contáctenos",
        "sup_report": "Reportar un problema",
        "sup_discussions": "Discusiones",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "Apoyo / Donación",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "developer_prefix": "Desarrollador"
    },
    "ru": {
        "menu_resources_docs": "Ресурсы & Документация",
        "menu_support": "Поддержка",
        "menu_social": "Социальные сети",
        "menu_developer": "Разработчик",
        "docs": "Читать документацию",
        "res_docs_documentation": "Документация",
        "res_docs_license": "Лицензия",
        "res_docs_pixiv": "Endpoint Pixiv OAuth",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Развернуто на Vercel",
        "sup_contact": "Свяжитесь с нами",
        "sup_report": "Сообщить об ошибке",
        "sup_discussions": "Обсуждения",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "Поддержка / Пожертвование",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "developer_prefix": "Разработчик"
    },
    "pt": {
        "menu_resources_docs": "Recursos & Documentação",
        "menu_support": "Suporte",
        "menu_social": "Redes sociais",
        "menu_developer": "Desenvolvedor",
        "docs": "Ler a documentação",
        "res_docs_documentation": "Documentação",
        "res_docs_license": "Licença",
        "res_docs_pixiv": "Endpoint Pixiv OAuth",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Implantado no Vercel",
        "sup_contact": "Contate-nos",
        "sup_report": "Relatar um problema",
        "sup_discussions": "Discussões",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "Suporte / Doação",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "developer_prefix": "Desenvolvedor"
    },
    "kr": {
        "menu_resources_docs": "리소스 & 문서",
        "menu_support": "지원",
        "menu_social": "소셜 미디어",
        "menu_developer": "개발자",
        "docs": "문서 읽기",
        "res_docs_documentation": "문서",
        "res_docs_license": "라이센스",
        "res_docs_pixiv": "Pixiv OAuth 엔드포인트",
        "res_docs_python": "Python 3.11+",
        "res_docs_vercel": "Vercel에 배포됨",
        "sup_contact": "문의하기",
        "sup_report": "문제 보고",
        "sup_discussions": "토론",
        "sup_fatony": "Fatony Ahmad Fauzi",
        "sup_donate": "지원 / 기부",
        "social_github": "GitHub",
        "social_linkedin": "LinkedIn",
        "developer_prefix": "개발자"
    },
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
ICON_CANDIDATES = ("pixiv_login_pro.ico", "pixiv_login.ico")


def resolve_icon_path() -> Path | None:
    for icon_name in ICON_CANDIDATES:
        p = app_dir() / icon_name
        if p.exists():
            return p
    return None


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


def _normalize_version_tag(version: str | None) -> str | None:
    if not version:
        return None
    value = str(version).strip()
    if not value:
        return None
    return value if value.startswith("v") else f"v{value}"


def _version_key(version: str | None) -> tuple[int, ...]:
    if not version:
        return (0, 0, 0)
    cleaned = str(version).strip().lstrip("vV")
    parts = []
    for token in cleaned.split("."):
        try:
            parts.append(int(token))
        except ValueError:
            parts.append(0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


def get_current_app_version(cfg: dict | None = None) -> str:
    try:
        if VERSION_FILE.exists():
            raw = VERSION_FILE.read_text(encoding="utf-8").strip()
            if raw:
                if raw.startswith("{"):
                    payload = json.loads(raw)
                    version = payload.get("version")
                    if isinstance(version, str) and version.strip():
                        return _normalize_version_tag(version) or APP_VERSION
                return _normalize_version_tag(raw.split("|")[0].strip()) or APP_VERSION
    except Exception:
        pass
    source_cfg = cfg or load_config()
    from_cfg = source_cfg.get("app_version")
    if isinstance(from_cfg, str) and from_cfg.strip():
        return _normalize_version_tag(from_cfg.strip()) or APP_VERSION
    return APP_VERSION


def get_current_app_code(cfg: dict | None = None) -> str:
    try:
        if VERSION_FILE.exists():
            raw = VERSION_FILE.read_text(encoding="utf-8").strip()
            if raw:
                if raw.startswith("{"):
                    payload = json.loads(raw)
                    code = payload.get("build_code")
                    if isinstance(code, str) and code.strip():
                        return code.strip()
                parts = raw.split("|", 1)
                if len(parts) == 2 and parts[1].strip():
                    return parts[1].strip()
    except Exception:
        pass
    source_cfg = cfg or load_config()
    from_cfg = source_cfg.get("app_build_code")
    if isinstance(from_cfg, str) and from_cfg.strip():
        return from_cfg.strip()
    return APP_BUILD_CODE


def set_current_app_identity(version: str, build_code: str) -> None:
    normalized = _normalize_version_tag(version) or APP_VERSION
    identity = {"version": normalized, "build_code": build_code.strip() or APP_BUILD_CODE}
    try:
        VERSION_FILE.write_text(json.dumps(identity, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass
    cfg = load_config()
    cfg["app_version"] = identity["version"]
    cfg["app_build_code"] = identity["build_code"]
    save_config(cfg)


def fetch_latest_release_meta() -> tuple[str | None, str | None]:
    try:
        resp = requests.get(LATEST_MANIFEST_URL, timeout=12)
        resp.raise_for_status()
        payload = resp.json()
        tag = _normalize_version_tag(payload.get("version"))
        code = str(payload.get("build_code", "")).strip() or None
        if tag:
            return tag, code
    except Exception:
        pass

    try:
        resp = requests.get(GITHUB_API_LATEST_RELEASE, timeout=12)
        resp.raise_for_status()
        payload = resp.json()
        tag = _normalize_version_tag(payload.get("tag_name"))
        release_id = payload.get("id")
        code = f"REL-{release_id}" if release_id else None
        return tag, code
    except Exception:
        return None, None


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

        # Debug
        self._debug_log: list[str] = []
        self._debug_window: tk.Toplevel | None = None
        self._debug_text: tk.Text | None = None
        self._version_check_in_progress = False

        self.lang_var = tk.StringVar(value=default_name)
        self.save_lang_var = tk.BooleanVar(value=True)

        self._set_app_icon()
        self._build_ui()
        self.apply_ui_language()
        self._update_copy_buttons()

        self.debug(f"Config file: {CONFIG_FILE}")
        self.debug(self.t("dbg_app_start"))
        self.debug(self.t("dbg_config_saved").format(CONFIG_FILE))
        self.after(1300, self.auto_check_updates)

    def _set_app_icon(self):
        icon_path = resolve_icon_path()
        if not icon_path:
            return
        try:
            self.iconbitmap(str(icon_path))
        except Exception:
            pass

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
        code = self.current_lang_code()
        lang_name = LANG_CODE_TO_NAME.get(code, code)
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

        self.debug(self.t("dbg_lang_changed").format(lang_name))

        if self.save_lang_var.get():
            self.cfg["default_lang"] = code
            save_config(self.cfg)
            self.debug(self.t("dbg_lang_saved").format(code))

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

        style.configure(
            "Debug.TButton",
            font=("Segoe UI", 9, "bold"),
            padding=(10, 5),
            foreground="#94a3b8",
            background="#1e293b",
            borderwidth=0,
        )
        style.map("Debug.TButton", background=[("active", "#334155")])

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

        title_wrap = ttk.Frame(header, style="App.TFrame")
        title_wrap.pack(side="left", fill="x", expand=True)

        self.header_title_label = ttk.Label(title_wrap, text=self.tx("app_header"), style="Header.TLabel")
        self.header_title_label.pack(anchor="w")
        self.header_subtitle_label = ttk.Label(title_wrap, text=self.tx("app_subtitle"), style="Sub.TLabel")
        self.header_subtitle_label.pack(anchor="w")

        self.debug_btn = ttk.Button(
            header,
            text="⚙ Debug",
            style="Debug.TButton",
            command=self.show_debug_window,
        )
        self.debug_btn.pack(side="right", padx=(8, 0))

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

        self.docs_btn = ttk.Button(top, text="Read the Docs", style="Secondary.TButton", command=lambda: open_url("https://pixiv-o-auth-token.vercel.app/documentation"))
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

        menubar.add_command(label=self.tx("menu_tutorial"), command=self.show_tutorial)

        version_menu = tk.Menu(menubar, tearoff=0)
        current_version = get_current_app_version(self.cfg)
        current_label = f"{self.tx('version_current')}: {current_version}"
        version_menu.add_command(
            label=current_label,
            state="disabled",
        )
        version_menu.add_separator()
        version_menu.add_command(label=self.tx("version_check_now"), command=lambda: self.check_version(manual=True))
        menubar.add_cascade(label=self.tx("menu_version"), menu=version_menu)

        resources_menu = tk.Menu(menubar, tearoff=0)
        resources_menu.add_command(label=self.tx('res_docs_documentation'), command=lambda: open_url("https://pixiv-o-auth-token.vercel.app/documentation"))
        resources_menu.add_command(label=self.tx('res_docs_license'), command=lambda: open_url("https://pixiv-o-auth-token.vercel.app/license"))
        resources_menu.add_command(label=self.tx('res_docs_pixiv'), command=lambda: open_url("https://oauth.secure.pixiv.net/auth/token"))
        resources_menu.add_command(label=self.tx('res_docs_python'), command=lambda: open_url("https://www.python.org"))
        resources_menu.add_command(label=self.tx('res_docs_vercel'), command=lambda: open_url("https://vercel.com"))
        resources_menu.add_command(label=self.tx('menu_changelog'), command=lambda: open_url(RELEASES_URL))
        menubar.add_cascade(label=self.tx("menu_resources_docs"), menu=resources_menu)

        support_menu = tk.Menu(menubar, tearoff=0)
        support_menu.add_command(label=self.tx('sup_contact'), command=lambda: open_url("https://pixiv-o-auth-token.vercel.app/contact"))
        support_menu.add_command(label=self.tx('sup_report'), command=lambda: open_url("https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/issues"))
        support_menu.add_command(label=self.tx('sup_discussions'), command=lambda: open_url("https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/discussions"))
        support_menu.add_command(label=self.tx('sup_fatony'), command=lambda: open_url("https://github.com/fatonyahmadfauzi"))
        support_menu.add_command(label=self.tx('sup_donate'), command=lambda: open_url("https://pixiv-o-auth-token.vercel.app/support"))
        menubar.add_cascade(label=self.tx("menu_support"), menu=support_menu)

        social_menu = tk.Menu(menubar, tearoff=0)
        social_menu.add_command(label=self.tx('social_github'), command=lambda: open_url("https://github.com/fatonyahmadfauzi"))
        social_menu.add_command(label=self.tx('social_linkedin'), command=lambda: open_url("https://www.linkedin.com/in/fatonyahmadfauzi"))
        menubar.add_cascade(label=self.tx("menu_social"), menu=social_menu)

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
        self.debug(self.t("dbg_tutorial_open"))
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
        ttk.Button(footer, text=self.tx("docs"), style="Primary.TButton", command=lambda: open_url("https://pixiv-o-auth-token.vercel.app/documentation")).pack(side="right")

    # ---------- Version / Update ----------
    def auto_check_updates(self):
        self.check_version(manual=False)

    def check_version(self, manual: bool = False):
        if self._version_check_in_progress:
            return
        self._version_check_in_progress = True

        current_version = get_current_app_version(self.cfg)
        current_code = get_current_app_code(self.cfg)

        def worker():
            latest_version, latest_code = fetch_latest_release_meta()

            def done():
                self._version_check_in_progress = False
                if not latest_version:
                    if manual:
                        messagebox.showwarning(self.tx("version_title"), self.tx("version_check_failed"))
                    return

                has_update = _version_key(latest_version) > _version_key(current_version)
                if not has_update and latest_code and latest_code != current_code:
                    has_update = True

                if has_update:
                    self.show_update_popup(current_version, current_code, latest_version, latest_code or APP_BUILD_CODE)
                elif manual:
                    current_line = f"{self.tx('version_current')}: {current_version}"
                    latest_line = f"{self.tx('version_latest')}: {latest_version}"
                    messagebox.showinfo(
                        self.tx("version_title"),
                        f"{current_line}\n"
                        f"{latest_line}\n\n"
                        f"{self.tx('version_up_to_date')}",
                    )

            self.after(0, done)

        threading.Thread(target=worker, daemon=True).start()

    def show_update_popup(self, current_version: str, current_code: str, latest_version: str, latest_code: str):
        popup = tk.Toplevel(self)
        popup.title(self.tx("version_title"))
        popup.geometry("460x230")
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        current_line = f"{self.tx('version_current')}: {current_version}"
        latest_line = f"{self.tx('version_latest')}: {latest_version}"

        body = ttk.Frame(popup, padding=14)
        body.pack(fill="both", expand=True)
        ttk.Label(body, text=self.tx("version_update_available"), style="Header.TLabel").pack(anchor="w", pady=(0, 10))
        ttk.Label(
            body,
            text=f"{current_line}\n{latest_line}",
            style="TLabel",
            justify="left",
        ).pack(anchor="w")

        btn_row = ttk.Frame(body)
        btn_row.pack(side="bottom", fill="x", pady=(16, 0))

        def later():
            popup.destroy()

        def do_update():
            popup.destroy()
            self.start_update_flow(latest_version, latest_code)

        ttk.Button(btn_row, text=self.tx("version_btn_later"), style="Secondary.TButton", command=later).pack(side="right")
        ttk.Button(btn_row, text=self.tx("version_btn_update"), style="Primary.TButton", command=do_update).pack(side="right", padx=(0, 8))

    def start_update_flow(self, latest_version: str, latest_code: str):
        self.log(self.tx("version_updating"))

        def worker():
            try:
                is_frozen = bool(getattr(sys, "frozen", False))
                if not is_frozen:
                    open_url(RELEASES_URL)
                    self.after(0, lambda: messagebox.showinfo(self.tx("version_title"), self.tx("version_update_done")))
                    return

                exe_path = Path(sys.executable).resolve()
                is_setup = "program files" in str(exe_path).lower() or "setup" in exe_path.name.lower()
                if is_setup:
                    setup_file = Path(tempfile.gettempdir()) / "pixiv_gui_setup_latest.exe"
                    self._download_to_file(SETUP_LATEST_URL, setup_file)
                    subprocess.Popen([str(setup_file), "/SP-", "/VERYSILENT", "/NORESTART"], shell=False)
                    self.after(0, lambda: messagebox.showinfo(self.tx("version_title"), self.tx("version_update_done")))
                    return

                new_exe = exe_path.with_name(exe_path.stem + "_new.exe")
                self._download_to_file(PORTABLE_LATEST_URL, new_exe)
                self._replace_exe_with_updater(exe_path, new_exe)
                set_current_app_identity(latest_version, latest_code)
                self.after(0, lambda: messagebox.showinfo(self.tx("version_title"), self.tx("version_update_done")))
                self.after(350, self.destroy)
            except Exception as exc:
                self.after(0, lambda: messagebox.showerror(self.tx("version_title"), f"{self.tx('version_update_failed')}: {exc}"))

        threading.Thread(target=worker, daemon=True).start()

    def _download_to_file(self, url: str, target: Path):
        resp = requests.get(url, timeout=40, stream=True)
        resp.raise_for_status()
        with target.open("wb") as fh:
            for chunk in resp.iter_content(chunk_size=1024 * 128):
                if chunk:
                    fh.write(chunk)

    def _replace_exe_with_updater(self, current_exe: Path, new_exe: Path):
        bat = current_exe.with_name("pixiv_gui_updater.bat")
        bat.write_text(
            "@echo off\n"
            "timeout /t 2 /nobreak >nul\n"
            f"if exist \"{current_exe}.old\" del /f /q \"{current_exe}.old\" >nul 2>nul\n"
            f"move /y \"{current_exe}\" \"{current_exe}.old\" >nul\n"
            f"move /y \"{new_exe}\" \"{current_exe}\" >nul\n"
            f"start \"\" \"{current_exe}\"\n"
            "del \"%~f0\"\n",
            encoding="utf-8",
        )
        subprocess.Popen(["cmd", "/c", str(bat)], creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


    def log(self, msg: str):
        self.output.insert("end", msg + "\n")
        self.output.see("end")
        # Also feed to debug buffer & live debug window
        self._debug_log.append(msg)
        if self._debug_window and self._debug_text:
            try:
                self._debug_text.configure(state="normal")
                self._debug_text.insert("end", msg + "\n")
                self._debug_text.see("end")
                self._debug_text.configure(state="disabled")
            except tk.TclError:
                pass

    def debug(self, msg: str):
        """Write to debug console ONLY (not the main output box)."""
        clean = re.sub(r'^\[[A-Z /]+\]\s*', '', msg)
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{stamp} | {clean}"
        self._debug_log.append(entry)
        if self._debug_window and self._debug_text:
            try:
                self._debug_text.configure(state="normal")
                self._debug_text.insert("end", entry + "\n")
                self._debug_text.see("end")
                self._debug_text.configure(state="disabled")
            except tk.TclError:
                pass

    # ---------- Debug Window ----------
    def show_debug_window(self):
        # If already open, bring to front
        if self._debug_window and self._debug_window.winfo_exists():
            self._debug_window.lift()
            self._debug_window.focus_force()
            return

        win = tk.Toplevel(self)
        win.title("Debug Console")
        win.geometry("900x500")
        win.minsize(600, 300)
        win.configure(bg="#0f172a")
        self._debug_window = win

        # ---- top bar ----
        bar = tk.Frame(win, bg="#1e293b", pady=6, padx=10)
        bar.pack(fill="x", side="top")

        tk.Label(
            bar,
            text="⚙  Debug Console",
            bg="#1e293b",
            fg="#e2e8f0",
            font=("Segoe UI Semibold", 10),
        ).pack(side="left")

        def copy_all():
            try:
                content = self._debug_text.get("1.0", "end")
                self.clipboard_clear()
                self.clipboard_append(content)
                self.update()
                self.debug("Debug copied.")
            except Exception:
                pass

        def clear_debug():
            try:
                self.debug("Debug logs cleared.")
                self._debug_text.configure(state="normal")
                self._debug_text.delete("1.0", "end")
                # Re-insert the single 'cleared' entry
                if self._debug_log:
                    self._debug_text.insert("end", self._debug_log[-1] + "\n")
                kept = self._debug_log[-1:]
                self._debug_log.clear()
                self._debug_log.extend(kept)
                self._debug_text.configure(state="disabled")
            except Exception:
                pass

        btn_cfg = dict(bg="#334155", fg="#e2e8f0", relief="flat",
                       font=("Segoe UI", 9), padx=10, pady=3,
                       cursor="hand2", activebackground="#475569",
                       activeforeground="#ffffff")

        tk.Button(bar, text="Copy All", command=copy_all, **btn_cfg).pack(side="right", padx=(4, 0))
        tk.Button(bar, text="Clear", command=clear_debug, **btn_cfg).pack(side="right")

        # ---- terminal area ----
        frame = tk.Frame(win, bg="#0f172a")
        frame.pack(fill="both", expand=True, padx=0, pady=0)

        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        text = tk.Text(
            frame,
            wrap="word",
            bg="#0f172a",
            fg="#94a3b8",
            insertbackground="#94a3b8",
            selectbackground="#1e40af",
            relief="flat",
            font=("Cascadia Mono", 9),
            padx=14,
            pady=10,
            yscrollcommand=scrollbar.set,
            state="normal",
            borderwidth=0,
        )
        text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text.yview)
        self._debug_text = text

        # Pre-populate with buffered history
        if self._debug_log:
            text.insert("1.0", "\n".join(self._debug_log) + "\n")
        text.see("end")
        text.configure(state="disabled")

        # Colour tags for keywords
        text.tag_config("err",  foreground="#f87171")
        text.tag_config("ok",   foreground="#34d399")
        text.tag_config("info", foreground="#60a5fa")

        def on_close():
            self._debug_window = None
            self._debug_text = None
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_close)

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
        self.debug(self.t("dbg_copy_access"))
        if not self.last_access_token:
            self.debug("[WARN] No access_token available")
            messagebox.showinfo("Copy", self.t("no_access"))
            return
        self.debug(self.t("dbg_copied_ok").format("access_token"))
        self._copy_to_clipboard(self.last_access_token, "copied_access")

    def copy_refresh_token(self):
        self.debug(self.t("dbg_copy_refresh"))
        if not self.last_refresh_token:
            self.debug("[WARN] No refresh_token available")
            messagebox.showinfo("Copy", self.t("no_refresh"))
            return
        self.debug(self.t("dbg_copied_ok").format("refresh_token"))
        self._copy_to_clipboard(self.last_refresh_token, "copied_refresh")

    # ---------- Actions ----------
    def open_login(self):
        self.debug(self.t("dbg_open_login"))
        self._set_default_lang_if_needed()

        self.code_verifier, code_challenge = oauth_pkce()

        login_params = {
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "client": "pixiv-android",
        }
        login_url = f"{LOGIN_URL}?{urlencode(login_params)}"
        self.log("Opening browser for login...")
        self.debug(self.t("dbg_browser_open"))
        open_url(login_url)

        messagebox.showinfo(self.t("next_step_title"), self.t("next_step_body"))

    def exchange_token(self):
        self.debug(self.t("dbg_exchange_click"))
        if not self.code_verifier:
            self.debug(self.t("dbg_no_pkce"))
            messagebox.showwarning("PKCE", self.t("pkce_warn"))
            return

        raw = self.code_entry.get().strip()
        if not raw:
            self.debug(self.t("dbg_no_input"))
            messagebox.showwarning("Input", self.t("input_warn"))
            return

        try:
            code = extract_code(raw)
            self.debug(self.t("dbg_code_parsed"))
        except Exception:
            messagebox.showerror("Error", self.t("parse_fail"))
            return

        self._set_default_lang_if_needed()

        def worker():
            self.after(0, lambda: self.debug(self.t("dbg_token_request")))
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
                self.after(0, lambda: self.debug(self.t("dbg_token_fail")))
                return

            def ui():
                if "access_token" not in data:
                    self.debug(self.t("dbg_token_fail"))
                    self.log("ERROR RESPONSE:")
                    self.log(json.dumps(data, indent=2, ensure_ascii=False))
                    return

                self.debug(self.t("dbg_token_success"))
                self.last_access_token = data.get("access_token")
                self.last_refresh_token = data.get("refresh_token")
                self._update_copy_buttons()

                self.log("=== LOGIN SUCCESS ===")
                self.log(f"access_token : {self.last_access_token}")
                self.log(f"refresh_token: {self.last_refresh_token}")
                self.log(f"expires_in   : {data.get('expires_in')}")

                self.cfg["refresh_token"] = self.last_refresh_token
                save_config(self.cfg)
                self.debug(self.t("dbg_config_saved").format(CONFIG_FILE))

            self.after(0, ui)

        threading.Thread(target=worker, daemon=True).start()

    def refresh_token(self):
        self.debug(self.t("dbg_refresh_click"))
        self.cfg = load_config()
        rt = self.cfg.get("refresh_token")
        if not rt:
            self.debug(self.t("dbg_no_rt"))
            messagebox.showinfo("Refresh", self.t("refresh_no_token"))
            return

        def worker():
            self.after(0, lambda: self.debug(self.t("dbg_refresh_request")))
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
                self.after(0, lambda: self.debug(self.t("dbg_refresh_fail")))
                return

            def ui():
                if "access_token" not in data:
                    self.debug(self.t("dbg_refresh_fail"))
                    self.log("ERROR RESPONSE:")
                    self.log(json.dumps(data, indent=2, ensure_ascii=False))
                    return

                self.debug(self.t("dbg_refresh_success"))
                self.last_access_token = data.get("access_token")
                self.last_refresh_token = data.get("refresh_token")
                self._update_copy_buttons()

                self.log("=== REFRESH SUCCESS ===")
                self.log(f"access_token : {self.last_access_token}")
                self.log(f"refresh_token: {self.last_refresh_token}")
                self.log(f"expires_in   : {data.get('expires_in')}")

                self.cfg["refresh_token"] = self.last_refresh_token
                save_config(self.cfg)
                self.debug(self.t("dbg_config_saved").format(CONFIG_FILE))

            self.after(0, ui)

        threading.Thread(target=worker, daemon=True).start()


if __name__ == "__main__":
    App().mainloop()
