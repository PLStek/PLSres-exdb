//// title = "Les warnings et erreurs"
//// description = "Comment voir tous les problèmes et les résoudre"

# {=title}

## Activer les warnings

La première étape évidente est d’activer les warnings et de **tous les corriger** (à moins que vous sachiez que c’est normal). Vous pouvez trouver ça pénible, mais c’est encore le meilleur moyen de repérer les erreurs pas évidentes directement à la compilation.

;;; shell ```bash
gcc -c -Wall -Wextra -Werror -Wno-unused-parameter -o module.o module.c
gcc -c -Wall -Wextra -Werror -Wno-unused-parameter -o main.o main.c
gcc -o -Wall -Wextra executable main.o module.o```
;;; doc
**`-Wall`** : Active tous les warnings principaux, pour les choses potentiellement problématiques. **Toujours essentiel**
**`-Wextra`** : Active des warnings supplémentaires, qui peuvent signaler des choses qui peuvent être problématiques mais qui peuvent aussi être faites exprès (un `case` sans `break`, des comparaisons de chaînes de caractères avec `==,` …), ou simplement des choses bizarres ou excédentaires (par exemple les variables ou paramètres inutilisés). **Moins essentiels mais peuvent beaucoup aider**.
**`-Werror`** : Les warnings deviennent des erreurs. Question de préférence.
**`-Wno-<nom du warning>`** : Désactive un warning spécifique. Par exemple, ci-dessus le compilateur donnait des warnings `unused-parameter` alors que c’était normal, on peut donc les désactiver
;;;

## Les erreurs courantes

Quelques messages d’erreurs pas évidents. Ce sont des messages d’erreur de GCC / MinGW, mais il y a des chances que ça ressemble sur les autres

### Erreurs et warnings à la compilation

Toutes les erreurs de compilation sont accompagnées du fichier, de la fonction et de la ligne où elles se trouvent, donc c’est en général assez facile à isoler.

;;; shell ```
Error : called object '...' is not a function or function pointer```
;;; doc
Vous appelez comme une fonction quelque chose qui n’est pas une fonction. Soit il y a une faute de frappe, soit vous avez quelque part une variable, constante ou type avec le même nom qu’une fonction
;;;

;;; shell ```
Warning : format '...' expects argument of type '...', but argument ... has type ...```
;;; doc
Vous n’avez pas donné le bon format dans un `printf` ou un `scanf`. Soit vous avez un mauvais format, soit les arguments ne sont pas dans le bon ordre, il y a des arguments en trop ou qui manquent.
;;;

;;; shell ```
Warning : control reaches end of non-void function```
;;; doc
Vous ne retournez pas de valeur dans une fonction qui doit retourner une valeur.
Par exemple, vous ne retournez pas une valeur sous toutes les conditions (dans un `if` mais pas dans le `else` par exemple, ou alors si le `return` est dans une boucle qui peut sortir avant d’exécuter le `return`)
Ça peut aussi arriver s’il manque une accolade fermante quelque part.
;;;

;;; shell ```
Warning : ... makes pointer from integer without a cast```
;;; doc
Quelque chose a interprété un entier comme un pointeur, donc soit vous vous êtes planté dans les arguments d’une fonction qui prend des pointeurs, soit vous avez oublié un `&` quelque part
;;;

;;; shell ```
Warning : implicit declaration of function '...'```
;;; doc
Vous utilisez une fonction non déclarée. Vérifiez qu’il n’y a pas de faute dans le nom de la fonction.
Si la fonction est dans un autre fichier, vous n’avez peut-être pas inclut ce qu’il fallait. Sinon, vérifiez que la fonction est bien déclarée avant son utilisation dans le code (soit définie, soit déclarée par un prototype)
;;;

;;; shell ```
Undefined reference to '...'```
;;; doc
La fonction est déclarée donc ça a passé la compilation, mais le linker n’a pas trouvé sa définition. Vérifiez déjà que vous avez bien implémenté la fonction.
Sinon, c’est probablement parce que vous avez oublié des fichiers ou des librairies à l’édition de liens. En particulier, n’oubliez pas `-lm` si vous utilisez `math.h`.
;;;

### Erreurs pendant l’exécution

;;; shell
Linux : `Erreur de segmentation` / `Segmentation Fault` \
Windows : Code de retour `0xC0000005` (`-1073741819` en décimal)
;;; doc
Votre programme a essayé d’**utiliser de la mémoire hors des régions qui lui sont attribuées**. Ça peut être que :

- Vous **dépassez des limites d’un tableau** (dans une boucle, en copiant des choses, en concaténant des chaînes de caractères, …)
- Vous utilisez de la **mémoire déjà libérée** (après avoir utilisé `free`)
- Vous utilisez un **pointeur non initialisé**, ou qui vaut `NULL`

Attention, ce n’est pas parce qu’il n’y a pas d’erreur de segmentation que votre utilisation de la mémoire est impeccable : il y a beaucoup de situations où vous pouvez lire de la mémoire non allouée (donc pas initialisée) ou écrire dedans (et donc potentiellement écraser d’autres données à vous) sans que le système ne réagisse.
Pour débugger ce genre d’erreurs, vous aurez besoin d’un **débugger** et/ou de **Valgrind**.
;;;

;;; shell
Linux : Un message d’erreur qui contient `assert` et `malloc.c` \
Windows : Code de retour `0xC0000374` (`-1073740940` en décimal)
;;; doc
Vous avez pourri les **métadonnées de l’allocateur dynamique**.
Typiquement, juste avant la zone allouée (dans les quelques octets avant le pointeur renvoyé par `malloc`), l’allocateur met ses métadonnées (taille de la zone, pointeurs vers d’autres zones pour gérer le tout, …).
Si vous **écrivez à un index négatif** d’un tableau alloué dynamiquement (ça peut arriver si vous parcourez un tableau de droite à gauche, ou si un `i-1` est mal géré), vous allez écrire par-dessus et complètement saboter la gestion du tas, ce qui crashera le programme (ou le fera planter indéfiniment selon les valeurs écrites) à la prochaine utilisation de l’allocateur (`malloc`, `free`, …)
Ça peut aussi arriver si vous utilisez deux fois `free` sur la même zone mémoire, ça pourrit aussi les métadonnées des autres zones allouées.
Vu que le **plantage** n’arrive **pas toujours au moment de l’erreur**, **Valgrind** est votre meilleur allié.
;;;
