# Changelog

All notable changes to the "Pixiv OAuth Token" toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
