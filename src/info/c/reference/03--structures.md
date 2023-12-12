//// title = "Structures"
//// description = "Création et utilisation des structures"

# {=title}

Une structure est un **type** de variable composé de plusieurs **champs** que vous définissez :

;;; code
```c/result/linenos
#include <stdio.h>

struct point {
	char nom;
	float x;
	float y;
};

// On peut passer et retourner des structures comme des variables normales
struct point symetrique(struct point p1, struct point p2) {
	struct point sym = {
		.nom = p1.nom,
		.x   = p1.x + 2*(p2.x - p1.x),
		.y   = p1.y + 2*(p2.y - p1.y)};
	return sym;
}

// Transforme p1 en son symétrique par rapport à p2
void symetrie_sur_place(struct point* p1, const struct point* p2) {
	// Pour accéder aux éléments d’une structure avec d’un pointeur dessus,
	// on utilise la flèche pointeur->champ (équivalent à (*pointeur).champ)
	p1->x += 2*(p2->x - p1->x);
	p1->y += 2*(p2->y - p1->y);
}

int main() {
	// Initialisation traditionnelle d’une structure, les champs doivent être dans l’ordre
	struct point A = {'A', 1.1, -0.3};

	// Initialisation version C99, en donnant les noms des champs
	// BEAUCOUP mieux, si l’ordre des champs n’est pas absolument évident
	struct point B = {.nom = 'B', .x = 2.0, .y = 1.4};

	// On récupère un champ avec variable.champ
	printf("A avant :                    (%f, %f)\n", A.x, A.y);

	symetrie_sur_place(&A, &B);
	printf("Symétrique par rapport à B : (%f, %f)\n", A.x, A.y) ;

	struct point sym = symetrique(A, B);
	printf("Re-symétrie :                (%f, %f)\n", sym.x, sym.y);

	return 0;
}
```
;;;

Pour éviter de devoir répéter `struct` à chaque utilisation, vous pouvez utiliser `typedef` :

;;; code
```c//linenos
// typedef <type de base> <nouveau nom>;
typedef struct {
	char nom;
	float x;
	float y;
} point_t;

// Plus besoin du mot-clé struct
point_t symetrique(point_t p1, point_t p2) {
	point_t sym = {
		.nom = p1.nom,
		.x   = p1.x + 2*(p2.x - p1.x),
		.y   = p1.y + 2*(p2.y - p1.y)};
	return sym;
}

int main() {
	// Ici non plus
	point_t A = {'A', 1.1, -0.3};
	// ...
}
```
;;;

En général, on suffixe les noms de types personnalisés avec `_t` (c’est ce que fait la bibliothèque standard), ou on les met en `CamelCase`, pour éviter les conflits avec les noms de variables (par exemple, appeler notre type `point` interdirait de nommer une variable `point`, ce qui peut être pénible).
