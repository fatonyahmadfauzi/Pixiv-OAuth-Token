# Journal des modifications

All notable changes to the "Pixiv OAuth Token" toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🔜 Coming Soon

- **Mobile Web Support** — The web app currently only supports desktop browsers. Upcoming update will bring full responsive mobile support, allowing users to generate Pixiv OAuth tokens directly from mobile devices without needing the desktop app.


---

## [1.0.5] - 2026-04-03

### ✨ Ajouté

- **Démarrage GUI compatible Internet**
Avant de lancer la fenêtre principale GUI, un écran de démarrage intelligent `NetLoadingScreen` effectue désormais une vérification de la connectivité Internet avant le vol. Si aucune connexion n'est trouvée, il réessaye en toute sécurité en arrière-plan jusqu'à ce qu'il soit connecté. De plus, un moniteur d'exécution actif affichera une alerte revenant à l'écran de chargement si la connexion est interrompue à mi-chemin pendant l'utilisation.
- **Modaux de documentation natifs GUI**
Remplacement des redirections du navigateur externe pour la documentation critique. **Changelog**, **Terms & Conditions** et **Politique de confidentialité** sont désormais affichés dans des fenêtres de dialogue `tkinter` natives, dynamiques et propres (récupérées de manière asynchrone directement à partir du dépôt GitHub).
- **Localisations complètes des terminaux**
L'interface interactive GitHub CLI (navigation des problèmes) et toutes les mises en page juridiques/support basées sur le terminal sont désormais authentiquement localisées dans les 11 langues prises en charge.

### ✨ Modifié

- **Esthétique CLI repensée**
Suppression des bordures de boîtes décoratives héritées pour un affichage de terminal nettement plus propre, modernisé et aligné à gauche.
- **Signature de code numérique automatisée**
Amélioration substantielle du pipeline `sign_auto.bat`. Le script découvre désormais automatiquement `signtool.exe` de manière dynamique au sein du SDK Windows, appliquant sans effort le certificat auto-signé simultanément à toutes les versions générées (y compris les configurations du programme d'installation et les alias de téléchargement `_latest`) pour supprimer les indicateurs de base « Éditeur inconnu » de SmartScreen.

### 🐞 Corrigé

- **Bogue des propriétés de l'installateur**
Correction d'une anomalie où le programme d'installation `Setup.exe` affichait `0.0.0.0` dans les propriétés Windows. Le constructeur injecte désormais correctement les en-têtes PE stricts `VersionInfoVersion` lors de la compilation pour refléter le numéro de version correspondant exactement (e.g., 1.0.5.0) immédiatement après le rendu.

---

## [1.0.4] - 2026-03-29

### 🐞 Corrigé

- **Portable CLI/GUI — Restauration de la version après la mise à jour** : `VERSION_FILE` et `CONFIG_FILE` ont été résolus à l'aide de `Path(__file__)`, qui en mode gelé (PyInstaller onefile) pointe vers le répertoire temporaire `_MEIPASS` — un répertoire qui est détruit à la fermeture de l'application. Les deux fichiers sont désormais résolus à l'aide de `_app_dir()` / `app_dir()` qui renvoie correctement le dossier contenant le `.exe` réel, garantissant ainsi la persistance de l'identité de la version lors des redémarrages.
- **CLI — La mise à jour a écrasé temp `.py` au lieu de exe** : lors de l'exécution en tant qu'exécutable gelé, `_self_update()` écrasait le `.py` extrait dans le répertoire temporaire au lieu de remplacer le `.exe` réel. La fonction détecte désormais `is_frozen` et télécharge directement le nouvel exécutable, en le remplaçant via un script de mise à jour `.bat` (même mécanisme que le GUI).

### ✨ Ajouté

- **Mise à jour automatique tenant compte de l'architecture (CLI + GUI)** : les flux de mise à jour portables et de configuration détectent désormais l'architecture de l'exécutable en cours d'exécution (`x64`, `x86`, `ARM64` ou générique) à partir de son nom de fichier et téléchargent la variante correspondante exacte à partir du dossier `downloads/`, évitant ainsi les incompatibilités accidentelles d'architecture lors des mises à jour.
- **CLI flux de mise à jour du programme d'installation de l'installation** : CLI reflète désormais le comportement de GUI pour les installations d'installation : lors de l'exécution à partir de `Program Files`, il télécharge le dernier programme d'installation de l'installation `.exe` et l'exécute en mode silencieux (`/VERYSILENT /NORESTART`) au lieu de tenter un échange binaire sur place.

---

## [1.0.3] - 2026-03-26

### ✨ Modifié

- Remplacement de l'étiquette de build locale par défaut de `REL-LOCAL` à `BUILD-UNKNOWN` dans les outils d'exécution/version et les manifestes générés.
- GUI inclut désormais une action **Changelog** dans le menu supérieur et une liste déroulante **Version** avec une entrée explicite de vérification de version.
- Ajout de la vérification automatique de la version de démarrage dans GUI avec des actions contextuelles de mise à jour (**Mise à jour** / **Plus tard**), ainsi que la gestion du flux de mise à jour pour les configurations gelées/distributions portables.
- Mise à jour de la génération de code de construction vers le style Unix `REL-U<unix_ms>` lors des changements de version (`patch/minor/major`).

## [1.0.2] - 2026-03-23

### ✨ Ajouté

- **Console de débogage (GUI)**
Un bouton `⚙ Debug` dédié dans le coin supérieur droit de l'en-tête GUI ouvre une console de terminal au thème sombre qui enregistre chaque événement d'application en temps réel. Les événements capturés incluent : le démarrage de l'application, les changements de langue, tous les clics sur les boutons (ouverture de connexion, jeton d'échange, jeton d'actualisation, copie du jeton d'accès/actualisation, didacticiel), les états des requêtes HTTP (envoi/succès/échec), les étapes du flux PKCE, les opérations du presse-papiers, les écritures de configuration et les avertissements. Tous les messages de débogage sont entièrement localisés dans les 11 langues prises en charge. La console prend en charge la diffusion en direct des nouveaux messages lorsqu'elle est ouverte, le pré-remplissage des journaux historiques depuis le début de la session, un bouton **Copier tout** et un bouton **Effacer**.

## [1.0.1] - 2026-03-22

### ✨ Ajouté

- **Nettoyeur README intelligent pour les versions**
Supprime automatiquement les sections de langue de localisation du fichier `` lors de la compilation du `.zip` distribuable, en remplaçant les liens internes par des liens GitHub absolus.
- **Support unifié pour double installateur**
Le script de création InnoSetup génère désormais un programme d'installation unifié qui invite les utilisateurs finaux à installer éventuellement le CLI autonome ou le GUI graphique.

### 🐞 Corrigé

- **Résolution du chemin de construction du programme d'installation**
Correction d'un problème d'incompatibilité de chemin critique dans `make_installer_iss_dual.py` où `iscc` n'a pas réussi à localiser `app\pixiv_oauth.ico` en générant des fichiers de build directement dans le répertoire `scripts\` configuré.

## [1.0.0] - 2026-03-21

### ✨ Ajouté

- Distributions exécutables autonomes initiales (`.exe`) compilées pour les modes GUI et CLI.
- Intégration sans serveur optimisée initiale synchronisée avec Vercel avec détection automatique de la langue.
- Ajout d'une passe d'obscurcissement JavaScript extrême pour les points de terminaison Web.
