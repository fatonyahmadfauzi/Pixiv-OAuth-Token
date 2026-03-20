# Pixiv OAuth Token


> 🌐 Disponible en otros idiomas: [English](../../README.md) | [Polski](README-PL.md) | [中文](README-ZH.md) | [日本語](README-JP.md) | [Deutsch](README-DE.md) | [Français](README-FR.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [Bahasa Indonesia](README-ID.md) | [한국어](README-KR.md)

---
Un conjunto de herramientas para generar tokens Pixiv OAuth en tres modos:

- CLI (`pixiv_login.py`)
- GUI (`pixiv_login_gui.py`)
- Aplicación web (`public/` + API sin servidor)

## Requisitos

- Pitón 3.11+
- Windows (requerido para los scripts de compilación `.bat` y el instalador de Inno Setup)
- Dependencias de Python de `requirements.txt`

## Ejecutar desde la fuente

```bash
python -m pip install -r requirements.txt
python pixiv_login.py
```

Ejecute la GUI:

```bash
python pixiv_login_gui.py
```

## Construir

### Construya todos los artefactos (CLI + GUI + Instalador + ZIP)

```bat
build_all_pro.bat patch
```

Argumento de versión:

- `patch`
- `minor`
- `major`
- `none`

Banderas opcionales:

- `noinst` (omitir instalador)
- `nosign` (saltar la firma)
- `nozip` (saltar zip)
- `nogui` (omitir GUI)
- `nopause` (sin pausa al final)

Ejemplo:

```bat
build_all_pro.bat patch noinst nosign
```

### Principales resultados

- CLI portátil: `dist_portable\Pixiv OAuth CLi (Portable).exe`
- GUI portátil: `dist_gui\Pixiv OAuth GUi (Portable).exe`
- CLI del instalador: `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe`
- GUI del instalador: `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe`
- Lanzamiento ZIP: `PixivOAuthRelease_v<version>.zip`
- Carpeta sincronizada automáticamente: `downloads/` (último archivo portátil/configuración + ZIP de lanzamiento)

## Firma

Editar `sign_auto.bat`:

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

Si falta el archivo PFX, se omite la firma.

## Versionado

La versión de la aplicación se almacena en `version.json`.

## Versión web (Vercel)

Una aplicación web responsiva y altamente optimizada que ofrece soporte dinámico en varios idiomas (11 idiomas con detección automática) y metadatos SEO completos.

### Funciones web clave
- **Páginas extensas**: página de inicio, descargas, tutorial, contacto, problemas y relaciones públicas, seguimiento de debates, visor de Markdown de documentación e integración de soporte/donación.
- **SEO avanzado**: etiquetas `<meta>` localizadas inyectadas automáticamente, datos estructurados JSON-LD extensos (enlaces de sitio, aplicaciones de software, etc.), generación automatizada de `hreflang`, `robots.txt` y `sitemap.xml`.
- **Seguridad y rendimiento**: ofuscación automática de JavaScript (manipulación extrema), minificación de HTML/CSS (a través de `node build_minify.js`) y prevención de limpieza `XSS` a través de `escapeHTML`.
- **GitHub API Proxy**: Los puntos finales de Vercel sin servidor (`/api/github`) representan solicitudes de API de GitHub utilizando un token de acceso personal (`GITHUB_PAT`) para evitar por completo los límites de tarifas públicas.

### Implementar en Vercel

1. Envíe el repositorio a GitHub.
2. Vercel → **Agregar nuevo...** → **Proyecto** → importar este repositorio.
3. Configure sus variables de entorno en Vercel:
- `PIXIV_CLIENT_SECRET`: Su secreto de cliente Pixiv OAuth.
- `GITHUB_PAT`: Opcional pero muy recomendado (Su token de acceso personal de GitHub para evitar límites de tasa en emisiones y lanzamientos de repositorios).
4. `vercel.json` ya configura:
- Limpiar URL (eliminar `.html`)
- Alojamiento estático de `public/`
- API sin servidor en `/api/*`
- Enrutamiento de páginas 404 personalizado incorporado
- Almacenamiento en caché en un futuro lejano a través de encabezados de Edge Cache.
5. Implementar.

> [!IMPORTANTE]
> Si realiza cambios en HTML, CSS o JS, recuerde ejecutar `node build_minify.js` antes de implementar para ofuscar automáticamente el código y comprimir los activos.

> Nota de seguridad: para producción, configure siempre `PIXIV_CLIENT_SECRET` en las variables de entorno de su proyecto Vercel.

## Descargar la aplicación (última versión)

URL básica:

`https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download`

Archivos:

- GUI portátil: `Pixiv OAuth GUi (Portable).exe`
- GUI de configuración: `Pixiv OAuth GUi Setup_v<version>.exe`
- CLI portátil: `Pixiv OAuth CLi (Portable).exe`
- CLI de configuración: `Pixiv OAuth CLi Setup_v<version>.exe`

### PowerShell (detección automática de activos de la última versión)

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

### PowerShell (URL fijas de `downloads/`)

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

Ejecute esto en **PowerShell** (no en CMD).

Si solo ejecutas:

```powershell
$guiPortable = "..."
```

y no aparece nada, eso es lo esperado. Solo almacena un valor en una variable. La descarga comienza cuando ejecuta `Invoke-WebRequest`.

Una vez finalizada la descarga, PowerShell vuelve a `PS C:\...>` sin errores:

```powershell
Get-ChildItem "Pixiv OAuth GUi (Portable).exe"
Start-Process ".\Pixiv OAuth GUi (Portable).exe"
```

Para la compilación del instalador:

```powershell
Invoke-WebRequest $guiSetup -OutFile "Pixiv OAuth GUi Setup.exe"
Start-Process ".\Pixiv OAuth GUi Setup.exe"
```

Si la política TLS bloquea la descarga:

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

### CMD (detección automática de activos de la última versión)

```cmd
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi Setup.exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi Setup.exe"
```

## Instalación de Python

```bash
python -m pip install -r requirements.txt
```

O instálelo directamente desde GitHub:

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```

## Licencia

MIT License. Ver `LICENSE`.
