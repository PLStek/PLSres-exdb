//// title = "Introduction"
//// description = "Introduction au langage Python"

# {=title}

De nos jours, Python est l'un des langages de programmation les plus populaires ([comme peuvent en témoigner](https://insights.stackoverflow.com/survey/2021#most-loved-dreaded-and-wanted-language-want) les [derniers récaps de StackOverflow](https://insights.stackoverflow.com/survey/2021#technology-most-popular-technologies)).

Python est un langage assez différent de ce que vous voyez en cours en TC :

- C'est un langage très, **très haut niveau**. En fait un des plus haut niveau dans les paradigmes « classiques » (c'est-à-dire tant qu'on ne part pas dans du pur déclaratif comme Prolog ou SQL). Il a donc des **fonctionnalités très avancées** et de très **fortes abstractions**, ce qui **facilite et accélère énormément la programmation**, et rend le code particulièrement propre et concis. Mais forcément, ça vient au prix des performances — à part du Javascript interprété, Python est aussi un des langages les plus lents existants (mais il y a des moyens d'arranger un peu ça)
- Python est un langage **interprété** : il n'y a pas de compilation vers du code machine au préalable, l'*interpréteur* s'occupe d'exécuter le code python comme vous l'écrivez (avec l'étape intermédiaire de compilation en *bytecode*, un truc qui ressemble à du code machine mais portable et spécifique à Python, que l'interpréteur interprète, un peu comme Java)
- C'est un langage totalement **orienté objet** (mais sans être aussi rigide là-dessus que Java)
- Il utilise ce qu'on appelle le ***duck typing*** : *« if it looks like a duck, swims like a duck, and quacks like a duck, then it is probably a duck »*. Si on fait abstraction des applications politiques de cette maxime, ça donne bien le ton : il n'y a pas de typage statique comme en C/C++ ou Java, tout est basé sur *l'interface* des objets. Si un objet se conforme à ce qu'attendent les fonctions qui l'utilisent, alors quel que soit son type, son origine ou son héritage, il peut être utilisé.
	- Le typage est donc *dynamique fort* : il n'y a pas de concept de type statique et définitif associé à une variable ou un argument de fonction, mais ça reste strict dans l'utilisation de l'interface des objets.

Globalement, Python est fait pour être **facile à utiliser**, **rapide à programmer**, tout en restant extrêmement puissant en terme de fonctionnalités. D'ailleurs on le recommande souvent aux débutants, si vous avez fait un peu d'info au lycée, c'est probablement par là que vous avez commencé.

En raison de ses limitations (nécessité d'un interpréteur, performances moyennes), Python est plus rarement utilisé pour créer de gros logiciels ou jeux, même s'il en est tout à fait capable et qu'on peut en croiser. Par contre, il est très populaire pour certains types d'applications :

- **Calcul scientifique** : Python a de très bonnes librairies pour le calcul scientifique, la data science et le machine learning (NumPy, SciPy, scikit-learn, Tensorflow, PyTorch, …), qui le rendent incontournable dans ce domaine
- **Outils informatiques** : Python est rapide à écrire et propose un très large panel de fonctionnalités, donc il est très utile pour créer des outils.
- **Web** : La librairie standard de Python offre de nombreuses fonctionnalités d'interaction avec le web en général, et il existe des frameworks très populaires pour écrire le backend d'applications et d'API web en Python (Flask, Django), qui en font un des langages les plus populaires du secteur avec JS et PHP
- **Prototypage** : La rapidité d'écriture permet de créer des prototypes en Python rapidement, c'est-à-dire de tester la conception d'algorithmes ou de délivrer des prototypes logiciels sans perdre du temps à implémenter ça proprement dans le langage final
- **Scriptage** : Python est très puissant et s'intègre bien avec les logiciels dans d'autres langages, donc c'est un langage très courant pour les plugins, extensions et scripts d'autres logiciels (Inkscape, Blender, mods de Civilization IV, …)
- **Automatisation** : Pour bricoler rapidement un petit script pour une tâche quelconque, c'est souvent entre Python ou un script shell ~~(n'écoutez pas les malades qui vous disent de faire ça en Perl)~~

**Note importante** : Ceci est une référence rapide du langage Python et de ses outils, pas un tuto de programmation en général. En principe vous avez fait IF1/IF2, vous devez au moins savoir à quoi correspondent les concepts de base (condition, boucle, …).
D'ailleurs rien ne remplacera un peu de recherche dans la [doc](https://docs.python.org/3), qui est très bien écrite, Python est tellement infiniment plus vaste que des langages bas niveau comme C qu'on ne peut jamais tout faire.

## Installation et utilisation

Notez qu'ici on partira du principe qu'on est sur **Python 3.10**. Il faut voir que contrairement à C/C++ par exemple, Python est un langage qui a une implémentation de référence, qui est maintenue et activement développée par la communauté, donc il y a de nouvelles versions majeures (3.x) plus ou moins tous les ans, avec chacune de nouvelles fonctionnalités. Du coup vous verrez régulièrement des notes du type "depuis Python 3.8 il y a ça" parce qu'on essaie de vous donner le langage le plus actualisé possible, mais sans vous causer de confusion si vous devez travailler avec une version plus ancienne pour une raison quelconque — mais on ne préviendra pas pour ce qui remonte plus loin que la 3.7 (juin 2018). À l'heure actuelle, la version 3.10 est bien en place, quoique pas encore dans tous les dépôts, mais à part les `match-case` ça ne change pas grand chose pour nous par rapport à la 3.9. En principe, et à moins que Python 4 soit sorti d'ici là, toutes les versions ultérieures de Python 3 devraient être rétrocompatibles.

Dans tous les cas, comme Python est interprété, vous pouvez non seulement exécuter des programmes, mais aussi faire et **tester des choses directement dans l'interpréteur de commandes** :

;;; shell ```bash
plstek$ python3
Python 3.10.4 (main, Apr  2 2022, 09:04:19) [GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
``` ```python
>>> print("Hello World !")
``` ```
Hello World !```
;;;


### Windows

Avant tout, vous avez besoin d'installer l'interpréteur Python. Pour ça, rendez-vous sur [https://www.python.org/](https://www.python.org/), onglet *Dowloads*, téléchargez et installez la dernière version. Ce n'est pas beaucoup plus compliqué que ça. Pour lancer un script python, utilisez la commande `python monscript.py` en ligne de commande ou dans PowerShell (clic droit sur l'icône du menu démarrer > PowerShell). Vous pouvez aussi double-cliquer sur le fichier `.py`, mais c'est comme en C, ça ferme immédiatement la console à la fin du programme. Vous pouvez ouvrir l'interpréteur de commandes directement dans le menu démarrer, ou avec la commande `python`

### Linux

La plupart des distributions Linux incorporent déjà une installation de Python parce qu'elles en ont besoin pour certains de leurs outils, mais c'est souvent une installation très dépassée, voire même Python 2. Installez juste les paquets `python3` et `python3-pip` avec votre gestionnaire de paquets (ex. `sudo apt-get install python3 python3-pip`). De là, vous avez accès à l'interpréteur par la commande `python3`, et lancez un script avec `python3 monscript.py`.

## Librairies et documentation

La librairie standard Python est extrêmement bien documentée, toute la doc est disponible sur [https://docs.python.org/3/](https://docs.python.org/3/), il y a même des tutos sur certains trucs un peu compliqués. Vous pouvez sélectionner la version exacte en haut de la page, et il y a même une traduction en français qui n'est pas encore parfaitement complète mais pas loin. Il est parfaitement impossible de tout retenir vous-même ou de tout décrire ici, donc comme le dit si bien la doc, *keep this under your pillow*.

Un des avantages de Python est le très, *très* large choix de librairie tierces pour faire à peu près ce que vous voulez. On en verra quelques unes ici. Toutes sont désormais disponibles sur [https://pypi.org/](https://pypi.org/) (PyPI, the Python Package Index). Pour installer une librairie, c'est avec la commande `pip install nom-de-la-librairie` (la commande est affichée sur le site PyPI si vous allez voir). Pour la mettre à jour c'est `pip install --upgrade librairie`.

## Style et philosophie

Python a une philosophie de simplicité, propreté et lisibilité bien à lui : le langage est fait pour être pratique, propre et lisible, il faut que le code reste pratique, propre et lisible, et que sa conception reste pratique, propre et lisible. C'est notamment expliqué par la [PEP20](https://pep20.org/), *The Zen of Python*, et la [PEP8](https://pep8.org/), un guide de style du code Python. D'ailleurs, la plupart du code sur ce site suit à peu près la PEP8, même dans d'autres langages. Rien ne vous oblige à les appliquer à la lettre, comme le cite la PEP8 elle-même *« A foolish consistency is the hobgoblin of little minds »*, mais c'est bien d'avoir un style lisible et cohérent au moins dans un projet.
