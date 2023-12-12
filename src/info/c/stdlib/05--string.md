//// title = "#include <string.h>"
//// description = "Description du contenu du header standard string.h"

# {=title}

Fonctions de manipulation des chaînes de caractères.

En C, une **chaîne de caractères** est représentée par un **tableau de caractères**, et est terminée par un **caractère nul** (0 ou `'\0'`). La plupart des fonctions qui suivent se reposent là-dessus, donc une chaîne de caractères mal terminée risque de causer beaucoup de problèmes.

## Manipulation de chaînes de caractères

Note : utiliser n’importe laquelle de ces fonctions avec des tableaux qui se superposent donnera un comportement indéterminé.

;;; code ```c
char* strcpy(char* destination, const char* source)
char* strncpy(char* destination, const char* source, size_t taille)
```
;;; doc
**Copie** la chaîne de caractères `source` dans `destination`

`strcpy` ne **vérifie pas la taille** des tableaux, donc faites attention à ce que destination soit assez longue.
`strncpy` copiera au maximum `taille` caractères, et si la chaîne de caractères est plus courte que `taille` ça remplira le reste de caractères nuls. Par contre, si la chaîne de caractères fait au moins `taille` caractères de long, elle ne mettra pas de caractère nul à la fin, donc faites attention à bien traiter ce cas.
Ces fonctions retournent `destination`
;;; example
```c
#define TAILLE 6

char chaine[TAILLE], buffer[TAILLE];
// ...
strcpy(buffer, chaine);
// Ou alors, en mettant manuellement un 0 à TAILLE-1 pour être sûr que ce soit bon
strncpy(buffer, chaine, TAILLE-1);
buffer[TAILLE-1] = '\0';
```
;;;

;;; code ```c
char* strcat(char* destination, const char* source)
char* strncat(char* destination, const char* source, size_t taille)
```
;;; doc
**Concatène** `source` à la suite de `destination` (au final vous aurez `destination` + `source` dans `destination`)

`strcat` ne **vérifie pas la taille** des tableaux, donc attention à ce que `destination` soit assez longue (longueur de la chaîne `destination` + longueur de la chaîne `source` + `1` pour le caractère nul)
`strncat` ajoutera au maximum `taille` caractères, donc `destination` devra faire au moins la longueur de la chaîne `destination` + `taille`. Si `source` fait au moins `taille` caractères de long, elle ne mettra pas de caractère nul à la fin.
Ces fonctions retournent `destination`
;;; example
```c
char debut[TAILLE] = "Hello ";
char fin[TAILLE] = "World !";
char complet[TAILLE*2];
strcpy(complet, debut);

strcat(complet, fin);
// Ou alors, en faisant attention au caractère nul
strncat(complet, fin, 2*TAILLE - strlen(complet) - 1);
complet[2*TAILLE - 1] = '\0';
```
;;;

## Exploitation de chaînes de caractères

;;; code ```c
int strcmp(const char* chaine1, const char* chaine2)
int strncmp(const char* chaine1, const char* chaine2, size_t taille)
```
;;; doc
**Compare** deux **chaînes de caractères**
Retourne **0** si les deux chaînes sont **identiques**, un nombre **négatif** si `chaine1 < chaine2`, un nombre **positif** si `chaine1 > chaine2` (ça compare caractère par caractère, ça retourne 0 si tout est identique, sinon ça s’arrête au premier caractère différent et la valeur retournée dépend seulement de ce dernier caractère)
`strncmp` comparera au maximum les `taille` premiers caractères des deux chaînes.
;;; example
```c
if (strcmp(nom, "Henriette") == 0)
	// ...
```
;;; warning
On rappelle que `chaine1 == chaine2` ne marche pas car ça compare les pointeurs, par le contenu
;;;

;;; code ```c
size_t strlen(const char* chaine)
```
;;; doc
Retourne la **longueur** de la chaîne de caractères (le nombre de caractères avant le caractère nul, caractère nul non inclus)
;;;

;;; code ```c
char* strchr(const char* chaine, char caractere)
char* strrchr(const char* chaine, char caractere)
```
;;; doc
**Recherche** la première occurrence trouvée du **caractère** donné dans une chaîne de caractères.

`strchr` cherche en partant du début (donc trouve la première occurrence)
`strrchr` cherche en partant de la fin (donc trouve la dernière occurrence)
Ces fonctions retournent le **pointeur** vers la position du caractère trouvé dans la chaîne, ou `NULL` s’il n’a pas été trouvé
;;; example
```c
int comptage(const char* chaine, char caractere) {
    int num = 0;
    char* position = strchr(chaine, caractere);
    while (position != NULL) {
        num += 1;
        // + 1 car la position retournée inclut le caractère trouvé
        position = strchr(position + 1, caractere);
    }
    return num;
}
```
;;; warning
Si vous voulez simplement l’index du caractère, vous pouvez toujours faire `pointeur_retourné – chaine`, mais `strcspn` fait sûrement ça mieux.
;;;

;;; code ```c
size_t strspn(const char* chaine, const char* caracteres)
size_t strcspn(const char* chaine, const char* caracteres)
```
;;; doc
`strspn` retourne l’index du premier caractère qui n’est pas dans les caractères donnés
`strcspn` retourne l’index du premier caractère qui est dans les caractères donnés
Si aucun caractère ne correspond, ces fonctions donneront l’index du caractère nul à la fin de la chaîne.
;;; example
```c
char buffer[100];
fgets(buffer, 100, stdin);
// Supprime le saut de ligne en fin de chaîne en terminant la chaîne à la place
// S’il n’y a pas de saut de ligne ça réécrira juste par-dessus le caractère nul existant
buffer[strcspn(buffer, "\n")] = '\0';
```
;;;

;;; code ```c
char* strpbrk(const char* chaine, const char* caracteres)```
;;; doc
Retourne le pointeur vers le premier caractère de la chaine qui est parmi les caractères, ou `NULL` s’il n’y en a aucun.
;;; example
```c
// Prend l’initiale de chaque mot de la chaîne
// Retourne le nombre de caractères écrits
int initiales(char* chaine, int maxi, char* resultat){
    if (chaine[0] == '\0') {
        resultat[0] = '\0';
        return 0;
    } else {
        resultat[0] = chaine[0];
    }
    int index = 1;
    char* espace = chaine;
    while ((espace = strpbrk(espace, " \n\t-_")) != NULL && index < maxi) {
        espace += 1;  // On passe au caractère suivant parce que le premier sera l’espace
        resultat[index++] = espace[0];
    }
    resultat[index] = '\0';
    return index;
}
```
;;;

;;; code ```c
char* strstr(const char* chaine, const char* souschaine)```
;;; doc
Retourne le pointeur vers la première occurrence de la `souschaine` dans la chaine de caractères, ou `NULL` s’il n’y en a pas
;;; example
```c
if (strstr(chaine, "yes") != NULL) {
    on_yes();
} else if (strstr(chaine, "no") != NULL) {
    on_no();
}
```
;;;

;;; code ```c
char* strtok(char* chaine, const char* separateur)```
;;; doc
**Éclate** une chaîne de caractères **à chaque occurrence** du séparateur donné.
Pour l’utiliser, commencez par l’appeler avec la chaîne de base pour avoir le premier token (ou `NULL`), puis rappelez la fonction avec `NULL` à la place de la chaîne pour récupérer chaque token suivant. La fonction retournera `NULL` quand il n’y aura plus de token à récupérer.
;;; example
```c/result/wrapmain; includes=["stdio.h", "string.h"]
char csv[] = "1,2,4,8,16,32";
char* token = strtok(csv, ",");
while (token != NULL) {
    printf("%s\n", token);
    token = strtok(NULL, ",");
}
```
;;; warning
La fonction **garde son état** entre deux appels, donc vous ne pouvez **pas** faire ça pour **deux chaînes différentes en même temps**.
Attention, la **chaîne d’origine sera modifiée** : la fonction remplacera progressivement les séparateurs avec des caractères nuls directement dans votre chaîne de caractères.
;;;

## Manipulation de mémoire brute

Ces fonctions ressemblent à celles pour les chaînes de caractères, mais vous pouvez les utiliser sur n’importe quoi, pour copier ou comparer des choses en mémoire en bloc.

;;; code ```c
int memcmp(const void* mem1, const void* mem2, size_t taille)```
;;; doc
**Compare** deux blocs de mémoire quelconques (octet par octet). Peut comparer n’importe quoi, tableaux, structures, …

- `mem1` et `mem2` : pointeurs vers les objets à comparer
- `taille` : taille en octets des zones mémoire à comparer.

Retourne `0` si les deux sont **identiques**, un nombre **négatif** si `mem1 < mem2`, un nombre **positif** si `mem1 > mem2`.
La comparaison lit les deux zones mémoire octet par octet, et s’arrête au premier octet différent entre les deux. Si ce dernier octet est plus petit dans `mem1` que dans `mem2`, la fonction retourne un nombre négatif quelconque, s’il est plus grand dans `mem1` elle retourne un nombre positif, et si tout est identique jusqu’à la taille donnée elle retourne `0`.
;;; example
```c
int array1[] = {1, 2, 3};
int array2[] = {1, 2, 4, 8};
if (memcmp(array1, array2, 3*sizeof(int)) == 0) {
    // C’est faux
}
```
;;; warning
Les zones mémoires ne contiennent **pas** forcément des valeurs qui ont **du sens octet par octet** ! Typiquement, comparer des nombres flottants IEEE754 octet par octet n’a aucun sens, mais aussi des nombres signés en complément à deux, et n’importe quel nombre entier plus large qu’un octet sur une machine *little endian* (valeurs encodées avec l’octet de poids faible en premier, incluant les architectures x86 et ARM qui font l’immense majorité des appareils grand public).

Donc pour **tester l’égalité pas de problème**, deux valeurs identiques pour `==` seront aussi identiques en mémoire (sauf pour les zéros négatifs des `float` et `double` mais normalement ça ne devrait pas vous poser trop de problème), mais **n’utilisez pas cette fonction pour tester si un des deux objets est plus grand que l’autre** si ce ne sont pas des octets bruts.
;;; example
```c/result/wrapmain; includes=["stdio.h", "string.h"]
unsigned int superieur = 1000000000;
unsigned int inferieur = 1;
int comparaison = memcmp(&superieur, &inferieur, sizeof(unsigned int));
if (comparaison < 0)
    printf("D’après memcmp, %d < %d !\n", superieur, inferieur);
else if (comparaison > 0)
    printf("D’après memcmp, %d > %d (OK)\n", superieur, inferieur);
```
;;;

;;; code ```c
void* memcpy(void* destination, const void* source, size_t taille)```
;;; doc
**Copie** `taille` octets de `source` vers `destination`.
Vous pouvez utiliser cette fonction pour copier absolument n’importe quoi (d’ailleurs vous pouvez même l’utiliser pour copier la représentation en mémoire entre des types différents, ce qui est généralement une mauvaise idée)
Retourne `destination`.
;;; example
```c
#include <string.h>
#define NUM_SOMMETS 50

typedef struct {
    int x;
    int y;
    int z;
} sommet_t;

sommet_t original[NUM_SOMMETS], modifie[NUM_SOMMETS];
extraire_sommets(original, "personnage.obj", NUM_SOMMETS);
// On copie pour modifier en gardant les originaux
memcpy(modifie, original, NUM_SOMMETS * sizeof(sommet_t));
modifier_sommets(modifie, NUM_SOMMETS);
```
;;; warning
Si `destination` et `source` se superposent (comme pour décaler des éléments au sein d’un même tableau), `memcpy` a un comportement indéterminé. Dans ces cas-là, utilisez `memmove()`.
;;;

;;; code ```c
void* memmove(void* destination, const void* source, size_t taille)```
;;; doc
**Copie** `taille` octets de `source` vers `destination`, en faisant attention à ne rien corrompre si les deux zones mémoire se superposent.
Retourne `destination`.
;;; example
```c
int testcpy[10], testmove[10], tableau[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
// On met la même chose dans testcpy et testmove
memcpy(testcpy, tableau, 10*sizeof(int));
memcpy(testmove, tableau, 10*sizeof(int));
// Déplacement d’un élément vers la droite
memcpy(testcpy + 1, testcpy, 9*sizeof(int));
memmove(testmove + 1, testmove, 9*sizeof(int));

for (int i = 0; i < 10; i++) printf("%d ", tableau[i]); printf("\n");
for (int i = 0; i < 10; i++) printf("%d ", testcpy[i]); printf("\n");
for (int i = 0; i < 10; i++) printf("%d ", testmove[i]); printf("\n");

// Dépend de l’implémentation, par exemple :
// tableau : 0 1 2 3 4 5 6 7 8 9
// memcpy  : 0 0 1 2 3 3 5 6 7 7
// memmove : 0 0 1 2 3 4 5 6 7 8
```
;;; note
Comme il y a des vérifications et un peu de bidouille pour être sûr de tout bien faire, `memmove` est généralement plus lente que `memcpy`, donc utilisez `memcpy` quand vous savez qu’il n’y a pas de superposition.
;;;

;;; code ```c
void* memset(void* zone, unsigned char valeur, size_t taille)```
;;; doc
**Remplit** une zone mémoire avec la valeur de l’octet donné

- `zone` : pointeur vers la zone mémoire à remplir
- `valeur` : valeur d’octet à assigner à toute la zone mémoire
- `taille` : taille en octets de la zone à remplir

Retourne `zone`.
;;; example
```c
int valeurs[TAILLE];
// Initialise le tableau à zéro
memset(valeurs, 0, TAILLE*sizeof(int));
```
;;; warning
Ça remplit **octet par octet**, donc pour **mettre un tableau ou une structure à zéro c’est parfait**, mais si vous utilisez une autre valeur ça la mettra à chaque octet donc si vous utilisez `memset` sur un tableau de `int` avec la valeur `1`, vos entiers auront la valeur `0x01010101`.
;;;
