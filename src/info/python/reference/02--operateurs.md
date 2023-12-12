//// title = "Opérateurs"
//// description = "Les opérateurs en Python"

# {=title}

La liste des opérateurs en Python, de la plus haute à la plus basse priorité :

Opérateur        | Description                            | Retourne
---------------- | -------------------------------------- | ---------------------------------------
`x**y`           | Exposant (puissance)                   | `x^y`
`+x`\ `-x`\ `~x` | Signe positif\ Opposé\ NON bit par bit | `x`\ `-x`\ `x = 0b1010` -> `0b0101`
`x*y`\ `x/y`\ `x//y`\ `x%y` | Multiplication\ Division réelle\ Division entière\ Modulo (reste de la division euclidienne) | `x*y`\ `5/2 = 2.5`\ `5//2 = 2`\ `5%2 = 1`
`x+y`\ `x-y`     | Addition\ Soustraction                 | `x+y`\ `x-y`
`x<<y`\ `x>>y`   | Décalage de `y` bits à gauche\ Décalage de `y` bits à droite | `0b0101 << 2 = 0b010100`\ `0b1010 >> 2 = 0b0010`
`x&y`            | ET bit par bit                         | `0b1100 & 0b1010 = 0b1000`
`x^y`            | OU exclusif bit par bit                | `0b1100 ^ 0b1010 = 0b0110`
`x|y`            | OU bit par bit                         | `0b1100 & 0b1010 = 0b1110`
Conditions       | Tous les opérateurs de conditions (qui renvoient un booléen), voir ci-dessous |
`not b`          | Inverse le booléen                     | Vrai si `b` est faux, et inversement
`a and b`        | ET logique                             | Vrai si `a` et `b` sont vrais
`a or b`         | OU logique                             | Vrai si au moins `a` ou `b` est vrai

Pour tous ces opérateurs, vous pouvez les appliquer sur place en les mettant devant un `=` : par exemple, `x += 1` est équivalent à `x = x + 1`, `x **= y` est équivalent à `x = x ** y`, …

Vous noterez les deux opérateurs de division :

- `/` fait une division réelle, qui renverra un `float` même si les opérandes sont entières (`5/2 = 2.5`)
- `//` fait une division entière, qui renverra une valeur entière (si les opérandes sont deux entiers ça renvoie un entier, si une des deux est un `float` ça renvoie un `float` mais avec une valeur entière). Dans tous les cas, ça arrondit toujours vers `-inf` (`5//2 = 2`, `-5//2 = -3`). Ça fait que vous avez toujours `y * (x//y) + (x%y)`, vous pouvez toujours décomposer en quotient/reste

## Conditions

Il y a plusieurs opérateurs qui permettent de tester des conditions, donc qui renvoient un booléen.

- **Opérateurs de comparaison** :
    - `x == y` : Renvoie `True` si `x` est égal à `y`
    - `x != y` : Renvoie `True` si `x` n'est pas égal à `y`
    - `x < y ` : Renvoie `True` si `x` est inférieur à `y`
    - `x <= y` : Renvoie `True` si `x` est inférieur ou égal à `y`
    - `x > y ` : Renvoie `True` si `x` est supérieur à `y`
    - `x >= y` : Renvoie `True` si `x` est supérieur ou égal à `y`
- **Recherche**
    - `valeur in collection` : L'opérateur `in` renvoie `True` si la valeur est dans la collection donnée. Ça peut avoir plusieurs sens : dans une liste, tuple ou ensemble c'est juste la présence de l'objet dans la collection, sur un dictionnaire ça donne si la `valeur` est l'une des *clés* du dictionnaire, et dans une chaîne de caractères, ça teste si la valeur est une sous-chaîne (`"s" in "plstek"` est vrai, mais aussi `"pls" in "plstek"` par exemple).
    - `valeur not in collection` : C'est l'inverse, ça renvoie `True` si la valeur *n'est pas* dans la collection
- **Identité**
    - `x is y` : Renvoie `True` si `x` et `y` pointent sur le même objet. Autrement dit, `x` et `y` sont deux noms pour le même objet en mémoire, pas juste deux objets égaux entre eux. C'est un opérateur qu'on n'utilise pas beaucoup : on s'en sert surtout pour vérifier si une variable vaut `None` (`if variable is None`, `variable is not None`)
    - `x is not y` : C'est l'inverse de `x is y`

Notez que contrairement à la plupart des autres langages vous pouvez enchaîner les opérateurs de comparaison, par exemple `0 <= x < 100` se comportera comme on l'attendrait, et teste si `x` est dans l'intervalle [0, 100[.

## Court-circuit des opérateurs logiques

Les opérateurs logiques `and` et `or` évaluent leurs conditions de gauche à droite, et dès que le résultat final est connu (donc dès qu'une condition est vraie pour `or` ou fausse pour `and`), l'évaluation s'arrête là et les autres conditions ne sont même pas évaluée. Ce qui veut dire que ceci est valide :

;;; example ```python
if len(liste) > 0 and liste[0] == 1:
    pass```
;;;

Normalement, si la liste est vide, prendre la valeur de `liste[0]` est une erreur — mais là si la liste est vide, `len(liste) > 0` est fausse et l'évaluation ne va pas plus loin, donc pas de problème. C'est aussi intéressant de mettre ses conditions dans l'ordre croissant de complexité pour optimiser un peu.
