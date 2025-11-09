# Les environnements virtuels en Python

## Qu'est-ce qu'un environnement virtuel ?

Un **environnement virtuel** est un espace isolé qui permet de gérer des dépendances de projets spécifiques sans interférer
avec d'autres projets ou avec l'environnement Python global de votre système. 

## Pourquoi utiliser un environnement virtuel ?
- **Isolation** : Éviter les conflits de versions entre les packages utilisées dans différents projets.
- **Facilité de gestion** : Travailler avec des dépendances spécifiques pour chaque projet.
- **Portabilité** : Permettre aux autres développeurs de répliquer facilement l'environnement de votre projet et ayant
exactement les mêmes package et version d'installés.

![image venv](images/python-virtual-envs.png)

En résumé, un environnement virtuel vous permet de :
1. Utiliser différentes versions de pacakge dans différents projets.
2. Garder l'environnement global propre en installant les dépendances uniquement dans le projet en cours.

# Utilisation de `uv` pour gérer les environnements virtuels

`uv` est un outil moderne et extrêmement rapide pour gérer les environnements virtuels et les dépendances des projets Python.
Il est écrit en Rust et offre des performances bien supérieures aux outils traditionnels comme pip et pipenv.

`uv` est développé par Astral, l'équipe derrière ruff, vous pouvez accéder à la documentation de uv ici https://docs.astral.sh/uv/

## Installation de `uv`
Pour installer `uv`, exécutez la commande suivante :

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Ou sur macOS avec Homebrew :
```bash
brew install uv
```

Pour windows: ⚠️ lancez powershell en mode administrateur ou VS code en mode admin en fonction de ce que vous utilisez (VS code conseillé)
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Pour la suite de toute l'unité, si vous êtes sur windows, utilisez seulement powershell ou VS code en mode admin pour les installations 

## Installation de Python 3.12

Une fois `uv` installé, vous devez installer Python 3.12 pour ce projet. `uv` peut gérer l'installation de Python automatiquement :

```bash
uv python install 3.12
```

Cette commande va télécharger et installer Python 3.12 si vous ne l'avez pas déjà sur votre système. `uv` gère les versions de Python de manière isolée, ce qui permet d'avoir plusieurs versions de Python sur votre machine sans conflit.

Pour vérifier que Python 3.12 est bien installé :

```bash
uv python list
```

Cette commande affiche toutes les versions de Python disponibles sur votre système.

## Installation des dépendances

A la racine du projet, vous pouvez voir qu'il y a trois fichiers disponibles :
- `.python-version` : spécifie la version de Python à utiliser (3.12)
- `pyproject.toml` : contient les métadonnées du projet et la liste des dépendances
- `uv.lock` : fichier de verrouillage qui garantit que tout le monde utilise exactement les mêmes versions de packages

Ces fichiers définissent les dépendances de notre projet et donc les packages que nous devons installer afin que celui tourne
sans soucis.

Si vous ouvrez le fichier `pyproject.toml` vous pouvez voir toutes ces dépendances ainsi que les versions requises dans la section `dependencies`.

Pour créer un environnement virtuel et installer les dépendances avec uv lancez la commande suivante à la racine du projet :

```bash
uv sync
```

Cette commande va :
1. Détecter la version de Python requise (3.12) grâce au fichier `.python-version`
2. Créer automatiquement un environnement virtuel dans le dossier `.venv/`
3. Installer toutes les dépendances listées dans `pyproject.toml`

Grâce à cette commande et aux environnements virtuels, chaque élève qui suit ce cours a les packages nécessaires avec les
bonnes versions !

## Activation et désactivation de l'environnement virtuel

Avec `uv`, vous pouvez activer l'environnement virtuel de manière traditionnelle :

```bash
source .venv/bin/activate
```

Ou sur Windows :
commencez par activer l'execution de script:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
ensuite activez le venv
```bash
.venv\Scripts\activate
```

Selon votre OS, vous devriez voir que votre terminal a changé et affiche désormais le nom de l'environnement virtuel au
début de la ligne
```bash
(.venv) user>
```

Vous pouvez aussi vérifier que le chemin de l'éxecutable python est bien celui de l'environnement virtuel : 
```bash
which python
```

Pour désactiver l'environnement : 
```bash
deactivate
```

Alternativement, `uv` permet d'exécuter des commandes directement dans l'environnement virtuel sans activation :
```bash
uv run python mon_script.py
```

## Installer des packages dans votre environnement virtuel

Au cours du projet, si vous avez besoin d'installer un package dans votre env, il vous suffit de faire : 
```bash
uv add <nom_du_package>
```

Celui-ci sera alors automatiquement ajouté au fichier pyproject.toml et installé dans votre environnement


Lorsque vous travaillez sur le projet faites bien attention à avoir votre environnement virtuel d'activé afin d'éviter les
problèmes de dépendances !

## Utilisation avec Jupyter Notebook

⚠️ **Important** : Lorsque vous travaillez avec des Jupyter Notebooks dans ce cours, vous devez :

1. **Activer votre environnement virtuel** avant de lancer Jupyter (normalement déjà fait avec les étapes précédentes) :

```bash
source .venv/bin/activate  # Sur macOS/Linux
# ou
.venv\Scripts\activate     # Sur Windows
```

Ou utilisez directement :

```bash
uv run jupyter notebook
```

Sur Windows il est vivement conseillé de faire tourner les notebook avec VS code

Si vous lancer les notebook depuis powershell et que vous avez une erreur sur votte browser, copié coller le lien localhost que la commande vous a donné

2. **Sélectionner le bon kernel** dans le notebook :
   - Une fois le notebook ouvert, regardez en haut à droite de la page
   - Vous devriez voir le nom du kernel Python utilisé (exemple : "Python 3.12")
   - Cliquez dessus pour vérifier ou changer le kernel
   - Assurez-vous de sélectionner le kernel correspondant à votre environnement virtuel `.venv` ou le nom du notebook

Si vous ne voyez pas votre environnement virtuel dans la liste des kernels disponibles, vous pouvez l'ajouter avec :

```bash
uv run python -m ipykernel install --user --name=dataengineer --display-name="Python (DataEngineer)"
```

Cette commande créera un kernel nommé "Python (DataEngineer)" que vous pourrez sélectionner dans vos notebooks.

## Suite
Lorsque tout est bon du côté des environnements, vous pouvez passer à la suite en ouvrant le notebook `Part2_Git.ipynb`