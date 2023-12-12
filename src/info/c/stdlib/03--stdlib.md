//// title = "#include <stdlib.h>"
//// description = "Description du contenu du header standard stdlib.h"

# {=title}

Définitions et fonctions d’utilité générale

## Définitions génériques
### Types

- **`size_t`** :Type entier non signé utilisé pour représenter une taille de tableau dans la plupart des fonctions de la librairie standard. En général le compilateur se débrouille tout seul pour convertir entre size_t et vos autres types entiers si besoin

### Constantes

- **`NULL`** : Valeur spéciale utilisée pour représenter un pointeur invalide (nul). Vaut en général `(void*)0`, mais pas nécessairement.
- **`EXIT_SUCCESS`** : Valeur à faire renvoyer à la fonction `main()` ou à passer à la fonction `exit()` pour signifier un arrêt normal du programme (vaut en général 0)
- **`EXIT_FAILURE`** : Valeur à faire renvoyer à la fonction `main()` ou à passer à la fonction `exit()` pour signifier un arrêt anormal générique

## Allocation dynamique de mémoire

Note : `void*` est le type utilisé pour des **pointeurs génériques**, sans type déterminé. Vous pouvez **donner n’importe quel type de pointeur** à une fonction qui prend `void*` en paramètre, et vous pouvez *cast* (convertir) un `void*` en n’importe quel type de pointeur, mais vous ne pouvez pas utiliser un pointeur de type `void*` sans le transformer en un vrai type au préalable.

;;; code
```c
void* malloc(size_t taille)
```
;;; doc
**Alloue une zone mémoire** de la taille demandée sur le tas

- `taille` : taille de la mémoire à allouer en octets

Retourne le pointeur vers la mémoire allouée, ou `NULL` si l’allocation a échoué. Le contenu initial de la zone allouée est indéterminé
;;; example
```c
list_item_t* element = malloc(sizeof(list_item_t));  // Alloue pour une structure
int* array = (int*)malloc(sizeof(int) * TAILLE);   // Pour un tableau d’entiers
```
;;;

;;; code
```c
void* calloc(size_t nombre_elements, size_t taille_element)
```
;;; doc
**Alloue** une zone mémoire sur le tas pour un tableau, et l’**initialise à zéro**

- `nombre_elements` : nombre d’éléments de la taille donnée à allouer
- `taille_element` : taille d’un élément en octets

Retourne le pointeur vers la mémoire allouée, ou `NULL` si l’allocation a échoué. Le contenu initial de la zone allouée vaudra zéro.
;;; example
```c
int* array = calloc(TAILLE, sizeof(int));
```
;;;

;;; code
```c
void free(void* pointeur)
```
;;; doc
**Libère** une zone mémoire **allouée dynamiquement** (par `malloc`, `calloc` ou `realloc`)

- `pointeur` : pointeur vers la zone mémoire à libérer

Après avoir libéré la mémoire, la valeur du pointeur reste la même mais pointe sur une zone mémoire non-allouée, donc invalide.
Si le pointeur est `NULL`, rien ne se passe.
Si le pointeur pointe sur une zone qui n’a pas été allouée dynamiquement ou sur une zone déjà libérée, le comportement est indéterminé (en général une erreur dans l’allocateur suivie d’un crash).
;;; example
```c
int* array = calloc(5, sizeof(int));
// Choses utiles
free(array);
```
;;;

;;; code
```c
void* realloc(void* pointeur, size_t nouvelle_taille)
```
;;; doc
**Redimensionne** une zone mémoire **allouée dynamiquement**

- `pointeur` : pointeur vers la zone mémoire existante. S’il est `NULL`, alloue de la mémoire comme `malloc`
- `nouvelle_taille` : nouvelle taille de la zone mémoire. Si elle vaut 0, le comportement est indéterminé

Si l’allocation réussit, **retourne un nouveau pointeur** vers la zone mémoire de la bonne taille. **L’ancien pointeur** (passé en paramètre pointeur) devient **invalide** et ne doit plus être utilisé.
Si l’allocation échoue, retourne `NULL`, et l’ancien pointeur reste valide et la zone mémoire qu’il référence reste inchangée.

Cette fonction peut soit rallonger la zone existante, soit en allouer une nouvelle. Dans ce cas, le contenu est bien recopié vers la nouvelle zone mémoire, et l’ancienne est libérée (d’où le fait que l’ancien pointeur n’est pas forcément valide ensuite)
;;; example
```c
int* tableau = malloc(5 * sizeof(int));
int* rallonge = realloc(tableau, 10 * sizeof(int));
// En cas d’échec on est toujours responsable de l’ancienne zone
if (rallonge == NULL) {
    free(tableau);
    return ERREUR;
} else {
    tableau = rallonge;
}
```
;;; warning
Si l’allocation échoue, l’ancienne zone mémoire reste valide et allouée, il faudra donc la gérer correctement pour éviter les fuites de mémoire
;;;

## Génération de nombres pseudo-aléatoires

Un générateur de nombres pseudo-aléatoires va générer une **suite de nombres** pseudo-aléatoires, c’est-à-dire qui **ont l’air** aussi aléatoires que possible **sans l’être vraiment**.

Attention : le générateur de nombres pseudo-aléatoires de la bibliothèque standard C n’a **aucune garantie de qualité** (il est généralement assez médiocre). C’est suffisant pour les applications où vous avez juste besoin de nombres qui **ont l’air** à peu près aléatoires, mais si un jour vous avez besoin d’un générateur de bonne qualité, utilisez-en un autre.

;;; code
```c
void srand(unsigned int seed)
```
;;; doc
Initialise le générateur

- `seed` : Valeur initiale du générateur, conditionne la suite générée

Cette fonction doit toujours être **appelée une** (et une seule) fois **avant** de générer des nombres. Comme c’est une suite pseudo-aléatoire, la même valeur initiale donnera la même suite, donc il faut donner des valeurs initiales différentes à chaque lancement. Pour cela on utilise souvent l’horloge, tant que la possibilité de lancer plusieurs fois le programme dans la même seconde n’est pas un problème.
On l’utilise généralement une fois au début de `main()`.
;;;

;;; code
```c
int rand(void)
```
;;; doc
Génère un nouveau nombre entier aléatoire entre `0` et `RAND_MAX`
`RAND_MAX` est une constante définie dans `stdlib.h` qui donne la valeur maximale d’un nombre renvoyé par `rand()`. Elle change selon l’implémentation, mais elle vaudra toujours au minimum 32767.
;;; example
```c/result
#include <stdlib.h>
#include <time.h>

int main() {
    srand(time(NULL));                   // Initialisation par l’horloge
    int a = rand();                      // Entier aléatoire dans [0, RAND_MAX[
    int b = rand() % 100;                // Entier aléatoire dans [0, 100[
    int c = (rand() % (20-10)) + 10;     // Entier aléatoire dans [10, 20[
    float d = (float)rand() / RAND_MAX;  // Réel aléatoire dans [0, 1[
	printf("a = %d\nb = %d\nc = %d\nd = %f\n", a, b, c, d);
}
```
;;;

## Conversion de chaînes de caractères

;;; code
```c
double atof(const char* str);
int atoi(const char* str);
long atol(const char* str);
```
;;; doc
**Convertit** simplement une **chaîne de caractères** en **nombre**

- `str` : chaîne de caractères à convertir

Ces fonctions convertissent la chaîne en partant du début, et **s’arrêten**t dès qu’elles rencontrent un **caractère invalide** (les caractères valides sont tous les nombres de la base 10, `+` ou `–` au début, et le `'.'` décimal pour `atof`)
Si la chaîne ne commence pas par un chiffre, ces fonctions renvoient `0` (indistinctement d’une chaîne qui contiendrait vraiment `"0"`). Si vous avez besoin de vérifier ce cas-là, il faudra utiliser le paramètre `endptr` de `strtol` et consorts
;;; example
```c/result/wrapmain; includes=["stdlib.h", "stdio.h"]
printf("atoi(\"%s\") -> %d\n", "99",   atoi("99"));
printf("atoi(\"%s\") -> %d\n", "-99",  atoi("-99"));
printf("atoi(\"%s\") -> %d\n", "99$",  atoi("99$"));
printf("atoi(\"%s\") -> %d\n", "$99",  atoi("$99"));
printf("atoi(\"%s\") -> %d\n", "vide", atoi("vide"));
printf("atoi(\"%s\") -> %d\n", "0",    atoi("0"));
printf("atoi(\"%s\") -> %d\n", "001",  atoi("001"));
printf("atoi(\"%s\") -> %d\n\n", "9.9",  atoi("9.9"));

printf("atof(\"%s\") -> %.1f\n", "99",   atof("99"));
printf("atof(\"%s\") -> %.1f\n", "9.9",  atof("9.9"));
printf("atof(\"%s\") -> %.1f\n", "9,9",  atof("9,9"));
```
;;;

;;; code
```c
long strtol(const char* str, char** endptr, int base)
unsigned long strtoul(const char* str, char** endptr, int base)
double strtod(const char* str, char** endptr);
```
;;; doc
Ces fonctions fonctionnent de la même façon que `atol` et `atod`, mais admettent plus de paramètres :

- `endptr` : pointeur sur un pointeur. Le pointeur vers la position qui suit immédiatement le nombre converti dans la chaîne de caractères y sera écrit. Si ça ne vous intéresse pas, vous pouvez donner `NULL`
- `base` : donne la base de laquelle convertir le nombre, entre 2 et 36 inclus

Si la conversion va jusqu’à la fin de la chaîne, `endptr` pointera sur le caractère nul en fin de chaîne.
;;; example
```c/result/wrapmain; includes=["stdlib.h", "stdio.h"]
char* suite;
long id = strtol("1100725|bureau RODULF", &suite, 10);
printf("ID: %ld, suite: %s\n\n", id, suite);

printf("strtoul(\"%s\", NULL, 2) -> %lu\n", "01111111", strtoul("01111111", NULL, 2));
printf("strtoul(\"%s\", NULL, 16) -> %lu\n", "7F",       strtoul("7F", NULL, 16));
printf("strtoul(\"%s\", NULL, 16) -> %lu\n", "0x7f",     strtoul("0x7F", NULL, 16));
```
;;;

## Gestion de l’exécution

;;; code
```c
void exit(int statut)
```
;;; doc
**Termine proprement** le programme (même en-dehors de `main()`)

- `statut` : code de retour à renvoyer. `EXIT_SUCCESS` (en principe 0) signifie la fin normale du programme, `EXIT_FAILURE` ou toute autre valeur différente de 0 implique une erreur.

`exit()` sort proprement, donc appelle les fonctions enregistrées par `atexit()`, flushe et ferme bien les fichiers et termine les processus fils, comme si le programme avait retourné normalement de `main()`.
;;;

;;; code
```c
void abort(void)
```
;;; doc
Termine immédiatement le programme.
;;; alert
Rien ne sera nettoyé comme par `exit()`, les fonctions enregistrées par `atexit()` ne seront pas appelées, les fichiers seront fermés brutalement sans flush. Le système prendra ça comme un arrêt forcé, donc peut créer un core dump et afficher un message d’erreur. Utiliser `abort()` est généralement une mauvaise idée à moins de savoir exactement ce que vous faites.
;;;

;;; code
```c
int atexit(void (*fonction)(void))
```
;;; doc
**Enregistre une fonction** qui sera **appelée** au moment où le **programme se terminera**, que ce soit en retournant de `main()` ou par `exit()`.

- `fonction` : fonction à enregistrer, doit être une fonction sans argument et sans valeur de retour.
;;; example
```c/result
#include <stdlib.h>
#include <stdio.h>

void aurevoir(void) {
    printf("Au revoir !\n");
}

int main() {
    atexit(aurevoir);
    printf("Bonjour !\n");
    return 0;
}
```
;;; note
Ce que prend `atexit()` en paramètre est un pointeur sur fonction, ça permet de passer une fonction comme paramètre d’une autre fonction.
;;;

## Fonctions mathématiques de base

;;; code
```c
int abs(int x)
long labs(long x)
```
;;; doc
Donne la valeur absolue d’un nombre entier
;;;

## Manipulation de tableaux

Note : n’essayez pas de gruger les questions d’algorithmique avec ces fonctions

;;; code
```c
void* bsearch(
	const void* valeur,
	const void* tableau,
	size_t taille_tableau,
	size_t taille_valeur,
	int (*comparaison)(const void*, const void*)
)
```
;;; doc
**Recherche une valeur** par dichotomie dans un **tableau trié**

- `valeur` : pointeur vers une variable contenant la valeur à rechercher
- `tableau` : tableau où chercher, **doit être trié en ordre croissant**
- `taille_tableau` : nombre d’éléments dans le tableau
- `taille_valeur` : taille d’un élément du tableau en octets. Doit être aussi la taille de la valeur pointée par l’argument valeur
- `comparaison` : fonction de comparaison, qui prend en argument deux pointeurs sur des éléments du tableau, et renvoie **0** s’ils sont **égaux**, une valeur **inférieure à 0** si le **premier va avant** le deuxième, et une valeur **supérieure à zéro** si le **premier va après** le deuxième.

Retourne un pointeur vers l’élément trouvé, `NULL` si la valeur n’est pas dans le tableau.
Comme vous définissez les tailles et la comparaison, les éléments du tableau peuvent être de n’importe quel type.
;;; example
```c/result
#include <stdlib.h>
#include <stdio.h>

#define TAILLE 10

int comparateur(const void* gauche_ptr, const void* droite_ptr) {
    int gauche = *((int*)gauche_ptr);
    int droite = *((int*)droite_ptr);
    return gauche - droite;  // droite > gauche -> <0
}

int main() {
    int tableau[TAILLE] = {1, 2, 5, 8, 10, 12, 16, 20, 24, 32};
    int valeur_cherchee = 12;
    int* trouve = bsearch(&valeur_cherchee, tableau, TAILLE, sizeof(int), comparateur);
    if (trouve == NULL) {
        printf("Pas trouve %d\n", valeur_cherchee);
    } else {
        // En principe l’arithmétique avec des pointeurs c’est pas génial,
        // mais bsearch est plutôt faite pour vérifier l’existence de la valeur,
        // pas forcément la retrouver, donc on fait comme on peut
        int index = trouve - tableau;
        printf("Trouve %d a l'index %d\n", valeur_cherchee, index);
    }
    return 0;
}
```
;;; note
L’argument `comparaison` est aussi un pointeur sur fonction
;;;

;;; code
```c
void qsort(
	void* tableau,
	size_t taille_tableau,
	size_t taille_element,
	int (*comparaison)(const void *, const void*)
)
```
;;; doc
**Trie un tableau** par l’algorithme quicksort

- `tableau` : tableau à trier
- `taille_tableau` : nombre d’éléments dans le tableau
- `taille_element` : taille d’un élément du tableau en octets
- `comparaison` : fonction de comparaison, qui prend en argument deux pointeurs sur des éléments du tableau, et renvoie **0** s’ils sont **égaux**, une valeur **inférieure à 0** si le **premier va avant** le deuxième, et une valeur **supérieure à zéro** si le **premier va après** le deuxième.

Le tableau sera **modifié sur place**. Comme vous définissez les tailles et la comparaison, les éléments du tableau peuvent être de n’importe quel type.
;;; example
```c/result
#include <stdlib.h>
#include <stdio.h>

#define TAILLE 10

int comparateur(const void* gauche_ptr, const void* droite_ptr) {
    int gauche = *((int*)gauche_ptr);
    int droite = *((int*)droite_ptr);
    return gauche - droite;  // droite > gauche -> <0
}

int main() {
    int tableau[TAILLE] = {1, 2, 2, 16, 12, 8, 32, 24, 20, 10};
    printf("Avant :");
    for (int i = 0; i < TAILLE; i++)
        printf(" %d", tableau[i]);

    qsort(tableau, TAILLE, sizeof(int), comparateur);

    printf("\nAprès :");
    for (int i = 0; i < TAILLE; i++)
        printf(" %d", tableau[i]);
    printf("\n");

    return 0;
}
```
;;;

## Interaction avec l’environnement

;;; code
```c
char* getenv(const char* nom_variable)
```
;;; doc
Donne la valeur d’une **variable d’environnement**

- `nom_variable` : nom de la variable à demander

Renvoie la valeur de la variable d’environnement sous forme d’une chaîne de caractères, ou `NULL` si la variable n’existe pas.
;;;

Les variables d’environnement sont des variables définies au niveau du shell qui va appeler votre programme, qui sont donc utiles pour faire passer certaines configurations sans modifier le programme, ou définir des valeurs pour plusieurs programmes différents.

;;; code
```c
int system(const char* commande)
```
;;; doc
Exécute une commande shell, comme si vous la lanciez dans l’invite de commande.
;;; alert
Les commandes shell sont évidemment **sensibles à l’environnement** donc **réduisent la portabilité**. De plus, exécuter des commandes shell depuis un programme peut être source de **lourdes vulnérabilités**, en particulier (mais pas seulement) si elles **dépendent des actions de l’utilisateur**. Utilisez plutôt les fonctions C appropriées quand c’est possible.
;;;
