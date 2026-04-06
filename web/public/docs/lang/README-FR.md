<p align="center">
  <img src="../../assets/favicon.svg" width="150" alt="Pixiv OAuth Token Logo">
</p>

<h1 align="center">Pixiv OAuth Token</h1>

<p align="center">
  <a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest"><img src="https://img.shields.io/github/v/release/fatonyahmadfauzi/Pixiv-OAuth-Token?color=success" alt="GitHub release"></a>
  <a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases/latest"><img src="https://img.shields.io/github/downloads/fatonyahmadfauzi/Pixiv-OAuth-Token/total.svg?color=blue" alt="Downloads"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"></a>
  <a href="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/actions/workflows/windows-release.yml"><img src="https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/actions/workflows/windows-release.yml/badge.svg" alt="Windows Build"></a>
</p>

> 🌐 Disponible dans d'autres langues : [English](../../../../README.md) | [Polski](README-PL.md) | [中文](README-ZH.md) | [日本語](README-JP.md) | [Deutsch](README-DE.md) | [Español](README-ES.md) | [Русский](README-RU.md) | [Português](README-PT.md) | [Bahasa Indonesia](README-ID.md) | [한국어](README-KR.md)

---

Une boîte à outils pour générer des jetons Pixiv OAuth en trois modes :

- CLI (`app/pixiv_login.py`)
- GUI (`app/pixiv_login_gui.py`)
- Application Web (`web/public/` + sans serveur API)

## Exigences

- Python 3.11+
- Windows (requis pour les scripts de build `.bat` et le programme d'installation d'Inno Setup)
- Python dépendances de `app/requirements.txt`

## Exécuter à partir des sources

```bash
cd app
python -m pip install -r requirements.txt
python pixiv_login.py
```

Exécutez GUI :

```bash
cd app
python pixiv_login_gui.py
```

### GUI Caractéristiques

| Fonctionnalité | Descriptif |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Multi-langue** | 11 langues — détectées automatiquement à partir de la configuration, commutables en direct via la liste déroulante |
| **⚙ Console de débogage** | Bouton dans l’en-tête en haut à droite ; ouvre un terminal sombre enregistrant **tous** les événements (clics sur les boutons, changements de langue, requêtes HTTP, étapes PKCE, presse-papiers, sauvegardes de configuration, avertissements) en temps réel et dans la langue actuelle |
| **Échange de jetons** | Coller pixiv:// URL ou code brut → échange contre accès + jeton d'actualisation |
| **Actualiser le jeton** | Actualisation en un clic à l'aide du rafraîchissement_token enregistré à partir de la configuration |
| **Copier les jetons** | Copiez instantanément access_token /fresh_token dans le presse-papiers |
| **Tutoriel** | Guide image étape par étape intégré à l'application |

## Construire

### Créez tous les artefacts (CLI + GUI + Installateur + ZIP)

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
- `nogui` (sauter GUI)
- `nopause` (pas de pause à la fin)

Exemple:

```bat
cd scripts
build_all_pro.bat patch noinst nosign
```

### Principaux résultats

- Portable CLI : `dist_portable\Pixiv OAuth CLi (Portable).exe`
- Portable GUI : `dist_gui\Pixiv OAuth GUi (Portable).exe`
- Programme d'installation unifié : `dist_installer\PixivLoginSetup_v<version>.exe` (installe à la fois CLI + GUI)
- Installateur CLI : `dist_installer\Pixiv OAuth CLi Setup_v<version>.exe` (Copie du programme d'installation unifié)
- Installateur GUI : `dist_installer\Pixiv OAuth GUi Setup_v<version>.exe` (Copie du programme d'installation unifié)
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

- Portable GUI : `Pixiv OAuth GUi (Portable).exe`
- Configuration GUI : `Pixiv OAuth GUi Setup_v<version>.exe`
- Portable CLI : `Pixiv OAuth CLi (Portable).exe`
- Configuration CLI : `Pixiv OAuth CLi Setup_v<version>.exe`

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

## Python installer

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
📦 Vous pouvez également consulter les notes de version directement sur la [page des versions GitHub](https://github.com/fatonyahmadfauzi/Pixiv-OAuth-Token/releases).

### Dernier : v1.0.5 (2026-04-03)

**✨ Ajouté**

- **Démarrage GUI Internet-Aware** — Vérification préalable de la connexion intelligente avant de démarrer le GUI, avec surveillance de la connexion à l'exécution en direct.
- **Modaux de documentation natifs GUI** — Les conditions générales, la politique de confidentialité et le journal des modifications sont désormais présentés directement dans des fenêtres contextuelles dynamiques plutôt que de forcer les redirections Web.
- **Localisations complètes des terminaux** — Le tracker GitHub CLI et les pages juridiques sont désormais authentiquement traduites dans les 11 langues prises en charge.

**✨ Modifié et corrigé**

- **Signature de code numérique automatisée** — Tous les exécutables regroupent de manière native une identité auto-signée pour supprimer Windows SmartScreen.
- **Bogue des propriétés de l'installateur** — Les exécutables d'installation diffusent correctement les versions de fichiers `1.0.5.0` strictement dans les en-têtes Windows PE au lieu de définir par défaut des zéros.
- **Esthétique CLI redessinée** — Les bordures des zones d'interface utilisateur ont été supprimées pour un affichage de terminal élégant aligné à gauche.

**🔜 À venir dans la prochaine mise à jour**

- Prise en charge du Web mobile : l'application Web bénéficiera d'une mise en page entièrement réactive pour les navigateurs mobiles.

## Licence

MIT License. Voir `LICENSE`.
