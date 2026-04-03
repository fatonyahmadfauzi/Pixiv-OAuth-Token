# Registro de cambios

All notable changes to the "Pixiv OAuth Token" toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🔜 Coming Soon

- **Mobile Web Support** — The web app currently only supports desktop browsers. Upcoming update will bring full responsive mobile support, allowing users to generate Pixiv OAuth tokens directly from mobile devices without needing the desktop app.


---

## [1.0.5] - 2026-04-03

### ✨ Añadido

- **Inicio GUI compatible con Internet**
Antes de abrir la ventana principal GUI, una pantalla de presentación inteligente `NetLoadingScreen` ahora realiza una verificación de conectividad a Internet antes del vuelo. Si no se encuentra ninguna conexión, lo vuelve a intentar de forma segura en segundo plano hasta que se conecte. Además, un monitor de tiempo de ejecución activo mostrará una alerta que regresará a la pantalla de carga si la conexión se interrumpe a mitad del uso.
- **Modales de documentación nativos GUI**
Se reemplazaron las redirecciones del navegador externo para documentación crítica. **Registro de cambios**, **Términos y condiciones** y **Política de privacidad** ahora se muestran dentro de las ventanas de diálogo `tkinter` nativas, dinámicas y limpias (se obtienen de forma asincrónica directamente desde el repositorio GitHub).
- **Localizaciones completas de terminales**
La interfaz interactiva GitHub CLI (navegación de problemas) y todos los diseños legales/de soporte basados ​​en terminales ahora están auténticamente localizados en los 11 idiomas admitidos.

### ✨ Cambiado

- **Estética CLI rediseñada**
Se eliminaron los bordes decorativos heredados de la caja para lograr una pantalla del terminal significativamente más limpia, modernizada y alineada a la izquierda.
- **Firma de código digital automatizada**
Se mejoró sustancialmente el oleoducto `sign_auto.bat`. El script ahora descubre automáticamente dinámicamente `signtool.exe` en lo profundo del SDK de Windows, aplicando sin esfuerzo el certificado autofirmado en todas las compilaciones generadas simultáneamente (incluidas las configuraciones del instalador y los alias de descarga `_latest`) para suprimir los indicadores básicos de "Editor desconocido" de SmartScreen.

### 🐞 Fijo

- **Error en las propiedades del instalador**
Se corrigió una anomalía por la cual el instalador `Setup.exe` mostraba `0.0.0.0` en Propiedades de Windows. El constructor ahora inyecta correctamente los estrictos encabezados PE `VersionInfoVersion` durante la compilación para reflejar el número de versión coincidente exacto (e.g., 1.0.5.0) inmediatamente después de la renderización.

---

## [1.0.4] - 2026-03-29

### 🐞 Fijo

- **Portátil CLI/GUI: reversión de la versión después de la actualización**: `VERSION_FILE` y `CONFIG_FILE` se resolvieron usando `Path(__file__)`, que en modo congelado (PyInstaller onefile) apunta al directorio temporal `_MEIPASS`, un directorio que se destruye cuando se cierra la aplicación. Ambos archivos ahora se resuelven usando `_app_dir()` / `app_dir()`, que devuelve correctamente la carpeta que contiene el `.exe` real, lo que garantiza que la identidad de la versión persista durante los reinicios.
- **CLI — La actualización sobrescribió el `.py` temporal en lugar de exe**: cuando se ejecutaba como un ejecutable congelado, `_self_update()` sobrescribía el `.py` extraído dentro del directorio temporal en lugar de reemplazar el `.exe` real. La función ahora detecta `is_frozen` y descarga el nuevo ejecutable directamente, reemplazándolo mediante un script de actualización `.bat` (el mismo mecanismo que GUI).

### ✨ Añadido

- **Actualización automática basada en la arquitectura (CLI + GUI)**: Tanto los flujos de actualización portátiles como los de configuración ahora detectan la arquitectura del ejecutable en ejecución (`x64`, `x86`, `ARM64` o genérico) a partir de su nombre de archivo y descargan la variante exacta que coincide de la carpeta `downloads/`, lo que evita discrepancias accidentales en la arquitectura durante las actualizaciones.
- **flujo de actualización del instalador de configuración CLI**: CLI ahora refleja el comportamiento de GUI para las instalaciones de configuración: cuando se ejecuta desde `Program Files`, descarga el último instalador de configuración `.exe` y lo ejecuta silenciosamente (`/VERYSILENT /NORESTART`) en lugar de intentar un intercambio binario en el lugar.

---

## [1.0.3] - 2026-03-26

### ✨ Cambiado

- Se reemplazó la etiqueta de compilación local predeterminada de `REL-LOCAL` a `BUILD-UNKNOWN` en todas las herramientas de tiempo de ejecución/versión y manifiestos generados.
- GUI ahora incluye una acción del menú superior **Registro de cambios** y un menú desplegable **Versión** con una entrada explícita de verificación de versión.
- Se agregó verificación automática de la versión de inicio en GUI con acciones emergentes de actualización (**Actualizar** / **Más tarde**), además de manejo del flujo de actualización para configuraciones congeladas/distribuciones portátiles.
- Se actualizó la generación de código de compilación al estilo Unix `REL-U<unix_ms>` en los cambios de versión (`patch/minor/major`).

## [1.0.2] - 2026-03-23

### ✨ Añadido

- **Consola de depuración (GUI)**
Un botón dedicado `⚙ Debug` en la esquina superior derecha del encabezado GUI abre una consola de terminal con tema oscuro que registra cada evento de la aplicación en tiempo real. Los eventos capturados incluyen: inicio de la aplicación, cambios de idioma, todos los clics en los botones (Abrir inicio de sesión, Token de intercambio, Token de actualización, Copiar acceso/token de actualización, Tutorial), estados de solicitud HTTP (envío/éxito/fallido), pasos de flujo de PKCE, operaciones del portapapeles, escrituras de configuración y advertencias. Todos los mensajes de depuración están completamente traducidos a los 11 idiomas admitidos. La consola admite la transmisión en vivo de mensajes nuevos mientras están abiertos, el llenado previo de registros históricos desde el inicio de la sesión, un botón **Copiar todo** y un botón **Borrar**.

## [1.0.1] - 2026-03-22

### ✨ Añadido

- **Limpiador inteligente README para versiones**
Elimina automáticamente las secciones de idioma de localización del archivo `` al compilar el `.zip` distribuible, reemplazando los enlaces internos con enlaces GitHub absolutos.
- **Soporte unificado de instalador dual**
El script del constructor InnoSetup ahora genera un instalador unificado que solicita a los usuarios finales instalar opcionalmente el CLI independiente o el GUI gráfico.

### 🐞 Fijo

- **Resolución de ruta de compilación del instalador**
Se solucionó un problema crítico de falta de coincidencia de rutas en `make_installer_iss_dual.py` donde `iscc` no pudo ubicar `app\pixiv_oauth.ico` al generar archivos de compilación directamente dentro del directorio `scripts\` configurado.

## [1.0.0] - 2026-03-21

### ✨ Añadido

- Distribuciones ejecutables independientes iniciales (`.exe`) compiladas para los modos GUI y CLI.
- Integración inicial optimizada sin servidor sincronizada con Vercel con detección automática de idioma.
- Se agregó un pase de ofuscación de JavaScript extremo para puntos finales web.
