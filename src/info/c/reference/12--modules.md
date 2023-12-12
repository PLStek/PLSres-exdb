//// title = "Modules"
//// description = "Découpage d’un projet C en modules"

# {=title}

Pour organiser votre code, il vaut mieux le dispatcher dans différents fichiers source. Vous aurez donc :

- `main.c` (vous pouvez donner n’importe quel nom mais on met souvent `main.c`) : fichier de code central, qui contient la fonction `main()`
- `module.c` : **Module** qui contient d’autres fonctions que vous pourrez **utiliser dans d’autres fichiers** de code
- `module.h` : Le fichier **header** (en-tête) associé à `module.c`, contient des **directives de préprocesseur** et les **prototypes** des fonctions définies dans `module.c`. Ce fichier sera inclus (`#include "module.h"`) dans les fichiers qui utilisent les fonctions de `module.c`

On n’inclut **jamais** un fichier .c dans un autre, que des .h, sinon vous allez dupliquer des déclarations et la compilation échouera.

Pour compiler plusieurs fichiers source, il y a juste à les **lier ensemble** :

;;; shell
```bash
# En une ligne
gcc -o executable main.c module1.c module2.c

# Ou si on veut lier manuellement
gcc -c -o main.o main.c
gcc -c -o module1.o module1.c
gcc -c -o module2.o module2.c
gcc -o executable main.o module1.o module2.o
```
;;;

Les fichiers auront généralement un contenu de ce type :

**`module.h` :**

;;; code
```c//linenos
// Il faut TOUJOURS protéger vos headers
// Définir une constante (unique dans tout le programme) et ne garder le code que si la constante n’est pas encore définie
// Ça fait que le code ne peut être inclus qu’une seule fois dans un fichier
// Sinon, le header peut être inclus plusieurs fois et la compilation échouera
// Par exemple, si vous avez module3.h qui inclut module.h, et main.c qui inclut module3.h et module.h,
// module.h serait inclus deux fois

#ifndef _MODULE_H
#define _MODULE_H

// C’est mieux de faire ses inclusions dans le header, pour que les fichiers qui l’importent aient bien tous les éléments pour utiliser le module,
// sinon il peut manquer des types ou des constantes par exemple
#include <stdlib.h>
#include "module2.h"

// Si vous définissez des constantes de préprocesseur qui doivent être utilisables par les fichiers qui utilisent le module, c’est toujours dans le header
#define TAILLE_PARAMETRES 5

// Toujours définir les types à exporter dans le header, sinon les fichiers qui utilisent le module n’auront pas les types qu’utilisent les fonctions
typedef struct {
	float x;
	float y;
} point_t;

// Si vous avez des constantes globales (ou variables globales mais c’est pas bien) que les fichiers appelants doivent pouvoir utiliser,
// vous devez les déclarer dans le header et définir leur valeur dans le .c
// Ne jamais assigner de valeur dans le .h, sinon la constante sera dupliquée et l’édition de liens échouera
export const point_t ORIGINE;
export const int PARAMETRES[TAILLE_PARAMETRES];

// Prototypes des fonctions définies dans module.c
float operation_tordue(point_t p1);

// Fin de la condition globale qui protège le header
#endif  /* _MODULE_H */
```
;;;

**`module.c` :**

;;; code
```c//linenos
// Inclure le header associé pour avoir les imports et les déclarations
#include "module.h"

// On définit les valeurs des constantes globales
const point_t ORIGINE = {0.0, 0.0};
const point_t PARAMETRES[TAILLE_PARAMETRES] = {1, 5, 2, 4, 3};
// Cette constante n’est pas exportée donc ne sera accessible que dans ce fichier
const point_t PARAMETRES_PRIVES[TAILLE_PARAMETRES] = {0.1, 0.2, 0.5, 1, 2};

// Cette fonction ne sera accessible que dans ce fichier
static float fonction_locale(float x) {
	float resultat = 0;
	for (int i = 0; i < TAILLE_PARAMETRES; i++)
		resultat += PARAMETRES_PRIVES[i]*x + PARAMETRES[i];
	return resultat;
}

// Définition des fonctions déclarées dans le header
float operation_tordue(point_t point) {
	return (fonction_locale(point.x) + fonction_locale(point.y)) / 2;
}
```
;;;

**`main.c` :**

;;; code
```c//linenos
#include <stdio.h>
#include "module.h"

int main() {
	point_t A = {1.2, 2.1};
	point_t B = operation_tordue(A);
	printf("Origine : (%f, %f)\n", ORIGINE.x, ORIGINE.y);
	printf("(%f, %f) -> (%f, %f)\n", A.x, A.y, B.x, B.y);
	return 0;
}
```
;;;
