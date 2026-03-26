# Journal des modifications

All notable changes to the "Pixiv OAuth Token" toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


---
## [1.0.3] - 2026-03-26 
### ✨ Modifié
- Remplacement de l'étiquette de build locale par défaut de `REL-LOCAL` à `BUILD-UNKNOWN` dans les outils d'exécution/version et les manifestes générés.
- L'interface graphique inclut désormais une action de menu supérieur **Changelog** et une liste déroulante **Version** avec une entrée de vérification de version explicite.
- Ajout d'une vérification automatique de la version de démarrage dans l'interface graphique avec des actions contextuelles de mise à jour (**Mise à jour** / **Plus tard**), ainsi que la gestion du flux de mise à jour pour les configurations gelées/distributions portables.
- Mise à jour de la génération de code de construction vers le style Unix `REL-U<unix_ms>` lors des changements de version (`patch/minor/major`).

## [1.0.2] - 2026-03-23 
### ✨ Ajouté
- **Console de débogage (interface graphique)**
Un bouton `⚙ Debug` dédié dans le coin supérieur droit de l'en-tête de l'interface graphique ouvre une console de terminal au thème sombre qui enregistre chaque événement d'application en temps réel. Les événements capturés incluent : le démarrage de l'application, les changements de langue, tous les clics sur les boutons (ouverture de connexion, jeton d'échange, jeton d'actualisation, copie du jeton d'accès/actualisation, didacticiel), les états des requêtes HTTP (envoi/succès/échec), les étapes du flux PKCE, les opérations du presse-papiers, les écritures de configuration et les avertissements. Tous les messages de débogage sont entièrement localisés dans les 11 langues prises en charge. La console prend en charge la diffusion en direct des nouveaux messages lorsqu'elle est ouverte, le pré-remplissage des journaux historiques depuis le début de la session, un bouton **Copier tout** et un bouton **Effacer**.

## [1.0.1] - 2026-03-22
### ✨ Ajouté
- **Nettoyeur README intelligent pour les versions**
Supprime automatiquement les sections de langue de localisation du fichier `` lors de la compilation du `.zip` distribuable, en remplaçant les liens internes par des liens GitHub absolus.
- **Support unifié pour double installateur**
Le script de création InnoSetup génère désormais un programme d'installation unifié qui invite les utilisateurs finaux à installer éventuellement la CLI autonome ou l'interface graphique graphique.

### 🐞 Corrigé
- **Résolution du chemin de construction du programme d'installation**
Correction d'un problème d'incompatibilité de chemin critique dans `make_installer_iss_dual.py` où `iscc` n'a pas réussi à localiser `app\pixiv_oauth.ico` en générant des fichiers de build directement dans le répertoire `scripts\` configuré.

## [1.0.0] - 2026-03-21
### ✨ Ajouté
- Distributions exécutables autonomes initiales (`.exe`) compilées pour les modes GUI et CLI.
- Intégration sans serveur optimisée initiale synchronisée avec Vercel avec détection automatique de la langue.
- Ajout d'une passe d'obscurcissement JavaScript extrême pour les points de terminaison Web.
