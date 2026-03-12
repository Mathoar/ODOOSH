# Projet Odoo.sh - Odoo 19.0

Dépôt de modules personnalisés pour Odoo.sh.

## Structure du dépôt

```
/
├── .gitignore
├── requirements.txt          # Dépendances Python supplémentaires
├── README.md
└── my_custom_module/          # Exemple de module personnalisé
    ├── __manifest__.py
    ├── __init__.py
    ├── models/
    ├── views/
    ├── security/
    ├── data/
    └── static/description/
```

Chaque dossier à la racine contenant un fichier `__manifest__.py` est automatiquement détecté comme module Odoo par Odoo.sh.

## Guide de mise en place Odoo.sh

### Prérequis

- Un compte Odoo.sh (https://www.odoo.sh)
- Un compte GitHub avec ce dépôt
- Un abonnement Odoo Enterprise (Odoo.sh nécessite une licence Enterprise)

### Étape 1 : Lier le dépôt à Odoo.sh

1. Connectez-vous sur **https://www.odoo.sh**
2. Cliquez sur **"Create a project"** (ou "Créer un projet")
3. Autorisez Odoo.sh à accéder à votre compte GitHub
4. Sélectionnez ce dépôt dans la liste
5. Choisissez la version **Odoo 19.0**
6. Odoo.sh va automatiquement créer votre premier build

### Étape 2 : Comprendre les branches

Odoo.sh utilise un système de branches Git avec 3 niveaux :

| Type de branche | Rôle | Exemple |
|----------------|------|---------|
| **Production** | Instance live, données réelles | `main` |
| **Staging** | Tests avant mise en production | `staging`, `preprod` |
| **Développement** | Développement et tests | `dev-*`, `feature-*` |

- **Production** : La branche `main` (ou `master`). Chaque push déclenche un rebuild.
- **Staging** : Créez des branches de staging depuis l'interface Odoo.sh pour tester avec une copie des données de production.
- **Développement** : Toute autre branche crée un environnement de développement isolé.

### Étape 3 : Workflow de développement

```bash
# 1. Créer une branche de développement
git checkout -b dev-ma-feature

# 2. Développer votre module
# (créer/modifier les fichiers)

# 3. Commiter et pousser
git add .
git commit -m "feat: ajout de mon nouveau module"
git push origin dev-ma-feature

# 4. Odoo.sh crée automatiquement un build de développement

# 5. Tester sur l'environnement de développement via Odoo.sh

# 6. Merger vers staging pour tests avancés
git checkout staging
git merge dev-ma-feature
git push origin staging

# 7. Merger vers main pour la production
git checkout main
git merge staging
git push origin main
```

### Étape 4 : Ajouter un nouveau module

1. Créez un dossier à la racine du dépôt avec le nom de votre module
2. Ajoutez les fichiers obligatoires :
   - `__manifest__.py` : métadonnées du module
   - `__init__.py` : imports Python
3. Développez votre module (models, views, security, etc.)
4. Commitez et poussez

### Fichiers spéciaux reconnus par Odoo.sh

| Fichier | Rôle |
|---------|------|
| `requirements.txt` | Dépendances Python installées au build |
| `oca_dependencies.txt` | Modules OCA à récupérer automatiquement |
| `.submodules` | Sous-modules Git (modules tiers) |
| `Dockerfile` | Personnalisation de l'image Docker (avancé) |

### Ajouter des modules OCA (plus tard)

Pour utiliser des modules de l'Odoo Community Association :

1. Créez un fichier `oca_dependencies.txt` à la racine :
```
# Format : nom_du_repo version
server-tools 19.0
web 19.0
```

2. Ou utilisez des sous-modules Git :
```bash
git submodule add -b 19.0 https://github.com/OCA/server-tools.git oca/server-tools
```

### Accéder au shell / logs

Depuis l'interface Odoo.sh :
- **Shell** : Onglet "Shell" pour accéder au terminal
- **Logs** : Onglet "Logs" pour voir les logs du serveur Odoo
- **Éditeur** : Onglet "Editor" pour éditer directement les fichiers en ligne

### Commandes utiles dans le shell Odoo.sh

```bash
# Mettre à jour un module
odoo-bin -u my_custom_module -d <database>

# Installer un module
odoo-bin -i my_custom_module -d <database>

# Voir les logs en temps réel
tail -f /var/log/odoo/odoo-server.log
```

## Développement local (optionnel)

Pour développer en local avant de pousser sur Odoo.sh :

```bash
# Cloner le dépôt
git clone <url-du-depot>
cd ODOOSH

# Installer Odoo 19.0 localement (Docker)
docker run -d -p 8069:8069 --name odoo19 \
  -v $(pwd):/mnt/extra-addons \
  odoo:19.0

# Accéder à Odoo : http://localhost:8069
```

## Support

- Documentation Odoo.sh : https://www.odoo.com/documentation/19.0/administration/odoo_sh.html
- Documentation développeur : https://www.odoo.com/documentation/19.0/developer.html
- Forum communautaire : https://www.odoo.com/forum
