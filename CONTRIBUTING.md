# Contributing to Pixiv OAuth Token

First off, thank you for considering contributing to **Pixiv OAuth Token**! It's people like you that make open-source projects great. 

This document provides guidelines and instructions for contributing to this repository.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
    - [Reporting Bugs](#reporting-bugs)
    - [Suggesting Enhancements](#suggesting-enhancements)
    - [Translating / Adding New Languages](#translating--adding-new-languages)
3. [Local Development Setup](#local-development-setup)
4. [Pull Request Process](#pull-request-process)

---

## Code of Conduct
By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand what behavior is expected.

## How Can I Contribute?

### Reporting Bugs
If you find a bug, please create an issue on our GitHub Issues page. Include as much detail as possible:
* Your Operating System (Windows, macOS, Linux).
* The browser you are using (if it's a web issue).
* Steps to reproduce the bug.
* Screenshots or error logs if applicable.

### Suggesting Enhancements
We welcome new ideas! If you have a feature request, please open an issue and explain:
* What the feature is.
* Why it would be useful for the users.
* How you think it should work.

### Translating / Adding New Languages
This project supports multiple languages. If you want to add a new language or improve an existing translation:
1. Go to the `web/public/` directory.
2. Find the folder for the language you want to edit (e.g., `id/` for Indonesian, `jp/` for Japanese), or create a new folder for a new language based on the `en/` folder.
3. Translate the HTML files and update the links accordingly.
4. If adding a new language, remember to update the language switcher menu in the main website files.

## Local Development Setup

This project consists of a Python desktop application and a web-based interface.

### 1. Web Development (Node.js)
To work on the website or documentation:

1. Ensure you have Node.js installed.
2. Open your terminal and navigate to the web directory:

```
cd web
npm install
```

To test the website locally, you can use the provided Python script:

```
python scripts/run_local_web_server.py
```

### 2. App Development (Python)
To work on the desktop application or login script:

1. Ensure you have Python 3.x installed.
2. Install the required dependencies:

```
pip install -r app/requirements.txt
```

The main scripts are located in the `app/` directory (e.g., `app/pixiv_login.py` and `app/pixiv_login_gui.py`).

## Pull Request Process

1. Fork the repository and create your branch from `main`.
2. Name your branch descriptively (e.g., `feature/add-dark-mode` or `fix/login-error`).
3. Make sure your code follows the existing style and runs without errors.
4. Update the `CHANGELOG.md` or documentation if your changes require it.
5. Open a Pull Request and describe the changes you made in detail.

---

Thank you for your contribution! 🚀
