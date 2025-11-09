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

Pour windows
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Installation des dépendances

A la racine du projet, vous pouvez voir qu'il y a deux fichiers disponibles :
- pyproject.toml
- uv.lock

Ces fichiers définissent les dépendances de notre projet et donc les packages que nous devons installer afin que celui tourne
sans soucis.

Si vous ouvrez le fichier `pyproject.toml` vous pouvez voir toutes ces dépendances ainsi que les versions requises dans la section `dependencies`.

Pour créer un environnement virtuel et installer les dépendances avec uv lancez la commande suivante à la racine du projet :

```bash
uv sync
```

Grâce à cette commande et aux environnements virtuels, chaque élève qui suit ce cours a les packages nécessaires avec les
bonnes versions !

## Activation et désactivation de l'environnement virtuel

Avec `uv`, vous pouvez activer l'environnement virtuel de manière traditionnelle :

```bash
source .venv/bin/activate
```

Ou sur Windows :
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


## Suite
Lorsque tout est bon du côté des environnements, vous pouvez passer à la suite en ouvrant le notebook `Part2_Git.ipynb`