# Änderungsprotokoll

Alle wesentlichen Änderungen am Toolkit „Pixiv OAuth Token“ werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
und dieses Projekt hält sich an [Semantische Versionierung](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🔜 Bald erhältlich
- **Mobile Web-Unterstützung** – Die Web-App unterstützt derzeit nur Desktop-Browser. Das bevorstehende Update wird eine vollständige reaktionsfähige Mobilunterstützung bieten, sodass Benutzer Pixiv-OAuth-Tokens direkt von Mobilgeräten aus generieren können, ohne die Desktop-App zu benötigen.

---

## [1.0.4] - 2026-03-29

### 🐞 Behoben
- **Portable CLI/GUI – Versions-Rollback nach dem Update**: `VERSION_FILE` und `CONFIG_FILE` wurden mit `Path(__file__)` aufgelöst, das im eingefrorenen Modus (PyInstaller onefile) auf das temporäre `_MEIPASS`-Verzeichnis verweist – ein Verzeichnis, das beim Schließen der App zerstört wird. Beide Dateien werden jetzt mit `_app_dir()` / `app_dir()` aufgelöst, wodurch korrekt der Ordner zurückgegeben wird, der die eigentliche `.exe` enthält, wodurch sichergestellt wird, dass die Versionsidentität über Neustarts hinweg bestehen bleibt.
- **CLI – Update überschrieb temporäres `.py` anstelle von exe**: Bei der Ausführung als eingefrorene ausführbare Datei überschrieb `_self_update()` das extrahierte `.py` im temporären Verzeichnis, anstatt das tatsächliche `.exe` zu ersetzen. Die Funktion erkennt nun `is_frozen` und lädt die neue ausführbare Datei direkt herunter und ersetzt sie über ein `.bat`-Updater-Skript (gleicher Mechanismus wie die GUI).

### ✨ Hinzugefügt
- **Architekturbewusste automatische Aktualisierung (CLI + GUI)**: Sowohl tragbare als auch Setup-Aktualisierungsabläufe erkennen jetzt die Architektur der ausgeführten ausführbaren Datei (`x64`, `x86`, `ARM64` oder generisch) anhand ihres Dateinamens und laden die genau passende Variante aus dem Ordner `downloads/` herunter, wodurch versehentliche Architekturkonflikte während Aktualisierungen verhindert werden.
- **CLI-Setup-Installer-Aktualisierungsablauf**: CLI spiegelt jetzt das GUI-Verhalten für Setup-Installationen wider – wenn es von `Program Files` ausgeführt wird, lädt es das neueste `.exe`-Setup-Installer herunter und führt es im Hintergrund aus (`/VERYSILENT /NORESTART`), anstatt einen direkten Binäraustausch zu versuchen.

---
## [1.0.3] - 2026-03-26 
### ✨ Geändert
– Standardmäßiges lokales Build-Label von `REL-LOCAL` durch `BUILD-UNKNOWN` für Laufzeit-/Versionstools und generierte Manifeste ersetzt.
- Die GUI enthält jetzt eine Aktion im Hauptmenü **Änderungsprotokoll** und ein Dropdown-Menü **Version** mit explizitem Versionsprüfungseintrag.
– Automatische Startversionsprüfung in der GUI mit Update-Popup-Aktionen (**Update** / **Später**) hinzugefügt, plus Update-Flow-Behandlung für eingefrorene Setup-/tragbare Distributionen.
– Aktualisierte Build-Code-Generierung auf Unix-Stil `REL-U<unix_ms>` bei Versionssprüngen (`patch/minor/major`).

## [1.0.2] - 2026-03-23 
### ✨ Hinzugefügt
- **Debug-Konsole (GUI)**
Eine spezielle `⚙ Debug`-Schaltfläche in der oberen rechten Ecke des GUI-Headers öffnet eine Terminalkonsole mit dunklem Design, die jedes Anwendungsereignis in Echtzeit protokolliert. Zu den erfassten Ereignissen gehören: App-Start, Sprachänderungen, alle Schaltflächenklicks (Anmeldung öffnen, Exchange-Token, Aktualisierungstoken, Zugriffs-/Aktualisierungstoken kopieren, Tutorial), HTTP-Anforderungsstatus (Senden/Erfolg/Fehler), PKCE-Ablaufschritte, Zwischenablagevorgänge, Konfigurationsschreibvorgänge und Warnungen. Alle Debug-Meldungen sind vollständig in allen 11 unterstützten Sprachen lokalisiert. Die Konsole unterstützt das Live-Streaming neuer Nachrichten im geöffneten Zustand, das Vorabfüllen historischer Protokolle ab Sitzungsbeginn, eine Schaltfläche **Alle kopieren** und eine Schaltfläche **Löschen**.

## [1.0.1] - 2026-03-22
### ✨ Hinzugefügt
- **Smart README Cleaner für Veröffentlichungen**
Entfernt beim Kompilieren des verteilbaren `.zip` automatisch Abschnitte der Lokalisierungssprache aus der `__p1__`-Datei und ersetzt interne Links durch absolute GitHub-Links.
- **Unified Dual Installer-Unterstützung**
Das InnoSetup-Builder-Skript generiert jetzt ein einheitliches Installationsprogramm, das Endbenutzer auffordert, optional die eigenständige CLI oder die grafische GUI zu installieren.

### 🐞 Behoben
- **Auflösung des Installationspfads**
Es wurde ein Problem mit kritischen Pfadkonflikten in `make_installer_iss_dual.py` behoben, bei dem `iscc` `app\pixiv_oauth.ico` nicht finden konnte, indem Build-Dateien direkt im konfigurierten `scripts\`-Verzeichnis generiert wurden.

## [1.0.0] - 2026-03-21
### ✨ Hinzugefügt
– Erste eigenständige ausführbare Distributionen (`.exe`), kompiliert für GUI- und CLI-Modi.
– Anfänglich optimierte serverlose Integration, synchronisiert mit Vercel mit automatischer Spracherkennung.
– Extremer JavaScript-Verschleierungspass für Web-Endpunkte hinzugefügt.
