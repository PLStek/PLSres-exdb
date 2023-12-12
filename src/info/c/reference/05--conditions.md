//// title = "Conditions"
//// description = "Structures de contrôle conditionnelles en C"

# {=title}

;;; code
```c//linenos
if (x == 0)
	// Si la condition est vraie
} else {
	// Si la condition est fausse
}

// Pour tous ces blocs de code (if, else if, else, while, for, …),
// Si le bloc ne contient qu’une ligne, les accolades ne sont pas obligatoires
if (x == 0)
	// Si la condition est vraie
else if (x == 1)
	// Si la première condition est fausse et la deuxième est vraie
else if (x == 2)
	// ...
else
	// Si toutes les conditions sont fausses

// Sélectionne la marche à suivre selon la valeur de la variable
// Ne marche qu’avec les types simples (entier, réel, caractère, énumération), pas de chaînes de caractères
switch (x) {
	case 0:
		// Si x == 0
		break;
	case 1: {
		int y = getval();
		printf("%d %d %d %d\n", x, y, x+y, x*y);
		break;
	}
	case 2:
	case 3:
		// Si x == 2 ou x == 3
		break;
	default:
		// Si x a toute autre valeur
		break;
}

// Ternaire : (condition)? <valeur si la condition est vraie> : <valeur si la condition est fausse>
int a = 15;
int b = 5;
int double_du_maximum = 2 * ((a > b)? a : b);
```
;;;

Si vous ne mettez pas de `break` à la fin d’un bloc `case`, **l’exécution continuera** dans le `case` suivant. Si vous compilez avec les warnings supplémentaires (option `-Wextra`), GCC vous préviendra dans les cas où ça a l’air d’être une erreur.

Vous noterez les accolades dans le `case 1` : les `case` ne sont pas des vrais blocs au même titre que les `if {}` ou les fonctions, donc normalement vous ne **pouvez pas déclarer de variables dedans**. Pour cela, il faut nous-même **créer un bloc** avec des **accolades**.

Notez que le `default` n’est absolument pas obligé d’être isolé à la fin : par exemple, si vous voulez que le comportement par défaut fassent la même chose qu’une option définie, vous pouvez juste les mettre ensemble comme des `case` habituels :

;;; example
```c
switch (x) {
	case 0:
	default:
		// Comportement par défaut
		break;
	case 1:
		// ...
}
```
;;;

Les **ternaires** sont des **expressions** (donc qui marchent même au milieu d’une plus grande expression), qui donnent la première valeur si la condition est vraie, la seconde si elle est fausse. C’est très pratique pour faire des **expressions conditionnelles** facilement sans prendre plusieurs lignes et des sous-variables dans des `if` sans intérêt, mais n’en abusez pas non plus parce que c’est un des éléments les moins lisibles du langage.
