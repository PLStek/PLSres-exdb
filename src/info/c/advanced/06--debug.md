//// title = "Test et débuggage"
//// description = "Les utilitaires pour aider au débuggage en C"

# {=title}

Vous avez déjà les options et les outils de débuggage dans la section appropriée, mais il y a certaines choses que vous pouvez faire directement dans votre code pour faciliter quelque peu les choses.

## Assertions

En programmation, une *assertion* est la vérification d'une condition qui *doit* être vraie. Si cette condition est fausse, alors il y a un bug (et notez bien — ce n'est pas pour rattraper des erreurs qui peuvent arriver à l'exécution : si ça échoue, le programme lui-même est faux).

Les assertions permettent donc de rattraper des situations qui ne devraient jamais arriver. Sauf qu'on connaît ce genre d'affirmations en programmation, les trucs qui ne devraient jamais arriver ça arrive forcément. Mettre des assertions pour vérifier ces situations permet d'être absolument certain que votre programme utilise ses fonctions correctement, et donc que vous n'arrivez jamais par hasard dans une situation jugée impossible, qui pourrirait la suite du programme et causerait des problèmes difficiles à débugger.

C'est un élément indispensable de la *programmation par contrat*, une technique pour améliorer la fiabilité du code. Pour faire très, très court, une fonction a :

- Des préconditions : l'état en entrant dans la fonction doit respecter certaines conditions (les arguments doivent être valides, le programme dans un état particulier, etc.). On écrit des assertions pour vérifier ça, comme ça la fonction ne pourra jamais être appelée de façon invalide
- Des postconditions : l'état en sortant de la fonction doit respecter sa documentation (la valeur de retour doit être valide, le programme dans un nouvel état particulier, etc.). C'est plus compliqué à vérifier, et c'est plutôt par des tests unitaires qu'on peut vérifier ça, mais on peut aussi écrire des assertions pour ça.

En C, les assertions sont apportées par le header `<assert.h>`. Elles sont conditionnées par la constante de préprocesseur `NDEBUG` (no debug) : si cette dernière est définie, les assertions sont désactivées. Donc par exemple, quand vous compilez en mode release, vous pouvez mettre l'option `-DNDEBUG` au compilateur pour désactiver toutes les assertions du programme et ne pas risquer un crash pour ça du côté de l'utilisateur — quoique la question de ce qui est préférable entre quitter immédiatement ou continuer dans un état invalide dépend du programme.

`assert(expression)` est une macro qui prend en paramètre une expression, typiquement une condition : si la condition est vraie, rien ne se passe, mais si la condition est fausse, `assert` affiche l'endroit et la condition qui a raté, et quitte le programme immédiatement.

;;; example ```c/result
#include <stdio.h>
#include <assert.h>

double moyenne(double nombres[], int taille) {
	assert(taille > 0);  // Si taille <= 0, on va droit vers une division par 0 et la moyenne n'aurait aucun sens

	double resultat = 0;
	for (int i = 0; i < taille; i++)
		resultat += nombres[i];
	return resultat / taille;
}

int main() {
	int tableau[] = {10, 16.5, 17, 11.3, 15.4};
	printf("%lf\n", moyenne(tableau, 0));
	return 0;
}```
;;;

### Assertions statiques

Une *assertion statique* est une assertion vérifiée à la compilation, et non à l'exécution comme les *assertion simples* ci-dessus. Ce type d'assertions n'est **disponible que depuis C11**. Il y a pour cela `static_assert(condition, "Message d'erreur si la condition est fausse")`. Comme c'est évalué à la compilation, la condition doit utiliser uniquement des constantes connues à la compilation. Ça peut par exemple servir pour tester certains comportements du compilateur, vérifier des incohérences dans des paramètres du programme que vous pouvez être amené à changer, ou tester vos macros.

;;; example ```c
#include <stdlib.h>
#include <assert.h>

#define VARIATION_MIN 0.8
#define VARIATION_MAX 0.9

double variation_aleatoire(double num) {
	static_assert(VARIATION_MIN >= 0, "La variation ne peut pas donner un nombre négatif");
	static_assert(VARIATION_MIN <= 1, "La variation minimale doit être inférieure ou égale au nombre initial");
	static_assert(VARIATION_MAX >= 1, "La variation maximale doit être supérieure ou égale au nombre initial");
	static_assert(VARIATION_MAX <= 2, "La variation maximale ne peut pas dépasser le double du nombre initial");
	static_assert(VARIATION_MAX > VARIATION_MIN, "La variation maximale doit être supérieure à la variation minimale");

	double variation = ((double)rand() / RAND_MAX) * (VARIATION_MAX - VARIATION_MIN) + VARIATION_MIN;
	return num * variation;
}

// In file included from _plsres_code_result.c:2:
// _plsres_code_result.c: In function ‘variation_aleatoire’:
// _plsres_code_result.c:10:5: error: static assertion failed: "La variation maximale doit être supérieure ou égale au nombre initial"
//    10 |     static_assert(VARIATION_MAX >= 1, "La variation maximale doit être supérieure ou égale au nombre initial");
//       |     ^~~~~~~~~~~~~
```
;;;

## Logging

Il y a beaucoup de situations où il est utile d'indiquer précisément les erreurs, où elles se produisent, et de permettre d'enregistrer ça pour référence ultérieure. Il y a aussi des moments où on voudrait avertir d'une situation bizarre sans être immédiatement fatale. Pour cela, vous pouvez vous faire un module de logging pour journaliser vos activités. Il y a des librairies existantes pour faire ça, mais qui sont souvent soit très lourdes, soit limitées, soit mal maintenues. Et comme d'habitude en C, on préfère faire tout nous-même à partir de la librairie standard plutôt que de trimballer des dépendances.

Pour ça, il peut être bien de faire ça avec des macros, en utilisant les macros et constantes de position (`__FILE__`, `__LINE__`, `__func__`). Par exemple :

;;; code ```c/result
#include <stdio.h>
#include <stdlib.h>

#ifdef NDEBUG
#define LOG(type, message) fprintf(stderr, "%s : %s\n", type, message)
#define DEBUG(message)
#else
#define LOG(type, message) fprintf(stderr, "%s in %s:%s, line %d :\n\t%s\n", type, __FILE__, __func__, __LINE__, message)
#define DEBUG(message) LOG("DEBUG", message)
#endif

#define ERROR(message) LOG("ERROR", message); exit(EXIT_FAILURE)
#define WARNING(message) LOG("WARNING", message)
#define INFO(message) LOG("INFO", message)


int main() {
	DEBUG("Ceci est une information de débuggage, qui ne sera affichée que si NDEBUG n'est pas définie");
	INFO("Ceci est une simple information");
	WARNING("Ceci est un avertissement");
	ERROR("Ceci est une erreur qui va forcer à quitter le programme");
	return 0;
}```
;;;

Ça peut aussi être intéressant d'afficher la date et l'heure, ou de faire un paramètre du préprocesseur pour choisir quels niveaux seront affichés ou non (par exemple n'afficher que les erreurs et les avertissement en mode release), à vous de déterminer vos propres besoins en la matière.
