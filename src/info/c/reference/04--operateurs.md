//// title = "Opérateurs"
//// description = "Les opérateurs disponibles en C"

# {=title}

Par **priorité descendante** (plus c’est haut, plus la priorité est élevée). Utilisez des parenthèses chaque fois que c’est nécessaire ou que vous n’êtes pas sûr.

Op.                       | Description                                                                                                          | Retourne
------------------------- | -------------------------------------------------------------------------------------------------------------------- | --------
`x++`\ `x--`              | Équivalent à `x = x+1`, renvoie l’ancienne valeur de `x`\ Équivalent à `x = x-1`, renvoie l’ancienne valeur de `x`   | `x`\ `x`
`++x`\ `--x`              | Équivalent à `x = x+1`, renvoie la nouvelle valeur de `x`\ Équivalent à `x = x-1`, renvoie la nouvelle valeur de `x` | `x + 1`\ `x - 1`
`+x`\ `-x`\ `!c`\ `~x`\ `*p`\ `&x`\ `(type)x` | Donne la valeur de `x`\ Prend l’opposé de `x`\ NON logique, inverse un booléen\ NON bit-à-bit, inverse les bits de `x`\ Déréférence le pointeur `p`\ Adresse de la variable `x`\ Conversion de type (cast) | `x`\ `-x`\ vrai si `c == 0`, sinon faux\ `x = 0b1010` ⟶ `0b0101`\ la valeur référencée par `p`\ le pointeur sur la variable `x`\ la valeur de `x` dans le nouveau type
`x * y`\ `x / y`\ `x % y` | Multiplication\ Division\ Modulo (reste de la division euclidienne de a par b)                                       | `x × y`\ `x ÷ y`\ `x mod y`
`x + y`\ `x - y`          | Addition\ Soustraction                                                                                               | `x + y`\ `x - y`
`x << b`\ `x >> b`        | Décalage de `b` bits vers la gauche (×2ᵇ)\ Décalage de `b` bits vers la droite (÷2ᵇ)                                 | `x = 0b0111` ⟶ `0b1110`\ `x = 0b1110` ⟶ `0b0111`
`x < y`\ `x > y`\ `x <= y`\ `x >= y` | Strictement inférieur\ Strictement supérieur\ Inférieur ou égal\ Supérieur ou égal | vrai si `x < y`, sinon faux\ vrai si `x > y`, sinon faux\ vrai si `x ≤ y`, sinon faux\ vrai si `x ≥ y`, sinon faux
`x == y`\ `x != y`        | Égal\ Différent | vrai si `x = y`, sinon faux\ vrai si `x ≠ y`, sinon faux
`x & y`                   | ET bit-à-bit                                                                                                         | `x = 0b1100`, `y = 0b1010` ⟶ `0b1000`
`x ^ y`                   | XOR (OU exclusif) bit-à-bit                                                                                          | `x = 0b1100`, `y = 0b1010` ⟶ `0b0110`
`x | y`                   | OU bit-à-bit                                                                                                         | `x = 0b1100`, `y = 0b1010` ⟶ `0b1110`
`c1 && c2`                | ET logique                                                                                                           | vrai si `c1` et `c2` sont vraies, sinon faux
`c1 || c2`                | OU logique                                                                                                           | vrai si au moins l’une de `c1` et `c2` est vraie, sinon faux
`x = y`\ `x += y, ...`    | `x` prend la valeur `y`, retourne la nouvelle valeur de `x`\ Équivalent à `x = x + y`. Marche pour n’importe quel opérateur (`-=`, `-=`, `*=`, ...). Renvoie la nouvelle valeur de `x` | `y`\ `x + y`

Attention à ne **pas confondre `=` avec `==`**, sinon ce sera une erreur très compliquée à débugger. Dans la plupart des cas, GCC vous donnera un warning si vous compilez avec tous les warnings (option `-Wall`). Pour éviter ce genre de problèmes, on peut *yodaïser* :

;;; code
```c
if (2 == x)
	// ...
```
;;;

Ça peut paraître moins naturel, mais comme `2 = x` est invalide vous êtes sûr qu’une telle erreur ne passera pas inaperçue.

{!exercise: info.c.divisibilite}

## Court-circuit des opérateurs logiques //// short

Info utile : les opérateurs logiques (`||` et `&&`) on un mécanisme qu’on appelle *« court-circuit »*, c’est-à-dire qu’en évaluant les conditions de gauche à droite, **dès que le résultat est connu sans ambiguité, les conditions suivantes ne sont pas évaluées du tout**. Par exemple, dans la condition `(i == 0 || tableau[i] == 0 || fonction_compliquée(tableau[i]))`, si `i == 0` est vrai, alors toute la condition est forcément vraie, il est donc inutile d’évaluer le reste de la condition. Du coup ça n’ira même pas chercher la valeur de `tableau[i]`, et ça n’exécutera pas `fonction_compliquée`. Pareil dans `(i > 1 && tableau[i] > 0 && fonction_compliquée(tableau[i]))`, si `i > 1` est faux alors toute la condition est fausse, donc le reste ne sera pas évalué.

C’est intéressant dans deux situations :

- Pour de l’optimisation, mettre les conditions les plus rapide à évaluer en premier permettra de ne faire les opérations compliquées que quand c’est strictement nécessaire
- Pour le traitement des erreurs. Par exemple, si on a `if (i < taille && tableau[i] > 0)`, normalement `tableau[i]` est invalide si `i >= taille`, donc il devrait être nécessaire de tester ce cas d’abord — mais grâce au court-circuit, la condition `i < taille` est testée d’abord et la condition `tableau[i] > 0` n’est évaluée que dans le cas où `i < taille`, où `tableau[i]` est valide, donc aucun problème.
