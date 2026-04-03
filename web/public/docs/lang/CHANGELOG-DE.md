# Änderungsprotokoll

All notable changes to the "Pixiv OAuth Token" toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🔜 Coming Soon

- **Mobile Web Support** — The web app currently only supports desktop browsers. Upcoming update will bring full responsive mobile support, allowing users to generate Pixiv OAuth tokens directly from mobile devices without needing the desktop app.


---

## [1.0.5] - 2026-04-03

### ✨ Hinzugefügt

- **Internetfähiger GUI Startup**
Vor dem Start des GUI-Hauptfensters führt nun ein intelligenter `NetLoadingScreen`-Begrüßungsbildschirm vor dem Flug eine Überprüfung der Internetverbindung durch. Wenn keine Verbindung gefunden wird, versucht es im Hintergrund sicher erneut, bis eine Verbindung hergestellt ist. Darüber hinaus zeigt ein aktiver Laufzeitmonitor eine Warnung an, die zum Ladebildschirm zurückspringt, wenn die Verbindung während der Nutzung unterbrochen wird.
- **Native GUI-Dokumentationsmodalitäten**
Externe Browser-Weiterleitungen für wichtige Dokumentation ersetzt. **Änderungsprotokoll**, **Allgemeine Geschäftsbedingungen** und **Datenschutzrichtlinie** werden jetzt in nativen, dynamischen und sauberen `tkinter`-Dialogfenstern angezeigt (die asynchron direkt aus dem GitHub-Repository abgerufen werden).
- **Umfassende Terminallokalisierungen**
Die interaktive GitHub CLI-Schnittstelle (Problemnavigation) und alle terminalbasierten Rechts-/Support-Layouts sind jetzt in allen 11 unterstützten Sprachen authentisch lokalisiert.

### ✨ Geändert

- **Neu gestaltete CLI-Ästhetik**
Die alten dekorativen Boxränder wurden entfernt, um eine deutlich übersichtlichere, modernisierte, linksbündige Terminalanzeige zu erhalten.
- **Automatisierte digitale Code-Signierung**
Die `sign_auto.bat`-Pipeline wurde erheblich aktualisiert. Das Skript erkennt `signtool.exe` nun dynamisch und automatisch tief im Windows SDK und wendet das selbstsignierte Zertifikat mühelos gleichzeitig auf alle generierten Builds an (einschließlich Installer-Setups und Download-`_latest`-Aliase), um grundlegende SmartScreen-Flags „Unbekannter Herausgeber“ zu unterdrücken.

### 🐞 Behoben

- **Fehler bei den Installer-Eigenschaften**
Es wurde eine Anomalie behoben, bei der der Installer `Setup.exe` in den Windows-Eigenschaften `0.0.0.0` anzeigte. Der Builder fügt jetzt während der Kompilierung ordnungsgemäß die strikten PE-Header `VersionInfoVersion` ein, um sofort beim Rendern die genau übereinstimmende Release-Nummer (e.g., 1.0.5.0) wiederzugeben.

---

## [1.0.4] - 2026-03-29

### 🐞 Behoben

- **Portable CLI/GUI – Versions-Rollback nach Update**: `VERSION_FILE` und `CONFIG_FILE` wurden mit `Path(__file__)` aufgelöst, das im eingefrorenen Modus (PyInstaller onefile) auf das temporäre `_MEIPASS`-Verzeichnis verweist – ein Verzeichnis, das beim Schließen der App zerstört wird. Beide Dateien werden jetzt mit `_app_dir()` / `app_dir()` aufgelöst, wodurch korrekt der Ordner zurückgegeben wird, der die eigentliche `.exe` enthält, wodurch sichergestellt wird, dass die Versionsidentität über Neustarts hinweg bestehen bleibt.
- **CLI – Update überschrieb temporäres `.py` anstelle von exe**: Bei der Ausführung als eingefrorene ausführbare Datei überschrieb `_self_update()` das extrahierte `.py` im temporären Verzeichnis, anstatt das tatsächliche `.exe` zu ersetzen. Die Funktion erkennt nun `is_frozen` und lädt die neue ausführbare Datei direkt herunter und ersetzt sie über ein `.bat`-Updater-Skript (gleicher Mechanismus wie GUI).

### ✨ Hinzugefügt

- **Architekturbewusstes automatisches Update (CLI + GUI)**: Sowohl portable als auch Setup-Update-Flows erkennen jetzt die Architektur der laufenden ausführbaren Datei (`x64`, `x86`, `ARM64` oder generisch) anhand ihres Dateinamens und laden die genau passende Variante aus dem Ordner `downloads/` herunter, wodurch versehentliche Architekturkonflikte während Aktualisierungen verhindert werden.
- **CLI Setup-Installationsprogramm-Aktualisierungsablauf**: CLI spiegelt jetzt das GUI-Verhalten für Setup-Installationen wider – wenn es von `Program Files` ausgeführt wird, lädt es das neueste `.exe`-Setup-Installationsprogramm herunter und führt es im Hintergrund aus (`/VERYSILENT /NORESTART`), anstatt einen direkten Binäraustausch zu versuchen.

---

## [1.0.3] - 2026-03-26

### ✨ Geändert

– Standardmäßiges lokales Build-Label von `REL-LOCAL` durch `BUILD-UNKNOWN` für Laufzeit-/Versionstools und generierte Manifeste ersetzt.
- GUI enthält jetzt eine Aktion im oberen Menü **Änderungsprotokoll** und ein Dropdown-Menü **Version** mit explizitem Versionsprüfungseintrag.
– Automatische Startversionsüberprüfung in GUI mit Update-Popup-Aktionen (**Update** / **Später**) hinzugefügt, plus Update-Flow-Behandlung für eingefrorene Setup-/tragbare Distributionen.
– Aktualisierte Build-Code-Generierung auf Unix-Stil `REL-U<unix_ms>` bei Versionssprüngen (`patch/minor/major`).

## [1.0.2] - 2026-03-23

### ✨ Hinzugefügt

- **Debug-Konsole (GUI)**
Eine spezielle `⚙ Debug`-Schaltfläche in der oberen rechten Ecke des GUI-Headers öffnet eine Terminalkonsole im dunklen Design, die jedes Anwendungsereignis in Echtzeit protokolliert. Zu den erfassten Ereignissen gehören: App-Start, Sprachänderungen, alle Schaltflächenklicks (Anmeldung öffnen, Exchange-Token, Aktualisierungstoken, Zugriffs-/Aktualisierungstoken kopieren, Tutorial), HTTP-Anforderungsstatus (Senden/Erfolg/Fehler), PKCE-Ablaufschritte, Zwischenablagevorgänge, Konfigurationsschreibvorgänge und Warnungen. Alle Debug-Meldungen sind vollständig in allen 11 unterstützten Sprachen lokalisiert. Die Konsole unterstützt das Live-Streaming neuer Nachrichten im geöffneten Zustand, das Vorabfüllen historischer Protokolle ab Sitzungsbeginn, eine Schaltfläche **Alle kopieren** und eine Schaltfläche **Löschen**.

## [1.0.1] - 2026-03-22

### ✨ Hinzugefügt

- **Smart README Cleaner für Veröffentlichungen**
Entfernt beim Kompilieren des verteilbaren `.zip` automatisch Abschnitte der Lokalisierungssprache aus der ``-Datei und ersetzt interne Links durch absolute GitHub-Links.
- **Unified Dual Installer-Unterstützung**
Das InnoSetup-Builder-Skript generiert jetzt ein einheitliches Installationsprogramm, das Endbenutzer auffordert, wahlweise das eigenständige CLI oder das grafische GUI zu installieren.

### 🐞 Behoben

- **Auflösung des Installationspfads**
Es wurde ein Problem mit kritischen Pfadkonflikten in `make_installer_iss_dual.py` behoben, bei dem `iscc` `app\pixiv_oauth.ico` nicht finden konnte, indem Build-Dateien direkt im konfigurierten `scripts\`-Verzeichnis generiert wurden.

## [1.0.0] - 2026-03-21

### ✨ Hinzugefügt

– Erste eigenständige ausführbare Distributionen (`.exe`), kompiliert für die Modi GUI und CLI.
– Anfänglich optimierte serverlose Integration synchronisiert mit Vercel mit automatischer Spracherkennung.
– Extremer JavaScript-Verschleierungspass für Web-Endpunkte hinzugefügt.
