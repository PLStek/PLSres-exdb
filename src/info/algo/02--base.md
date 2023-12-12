//// title = "Bases de l'algorithmique"
//// description = "Les variables et structures de contrôle de base"

# {=title}

Ici on va expliquer très rapidement les structures fondamentales de l'algorithmique **impérative**, qui se retrouvent dans à peu près tous les langages de programmation de ce paradigme.

## Variables

Une variable est une valeur stockée en mémoire. C'est essentiel pour retenir des informations pendant l'exécution. À un bas niveau d'abstraction, on associe souvent une variable à un type.

;;; example
```
Soit x un entier
Soit y, z des réels
Soit ville une chaîne de caractères
x <- 2
y <- √2
z <- x*y
ville <- "La Racineuse"
```
;;;

## Sous-programme

Un « sous-programme » est une subdivision d'un programme, ou un bloc de code avec sa propre utilité, et utilisé en l'appelant ailleurs. C'est l'élément le plus fondamental de la modularité des programmes. On considère généralement qu'un sous-programme doit faire une et une seule chose. Autrefois, on distinguait bien plusieurs types de sous-programmes :

- Une procédure est un sous-programme qui fait des actions par lui-même (la procédure procède à des opérations)
- Une fonction est un sous-programme qui prend des paramètres et qui les traite pour renvoyer un résultat (comme en mathématiques), sans affecter son environnement (en principe).

Dans la plupart des langages modernes la distinction n'a plus vraiment lieu d'être, et on désigne tout par le terme de « fonction », résultat ou pas.

Un sous-programme **encapsule** des opérations. Il a :

- Une **interface** : comment il doit être utilisé, c'est-à-dire un *nom*, des *paramètres*, et éventuellement une *valeur de retour*. C'est ce que voit le reste du programme.
- Un **corps**, ou **implémentation** : comment il fait réellement les choses. Si c'est bien fait, l'implémentation est *encapsulée* : le reste du programme n'a pas à se préoccuper de *comment* ça marche tant que la *façon de l'utiliser* (l'interface) ne change pas.

;;; example ```
#        nom     paramètres                   valeur de retour (ici son type)
Fonction moyenne(valeurs:liste de nombres) -> nombre
	Précondition : `valeurs` n'est pas vide

	Soit somme un nombre
	somme <- 0
	Pour chaque `élément` de `valeurs` :
		somme <- somme + élément
	Retourner somme / longueur(valeurs)  # Valeur de retour

# Programme principal, selon le langage ça peut être une quelconque fonction `main` ou juste être dans l'espace global.
Soit notes une liste de nombres
Soit moyenneGénérale un nombre

notes <- [12, 14.5, 17, 10.5, 13]
# On donne `notes` en paramètre à la fonction moyenne (c'est ce qui se retrouvera dans le paramètre `valeurs`),
# `moyenne` renvoie son résultat et on le met dans la variable `moyenneGénérale`
moyenneGénérale <- moyenne(notes)```
;;;


## Bloc conditionnel

Un bloc conditionnel permet de distinguer plusieurs cas de figure pendant l'exécution. On a généralement une ou plusieurs conditions (expression dont le résultat est vrai ou faux). Si la première condition est vraie, le premier bloc est exécuté ; si la première est fausse et la seconde est vraie, on exécute le second bloc ; et ainsi de suite. Et enfin, si aucune des conditions n'est vraie, le dernier bloc, « sinon », est exécuté.

- En C, C++, Java et JavaScript, ça s'écrit `if (condition) {...} else if (condition) {...} else {...}`
- En Python, `if condition:`, `elif condition:` et `else:`

;;; example ```
Fonction moyenne(valeurs:liste de nombres) -> nombre
	Si valeurs est vide:
		Erreur
	...```
;;; example ```
Fonction somme(valeurs:liste de nombres) -> nombre
	Si valeurs est vide:
		Renvoyer 0
	Sinon:
		Renvoyer tête(valeurs) + somme(reste(valeurs))```
;;; example ```
Fonction somme(valeurs:liste de nombres) -> nombre
	Si valeurs est vide:
		Renvoyer 0
	Sinon, si reste(valeurs) est vide:
		Renvoyer tête(valeurs)
	Sinon:
		Renvoyer tête(valeurs) + somme(reste(valeurs))```
;;;

### Sélecteur

Il existe un autre type de bloc conditionnel, qui consiste à faire une action différente en fonction de la valeur d'une variable. C'est en gros un raccourci pour `if (variable == 0) ... else if (variable == 1) ... else if (variable == 2), etc.`, mais ça permet souvent aux compilateurs de l'optimiser mieux.

- En C, C++, Java et JavaScript, ça s'exprime par un bloc `switch (variable)`, chaque valeur avec `case 0: ...; break;`, et `default: ...; break;` si la valeur ne correspond à aucune des autres.
- En Python, et seulement depuis la version 3.10, il y a `match variable:` puis `case 0:`. C'est une structure qui a aussi infiniment plus de possibilités d'évaluation de motifs.

;;; example ```c
int option;
scanf("%d", &option);
switch (option) {
	case 1:
		continuer_partie();
		break;
	case 2:
		nouvelle_partie();
		break;
	case 3:
		menu_options();
		break;
	case 4:
		exit(EXIT_SUCCESS);
		break;
	default:
		printf("Option invalide\n");
		break;
}```
;;;

## Boucle

Une boucle est un bloc que l'on exécute plusieurs fois. On appelle un passage de la boucle une **itération** Il y a plusieurs types de boucles, différents selon le langage :

- Boucles « tant que » : Exécute le corps de la boucle tant qu'une condition est vraie. À chaque début d'itération, la condition est vérifiée : si elle est vraie, on exécute le corps une nouvelle fois ; sinon, on sort de la boucle et on continue après. Ça veut dire que si la condition est fausse avant même de commencer la boucle, on n'entre pas du tout dedans.
	- Dans pratiquement tous les langages impératifs, cette boucle s'exprime avec `while condition`
- Boucles « faire ... tant que » : Pareil, sauf que la condition est évaluée à la **fin** de chaque itération, donc ça exécutera toujours au moins une itération avant de vérifier s'il faut sortir.
	- En C, C++, Java, JavaScript, ces boucles s'expriment avec `do {...} while (condition)`.
	- Ces boucles n'existent pas en Python (en tout cas pas directement)
- Boucles « pour » traditionnelles : Exécute du code un certain nombre de fois. Typiquement, on a un **compteur** qui parcourt un intervalle
	- En C, C++, Java, JavaScript c'est `for (int i = début; i < fin; i += pas)` pour [début, fin[ avec un pas
	- En Python, `for i in range(début, fin, pas)`
- Boucles « pour chaque » (*for each*), pour itérer sur les éléments d'un conteneur
	- En C ça n'existe qu'avec des bidouilles de boucles `for` spécifiques à votre cas (comme `for (element_t* element; element != NULL; element = element->suivant)` pour une liste chaînée)
	- En C++ ça se fait sur les conteneurs de la STL en bricolant avec des itérateurs (`for (std::vector<type>::iterator it = conteneur.begin(); it != conteneur.end(); it++)`)
	- En Java, `for (Type élément : conteneur)`
	- En Javascript, `for (let élément of conteneur)`
	- En Python, `for élément in conteneur`

;;; example ```
factorielle(entier opérande) -> entier
	entier résultat := 1
	Tant que opérande > 1:
		résultat := résultat × opérande
		opérande := opérande - 1
	<<-- résultat```
;;; example ```
factorielle(entier opérande) -> entier
	Si opérande ≤ 1:
		<<-- 1

	entier résultat := 1
	Pour i allant de 2 à opérande inclus:
		résultat := résultat × i
	<<-- résultat```
;;; example ```c
// Entrée utilisateur avec validation
int value;
do {
	puts("Entrez un chiffre : ");
	scanf("%d", &value);
} while (value < 0 || value > 9);```
;;; example ```python
# Itère sur les lignes d'un fichier en les affichant si elles ne sont pas vides
with open("fichier.txt", "r") as fichier.
	for ligne in fichier:
		if ligne.strip() != "":
			print(ligne)```
;;;
