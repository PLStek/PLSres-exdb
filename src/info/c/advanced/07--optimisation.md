//// title = "Optimisation"
//// description = "Quelques techniques pour optimiser votre code en C"

# {=title}

Il y a plein de choses à faire pour optimiser du code, la première étant évidemment d'utiliser le bon algo. Beaucoup de choses seront spécifiques à votre situation, mais il y a quelques trucs qui peuvent permettre un peu d'optimisation au niveau du code.

Attention : **l'optimisation est la toute dernière étape**. Ça va souvent diminuer la maintenabilité du code et ça vous fera passer par quelques erreurs difficiles, donc il ne faut pas faire ça tant que vous ne savez pas exactement que tout fonctionne.

## Options de compilation

Comme décrit sur la {> info.c.compilation#optimisation: page appropriée}, il existe des options qui activent des optimisations à la compilation. Les gros compilateurs modernes comme GCC sont des outils très puissants, capable d'appliquer certaines optimisations sur le code compilé.

;;; doc
*(Ce sont des O majuscule)*
**`-O1`** : Réalise les optimisations de base
**`-O2`** : Active toutes les optimisations sûres. **Généralement le meilleur choix**
**`-O3`** : Active toutes les optimisations qui marchent dans la plupart des cas, peut rarement causer des bugs
**`-Ofast`** : Active toutes les optimisations, même celles qui peuvent aller contre le standard (causant parfois de gros problèmes)
**`-Os`** : Optimise la taille de l’exécutable (peut avoir son importance pour l’embarqué par exemple)
**`-Og`** : Active les optimisations qui ne parasitent pas le débuggage, **meilleure option pendant le développement**
;;;

## Court-circuit des opérateurs logiques

Quand vous avez des conditions complexes, il peut être intéressant d'exploiter à bon escient le mécanisme de {> info.c.reference.operateurs#short: court-circuit des opérateurs logiques}, c'est-à-dire que les opérateurs logiques `||` et `&&` évaluent les conditions de gauche à droite et arrêtent toute évaluation dès que le résultat est connu (donc s'il a trouvé une valeur vraie pour `||` ou fausse pour `&&`). Il est donc généralement intéressant de placer les conditions dans l'ordre croissant de leur complexité pour tirer parti de ce mécanisme :

;;; example ```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

#define LARGEUR 1000000
#define HAUTEUR 1000
#define VALMAX 100000
#define SEUIL 10000
#define MOYENNE (VALMAX/2)

#define TIMER_INIT() clock_t _timer_start, _timer_end
#define TIMER_START() _timer_start = clock()
#define TIMER_END() _timer_end = clock(); printf("Line %d : %.6lf seconds\n", __LINE__, (double)(_timer_end - _timer_start) / CLOCKS_PER_SEC)

double moyenne(int* values, int x) {
	double resultat = 0;
	for (int y = 0; y < HAUTEUR; y++)
		resultat += values[x * HAUTEUR + y];
	return resultat / HAUTEUR;
}

bool moyenne_superieure(int* values, int x) {
	double val = moyenne(values, x);
	return val > MOYENNE;
}

int main() {
	TIMER_INIT();

	int* values = malloc(sizeof(int) * LARGEUR * HAUTEUR);
	bool conditions[LARGEUR];

	for (int x = 0; x < LARGEUR; x++)
		for (int y = 0; y < HAUTEUR; y++)
			values[x * HAUTEUR + y] = (7*(x*x + y*y) ^ 0x51AB7B13) % VALMAX;

	TIMER_START();  // Ordre des conditions sous-optimal
	for (int x = 0; x < LARGEUR; x++)
		conditions[x] = moyenne_superieure(values, x) && values[x * HAUTEUR] > SEUIL && x % 10 != 0;
	TIMER_END();

	TIMER_START();  // Ordre des conditions par complexité croissante
	for (int x = 0; x < LARGEUR; x++)
		conditions[x] = x % 5 != 0 && values[x * HAUTEUR] > SEUIL && moyenne_superieure(values, x);
	TIMER_END();

	free(values);
}

// Line 41 : 2.700417 seconds
// Line 46 : 1.028213 seconds```
;;;

## Inlining

Quand vous avez une fonction simple appelée très souvent, la simple opération d'appeler la fonction peut introduire des délais significatifs, car à chaque appel il faut allouer de la place sur la pile pour les variables, mettre les bonnes valeurs dans les bons registres, sauter vers le code de la fonction, l'exécuter, puis tout virer et revenir.

Pour éviter tout cela, il est possible d'utiliser le mot-clé `inline` à la définition de la fonction (pas devant le prototype). Le code de la fonction sera alors copié et adapté partout où la fonction est appelée. Ça éliminera alors complètement tous ces délais. Notez que le compilateur peut parfois automatiquement rendre une fonction `inline` quand les optimisations appropriées sont activées, s'il le juge utile. Le mot-clé `inline` va simplement forcer ce comportement. En réalité, dans la majorité des cas, utiliser `-O2` fera ce travail pour vous.

Attention, sur certains compilateurs, les fonction `inline` ne fonctionneront pas sans activer les optimisations (minimum `-O1` pour GCC).

;;; example ```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

#define TAILLE 100000

#define TIMER_INIT() clock_t _timer_start, _timer_end
#define TIMER_START() _timer_start = clock()
#define TIMER_END() _timer_end = clock(); printf("Line %d : %.6lf seconds\n", __LINE__, (double)(_timer_end - _timer_start) / CLOCKS_PER_SEC)

uint32_t xorshift32(uint32_t value) {
	value ^= (value << 13);
	value ^= (value >> 17);
	value ^= (value << 5);
	return value;
}

inline uint32_t inline_xorshift32(uint32_t value) {
	value ^= (value << 13);
	value ^= (value >> 17);
	value ^= (value << 5);
	return value;
}

int main() {
	TIMER_INIT();
	uint32_t values[TAILLE];
	for (int i = 0; i < TAILLE; i++)
		values[i] = i;

	TIMER_START();
	for (int i = 0; i < TAILLE; i++)
		for (int j = 0; j < TAILLE; j++)
			values[j] = xorshift32(values[i]);
	TIMER_END();

	for (int i = 0; i < TAILLE; i++)
		values[i] = i;

	TIMER_START();
	for (int i = 0; i < TAILLE; i++)
		for (int j = 0; j < TAILLE; j++)
			values[j] = inline_xorshift32(values[i]);
	TIMER_END();
}

// Line 36 : 17.702862 seconds
// Line 46 : 10.444619 seconds```
;;;
