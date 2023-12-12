//// title = "Tableaux et chaînes de caractères"
//// description = "Comment utiliser des tableaux et des chaînes de caractères"

# {=title}

;;; code
```c//linenos
// Simple déclaration d’un tableau de 6 entiers
// Les valeurs sont indéterminées à la déclaration
int tableau[6];
tableau[0] = 1;
tableau[1] = 2;
tableau[2] = 3;

// Tableau de 6 entiers initialisés à 0
int tableau2[6] = {0};

// Tableau de 6 entiers initialisés à la main
// Le mot-clé const empêche de modifier le tableau après l’initialisation
const int tableau3[6] = {3, 7, 15, 1, 292, 1};

// Si vous avez besoin d’initialiser seulement certains éléments du tableau, même si c’est rarement utile
int tableau4[6] = {[1] = 7, [3] = 1, [5] = 1};

// Une chaîne de caractères est un tableau de char, terminé par un caractère nul ('\0')
// Le terminateur permet d’avoir des chaînes de taille variable dans un tableau de taille fixe (ici 3 caractères dans un tableau de 10)
char chaine[10];
chaine[0] = 'L';
chaine[1] = 'O';
chaine[2] = 'L';
chaine[3] = '\0';

// Chaîne de caractère initialisée plus simplement.
// Ne pas mettre le caractère nul entre les guillemets, mais il faut le prévoir dans la taille du tableau
char chaine2[4] = "LOL";

// Si vous ne mettez pas la taille, elle sera déterminée automatiquement à la compilation
char chaine3[] = "LOL";     // 4 char
int tableau4[] = {1, 2, 3}  // 3 int
```
;;;

Ne pas oublier que les **indices** de tableaux **commencent à 0** : le premier élément est à 0, le second à 1, le dernier à la `taille du tableau – 1`.

Utiliser un **indice hors du tableau** (≥ taille ou < 0) donne un **comportement indéterminé**, qui peut ne rien faire, corrompre la mémoire de votre programme ou le faire crash plus ou moins aléatoirement.

En déclarant un tableau de cette façon (statiquement), la **taille** doit être **connue à la compilation** (nombre, expression à résultat constant, ou `#define`), donc ne doit pas être une variable. En théorie la déclaration de tableau à taille variable est plus ou moins possible, mais c’est dangereux (fort risque de stack overflow), optionnel dans le standard, pas supporté par tous les compilateurs et ceux qui le supportent essaieront de vous en dissuader. Pour ça utilisez l’{> info.c.reference.dynalloc: allocation dynamique}.

Attention : vous ne pouvez **pas comparer** deux **tableaux** ou deux **chaînes de caractères** avec **`==`** : ça comparerait les pointeurs, pas le contenu. Pour les tableaux vous pouvez utiliser la fonction `memcmp(tab1, tab2, taille)`, et pour les chaînes de caractères `strcmp(str1, str2)`. Les deux retournent `0` si les deux sont égaux, un autre nombre sinon. Ces fonctions sont définies dans {>info.c.stdlib.string : `string.h`}.

## Caractères spéciaux

Certains caractères spéciaux que vous ne pouvez normalement pas écrire dans le code peuvent être codés par des *escape sequences* comme ceci :

- `'\n'` : Saut de ligne
- `'\t'` : Tabulation
- `'\''` : Apostrophe (dans la définition d’un caractère, où vous ne pouvez pas écrire `'''`. Ça ne pose pas de problème dans les chaînes de caractères : `"'"`)
- `'\"'` : Guillemet double (dans la définition d’une chaîne de caractères, ça ne pose pas de problème pour un caractère entre apostrophes)
- `'\r'` : Retour au début de la ligne (sans retour à la ligne, ça peut servir à réécrire par-dessus la ligne en cours)
- `'\nnn'` : Octet de valeur octale nnn (ex. `'\075'` ⟶ `'='`)
- `'\xHH'` : Octet de valeur hexadécimale HH (ex `'\x3D'` ⟶ `'='`)
- `'\uHHHH'` ou `'\uHHHHHHHH'` : Caractère unicode numéroté HHHH (en hexadécimal, ex. `'\u00E6'` ⟶ `'æ'`)
- `'\\'` : Backslash (sinon un `\` seul sera interprété comme une autre de ces séquences)

## Tableaux à deux dimensions

Il y a plusieurs recettes possibles pour faire des tableaux à deux dimensions (ou plus, vous avez juste à empiler plus de dimensions sur le même principe).

### Tableau statique : taille connue à la compilation

Quand vous connaissez la taille du tableau à la compilation (pour toutes les dimensions), vous pouvez simplement déclarer et utiliser le tableau normalement, mais avec plusieurs dimensions :

;;; example ```c
int grid[4][3] = {
	{ 0,  1,  2},
	{10, 11, 12},
	{20, 21, 22},
	{30, 31, 32},
};
grid[1][2] = 100;```
;;;

Une fonction peut demander un tableau à deux dimensions en paramètre, mais seule la taille de la première dimension peut être variable :

;;; example ```c
int shortest(int vectors[][3], int n_vectors);```
;;;

Si vous avez plus de dimensions, ce sera du type `int matrices[][4][4]`, …

Quand vous manipulez ce type de tableau, la bonne utilisation du cache fera que ça ira plus vite si vous itérez sur les dimensions dans l’ordre :

;;; example ```c
int grid[3][4];
for (int x = 0; x < 3; x++) {
	for (int y = 0; y < 4; y++) {
		grid[x][y] = x + y;
	}
}```
;;;

### Gérer l’indexation vous-mêmes

Si vous ne connaissez pas la taille du tableau à la compilation, il faudra dans tous les cas gérer l’allocation vous-même, donc le compilateur ne peut plus vous aider avec des `tableau[x][y]`.
La première possibilité, faire un tableau de tableaux, est expliquée plus bas mais est globalement une mauvaise idée, c’est plus lent, plus lourd en ressources et en mémoire, et demande beaucoup plus de manipulations de pointeurs.

La recette plus efficace est un peu plus tordue conceptuellement, et l’idée est d’utiliser un tableau en une dimension, mais sur 2 dimensions. Mettons que vous voulez un tableau de 3×4 éléments :

```
0  1  2  3
4  5  6  7
8  9 10 11
```

Vous avez un nombre fini d’éléments, connu, donc vous pouvez créer une bijection avec les indices d’un tableau en une dimension :

```
| 0  1  2  3 |
| 4  5  6  7 | ⟶ | 0 1 2 3 | 4 5 6 7 | 8 9 10 11 |
| 8  9 10 11 |
```

Pour ça, si on a la position (x, y) dans le tableau, on sait que chaque ligne fait `LARGEUR` éléments de long, donc il suffit de faire l’opération `y * LARGEUR + x` (par exemple ici, l’élément à la 3ème colonne de la 2ème ligne serait à `1*4 + 2 = 6`)
Vous pouvez simplifier ça avec une macro.

;;; example ```c
#define INDEX_2D(x, y) ((y)*(LARGEUR)+(x))

int* grid = malloc(sizeof(int) * LARGEUR * HAUTEUR);
for (int y = 0; y < HAUTEUR; y++) {
	for (int x = 0; x < LARGEUR; x++) {
		grid[y * LARGEUR + x] = x + y;
		// OU
		grid[INDEX_2D(x, y)] = x + y;
	}
}
free(grid);
```
;;;

Faites toujours attention à ne pas confondre vos dimensions, sinon vous prendrez pas le bon élément. Du coup nommez plutôt vos compteurs `x` et `y` ou quelque chose comme ça, plutôt que `i` et `j` qui ne sont pas très spécifiques et que vous pouvez confondre.

Ce type de tableau est particulièrement efficace parce qu’il est entièrement contigu en mémoire, donc du moment que vous itérez correctement, le cache sera utilisé très efficacement. Ça peut se passer en argument de fonction avec simplement un `void fonction(int* tableau, int largeur, int hauteur)`. Vous avez aussi différentes manières d’itérer dessus pour optimiser un peu certains cas :

;;; example
Itérer sur tous les éléments dans l’ordre ((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), …)
```c
for (int i = 0; i < LARGEUR * HAUTEUR; i++) {
	int valeur = grid[i];
	int x = i % LARGEUR;
	int y = i / LARGEUR;
}

for (int* ptr = grid; ptr < grid + LARGEUR * HAUTEUR; ptr++)
	*ptr;
```
;;;

### Faire un tableau de tableaux

Cette option est globalement plus lourde, mais plus facile à appréhender vu que vous gardez deux dimensions bien définies. Ça présente aussi l’avantage de pouvoir isoler les lignes, donc par exemple de donner une ligne seule à une fonction avec `tableau[ligne]`. L’idée est d’allouer un tableau de tableaux, puis allouer les tableaux pour le remplir. Il ne faudra bien sûr pas oublier de libérer tous les tableaux, même les secondaires.

;;; example ```c
// Allocation du tableau principal
// Notez bien que c’est un tableau de pointeurs, donc c’est par rapport
// à la taille d’un pointeur sizeof(int*) et pas sizeof(int)
int** grid = malloc(sizeof(int*) * HAUTEUR);

// Allocation des tableaux secondaires
for (int y = 0; y < HAUTEUR; y++)
	grid[y] = malloc(sizeof(int) * LARGEUR);  // Cette fois c’est bien des int

// Utilisation
int valeur = grid[1][2];
grid[1][2] = valeur;
int* ligne = grid[1];

// Destruction
for (int y = 0; y < HAUTEUR; y++)
	free(grid[y]);  // Bien libérer tous les tableaux secondaires
free(grid);```
;;;

Le tableau global est un pointeur sur pointeur, donc `int**` — si vous voulez passer ce type de pointeurs à une fonction, ce sera `void fonction(int** tableau, int largeur, int hauteur)`

Bien qu’elle puisse être plus simple à appréhender, cette solution demande beaucoup plus de manipulations pour créer et détruire le tableau, bidouille beaucoup plus de pointeurs, et consomme plus de mémoire (il y a la taille du tableau principal en plus, et c’est bien pire si vous avez 3 dimensions ou plus). Vu que ça demande de déréférencer un pointeur de plus et que ça utilise souvent un peu moins bien le cache, c’est aussi plus lourd en terme de performances, et plus il y a de tableaux secondaires, plus c’est lourd (donc si vous avez un tableau de 100 × 1000, faites 100 tableaux de 1000 éléments plutôt que 1000 tableaux de 100 éléments), alors que la solution précédente sera à peu près aussi performante dans les deux cas. Par exemple :

;;; example
```c
#include <stdio.h>
#include <math.h>
#include <time.h>
#include <stdlib.h>

#define LARGEUR 1000
#define HAUTEUR 100000
#define INDEX_2D(x, y) ((y)*(LARGEUR)+(x))

int main() {
    // ------ Tableau à bijection
    int start = time(NULL);

    // Allocation
    int* grid = malloc(sizeof(int) * LARGEUR * HAUTEUR);

    // Itération sur tous les éléments dans l’ordre
    for (int i = 0; i < LARGEUR * HAUTEUR; i++) {
        grid[i] = i;
    }

    // Boucle principale
    unsigned int result = 0;
    for (int i = 0; i < 2000; i++) {
        for (int index = 0; index < HAUTEUR * LARGEUR; index++) {
            result += grid[index] - index / LARGEUR - index % LARGEUR;
        }
    }
    free(grid);

    int end = time(NULL);

    printf("Bijection           : %u en %d secondes\n", result, end - start);

    // ------ Tableau de tableaux

    start = time(NULL);

    // Allocation
    int** grid2 = malloc(sizeof(int*) * HAUTEUR);
    for (int y = 0; y < HAUTEUR; y++) {
        grid2[y] = malloc(sizeof(int) * LARGEUR);
        for (int x = 0; x < LARGEUR; x++)
            grid2[y][x] = y * LARGEUR + x;
    }

    // Boucle principale
    result = 0;
    for (int i = 0; i < 2000; i++) {
        for (int y = 0; y < HAUTEUR; y++) {
            for (int x = 0; x < LARGEUR; x++) {
                result += grid2[y][x] - x - y;
            }
        }
    }

    // Destruction
    for (int y = 0; y < HAUTEUR; y++)
        free(grid2[y]);
    free(grid2);
    end = time(NULL);

    printf("Tableau de tableaux : %u en %d secondes\n", result, end - start);
    return 0;
}

// ------ Moyennes chez moi
// Hauteur 1000, Largeur 100000 :
// Bijection           : 1378068480 en 14 secondes
// Tableau de tableaux : 1378068480 en 55 secondes
//
// Hauteur 100000, Largeur 1000 :
// Bijection           : 1378068480 en 14 secondes
// Tableau de tableaux : 1378068480 en 64 secondes
```
;;;
