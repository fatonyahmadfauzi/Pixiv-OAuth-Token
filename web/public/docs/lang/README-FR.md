# Pixiv OAuth Token

> 🌐 Disponible dans d'autres langues : [English](../../../../README.md) | [Polski](README-PL.md) | [中文](README-ZH.md) | [日本語](README-JP.md) | [Deutsch](README-DE.md) | [Español](README-ES.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [Bahasa Indonesia](README-ID.md) | [한국어](README-KR.md)

---

Une boîte à outils pour générer des jetons Pixiv OAuth dans trois modes :

- CLI (`app/pixiv_login.py`)
- Interface graphique (`app/pixiv_login_gui.py`)
- Application Web (`web/public/` + sans serveur API)

## Exigences

- Python 3.11+
- Windows (requis pour les scripts de build `.bat` et le programme d'installation d'Inno Setup)
- Dépendances Python de `app/requirements.txt`

## Exécuter à partir des sources

```bash
cd app
python -m pip install -r requirements.txt
python pixiv_login.py
```

Exécutez l'interface graphique :

```bash
cd app
python pixiv_login_gui.py
```

### Fonctionnalités de l'interface graphique

| Fonctionnalité            | Descriptif                                                                                                                                                                                                                                                                               |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Multi-langue**          | 11 langues — détectées automatiquement à partir de la configuration, commutables en direct via la liste déroulante                                                                                                                                                                       |
| **⚙ Console de débogage** | Bouton dans l’en-tête en haut à droite ; ouvre un terminal sombre enregistrant **tous** les événements (clics sur les boutons, changements de langue, requêtes HTTP, étapes PKCE, presse-papiers, sauvegardes de configuration, avertissements) en temps réel et dans la langue actuelle |
| **Échange de jetons**     | Coller pixiv:// URL ou code brut → échange contre accès + jeton d'actualisation                                                                                                                                                                                                          |
| **Actualiser le jeton**   | Actualisation en un clic à l'aide du rafraîchissement_token enregistré à partir de la configuration                                                                                                                                                                                      |
| **Copier les jetons**     | Copiez instantanément access_token /fresh_token dans le presse-papiers                                                                                                                                                                                                                   |
| **Tutoriel**              | Guide image étape par étape intégré à l'application                                                                                                                                                                                                                                      |

## Construire

### Construisez tous les artefacts (CLI + GUI + Installer + ZIP)

```bat
cd scripts
build_all_pro.bat patch
```

Argument de version :

- `patch`
- `minor`
- `major`
- `none`

Indicateurs facultatifs :

- `noinst` (ignorer l'installateur)
- `nosign` (ignorer la signature)
- `nozip` (ignorer le zip)
- `nogui` (ignorer l'interface graphique)
- `nopause` (pas de pause à la fin)

Exemple:

```bat
cd scripts
build_all_pro.bat patch noinst nosign
```

### Principaux résultats

- CLI portable : `dist_portable\Pixiv OAuth CLi (Portable).exe`
- Interface graphique portable : `dist_gui\Pixiv OAuth GUi (Portable).exe`
- Programme d'installation unifié : `dist_installer\PixivLoginSetup_v<version>.exe` (installe à la fois CLI + GUI)
- CLI du programme d'installation : `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe` (Copie du programme d'installation unifié)
- Interface graphique du programme d'installation : `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe` (copie du programme d'installation unifié)
- Version ZIP : `PixivOAuthRelease_v<version>.zip`
- Dossier synchronisé automatiquement : `downloads/` (dernier portable/configuration + version ZIP)

## Signature

Modifier `scripts/sign_auto.bat` :

- `PFX_PATH`
- `PFX_PASS`
- `TS_URL`

Si le fichier PFX est manquant, la signature est ignorée.

## Gestion des versions

L’identité de version/build de l’application est stockée dans `version.json`.

- `version` : version sémantique (`X.Y.Z`)
- `build_code` : identifiant de build unique

La solution de secours par défaut non publiée est désormais `BUILD-UNKNOWN` (au lieu de `REL-LOCAL`), tandis que les modifications de version génèrent des codes de construction de style Unix via `scripts/bump_version.py` :

- `REL-U<unix_ms>`

## Version Web (Vercel)

Une application Web hautement optimisée et réactive offrant une prise en charge multilingue dynamique (11 langues avec détection automatique) et des métadonnées SEO complètes.

### Principales fonctionnalités Web

- **Pages étendues** : page d'accueil, téléchargements, didacticiel, contact, problèmes et relations publiques, suivi des discussions, visionneuse de documentation Markdown et intégration support/don.
- **Référencement avancé** : balises `<meta>` localisées automatiquement injectées, données structurées JSON-LD étendues (liens annexes, application logicielle, etc.), génération automatisée de `hreflang`, `robots.txt` et `sitemap.xml`.
- **Sécurité et performances** : obscurcissement automatique de JavaScript (modification extrême), minification HTML/CSS (via `cd web && node build_minify.js`) et prévention propre `XSS` via `escapeHTML`.
- **GitHub API Proxy** : les points de terminaison Vercel sans serveur (`/api/github`) proxy GitHub API requêtes utilisant un jeton d'accès personnel (`GITHUB_PAT`) pour contourner complètement les limites de débit publiques.

### Déployer sur Vercel

1. Poussez le référentiel vers GitHub.
2. Vercel → **Ajouter un nouveau...** → **Projet** → importer ce dépôt.
3. Définissez vos variables d'environnement dans Vercel :

- `PIXIV_CLIENT_SECRET` : Votre secret client Pixiv OAuth.
- `GITHUB_PAT` : facultatif mais fortement recommandé (votre jeton d'accès personnel GitHub pour éviter les limites de taux sur les problèmes et les versions de repo).

4. `vercel.json` configure déjà :

- Nettoyer les URL (suppression de `.html`)
- Hébergement statique à partir de `public/`
- API sans serveur à `/api/*`
- Routage de pages 404 personnalisé intégré
- Mise en cache dans un futur lointain via les en-têtes Edge Cache.

5. Déployez.

> [!IMPORTANT]
> Si vous apportez des modifications au HTML, CSS ou JS, n'oubliez pas d'exécuter `cd web && node build_minify.js` avant le déploiement pour obscurcir automatiquement le code et compresser les ressources.

> Note de sécurité : pour la production, définissez toujours `PIXIV_CLIENT_SECRET` dans les variables d'environnement de votre projet Vercel.

## Télécharger l'application (dernière version)

URL de base :

`https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest/download`

Fichiers :

- Interface graphique portable : `Pixiv OAuth GUi (Portable).exe`
- Interface graphique de configuration : `Pixiv OAuth GUi Setup_v<version>.exe`
- CLI portable : `Pixiv OAuth CLi (Portable).exe`
- CLI d'installation : `Pixiv OAuth CLi Setup_v<version>.exe`

### PowerShell (détection automatique des ressources de la dernière version)

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

### PowerShell (URL corrigées de `downloads/`)

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

Exécutez-le dans **PowerShell** (pas CMD).

Si vous exécutez seulement :

```powershell
$guiPortable = "..."
```

et rien n'apparaît, c'est prévu. Il stocke uniquement une valeur dans une variable. Le téléchargement démarre lorsque vous exécutez `Invoke-WebRequest`.

Une fois le téléchargement terminé et PowerShell revient à `PS C:\...>` sans erreur :

```powershell
Get-ChildItem "Pixiv OAuth GUi (Portable).exe"
Start-Process ".\Pixiv OAuth GUi (Portable).exe"
```

Pour la version d'installation :

```powershell
Invoke-WebRequest $guiSetup -OutFile "Pixiv OAuth GUi Setup.exe"
Start-Process ".\Pixiv OAuth GUi Setup.exe"
```

Si la stratégie TLS bloque le téléchargement :

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

### CMD (détection automatique des ressources de la dernière version)

```cmd
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi \(Portable\)''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi (Portable).exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth GUi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth GUi Setup.exe"
for /f "delims=" %u in ('powershell -NoProfile -Command "$r=Invoke-RestMethod https://api.github.com/repos/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest; ($r.assets|? name -match ''Pixiv OAuth CLi Setup''|select -first 1).browser_download_url"') do curl -L "%u" -o "Pixiv OAuth CLi Setup.exe"
```

## Installation de Python

```bash
cd app
python -m pip install -r requirements.txt
```

Ou installez directement depuis GitHub :

```bash
python -m pip install "git+https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token.git"
```

## 🧾 Journal des modifications

Consultez tous les changements notables pour chaque version dans le fichier [Journal des modifications](CHANGELOG-FR.md).
📦 Vous pouvez également consulter les notes de version directement sur la [GitHub page Releases](https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases).

### Dernier : v1.0.4 (2026-03-29)

**🐞 Corrigé**

- CLI/GUI portable : la version ne revient plus à l'ancienne version après la mise à jour — `VERSION_FILE` / `CONFIG_FILE` sont désormais correctement enregistrés à côté du `.exe` au lieu du dossier d'extraction temporaire de PyInstaller.
- Mise à jour gelée de la CLI : remplace désormais correctement le `.exe` réel via un script de mise à jour `.bat` au lieu d'écraser un fichier temporaire.

**✨ Ajouté**

- **Mise à jour tenant compte de l'architecture** — la CLI et l'interface graphique détectent désormais automatiquement l'architecture en cours d'exécution (`x64`, `x86`, `ARM64`) et téléchargent la variante de construction correspondante lors de la mise à jour.
- **Flux de mise à jour de la configuration CLI** — La CLI exécute désormais silencieusement le programme d'installation lors de la mise à jour à partir d'une installation `Program Files` (reflète le comportement de l'interface graphique).

**🔜 À venir dans la prochaine mise à jour**

- Prise en charge du Web mobile : l'application Web bénéficiera d'une mise en page entièrement réactive pour les navigateurs mobiles.

## Licence

MIT License. Voir `LICENSE`.
