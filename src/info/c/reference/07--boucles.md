//// title = "Boucles"
//// description = "Les boucles en C"

# {=title}

;;; code
```c//linenos
// Tourne tant que la condition est vraie
int x = 0;
while (x < 10) {
	x += 1;
}

// Tourne tant que la condition est vraie, mais en évaluant la condition à la fin
// Donc tourne au moins une fois avant de pouvoir éventuellement sortir
int x;
do {
	scanf("%d", &x);
} while (x < 10 && x >= 0);

// Tourne un certain nombre de fois, avec un compteur
int tableau[10];
for (int i = 0; i < 10; i++) {
	tableau[i] = 2*i;
}
```
;;;

Dans l’introduction de la boucle `for` :

-	Le **premier** élément est exécuté **une fois avant d’entrer** dans la boucle (initialisation)
-	Le **deuxième** est la **condition vérifiée avant chaque tour** de boucle (on sort de la boucle dès que la condition est fausse, même avant le premier tour)
-	Le **troisième** est une instruction **exécutée après chaque tour** de boucle (sert généralement à incrémenter le compteur)

Attention, ces éléments sont séparés par des **points-virgules**, pas des virgules.

Ça fait que les boucles `for` sont bien plus puissantes que de simples compteurs, même si c’est à ça qu’elles sont le plus utiles :

;;; example
```c
for (int i = 0; i < 100; i += 2) {
	// Itère sur les nombres pairs de 0 à 100 exclus
}

for (int i = 100; i >= 0; i--) {
	// Itère de 100 à 0 inclus, dans le sens décroissant
}

for (int index_in = 0, index_out = 0; index_in < TAILLE_ENTREE && index_out < TAILLE_SORTIE; index_in++) {
	// Plusieurs variables de boucle et plusieurs conditions
	if (entree[index_in] != ' ')
		sortie[index_out++] = entree[index_in];
}

for (int index = 0; chaine[index] != '\0' /* fin de chaîne */; index++) {
	// Itère sur une chaîne de caractères et s’arrête au caractère nul
}

// etc.
```
;;;

Certains mots-clés permettent de contrôler l’exécution des boucles :

- `break` : sort immédiatement de la boucle (et reprend au code situé immédiatement après la boucle)
- `continue` : saute le reste de l’itération en cours et passe immédiatement à l’itération suivante
