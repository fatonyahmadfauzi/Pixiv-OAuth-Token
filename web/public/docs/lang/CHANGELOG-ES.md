# Registro de cambios

Todos los cambios notables en el kit de herramientas "Pixiv OAuth Token" se documentarán en este archivo.

El formato se basa en [Mantener un registro de cambios](https://keepachangelog.com/en/1.0.0/),
y este proyecto se adhiere a [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🔜 Próximamente

- **Soporte web móvil**: la aplicación web actualmente solo admite navegadores de escritorio. La próxima actualización brindará soporte móvil totalmente responsivo, lo que permitirá a los usuarios generar tokens Pixiv OAuth directamente desde dispositivos móviles sin necesidad de la aplicación de escritorio.

---

## [1.0.4] - 2026-03-29

### 🐞 Corregido

- **CLI/GUI portátil: reversión de la versión después de la actualización**: `VERSION_FILE` y `CONFIG_FILE` se resolvieron usando `Path(__file__)`, que en modo congelado (PyInstaller onefile) apunta al directorio temporal `_MEIPASS`, un directorio que se destruye cuando se cierra la aplicación. Ambos archivos ahora se resuelven usando `_app_dir()` / `app_dir()`, que devuelve correctamente la carpeta que contiene el `.exe` real, lo que garantiza que la identidad de la versión persista durante los reinicios.
- **CLI: la actualización sobrescribió el `.py` temporal en lugar de exe**: cuando se ejecutaba como un ejecutable congelado, `_self_update()` sobrescribía el `.py` extraído dentro del directorio temporal en lugar de reemplazar el `.exe` real. La función ahora detecta `is_frozen` y descarga el nuevo ejecutable directamente, reemplazándolo mediante un script de actualización `.bat` (el mismo mecanismo que la GUI).

### ✨ Agregado

- **Actualización automática basada en la arquitectura (CLI + GUI)**: tanto los flujos de actualización portátiles como los de configuración ahora detectan la arquitectura del ejecutable en ejecución (`x64`, `x86`, `ARM64` o genérico) a partir de su nombre de archivo y descargan la variante coincidente exacta de la carpeta `downloads/`, lo que evita discrepancias accidentales en la arquitectura durante las actualizaciones.
- **Flujo de actualización del instalador de configuración CLI**: CLI ahora refleja el comportamiento de la GUI para las instalaciones de configuración: cuando se ejecuta desde `Program Files`, descarga el último instalador de configuración `.exe` y lo ejecuta silenciosamente (`/VERYSILENT /NORESTART`) en lugar de intentar un intercambio binario in situ.

---

## [1.0.3] - 2026-03-26

### ✨ Cambiado

- Se reemplazó la etiqueta de compilación local predeterminada de `REL-LOCAL` a `BUILD-UNKNOWN` en todas las herramientas de tiempo de ejecución/versión y manifiestos generados.
- La GUI ahora incluye una acción del menú superior **Registro de cambios** y un menú desplegable **Versión** con una entrada explícita de verificación de versión.
- Se agregó verificación automática de la versión de inicio en la GUI con acciones emergentes de actualización (**Actualizar** / **Más tarde**), además de manejo del flujo de actualización para configuraciones congeladas/distribuciones portátiles.
- Se actualizó la generación de código de compilación al estilo Unix `REL-U<unix_ms>` en los cambios de versión (`patch/minor/major`).

## [1.0.2] - 2026-03-23

### ✨ Agregado

- **Consola de depuración (GUI)**
  Un botón dedicado `⚙ Debug` en la esquina superior derecha del encabezado de la GUI abre una consola de terminal con tema oscuro que registra cada evento de la aplicación en tiempo real. Los eventos capturados incluyen: inicio de la aplicación, cambios de idioma, todos los clics en los botones (Abrir inicio de sesión, Token de intercambio, Token de actualización, Copiar acceso/token de actualización, Tutorial), estados de solicitud HTTP (envío/éxito/fallido), pasos de flujo de PKCE, operaciones del portapapeles, escrituras de configuración y advertencias. Todos los mensajes de depuración están completamente traducidos a los 11 idiomas admitidos. La consola admite la transmisión en vivo de mensajes nuevos mientras están abiertos, el llenado previo de registros históricos desde el inicio de la sesión, un botón **Copiar todo** y un botón **Borrar**.

## [1.0.1] - 2026-03-22

### ✨ Agregado

- **Limpiador inteligente README para versiones**
  Elimina automáticamente las secciones de idioma de localización del archivo `__p1__` al compilar el `.zip` distribuible, reemplazando los enlaces internos con enlaces GitHub absolutos.
- **Soporte unificado de instalador dual**
  El script del constructor InnoSetup ahora genera un instalador unificado que solicita a los usuarios finales que instalen opcionalmente la CLI independiente o la GUI gráfica.

### 🐞 Corregido

- **Resolución de ruta de compilación del instalador**
  Se solucionó un problema crítico de falta de coincidencia de rutas en `make_installer_iss_dual.py` donde `iscc` no pudo ubicar `app\pixiv_oauth.ico` al generar archivos de compilación directamente dentro del directorio `scripts\` configurado.

## [1.0.0] - 2026-03-21

### ✨ Agregado

- Distribuciones ejecutables independientes iniciales (`.exe`) compiladas para modos GUI y CLI.
- Integración inicial optimizada sin servidor sincronizada con Vercel con detección automática de idioma.
- Se agregó un pase de ofuscación de JavaScript extremo para puntos finales web.
