//// title = "Arbres"
//// description = "Les arbres comme structure de données"

# {=title}

Un **arbre** est une structure qui va stocker des données sous forme arborescente.

{!svg: info/algo/tree-example.svg}

## Terminologie

Dans les arbres il y a des noms bien précis pour les différents éléments :

- Un **nœud** est un élément de l'arbre, qui a un **parent** et éventuellement des **enfants**.
- La **racine** est le nœud au sommet de l'arbre, duquel partent tous les autres. Comme les programmeurs des années 70 voyaient rarement le soleil, la racine est généralement représentée en haut de l'arbre.
- Une **feuille** est un nœud terminal de l'arbre, qui n'a pas d'enfants.
- On peut éventuellement appeler une liaison entre deux nœuds une **arête**. Dans un arbre, elle est toujours dirigée du parent vers le nœud fils.
- La **profondeur** d'un nœud est le nombre de parents qu'il faut remonter pour atteindre la racine.
- Un arbre est une **structure récursive**, donc chaque nœud avec ses enfants constitue un **sous-arbre**, qui se comporte exactement comme un arbre complet (le nœud sélectionné est considéré comme la racine)

{!svg: info/algo/tree-terminology.svg}

## Types d'arbres

Il y a différents types d'arbres, qui ont différentes utilités. Fondamentalement, un arbre est une structure qui suit les règles suivantes :

- Un nœud a toujours un et un seul parent, sauf la racine qui n'en a pas
- Un nœud peut avoir aucun, un ou plusieurs enfants

Et ce type de structure est ce qu'on utilise souvent quand on a juste besoin d'un arbre. Cela dit, on peut rajouter d'autres règles, et donc de nouvelles propriétés, qui permettent d'utiliser des arbres de toutes sortes de façons particulières.

### Arbre n-aire

Quand tout nœud a *au plus* `n` enfants, on dit qu'il est *n-aire* (binaire, ternaire, …). On appelle `n` le *degré* de l'arbre.

- Un arbre de degré 0 est un scalaire, un élément unique
- Un arbre de degré 1 est une liste (chaque élément est suivi d'un seul autre, ou termine la liste)
- Et ensuite, on a des arbres binaires, etc.

Un arbre n-aire a des propriétés supplémentaires :

- Tout élément de l'arbre peut être identifié par un nombre, comme dans une liste. On peut par exemple prendre le numéro du nœud fils à jusqu'à atteindre le nœud désiré, dans la base du degré de l'arbre. Ça a notamment son importance pour les algorithmes de compression par dictionnaire (Huffmann, …), où on peut facilement représenter un élément d'un arbre binaire par une suite de bits. Ça fait aussi que l'arbre peut être représenté en mémoire par un tableau, en utilisant ce nombre comme un index.

### Arbre binaire

Un arbre binaire est un arbre de degré 2 (un nœud de l'arbre peut avoir au plus 2 enfants). Ils trouvent surtout leur utilité dans la construction de structures de données particulières. On peut ajouter des propriétés diverses et variées :

- Dans un arbre binaire **plein** ou **strict**, chaque nœud a soit deux, soit aucun nœud fils

{!svg: info/algo/full-binary-tree.svg}

- Un arbre **complet** est un arbre où tous les niveaux sont complets, sauf éventuellement le dernier

{!svg: info/algo/complete-binary-tree.svg}

- Un arbre binaire **parfait** est un arbre à la fois strict et complet (tous les niveaux occupés sont complets, même le dernier)

{!svg: info/algo/perfect-binary-tree.svg}

- Un arbre binaire est dit **équilibré** quand pour chaque nœud, les sous-arbres gauche et droit ont la même profondeur ou une différence de profondeur de 1. Un arbre équilibré est optimal en termes de performance des accès (parfaitement O(log n))

{!svg: info/algo/balanced-binary-tree.svg}

- Un arbre binaire **dégénéré** est un arbre binaire où beaucoup de nœuds, voire tous les nœuds n'ont qu'un seul fils. C'est le pire cas possible en terme de performance (ça fait du O(n) vu que ça fait comme une liste). C'est ce que peuvent produire les approches naïves à certains problèmes.

{!svg: info/algo/degenerate-binary-tree.svg}

{!exercise: info.algo.parcours-arbre}

### Arbre binaire de recherche

Un arbre binaire de recherche est un arbre binaire classique, avec les propriétés suivantes :

- Le sous-nœud gauche doit toujours avoir une valeur inférieure (ou éventuellement égale) à son parent
- Le sous-nœud droit doit toujours avoir une valeur supérieure (éventuellement égale) à son parent

{!svg: info/algo/binary-search-tree.svg}

Ces propriétés permettent de rechercher facilement une valeur dans l'arbre : si la valeur qu'on recherche est inférieure au nœud, on descend à gauche, si elle est supérieure on descend à droite.

Dans un arbre binaire de recherche **équilibré**, la recherche, l'insertion et la suppression d'un élément se font en O(log n). Plus l'arbre est déséquilibré, plus les performances seront mauvaises, jusqu'au pire cas de O(n) quand l'arbre est totalement dégénéré. Il est possible de toujours garder un arbre binaire de recherche équilibré, quand il est possible de sacrifier un peu de temps à l'insertion au profit de la recherche.

Les arbres binaires de recherche peuvent être à la base de certaines implémentations d'un ensemble ou d'une table associative (il suffit d'associer une clé et une valeur à chaque nœud au lieu de juste la clé), qui ont alors des complexités autour de O(log n) pour l'accès, l'insertion et la suppression. C'est notamment le cas de `TreeSet` et `TreeMap` en Java, et de `std::set` et `std::map` en C++.

{!exercise: info.algo.binary-search-tree}

{!exercise: info.algo.treemap-implementation}

### Tas

Typiquement, un tas implémente une *file à priorités* : ça permet de pouvoir retirer l'élément avec la plus haute *priorité* de façon efficace. Ce qu'on appelle la plus « haute priorité » est une question de point de vue : ça peut être le minimum d'abord, ou le maximum d'abord.

Un tas est aussi un arbre binaire, qui suit d'autres règles particulières :

- Un tas est un arbre binaire complet (on remplit les niveaux de profondeur un par un, et chaque niveau est rempli de gauche à droite)
- Tout nœud a une priorité supérieure ou égale à tous ses enfants

{!svg: info/algo/heap.svg}

Ça fait que la racine de l'arbre sera toujours l'élément à la plus haute priorité de l'arbre, les enfants de la racine la suivent immédiatement en priorité, et ainsi de suite. Du coup, rechercher l'élément à la plus haute priorité se fait en O(1), défiler l'élément à la plus haute priorité se fait en O(log n) et insérer un élément se fait en O(log n).

Les tas sont à la base de la plupart des files à priorité, bien que ça ne soit pas toujours des tas binaires bruts comme ça : il y a par exemple les tas binomiaux qui permettent de fusionner des tas efficacement, ou les tas de Fibonacci qui impliquent plus de manips mais ont une complexité moyenne plus intéressante.

C'est aussi la base du tri par tas (en fait, toutes les implémentations de files à priorités sont homologues à un algorithme de tri). Le tri par tas (*heap sort*) est en O(n·log n), et revient à construire un tas à partir de la liste à trier, puis de ressortir les éléments dans l'ordre. Ça implique plus de manips préalables, mais il n'y a pas de pire cas en O(n²), contrairement à beaucoup d'autres tris.

{!exercise: info.algo.binary-heap}
