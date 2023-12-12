//// title = "Allocation dynamique de mémoire"
//// description = "Allouer dynamiquement de la mémoire en C"

# {=title}

La déclaration habituelle (statique) des variables ne permet d’utiliser qu’une quantité fixe de mémoire, de taille connue à la compilation. Si vous ne connaissez ça qu’à l’exécution, il faut **allouer de la mémoire** dynamiquement :

;;; code
```c//linenos
#include <stdlib.h>  // malloc est défini dans stdlib.h

// ...
int taille = rand() % 10;
int* tableau = malloc(sizeof(int) * taille);  // Alloue la mémoire
// Faire des choses
free(tableau);  // Libère la mémoire

// Si on décompose :
//                    |taille d’un élément  |nombre d’éléments
//                    |                     |
int* tableau =  malloc(sizeof(int)        * taille);
```
;;;

La fonction `malloc(nombre d’octets)` **alloue une zone mémoire** de la taille demandée. Pour obtenir la **taille en octets** d’un type de variable on utilise `sizeof(type)`. Si on veut un **tableau**, on multiplie ça par le nombre d’éléments. Au départ, la zone mémoire allouée a un contenu indéterminé.

Pour créer un tableau, vous pouvez aussi utiliser `calloc(nombre d’éléments, taille d’un élément)`, qui initialise la zone allouée à 0.

;;; example
```c
#include <stdlib.h>

// ...
int taille = rand() % 10;
int* tableau = calloc(taille, sizeof(int));
free(tableau);
```
;;;

La **gestion** de la mémoire allouée dynamiquement est entièrement **votre responsabilité**, vous devez donc impérativement la **libérer** avec `free(pointeur)` après utilisation, sinon elle restera allouée (donc inutilisable pour autre chose), pour rien.

`malloc` renvoie un pointeur de type `void*` (un pointeur sur une zone mémoire de type inconnu), donc vous pouvez l’assigner à des pointeurs de n’importe quel type.

Une **erreur de segmentation** arrive quand le système vous prend à essayer **d’utiliser de la mémoire** qui n’est **pas à vous** (typiquement quand vous **dépassez d’un tableau**, **déréférencez un pointeur nul**, ou libérez deux fois la même zone mémoire). Ça se traduit par un message `Segmentation Fault` ou `Erreur de segmentation` sous Linux, ou par un code d’erreur `0xC0000005` sous Windows, suivi de l’arrêt forcé du programme.

Si vous écrivez à un index négatif proche (-1, -2, …) d’un tableau alloué dynamiquement, vous allez écraser les métadonnées de l’allocateur, qui lui disent typiquement la taille de la zone allouée et des infos sur les zones suivantes ou précédentes. Ça se traduira généralement par l’échec d’une quelconque assertion dans `malloc.c` sous Linux, par un code d’erreur `0xC0000374` sous Windows, ou par un plantage complet du programme selon ce que vous y avez écrit, une prochaine fois que vous essaierez d’utiliser `free()` ou `malloc()`. Ces erreurs arriveront aussi si vous utilisez `free()` sur de la mémoire qui n’a pas été allouée dynamiquement.

## La responsabilité

Quand vous allouez des ressources, elles doivent **toujours** finir par être désallouée. Quand c'est juste une fonction qui alloue une ressource pour son usage personnel, pas de souci. Par contre quand c'est une ressource qui doit être utilisée ailleurs avant d'être détruite, ça pose des problèmes de *responsabilité* — qui est propriétaire de la ressource, qui a la responsabilité de la désallouer le moment venu ?

Globalement, **celui qui alloue la ressource en est responsable**. Ça paraît assez normal de ne pas laisser vos déchets aux autres. Une fonction désalloue ses propres ressources, un module ou une librairie désalloue ses propres objets, et ainsi de suite. Ce principe évite plusieurs problèmes :

- Allouer des ressources et demander à quelqu'un d'autre de les désallouer casserait l'encapsulation. Si l'objet change, il faudrait que tous les programmes qui l'utilisent changent leur code pour s'adapter.
- Il y aurait plus de risques d'oubli, et laisserait plus la désallocation au hasard de la bonne lecture de la doc par les autres programmeurs (ou de votre propre mémoire)

Il y a différentes techniques pour respecter ça. La première, c'est de demander à la fonction appelante d'allouer ses propres ressources, puis la librairie l'initialise et l'appelant se débrouille ensuite. Ce n'est pas toujours possible, mais généralement plus propre. Ça a aussi l'avantage que la fonction appelante a la pleine maîtrise de ses ressources : l'objet peut être alloué statiquement, dynamiquement, être dans un tableau, etc. : la librairie n'en a rien à faire.

;;; code
```c
void fonction_appelante() {
	objet_t objet;
	initialiserObjet(&objet);
	utiliserObjet(&objet);
	détruireObjet(&objet);  // S'il y a de la mémoire allouée dynamiquement dans l'objet
	// L'objet est désormais invalide
}
```
;;;

On préfère éviter de retourner de la mémoire allouée dynamiquement d'une fonction utilitaire, mais parfois on n'a pas le choix. Dans ce cas, il faut définir une autre fonction qui s'occupe de la destruction, pour bien encapsuler tout le cycle de vie de l'objet

;;;
```c
void fonction_appelante() {
	objet_t* objet = créerObjet();
	utiliserObjet(objet);
	détruireObjet(objet);
}
```
;;;
