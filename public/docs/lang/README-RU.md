# Pixiv OAuth Token


> 🌐 Доступно na innych językach: [English](../../README.md) | [Polski](README-PL.md) | [中文](README-ZH.md) | [日本語](README-JP.md) | [Deutsch](README-DE.md) | [Français](README-FR.md) | [Español](README-ES.md) | [Português](README-PT.md) | [Bahasa Indonesia](README-ID.md) | [한국어](README-KR.md)

---
Набор инструментов для генерации токенов Pixiv OAuth в трёх режимах:

- CLI (`pixiv_login.py`)
- Графический интерфейс (`pixiv_login_gui.py`)
- Веб-приложение (`public/` + бессерверный API)

## Требования

- Питон 3.11+
- Windows (требуется для сценариев сборки `.bat` и установщика Inno Setup)
- Зависимости Python от `requirements.txt`

## Запуск из исходного кода

```bash
python -m pip install -r requirements.txt
python pixiv_login.py
```

Запустите графический интерфейс:

```bash
python pixiv_login_gui.py
```

## Строить

### Сборка всех артефактов (CLI + GUI + Installer + ZIP)

```bat
build_all_pro.bat patch
```

Аргумент версии:

- `patch`
- `minor`
- `major`
- `none`

Дополнительные флаги:

- `noinst` (пропустить установку)
- `nosign` (пропустить подпись)
- `nozip` (пропустить zip)
- `nogui` (пропустить графический интерфейс)
- `nopause` (без паузы в конце)

Пример:

```bat
build_all_pro.bat patch noinst nosign
```

### Основные выходы

- Портативный интерфейс командной строки: `dist_portable\Pixiv OAuth CLi (Portable).exe`
- Портативный графический интерфейс: `dist_gui\Pixiv OAuth GUi (Portable).exe`
- Интерфейс командной строки установщика: `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe`
- Графический интерфейс установщика: `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe`
- ZIP-архив выпуска: `PixivOAuthRelease_v<version>.zip`.
- Папка с автоматической синхронизацией: `downloads/` (последняя портативная версия/установка + ZIP-версия)

## Подписание

Отредактируйте `sign_auto.bat`:

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

Если файл PFX отсутствует, подписывание пропускается.

## Управление версиями

Версия приложения хранится в `version.json`.

## Веб-версия (Версель)

Высокооптимизированное, отзывчивое веб-приложение с динамической многоязычной поддержкой (11 языков с автоматическим определением) и полными метаданными SEO.

### Ключевые веб-функции
- **Обширные страницы**: домашняя страница, загрузки, руководство, контакты, проблемы и рекламные сообщения, трекер обсуждений, средство просмотра документации Markdown и интеграция поддержки/пожертвований.
– **Расширенное SEO**: автоматическое внедрение локализованных тегов `<meta>`, обширные структурированные данные JSON-LD (дополнительные ссылки, программное обеспечение и т. д.), автоматическое создание `hreflang`, `robots.txt` и `sitemap.xml`.
- **Безопасность и производительность**: автоматическая обфускация JavaScript (экстремальное искажение), минификация HTML/CSS (через `node build_minify.js`) и чистое предотвращение `XSS` через `escapeHTML`.
- **Прокси-сервер API GitHub**: бессерверные конечные точки Vercel (`/api/github`) прокси-сервера GitHub API запрашивают с использованием токена личного доступа (`GITHUB_PAT`) для полного обхода общедоступных ограничений скорости.

### Развертывание в Верселе

1. Отправьте репозиторий на GitHub.
2. Vercel → **Добавить новый...** → **Проект** → импортируйте этот репозиторий.
3. Установите переменные среды в Vercel:
- `PIXIV_CLIENT_SECRET`: секрет вашего клиента Pixiv OAuth.
- `GITHUB_PAT`: необязательно, но настоятельно рекомендуется (ваш токен личного доступа GitHub, чтобы избежать ограничений скорости при проблемах с репозиториями и выпусках).
4. `vercel.json` уже настраивает:
- Очистить URL-адреса (удалив `.html`).
- Статический хостинг от `public/`
- Бессерверные API на `/api/*`.
- Встроенная пользовательская маршрутизация страниц 404.
- Кэширование далекого будущего через заголовки Edge Cache.
5. Развертывание.

> [!ВАЖНО]
> Если вы вносите изменения в HTML, CSS или JS, не забудьте запустить `node build_minify.js` перед развертыванием, чтобы автоматически запутать код и сжать ресурсы.

> Примечание по безопасности: в рабочей среде всегда устанавливайте `PIXIV_CLIENT_SECRET` в переменных среды проекта Vercel.

## Скачать приложение (последняя версия)

Базовый URL:

`https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download`

Файлы:

- Портативный графический интерфейс: `Pixiv OAuth GUi (Portable).exe`
- Графический интерфейс настройки: `Pixiv OAuth GUi Setup_v<version>.exe`
- Портативный интерфейс командной строки: `Pixiv OAuth CLi (Portable).exe`
- Настройка CLI: `Pixiv OAuth CLi Setup_v<version>.exe`

### PowerShell (автоматическое определение ресурсов последней версии)

```powershell
$api = "https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest"
$assets = (Invoke-RestMethod -Uri $api).assets

function Get-AssetUrl([string]$pattern) {
  ($assets | Where-Object { $_.name -match $pattern } | Select-Object -First 1).browser_download_url
}

$guiPortable = Get-AssetUrl "Pixiv OAuth GUi \(Portable\)"
$cliPortable = Get-AssetUrl "Pixiv OAuth CLi \(Portable\)"
$guiSetup    = Get-AssetUrl "Pixiv OAuth GUi Setup"
$cliSetup    = Get-AssetUrl "Pixiv OAuth CLi Setup"

Invoke-WebRequest $guiPortable -OutFile "Pixiv OAuth GUi (Portable).exe"
Invoke-WebRequest $cliPortable -OutFile "Pixiv OAuth CLi (Portable).exe"
Invoke-WebRequest $guiSetup    -OutFile "Pixiv OAuth GUi Setup.exe"
Invoke-WebRequest $cliSetup    -OutFile "Pixiv OAuth CLi Setup.exe"
```

### PowerShell (исправлены URL-адреса из `downloads/`)

```powershell
$guiPortable = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads/Pixiv%20OAuth%20GUi%20(Portable)_latest.exe"
$cliPortable = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads/Pixiv%20OAuth%20CLi%20(Portable)_latest.exe"
$guiSetup    = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads/Pixiv%20OAuth%20GUi%20Setup_latest.exe"
$cliSetup    = "https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/raw/HEAD/downloads/Pixiv%20OAuth%20CLi%20Setup_latest.exe"

Invoke-WebRequest $guiPortable -OutFile "Pixiv OAuth GUi (Portable).exe"
Invoke-WebRequest $cliPortable -OutFile "Pixiv OAuth CLi (Portable).exe"
Invoke-WebRequest $guiSetup    -OutFile "Pixiv OAuth GUi Setup.exe"
Invoke-WebRequest $cliSetup    -OutFile "Pixiv OAuth CLi Setup.exe"
```

Запустите это в **PowerShell** (не в CMD).

Если вы запускаете только:

```powershell
$guiPortable = "..."
```

и ничего не появляется, что ожидается. Он сохраняет только значение в переменной. Загрузка начинается при запуске `Invoke-WebRequest`.

После завершения загрузки PowerShell возвращается к `PS C:\...>` без ошибок:

```powershell
Get-ChildItem "Pixiv OAuth GUi (Portable).exe"
Start-Process ".\Pixiv OAuth GUi (Portable).exe"
```

Для сборки установщика:

```powershell
Invoke-WebRequest $guiSetup -OutFile "Pixiv OAuth GUi Setup.exe"
Start-Process ".\Pixiv OAuth GUi Setup.exe"
```

Если политика TLS блокирует загрузку:

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

### CMD (автоматическое определение ресурсов последней версии)

```cmd
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi Setup.exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi Setup.exe"
```

## Установка Python

```bash
python -m pip install -r requirements.txt
```

Или установите прямо с GitHub:

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```

## Лицензия

MIT License. См. `LICENSE`.
> 🌐 Доступно на других языках: [Polski](docs/lang/README-PL.md) | [中文](docs/lang/README-ZH.md) | [日本語](docs/lang/README-JP.md) | [Deutsch](docs/lang/README-DE.md) | [Французский](docs/lang/README-FR.md) | [Испанский](docs/lang/README-ES.md) | [Русский](docs/lang/README-RU.md) | [Португальский](docs/lang/README-PT.md) | [Бахаса Индонезия](docs/lang/README-ID.md) | [한국어](docs/lang/README-KR.md)
