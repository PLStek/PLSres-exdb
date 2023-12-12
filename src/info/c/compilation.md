//// title = "La compilation avec GCC"
//// description = "Utilisation et options basiques de GCC pour le langage C"

# {=title}

GCC (GNU Compiler Collection) contient des compilateurs pour plusieurs langages, dont C et C++. MinGW est un portage de la suite GCC pour Windows. La plupart des options de base sont similaires entre GCC, Clang et MSVC, si vous utilisez autre chose que GCC et que l’une de ces options ne marche pas, ça se trouve facilement sur le web.

## La base de la compilation

La chaîne de compilation de GCC (les autres sont très similaires avec des outils légèrement différents) :

{!svg: info/c/compilation-chaine.svg : code source - préprocessing - compilation - assemblage - édition de liens - exécutable}

Pour **compiler directement** des fichiers source C en exécutable :

;;; shell
```bash
gcc -o executable main.c module.c
```
;;; doc
**`-o <fichier>`** : spécifie le nom du fichier produit (sinon il s’appellera par défaut `a.out`)
;;;

Pour un projet plus important avec des librairies, on préfère généralement **compiler** les fichiers sources (.c) **individuellement** en **fichiers objets** (.o), puis faire **l’édition de liens** séparément :

;;; shell
```bash
gcc -c -o module.o module.c        # Compilation
gcc -c -o main.o main.c            # Compilation
gcc -o executable main.o module.o  # Édition de liens
```
;;; doc
**`-c`** : Compile et assemble le fichier de code sans faire l’édition de lien
;;;

## Modules et librairies
### Headers

Par défaut, GCC cherche les headers inclus par `#include <module.h>` dans son répertoire de headers par défaut, où il y a la bibliothèque standard et les librairies que vous y avez installé.

Les headers inclus par `#include "module.h"` sont pris par défaut dans le même répertoire que le fichier source qui les incluent. Vous pouvez utiliser un chemin relatif : `#include "../dossier/module.h"`

Dans des projets plus larges, surtout des librairies, on préfère généralement séparer les headers des fichiers source (on regroupe souvent les headers dans un dossier `include/` et les fichiers source dans `src/`). Pour ça, il faut ajouter le dossier à la compilation :

;;; shell
```bash
gcc -I./include -c -o build/module.o src/module.c  # Compilation
gcc -I./include -c -o build/main.o src/main.c      # Compilation
gcc -o executable build/main.o build/module.o  # Édition de liens
```
;;; doc
**`-I<dossier>`** : Donne un dossier supplémentaire où chercher les fichiers header
;;;

Inutile de laisser cette option pour l’édition de lien.

### Librairies

Si vous utilisez des librairies autres que la bibliothèque standard, il faudra les préciser au moment de l’édition de liens :

;;; shell
```bash
gcc -c -o module.o module.c                  # Compilation
gcc -c -o main.o main.c                      # Compilation
gcc -o executable main.o module.o -lm -lpng  # Édition de liens
```
;;; doc
**`-l<librairie>`** : Lie avec la librairie donnée. Doit toujours être donné après les fichiers source / objets
**`-static`** : S’il existe une version statique et une version dynamique de la même librairie, GCC utilisera la version dynamique par défaut. Si vous tenez à lier statiquement, utilisez `-static` pour le forcer.
;;;

Une librairie aura généralement un nom de fichier du type `libqqch.so` (ou `.a`, `.dylib`, `.dll`, `.lib`, … selon le système et le type de linkage). Pour lier une librairie appelée `libqqch.so`, il faudra mettre l’option `-lqqch`

Notez qu’avec la glibc (la bibliothèque standard C utilisée en général par GCC), la librairie de maths (que vous utilisez avec `<math.h>`) est séparée, il faudra donc la lier avec `-lm`.

Par défaut, GCC (plus précisément ld) va chercher ses librairies dans les répertoires donnés par la variable d’environnement `LD_LIBRARY_PATH`. Pour spécifier votre propre répertoire de librairies, utilisez l’option `-L`, qui marche comme `-I`

;;; shell
```bash
gcc -I./include -c -o build/module.o src/module.c             # Compilation
gcc -I./include -c -o build/main.o src/main.c                 # Compilation
gcc -o executable build/main.o build/module.o -L./lib -lqqch  # Linkage
```
;;; doc
**`-L<dossier>`** : Donne un dossier supplémentaire où chercher les librairies pour l’édition de liens
;;;

Pour lier avec une librairie statique locale, vous pouvez juste l’ajouter avec vos propres fichiers objets

;;; shell
```bash
gcc -I./include -c -o build/module.o src/module.c        # Compilation
gcc -I./include -c -o build/main.o src/main.c            # Compilation
gcc -o executable build/main.o build/module.o libqqch.a  # Linkage
```
;;;

### Modes de linkage
Une librairie peut être liée de deux façons :

- **Lien statique** : la librairie est directement intégrée à votre exécutable
	- Avantages
		- Le programme tient en un seul fichier, aucun problème de dépendance possible
	- Inconvénients
		- L’exécutable est plus lourd et prend plus de mémoire
- **Lien dynamique** : la librairie reste dans un fichier extérieur et l’exécutable la référence
	- Avantages :
		- Si la librairie est utilisée par plusieurs programmes, elle ne sera chargée qu’une seule fois en mémoire
		- La librairie peut être gérée séparément du programme donc peut être mise à jour séparément
		- Seul moyen de satisfaire certains termes de certaines licences comme la LGPL (qui autorise l’utilisation de la librairie par un programme sous licence incompatible avec la GPL si seule la librairie compilée est liée avec le programme)
		- Permet de réutiliser plus facilement les librairies, en particulier les plus génériques
	- Inconvénients :
		- Selon votre gestion des librairies, ça peut causer des soucis de dépendances
		- Ça implique une distribution en plusieurs fichiers

En général, on préfère lier dynamiquement. On préfère lier statiquement si la librairie est vraiment spécifique au projet (elle ne sera utilisée nulle part ailleurs), si on compile pour un environnement où on ne peut pas compter sur la bonne gestion des dépendances, ou dans un environnement où l’exécutable doit être complet (en embarqué, typiquement)


### Compiler une librairie statique
Une librairie statique est juste une collection de fichiers objets rassemblés dans une archive par l’outil archiveur (`ar`) :

;;; shell
```bash
# On compile les fichiers objet normalement
gcc -I./include -c -o file1.o file1.c
gcc -I./include -c -o file2.o file2.c
# Archivage dans libqqch.a
ar rcs libqqch.a file1.o file2.o
```
;;;

### Compiler une librairie dynamique

Une librairie statique est du code lié d’une façon particulière pour que d’autres programmes puissent le référencer

;;; shell
```bash
gcc -I./include -c -fPIC -o file1.o file1.c
gcc -I./include -c -fPIC -o file2.o file2.c
# Création de la librairie
gcc -shared -o libqqch.so file1.o file2.o
```
;;; doc
**`-fPIC`** : Compile du code indépendant de sa position en mémoire (*Position-Independent Code*), nécessaire car une librairie partagée peut être chargée n’importe où en mémoire pour être partagée entre plusieurs programmes
**`-shared`** : Lie une librairie partagée au lieu d’un exécutable, ne fonctionne qu’avec des fichiers compilés en PIC
;;;

## Débuggage
### Débugger le code source

Pendant le développement, **mettez TOUJOURS tous les warnings**. Les warnings sont là pour pointer des choses qui ne sont pas forcément des erreurs en soi, ou que le compilateur peut arranger par lui-même de façon moyennement sûre, mais qui ne sont pas ou probablement pas ce que vous voulez vraiment faire. Ils vous préviendront de nombreux problèmes autrement compliqués à débugger dès la compilation.

;;; shell
```bash
gcc -c -Wall -Wextra -Werror -Wno-unused-parameter -o module.o module.c
gcc -c -Wall -Wextra -Werror -Wno-unused-parameter -o main.o main.c
gcc -o -Wall -Wextra executable main.o module.o
```
;;; doc
**`-Wall`** : Active tous les warnings principaux, pour les choses potentiellement problématiques. **Toujours essentiel**
**`-Wextra`** : Active des warnings supplémentaires, qui peuvent signaler des choses qui peuvent être problématiques mais qui peuvent aussi être faites exprès (un `case` sans `break`, des comparaisons de chaînes de caractères avec `==`, …), ou simplement des choses bizarres ou excédentaires (par exemple les variables ou paramètres inutilisés). **Moins essentiels mais peuvent beaucoup aider**.
**`-Werror`** : Les warnings deviennent des erreurs. Question de préférence.
**`-Wno-<nom du warning>`** : Désactive un warning spécifique. Par exemple, ci-dessus le compilateur donnait des warnings `unused-parameter` alors que c’était normal, on peut donc les désactiver
;;;

### Compiler pour les outils de débuggage

Un débugger comme GDB ou d’autres outils comme Valgrind peuvent manipuler n’importe quel exécutable, mais pour avoir des infos plus précises sur le code source il faudra y ajouter des symboles de débuggage, sinon le mieux que vous aurez ce sera les positions dans le code machine :

;;; shell
```bash
gcc -c -g -o module.o module.c
gcc -c -g -o main.o main.c
gcc -o executable main.o module.o
```
;;; doc
**`-g`** : Compile avec les symboles de débuggage, très utile pendant le développement, à ne pas laisser en release (ça alourdit, ralentit et ça laisse traîner des infos que vous ne voulez pas laisser aussi faciles d’accès si vous développez un logiciel propriétaire)
;;;

## Optimisation //// optimisation

Le compilateur peut réaliser un certain nombre d’optimisations sur le code compilé. Augmenter le niveau d’optimisation augmentera le temps de compilation, accélèrera (en théorie) l’exécution et modifiera de plus en plus le code (donc diminuera son rapport avec le code original, donc le rendra plus difficile à débugger). Il est donc mieux ne pas utiliser les options autres que `-Og` avant la fin du développement (à part pour les benchmarks bien sûr).

;;; doc
*(Ce sont des O majuscule)*
**`-O1`** : Réalise les optimisations de base
**`-O2`** : Active toutes les optimisations sûres. **Généralement le meilleur choix**
**`-O3`** : Active toutes les optimisations qui marchent dans la plupart des cas, peut rarement causer des bugs
**`-Ofast`** : Active toutes les optimisations, même celles qui peuvent aller contre le standard (causant parfois de gros problèmes)
**`-Os`** : Optimise la taille de l’exécutable (peut avoir son importance pour l’embarqué par exemple)
**`-Og`** : Active les optimisations qui ne parasitent pas le débuggage, **meilleure option pendant le développement**
;;;

## Respecter un standard

Pour diverses raisons (portabilité, compatibilité, etc.), vous pouvez vouloir respecter un standard particulier du langage. Vous pouvez dire au compilateur de compiler pour un certain standard (donc de vérifier la syntaxe de ce standard et d’utiliser sa librairie standard) :

;;; doc
**`-std=<standard>`** : Utilise le standard demandé (typiquement `c89`, `c99`, `c11`)
**`-pedantic`** : Vérifie que le code respecte strictement et rigoureusement le standard (d’habitude GCC et la quasi-totalité des compilateurs tolèrent certains écarts)
**`-ansi`** : Utilise le standard ANSI original (équivalent à `-std=c89`). Avec `-ansi -pedantic`, ça implique que votre code compilera sur absolument n’importe quel compilateur C (qui marche).
;;;

## Pour les curieux

Si on se souvient de la chaîne de compilation :

{!svg: info/c/compilation-chaine.svg : code source - préprocessing - compilation - assemblage - édition de liens - exécutable}

Vous pouvez arrêter le processus à n’importe quel point de celle-ci pour voir ce qu’il en ressort. Ça ne sert pas à grand-chose à moins d’un bug particulièrement tordu dans une macro ou de faire de l’optimisation au niveau du code assembleur, mais ça reste intéressant :

;;; doc
**`-E`** : Arrête après le préprocessing (donne le code C après passage du préprocesseur)
**`-S`** : Arrête après la compilation (donne le code assembleur qui en résulte)
**`-c`** : Arrête après l’assemblage (donne des fichiers objets compilés)
;;;
