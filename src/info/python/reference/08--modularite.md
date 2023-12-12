//// title = "Modularité"
//// description = "L'organisation en modules et packages en Python"

# {=title}

Il est très facile de diviser son code en modules en Python, et c'est l'un des meilleurs moyens d'organiser ses projets. Séparer son code en modules permet d'avoir un projet mieux organisé, où on s'y retrouve mieux, ça évite de devoir naviguer constamment dans un fichier de 3400 lignes, et ça rend des éléments réutilisables.

## Créer et importer un module

Pour ça rien de plus simple : séparez juste le code de façon à peu près logique, puis il suffit d'importer le module et d'utiliser son contenu. Le contenu global du module est accessible comme n'importe quel autre du moment qu'il est trouvable (dans le même répertoire en général).

Par exemple, pour un jeu de la vie un peu minimaliste, plutôt que de tout bourrer au même endroit, on peut faire un module d'interface et un module qui s'occupe de la simulation, comme ça c'est mieux organisé et on peut relier différentes interfaces dessus sans avoir à changer le module de simulation

;;; code
__**`life.py`**__

```python/keep/name="life.py"; next=1
"""
Fonctions permettant la simulation du jeu de la vie
Ce fichier sera importé comme un module
Comme le fichier s'appelle `life.py`, il sera importé avec `import life`
(ou `from life import create_grid, next_turn`)
"""

import numpy as np

def create_grid(width, height, prob_alive):
    return np.random.rand(width, height) < prob_alive

def next_turn(grid):
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            neighbors = grid[x-1:x+2, y-1:y+2].flatten()
            cell_alive = grid[x, y]
            live_neighbors = neighbors.sum() - cell_alive
            grid[x, y] = (live_neighbors == 3 or (cell_alive and live_neighbors == 2))
```
;;; code
__**`main.py`**__

```python/result/stdin="12\n12\n0.25\n\n\n\n\nq\n"
# On importe notre module par son nom
import life

def print_grid(grid):
    print("")
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            print("O" if grid[x, y] else "-", end=" ")
        print("")

# Le `if __name__ == "__main__"` permet de distinguer l'utilisation comme module ou comme script
# Par exemple, un autre script pourrait vouloir réutiliser la fonction `print_grid` qui est ici.
# Sans ça, ce serait impossible d'importer ce module car ça lancerait immédiatement le jeu de la
# vie. Mais avec ça, ça ne l'exécutera que si le script est exécuté directement et pas importé.
if __name__ == "__main__":
    width = int(input("Width of the grid : "))
    height = int(input("Height of the grid : "))
    initial_probability = float(input("Probability of each cell being initially alive : "))

    # On peut utiliser ce que contient notre module comme on veut
    grid = life.create_grid(width, height, initial_probability)
    while True:
        print_grid(grid)
        if input("Enter to continue, q to quit : ").strip().lower() == "q":
            break
        else:
            life.next_turn(grid)
```
;;;

## Créer et importer un package

Ce qu'on appelle un *package* en Python, c'est un regroupement de modules, qui permet un (ou plusieurs !) niveau d'organisation en plus. Ce n'est pas rare que pour un gros projet, il y ait plusieurs grandes parties du programme, et mettre les modules des différentes parties au même endroit n'a pas grand sens.

Pour ça, il suffit de regrouper les modules dans des répertoires séparés. Par exemple, on peut imaginer une organisation comme ceci :

- DS50_preprocessing/
    - pipeline/
        - database.py
        - filter.py
        - final.py
        - review.py
        - tag.py
        - user.py
    - util/
        - data.py
        - pipeline.py
        - tag.py
    - preprocess.py

D'ailleurs, dans des grandes librairies, il n'est pas rare d'avoir des packages contenant des sous-packages, voire des sous-sous-packages.
Pour importer un module d'un package, on sépare le nom du package et le nom du module d'un point. On peut aussi importer directement un module d'un package.

;;; code ```python
# Le plus propre en théorie, mais peut pas mal alourdir le code
import package.module      # Import
package.module.fonction()  # Utilisation```
;;; code ```python
# Du moment qu'il n'y a pas d'ambiguïté de nom ou d'origine
from package import module  # Import
module.fonction()           # Utilisation```
;;; code ```python
# Pareil
from package.module import fonction  # Import
fonction()                           # Utilisation```
;;;

Dans un module **à l'intérieur du package**, il est possible d'importer des choses des autres modules du même package avec `.module`

;;; code ```python
from . import module
module.fonction()```
;;; code ```python
from .module import fonction
fonction()```
;;;

Quand le module est dans un sous-package, il est aussi possible de remonter dans l'arborescence avec `..`
Mettons qu'on a ceci :

- package/
    - souspackage1/
        - sousmodule1.py
        - sousmodule2.py
    - souspackage2/
        - sousmodule3.py
    - module.py

Alors `sousmodule1.py` peut importer les autres modules comme ceci :

;;; code ```python
# Pour importer les modules avec leur nom
from . import sousmodule2
from .. import module
from ..souspackage2 import sousmodule3```
;;; code ```python
# Pour importer du contenu du module
from .sousmodule2 import Contenu1, Contenu2
from ..module import Contenu3
from ..souspackage2.sousmodule3 import Contenu4```
;;;

### Initialisation du package

Traditionnellement, un *package* Python doit contenir un fichier appelé `__init__.py`. En Python moderne il n'est plus obligatoire, mais il peut servir quand même. En gros, le fichier `__init__.py` contient ce qui est importé quand on fait simplement `import package`, sans importer un module en particulier dans le package.

Quand `__init__.py` n'existe pas ou s'il est vide, `import package` importera juste un module vide (vous ne pouvez pas utiliser `package.module.fonction()` en ayant juste utilisé `import package`).

Il y a plusieurs possibilités d'utilisation de `__init__.py` (qui ne sont pas mutuellement exclusives) :

- Mettre des éléments génériques du package. Dans les librairies qu'on distribue, on met traditionnellement une constante `__version__` qui rend accessible le numéro de version de la librairie depuis le code par exemple. Vous pouvez y mettre ce que vous voulez, c'est comme un module normal.
- Importer les différents modules du package pour les rendre utilisables par `package.module.contenu` avec seulement `import package` (c'est par exemple ce que font numpy ou Pygame). Attention cependant, si le package est un peu lourd, ça prendra du temps et de la mémoire pour charger beaucoup de contenu inutile.
- Importer directement tout le contenu des modules avec `from .module import *` ou `from .module import contenu1, contenu2, …` pour chaque module du package. Ça fera que le package se comportera comme un module normal, avec tout son contenu simplement avec `import package`. Ça permet d'organiser le code du package sans forcer des séparations logiques pour les programmeurs, ce qui peut être pratique pour de petits packages cohérents, ou des librairies qui exposent peu de contenu au programmeur mais qui ont besoin de beaucoup de code en interne pour fonctionner.
