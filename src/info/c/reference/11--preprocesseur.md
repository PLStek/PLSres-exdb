//// title = "Les directives de préprocesseur"
//// description = "Utilisation du préprocesseur en C/C++"

# {=title}

Le **préprocesseur** est un outil qui **transforme le code** avant de le donner au compilateur (si vous voulez faire des expériences, utiliser GCC avec l’option `-E` sort le code transformé par le préprocesseur sans compilation). Il se commande par des directives qui commencent par le caractère `#` :

;;; code
```c//linenos
// Inclut un fichier de la bibliothèque standard dans le fichier actuel
#include <string.h>

// Inclut un fichier local dans le fichier actuel
#include "module.h"

// Définit une constante. Le préprocesseur remplacera toutes ses instances dans le code par sa valeur
// Donc utiliser NOM_CONSTANTE est strictement équivalent à écrire 10, sauf que vous avez un vrai nom
// Et que vous pouvez l’utiliser à plusieurs endroits
#define NOM_CONSTANTE 10

// Définit une macro. Pareil qu’une constante (c’est bêtement copié-collé), mais avec des arguments
// (qui sont bêtement copié-collés dedans).
// Utiliser NETTOYER_NEWLINE(entree); est équivalent à écrire entree[strcspn(entree, "\n")] = '\0';
// On ne met pas de point-virgule à la fin de la macro, sinon ça empêche de l’utiliser dans une expression
#define NETTOYER_NEWLINE(chaine) chaine[strcspn(chaine, "\n")] = '\0'

// Une macro peut avoir plusieurs lignes, on utilise \ pour passer à la ligne
// Ici on met la macro dans un do-while(0), qui ne change rien mais qui permet d’éviter tout problème à l’expansion de la macro (voir ci-après)
#define FREE_2D(tableau2d, taille)		\
	do {								  \
		for (int i = 0; i < taille; i++)  \
			free(tableau2d[i]);		   \
		free(tableau2d);				  \
	} while (0)

// Définit une constante sans lui donner de valeur, ça permet de créer des options pour paramétrer la compilation
#define _MODULE_H

// Conditions, ne compile les blocs que si la condition est vraie
// Ne garde le bloc que si la constante _WIN32 est définie
#ifdef _WIN32
printf("Windows\n");
// Sinon, si __APPLE__ est défini.
// defined(CONSTANTE) teste la même chose que #ifdef, mais on peut utiliser des opérations logiques avec
#elif defined(__APPLE__)
printf("OSX ou iOS\n");
// Même chose avec des opérateurs OU (||)
#elif defined(__linux__) || defined(__unix__) || defined(__ANDROID__)
printf("Autre UNIX-like\n");
// Sinon
#else
printf("Inconnu\n");
// Fin du bloc conditionnel (obligatoire)
#endif

// Ne garde le bloc (tout ce qu’il y a avant le prochain #elif, #else ou #endif)
// que si _MODULE_H n’est PAS défini
#ifndef _MODULE_H
#define _MODULE_H
// ...
#endif
```
;;;

## Pièges dans la résolution des macros

Attention, les **macros** remplacent **vraiment bêtement**, et ça peut vous jouer des tours potentiellement cauchemardesques : par exemple, pour :

;;; counterexample
```c
#define carre(x) x*x
#define double(x) x+x
```
;;;

Si vous utilisez `carre(1+2)`, ce sera résolu en `1+2*1+2 = 5` au lieu de `(1+2)*(1+2) = 9`, et si vous faites `2 * double(5)`, ce sera résolu en `2*5+5 = 15` au lieu de `2*(5+5) = 20`. En général, mettez toujours des parenthèses à tous les paramètres de macro qui peuvent cacher ce genre d’arnaques et mettez le résultat de ce type de macro entre parenthèses. Il vaut mieux en abuser qu’en rater :

;;; example
```c
#define carre(x) ((x)*(x))
#define double(x) ((x)+(x))
```
;;;

C’est aussi pour ça qu’il y a le `do{...} while(0)` bizarre autour de la macro à plusieurs lignes : mettons que vous l’utilisiez comme ceci :

;;; code
```c
if (tableau != NULL)
	FREE_2D(tableau);
```
;;;

Sans ce do-while, ce serait étendu en :

;;; counterexample
```c
if (tableau != NULL)
    for (int i = 0; i < taille; i++)
        free(tableau2d[i]);
free(tableau2d);
```
;;;

`free(tableau2d)` n’est plus compris dans le if, donc plein de problèmes cauchemardesques à débugger en perspective. Il faut donc mettre ça entre accolades pour en faire un bloc unique. Et comme mettre un point-virgule après la fin d’un simple bloc entre accolades comme ça est faux, on met ça dans un `do-while(0)` (strictement équivalent à juste exécuter une fois le bloc de code, le compilateur dégagera la boucle à l’optimisation) sans point-virgule pour que tout soit sûr d’être utilisable exactement comme une fonction habituelle.

## Constantes prédéfinies

Certaines constantes sont prédéfinies pour vous aider à conditionner ou gérer certaines situations.

### Position

Ces constantes de préprocesseur donnent des informations sur l’endroit où elles sont utilisées et sur la compilation

- **`__FILE__`** : Nom du fichier source
- **`__LINE__`** : Numéro de ligne dans le fichier
- **`__DATE__`** : Date de compilation
- **`__TIME__`** : Heure de compilation
- **`__STDC_VERSION__`** : Version du standard C. Si vous avez besoin de tester ça pour les fonctionnalités ajoutées dans les standards plus récents, ce sera souvent du type `#if __STDC_VERSION__ >= 199900L` (pas la peine de s’embêter à retenir les mois si c’est pas pour de l’égalité stricte). Les `L` à la fin indiquent juste que les valeurs sont de type `long`. Cependant ne vous embêtez pas trop avec ça, ça peut très éventuellement servir pour certains gros projets qui doivent être extrêmement portables, mais en ce qui vous concerne vous pouvez juste imposer la version du standard pour compiler votre programme (de nos jours C99 est bon quasiment partout et C11 marche sur tous les compilateurs majeurs).
	- `199409L` : Standard ANSI, C89 (amendé en 1994, d’où le 1994 au lieu de 1989)
	- `199901L` : C99, la version minimum qu’on utilise généralement sur cette ressource
	- `201112L` : C11, la dernière grosse version de 2011
	- `201710L` : C17, c’est pareil que C11 mais avec quelques corrections d’erreurs et d’ambiguités dans le standard
- **`__cplusplus`** est définie seulement si vous utilisez un compilateur C++, ça peut servir pour certains cas particuliers d’interfaçage entre C et C++

Il y a aussi la constante `__func__`, qui donne le nom de la fonction où elle se trouve. C’est une vraie constante (pas de préprocesseur).

Tout cela est notamment utile pour faire des messages d’erreur pour faciliter le débuggage :

;;; example ```c/result/linenos
#include <stdlib.h>
#include <stdio.h>

// Pour l’exemple, mais en principe c’est le genre de constantes qu’on donne en ligne de commande avec l’option -D
#define DEBUG

#ifdef DEBUG
#define ERROR(message) printf("ERROR in %s:%s, line %d :\n\t%s\n", __FILE__, __func__, __LINE__, message); \
                       exit(EXIT_FAILURE);
#else
#define ERROR(message) printf("ERROR : %s\n", message); \
                       exit(EXIT_FAILURE);
#endif

int main(int argc, char** argv) {
	// Note : c’est pour l’exemple, si les arguments en ligne de commande sont pas bons,
	// c’est mieux de sortir le message d’aide avec la liste des options
	if (argc < 2)
		ERROR("Not enough arguments supplied");
}```
;;;

Notez bien que ça donne le fichier/ligne/fonction où la constante est utilisée, donc pour ce type de raccourci pour construire un message d'erreur vous devez le faire soit manuellement, soit dans une macro. Si vous faites une vraie fonction comme ça, ça vous affichera juste la position de la fonction d'erreur.

### Détection du système

Vous pouvez détecter sur quel système le code est compilé grâce à certaines constantes de préprocesseur, par exemple pour définir des comportements différents selon les systèmes (en particulier, tout ce qui touche au système de fichiers devra presque toujours être séparé entre Windows et le reste). Ce sera toujours des constantes qui seront définies sur le ou les systèmes concernés et pas ailleurs, donc ça se teste avec `#ifdef` ou `#if defined(CONSTANTE)`. Ici, on listera les constantes principales définies par GCC, ça peut être légèrement différent sur les autres compilateurs mais pas trop non plus.

- `__unix__` : Défini sur tous les systèmes qui implémentent l’interface d’UNIX, devenue plus ou moins standard : BSD et dérivés, Linux, Oracle Solaris, mais **pas les systèmes Apple** (MacOS, iOS) qui sont pourtant des dérivés de BSD
- `__linux__` : Défini sous Linux
- `__APPLE__` et `__MACH__` sont définis sur les systèmes Apple (iOS / MacOS)
	- Pour des raisons historiques, il faut que les deux soient définis pour savoir que c’est un système Apple, avec `#if defined(__APPLE__) && defined(__MACH__)` (`__MACH__` seul pourrait définir NeXTSTEP, l’ancêtre de ces systèmes)
	- Une fois que vous savez que vous êtes chez Apple, vous pouvez inclure `<TargetContitionals.h>` qui contient des constantes pour déterminer plus précisément le système (iOS / MacOS / émulateur iOS)
- `_WIN32` : Défini sous tous les systèmes Windows (32 ET 64 bits)
- `_WIN64` : Défini sous les systèmes Windows 64 bits seulement
- Une fois que vous savez que vous êtes sur un système UNIX-like (`defined(__unix__) || (defined(__APPLE__) && defined(__MACH__))`), vous avez accès au header `<unistd.h>`, qui contient des définitions standard pour les systèmes UNIX. Dans ce header, vous avez la constante `_POSIX_VERSION`, qui, si elle est définie, indique que le système est compatible POSIX. Vous pouvez aussi vérifier la version de POSIX avec laquelle le système est compatible (`198808L`, `199009L`, `199506L`, `200112L`, `200809L`).

;;; example ```c
#if defined(__unix__) || (defined(__APPLE__) && defined(__MACH__))
// Nous sommes sous un système type UNIX
#include <unistd.h>
#elif defined(_WIN32)
// Nous sommes sous Windows
#include <Windows.h>
#else
#error Ce programme n’est pas compatible avec ce système
#endif```
;;;

Vous pouvez trouver une liste beaucoup plus complète [ici](http://web.archive.org/web/20191012035921/http://nadeausoftware.com/articles/2012/01/c_c_tip_how_use_compiler_predefined_macros_detect_operating_system). Vous pouvez éventuellement regarder quelles sont les macros prédéfinies sur votre machine avec `gcc -dM -E -x c /dev/null` en ligne de commande (ça marche pour GCC et Clang).
