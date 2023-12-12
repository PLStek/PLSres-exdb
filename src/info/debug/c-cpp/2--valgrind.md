//// title = "Valgrind pour corriger l’utilisation de la mémoire"
//// description = "Utilisation des outils Valgrind pour surveiller les programmes de près"

# {=title}

[Valgrind](https://valgrind.org/) est un outil permettant d’émuler certaines fonctionnalités du système pour vous aider à retracer ce que fait vraiment votre programme. Il n’est disponible **que sur les UNIX-like** (Mac, Linux, …), pas sous Windows, mais il fonctionne très bien sous **WSL 2** (Windows Subsystem for Linux). Il existe quelques outils ressemblants pour Windows pur (par exemple [Dr. Memory](https://drmemory.org/)), qui marchent bien mais qui sont tout de même moins avancés.
Pour utiliser Valgrind au mieux, vous devrez compiler votre programme avec les symboles de débuggage (option `-g`). Notez que comme Valgrind émule certaines fonctions, le programme sera nettement plus lent qu’en dehors.

## Memcheck

Memcheck est l’outil par défaut quand vous utilisez Valgrind, qui sert à **détecter les problèmes d’utilisation de la mémoire**.

;;; shell ```bash
# Lance simplement memcheck
valgrind ./programme
# Pour mettre des arguments, c’est valgrind, arguments pour valgrind, programme, arguments pour le programme
valgrind --leak-check=full --track-origins=yes ./programme arg1 arg2```
;;; doc
Options pour memcheck :
**`--leak-check=full`** : détaille entièrement chaque fuite de mémoire (par défaut, donne les positions et des stats)
**`--track-origins=yes`** : détaille où a été allouée la mémoire problématique en plus de pointer l’emplacement du problème
;;;

Memcheck vous donnera la pile d’exécution (pile d’appels de fonctions), la position et le problème pour chaque problème qu’il détaille :

;;; shell ```
Invalid read```
;;; doc
Le programme lit de la mémoire qui ne lui appartient pas. Problème très commun, souvent indétectable autrement parce que ça plantera rarement le programme, mais qui peut causer beaucoup de bugs plus ou moins discrets ou problématiques vu que vous allez utiliser des valeurs non initialisées.
;;; shell ```
Invalid write```
;;; doc
Le programme écrit à un endroit où il ne devrait pas, erreurs les plus susceptibles de causer des erreurs de segmentation.
;;; shell ```
Conditional jump or move depends on uninitialised value(s)```
;;; doc
Votre programme utilise une valeur non initialisée (donc plus ou moins aléatoire), typiquement dans une condition ou un appel de fonction.
;;; shell ```
Invalid free```
;;; doc
Votre programme tente de libérer de la mémoire qu’il ne devrait pas (pas allouée ou déjà libérée).
;;; shell ```
Argument has a fishy value```
;;; doc
La taille que vous avez donnée à `malloc` (ou apparenté) est invalide ou très bizarre (négative, zéro, absurdement grande, …).
;;; shell ```
Syscall param write(buf) points to uninitialised byte(s)```
;;; doc
Des valeurs non initialisées sont données à un appel système (si vous les écrivez dans un fichier par exemple).
;;; shell ```
Source and destination overlap in memcpy```
;;; doc
Vous avez donné des zones mémoires qui se superposent à `memcpy`, donc soit des arguments ne sont pas bons, soit c’est fait exprès et vous devriez plutôt utiliser `memmove`.
;;; shell ```
Mismatched free() / delete / delete []```
;;; doc
En C++, vous avez tenté de libérer la mémoire avec la mauvaise fonction (`malloc` / `calloc` / `realloc` ⟶ `free`, `new` ⟶ `delete`, `new[]` ⟶ `delete[]`).
;;;

À la fin, memcheck vous donnera un résumé de votre utilisation de la mémoire, sous plusieurs catégories :

- **Still reachable** : vous avez encore un pointeur sur la zone mémoire à la fin, donc vous auriez pu libérer cette mémoire avec un free à la fin. Comme c’est juste à la fin, en théorie ça ne pose pas de problème (ce sera de toute façon détruit avec le reste du processus), mais il vaut toujours mieux nettoyer derrière vous.
- **Definitely lost** : la mémoire est perdue, tous les pointeurs ont disparu sans que la mémoire ait été libérée. Il faudra la libérer au bon endroit.
- **Indirectly lost** : il existe encore un pointeur vers la zone mémoire, mais ce pointeur se trouve lui-même dans un bloc perdu (par exemple, vous avez un pointeur dans une structure, et vous avez libéré la structure sans libérer le pointeur qui est dedans). Vous devrez vous arranger pour libérer correctement vos pointeurs imbriqués.
- **Possibly lost** : il existe une chaîne de pointeurs existante vers la zone mémoire, sauf que l’un d’entre eux est un « pointeur intérieur » (un pointeur qui pointe au milieu de la zone mémoire plutôt qu’au début), donc ça peut être bon mais vraiment bizarre, ou bien un pointeur mal initialisé qui tombe dessus par hasard. Si vous n’êtes pas certain que c’est fait exprès, à traiter comme de la mémoire complètement perdue.

## Les autres outils

Valgrind est une collection de divers outils, que vous pouvez lancer individuellement avec `--tool=outil` :

- `memcheck` : Détection des erreurs d’utilisation de la mémoire
- `helgrind`, `drd` : Détection des erreurs de multithreading
- `massif` : Profilage de l’utilisation du tas
- `callgrind` : Construit des graphes d’appels pour profiler les ressources utilisées par les différentes fonctions
- `cachegrind` : Profile l’utilisation de la mémoire cache

(Ce n’est pas exclus qu’on rajoute des sections sur ces outils un jour :)
