//// title = "Pointeurs sur fonction"
//// description = "L’utilisation de pointeurs sur fonction"

# {=title}

Parfois ça peut être pratique de passer une **fonction en paramètre d’une autre** — par exemple pour donner un comportement spécifique (comparateurs, …), ou pour de la programmation évènementielle (donner une fonction *callback* à exécuter à un moment donné). Pour cela, on peut utiliser un pointeur sur fonction. Globalement on fonctionne pareil que pour n’importe quel autre paramètre, mais avec une déclaration de type bien particulière :

;;; code ```c
int fonction_avec_callback(int param1, int (*callback)(char*, int)) {
	callback("chaine", param1);
}```
;;;

La syntaxe est un peu bizarre, mais finalement c’est comme **déclarer un prototype de fonction** (sans noms d’arguments) avec juste `(*nom)` à la place du nom de la fonction. Pour l’utiliser, vous pouvez juste l’appeler **comme une fonction habituelle** avec le nom du pointeur.

;;; code ```c
void (*nom)()  // Pas de type de retour, pas d’arguments
type_retour (*nom)(type_arg1, type_arg2, type_arg3)  // Type de retour et arguments```
;;;

Pour passer un pointeur sur fonction, donnez juste le nom de la fonction. Vous pouvez mettre un `&` mais ce n’est pas obligé.

;;; example ```c/result/linenos
#include <stdio.h>
#include <stdbool.h>

// Compte les éléments du tableau qui sont vrais d’après un prédicat
// Note : c’est un exemple, mais si vous avez ce genre de choses faites
// juste la boucle vous-même sans passer par une fonction intermédiaire.
int count_true(int* array, size_t size, bool (*predicate)(int value)) {
    int count = 0;
    for (size_t i = 0; i < size; i++) {
        bool test_result = predicate(array[i]);
        if (test_result)
            count += 1;
    }
    return count;
}

bool positif(int val) {
    return val > 0;
}

int main(void) {
    int tableau1[10] = {1, 112, -13, 0, 114, 23, -8, 1, 43, 3};
    int tableau2[10] = {1, 112, 113, 2, 114, 23, 98, 1, 43, 3};

    printf("Tableau 1 : %d\n", count_true(tableau1, 10, positif));
    printf("Tableau 2 : %d\n", count_true(tableau2, 10, positif));
}
```
;;;

Si vous utilisez plusieurs fois un même type de pointeur sur fonction, vous pouvez faire un typedef dessus. Après ça vous pourrez l’utiliser comme n’importe quel type défini.

;;; code ```c
typedef bool (*int_predicate)(int value);

int count_true(int* array, size_t, int_predicate predicate) {
	// ...
	predicate(array[i]);
```
;;;

Attention cependant, un pointeur sur fonction n’est pas un simple type : il a un type de retour, des types d’arguments, et ce n’est pas une variable habituelle. **Un `typedef` cache toutes ces infos**, ce qui peut rendre ça particulièrement **obscur** si ce n’est pas parfaitement documenté à côté.

Globalement, les pointeurs sur fonction sont bien pratiques dans certaines situations, mais n’en abusez pas non plus : par exemple, dans le cas ci-dessus pour appliquer la même fonction sur un tableau entier, vous feriez mieux de faire la boucle vous-même. Ce type de fonction avec un pointeur sur fonction en paramètre ne permet pas une aussi bonne optimisation par le compilateur, peut être un peu plus confuse à utiliser, force plus de travail de documentation, et spaghettifie le code (ça fait aller l’exécution dans tous les sens dans le code au lieu d’y aller tout droit). Et non, ce n’est pas franchement meilleur pour la modularisation, c’est juste un léger raccourci qui fait faire des bonds dans le code quand vous cherchez à le lire. Donc à utiliser, mais là où c’est pertinent.
