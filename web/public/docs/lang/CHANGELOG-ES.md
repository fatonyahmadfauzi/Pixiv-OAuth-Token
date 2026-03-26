# Registro de cambios

All notable changes to the "Pixiv OAuth Token" toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


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
Elimina automáticamente las secciones de idioma de localización del archivo `` al compilar el `.zip` distribuible, reemplazando los enlaces internos con enlaces GitHub absolutos.
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
