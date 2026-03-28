# Changelog

All notable changes to the "Pixiv OAuth Token" toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🔜 Coming Soon
- **Mobile Web Support** — The web app currently only supports desktop browsers. Upcoming update will bring full responsive mobile support, allowing users to generate Pixiv OAuth tokens directly from mobile devices without needing the desktop app.

---

## [1.0.4] - 2026-03-29

### 🐞 Fixed
- **Portable CLI/GUI — Version rollback after update**: `VERSION_FILE` and `CONFIG_FILE` were resolved using `Path(__file__)`, which in frozen (PyInstaller onefile) mode points to the temporary `_MEIPASS` directory — a directory that is destroyed when the app closes. Both files are now resolved using `_app_dir()` / `app_dir()` which correctly returns the folder containing the actual `.exe`, ensuring version identity persists across restarts.
- **CLI — Update overwrote temp `.py` instead of exe**: When running as a frozen executable, `_self_update()` was overwriting the extracted `.py` inside the temporary directory instead of replacing the actual `.exe`. The function now detects `is_frozen` and downloads the new executable directly, replacing it via a `.bat` updater script (same mechanism as the GUI).

### ✨ Added
- **Architecture-aware auto-update (CLI + GUI)**: Both portable and setup update flows now detect the architecture of the running executable (`x64`, `x86`, `ARM64`, or generic) from its filename and download the exact matching variant from the `downloads/` folder, preventing accidental architecture mismatches during updates.
- **CLI setup installer update flow**: CLI now mirrors the GUI behavior for setup installations — when running from `Program Files`, it downloads the latest `.exe` setup installer and runs it silently (`/VERYSILENT /NORESTART`) instead of attempting an in-place binary swap.

---
## [1.0.3] - 2026-03-26 
### ✨ Changed
- Replaced default local build label from `REL-LOCAL` to `BUILD-UNKNOWN` across runtime/version tooling and generated manifests.
- GUI now includes a **Changelog** top-menu action and a **Version** dropdown with explicit version check entry.
- Added automatic startup version check in GUI with update popup actions (**Update** / **Later**), plus update flow handling for frozen setup/portable distributions.
- Updated build-code generation to unix-style `REL-U<unix_ms>` on version bumps (`patch/minor/major`).

## [1.0.2] - 2026-03-23 
### ✨ Added
- **Debug Console (GUI)**
  A dedicated `⚙ Debug` button in the top-right corner of the GUI header opens a dark-themed terminal console that logs every application event in real-time. Events captured include: app startup, language changes, all button clicks (Open Login, Exchange Token, Refresh Token, Copy access/refresh token, Tutorial), HTTP request states (sending/success/failed), PKCE flow steps, clipboard operations, config writes, and warnings. All debug messages are fully localized in all 11 supported languages. The console supports live-streaming of new messages while open, pre-population of historical logs from session start, a **Copy All** button, and a **Clear** button.

## [1.0.1] - 2026-03-22
### ✨ Added
- **Smart README Cleaner for Releases**
  Automatically removes localization language sections from the `README.md` file when compiling the distributable `.zip`, replacing internal links with absolute GitHub links.
- **Unified Dual Installer Support**
  The InnoSetup builder script now generates a unified installer that prompts end users to optionally install the standalone CLI or the graphical GUI.

### 🐞 Fixed
- **Installer Build Path Resolution**
  Fixed a critical path mismatch issue in `make_installer_iss_dual.py` where `iscc` failed to locate `app\pixiv_oauth.ico` by generating build files directly within the configured `scripts\` directory.

## [1.0.0] - 2026-03-21
### ✨ Added
- Initial standalone executable distributions (`.exe`) compiled for GUI and CLI modes.
- Initial optimized serverless integration synced to Vercel with automatic language detection.
- Extreme JavaScript obfuscation pass added for web endpoints.
