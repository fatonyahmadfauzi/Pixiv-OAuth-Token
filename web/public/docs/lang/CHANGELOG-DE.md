# Änderungsprotokoll

All notable changes to the "Pixiv OAuth Token" toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


---
## [1.0.3] - 2026-03-26 
### ✨ Geändert
– Standardmäßiges lokales Build-Label von `REL-LOCAL` durch `BUILD-UNKNOWN` für Laufzeit-/Versionstools und generierte Manifeste ersetzt.
– Die GUI enthält jetzt eine Aktion im oberen Menü „Änderungsprotokoll“ und ein Dropdown-Menü „Version“ mit explizitem Versionsprüfungseintrag.
– Automatische Startversionsprüfung in der GUI mit Update-Popup-Aktionen (**Update** / **Später**) hinzugefügt, plus Update-Flow-Behandlung für eingefrorene Setup-/tragbare Distributionen.
– Aktualisierte Build-Code-Generierung auf Unix-Stil `REL-U<unix_ms>` bei Versionssprüngen (`patch/minor/major`).

## [1.0.2] - 2026-03-23 
### ✨ Hinzugefügt
- **Debug-Konsole (GUI)**
Eine spezielle `⚙ Debug`-Schaltfläche in der oberen rechten Ecke des GUI-Headers öffnet eine Terminalkonsole mit dunklem Design, die jedes Anwendungsereignis in Echtzeit protokolliert. Zu den erfassten Ereignissen gehören: App-Start, Sprachänderungen, alle Schaltflächenklicks (Anmeldung öffnen, Exchange-Token, Aktualisierungstoken, Zugriffs-/Aktualisierungstoken kopieren, Tutorial), HTTP-Anforderungsstatus (Senden/Erfolg/Fehler), PKCE-Ablaufschritte, Zwischenablagevorgänge, Konfigurationsschreibvorgänge und Warnungen. Alle Debug-Meldungen sind vollständig in allen 11 unterstützten Sprachen lokalisiert. Die Konsole unterstützt das Live-Streaming neuer Nachrichten im geöffneten Zustand, das Vorabfüllen historischer Protokolle ab Sitzungsbeginn, eine Schaltfläche **Alle kopieren** und eine Schaltfläche **Löschen**.

## [1.0.1] - 2026-03-22
### ✨ Hinzugefügt
- **Smart README Cleaner für Veröffentlichungen**
Entfernt beim Kompilieren des verteilbaren `.zip` automatisch Abschnitte der Lokalisierungssprache aus der ``-Datei und ersetzt interne Links durch absolute GitHub-Links.
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
