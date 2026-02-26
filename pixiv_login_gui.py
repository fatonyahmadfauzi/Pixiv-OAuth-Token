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


# ===== LANGUAGE =====
SUPPORTED_LANGS = ("en", "id", "pl", "zh", "jp", "de", "fr", "es", "ru", "pt", "kr")

LANG_CHOICES = [
    ("English", "en"),
    ("Indonesia", "id"),
    ("Polski", "pl"),
    ("日本語", "jp"),
    ("中文", "zh"),
    ("Deutsch", "de"),
    ("Français", "fr"),
    ("Español", "es"),
    ("Русский", "ru"),
    ("Português", "pt"),
    ("한국어", "kr"),
]

LANG_NAME_TO_CODE = {name: code for name, code in LANG_CHOICES}
LANG_CODE_TO_NAME = {code: name for name, code in LANG_CHOICES}


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
        default_name = LANG_CODE_TO_NAME.get(default_code, "English")

        self.code_verifier: str | None = None
        self.last_access_token: str | None = None
        self.last_refresh_token: str | None = self.cfg.get("refresh_token")

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

        if self.save_lang_var.get():
            self.cfg["default_lang"] = self.current_lang_code()
            save_config(self.cfg)

    def _set_default_lang_if_needed(self):
        if self.save_lang_var.get():
            self.cfg["default_lang"] = self.current_lang_code()
            save_config(self.cfg)

    # ---------- UI ----------
    def _build_ui(self):
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        self.lang_label = ttk.Label(top, text="Language:")
        self.lang_label.pack(side="left")

        self.lang_combo = ttk.Combobox(
            top,
            textvariable=self.lang_var,
            values=[name for name, _ in LANG_CHOICES],
            width=14,
            state="readonly",
        )
        self.lang_combo.pack(side="left", padx=(6, 16))
        self.lang_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_ui_language())

        self.save_lang_check = ttk.Checkbutton(top, text="Save as default", variable=self.save_lang_var, command=self.apply_ui_language)
        self.save_lang_check.pack(side="left")

        self.open_login_btn = ttk.Button(top, text="Open Login Page", command=self.open_login)
        self.open_login_btn.pack(side="right")

        self.refresh_btn = ttk.Button(top, text="Refresh Token", command=self.refresh_token)
        self.refresh_btn.pack(side="right", padx=(0, 8))

        self.paste_frame = ttk.LabelFrame(self, text="Paste URL / Code", padding=10)
        self.paste_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.code_entry = ttk.Entry(self.paste_frame)
        self.code_entry.pack(fill="x", expand=True)

        btn_row = ttk.Frame(self.paste_frame)
        btn_row.pack(fill="x", pady=(8, 0))

        self.exchange_btn = ttk.Button(btn_row, text="Exchange Token", command=self.exchange_token)
        self.exchange_btn.pack(side="right")

        copy_row = ttk.Frame(self, padding=(10, 0, 10, 10))
        copy_row.pack(fill="x")

        self.copy_access_btn = ttk.Button(copy_row, text="Copy access_token", command=self.copy_access_token)
        self.copy_access_btn.pack(side="left")

        self.copy_refresh_btn = ttk.Button(copy_row, text="Copy refresh_token", command=self.copy_refresh_token)
        self.copy_refresh_btn.pack(side="left", padx=(8, 0))

        self.output_frame = ttk.LabelFrame(self, text="Output", padding=10)
        self.output_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.output = tk.Text(self.output_frame, wrap="word")
        self.output.pack(fill="both", expand=True)

        self.geometry("820x600")
        self.minsize(820, 600)

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
