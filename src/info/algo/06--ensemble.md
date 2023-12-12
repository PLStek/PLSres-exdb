//// title = "Ensembles et tables associatives"
//// description = "Les ensembles et les tables associatives"

# {=title}

## Généralités
### Ensembles

Un ensemble est une structure de données qui marche comme un ensemble en mathématiques. C'est une structure qui contient des éléments, où on peut insérer, supprimer des éléments, et vérifier si une valeur est présente dans l'ensemble ou pas. En général il est possible d'itérer sur les éléments de l'ensemble, mais il n'y aura pas d'ordre particulier. En principe il y a aussi des opérations logiques entre ensembles (union, intersection, soustraction, …). Tout ça fait qu'un ensemble ne contient pas de doublons : soit une valeur y est, soit elle n'y est pas, elle ne peut pas y être plusieurs fois. C'est utile dès qu'on veut simplement savoir si une valeur est dans un conteneur ou pas, par exemple pour avoir des ensembles de valeurs particulières, ou pour garder la trace de valeurs déjà traitées.

On peut faire le parallèle avec une liste sans ordre particulier — mais le fait de retirer la propriété d'ordre permet d'avoir des opérations bien plus efficaces.

En gros, il y a deux implémentations génériques possibles d'un ensemble (il y en a d'autres, mais plus spécialisées) :

- Un arbre binaire de recherche : les opérations ont donc la complexité habituelle d'un arbre binaire de recherche, soit O(log n) pour rechercher, insérer et supprimer si l'arbre est bien équilibré. En général, ça fera aussi qu'itérer sur l'ensemble donnera les éléments triés
- Une table de hash : C'est une structure un peu particulière, décrite plus bas, où on calcule un *hash* de la valeur à insérer (un nombre entier calculé à partir de la valeur à insérer, idéalement unique), qu'on utilise comme index dans un tableau. Ça permet de rechercher, insérer et supprimer avec une complexité moyenne en Θ(1) mais avec un pire cas en O(n), qui dépendent de divers compromis dans la conception. À moins de conserver leur ordre par ailleurs, l'ordre des éléments à l'itération est imprévisible.

Dans quelques langages :

- C : Implémentation manuelle
- C++ : `std::set` (en principe c'est un arbre)
- Java : `TreeSet` et ses dérivés utilise un arbre, et `HashSet` et ses dérivés utilise une table de hash. Si vous avez besoin d'itérer dessus dans l'ordre naturel des éléments, utilisez `TreeSet`, si vous voulez itérer dans l'ordre où les valeurs ont été insérées, il y a `LinkedHashSet` — dans la plupart des autres cas, `HashSet` est le meilleur choix
- Python : `set` est un ensemble modifiable (utilisable avec la syntaxe `{élément1, élément2, ...}`), `frozenset` est un ensemble non-modifiable après sa création. Les deux utilisent des tables de hash
- JavaScript : `Set` (l'implémentation n'est pas imposée par le standard, tant que c'est plus rapide qu'un tableau)

### Tables associatives

Une table associative (ou dictionnaire) est une structure qui contient des couples clés-valeurs. Une valeur est associée à chaque clé, et il est possible de récupérer la valeur simplement à partir de la clé. C'est une structure extrêmement utile dans énormément de cas de figure : dès qu'on veut associer une valeur à une autre, pour avoir des identifiants pointant sur des objets, implémenter un cache, etc.

En gros, une table associative est un ensemble, sauf qu'au lieu de stocker une seule valeur, on stocke les clés comme n'importe quel ensemble, sauf qu'on associe une valeur avec chaque clé. Du coup, les implémentations et leurs performances sont exactement les mêmes.

- C : Implémentation manuelle
- C++ : `std::map` (aussi un arbre)
- Java : Tout comme les ensembles, il y a `TreeMap`, `HashMap`, `LinkedHashMap` et leurs dérivés
- Python : Les dictionnaires de base du langage (`dict`, qui s'utilisent avec la syntaxe `{clé: valeur, clé2: valeur2, ...}`) sont des tables de hachages, sur lesquelles on itère dans l'ordre d'insertion des éléments
- JavaScript : `Map` (l'implémentation n'est pas non plus imposée par le standard). En principe, les objets de base (la syntaxe `{clé: valeur, ...}`) font ça aussi, mais les `Map` sont beaucoup mieux (les objets ne sont pas faits pour ça à la base, limitent leurs clés aux chaînes de caractères, leur taille est difficile à déterminer, itération compliquée, optimisation différente (en général accès plus rapide mais insertion/délétion beaucoup plus lente), propriétés par défaut qui peuvent entrer en collision avec les vôtres).

## Table de hash

Une table de hash permet d'implémenter un ensemble ou une table associative. Si ce n'est pas implémenté n'importe comment, une table de hash est généralement plus performante qu'un arbre, ce qui explique qu'elles soient souvent utilisées à cet escient. En fait, le principal inconvénient par rapport aux arbres, c'est qu'itérer sur une table de hash donne les éléments dans un ordre totalement imprévisible (à moins de stocker l'ordre séparément).

Fondamentalement, une table de hash est un tableau, qui stocke les éléments de l'ensemble ou les couples clé-valeur de la table associative. La taille du tableau est arbitraire.

Pour *insérer* un élément, on prend un *hash* de la clé. La fonction de hash est une fonction qui prend une clé de la table, et qui renvoie un nombre entier. On utilise `hash(clé) % taille(tableau)` comme index dans le tableau. La clé ou le couple clé-valeur sera alors stocké à cet index dans le tableau. Du coup, idéalement, l'insertion, la recherche et la suppression sont en Θ(1) : Il suffit de calculer le hash et le reste n'est qu'un accès au tableau.

Malheureusement, il y a un gros problème : les collisions. Quand le calcul `hash(clé) % taille(tableau)` donne le même index pour deux clés différentes, ça donne ce qu'on appelle une *collision* : deux clés différentes sont supposées se retrouver au même endroit. Concrètement, ça se produit quand vous insérez un élément, mais que son index est déjà occupé.

Il y a plusieurs techniques pour résoudre ce problème :

- La première, c'est d'insérer l'élément dans la première case vide après l'index calculé. L'avantage, c'est que l'implémentation est plus facile et performante, mais ça aura tendance à créer plus de collisions, et à remplir votre table (à force d'insérer des éléments, il y aura un moment où la table sera entièrement remplie, donc il faudra gérer cette situation, soit par une erreur, soit en rallongeant le tableau).
- L'autre, c'est d'utiliser des listes chaînées : chaque case contient une liste chaînée d'éléments. Quand il y a une collision, on rajoute simplement le nouvel élément au bout de la liste chaînée qui est dans sa case. L'avantage c'est que vous pouvez rajouter des éléments à l'infini sans toucher au tableau de base, et une collision ne se propagera pas ; l'inconvénient, c'est que ça prend nettement plus d'espace et de temps, et plus il y a d'éléments, plus ça en prend.

Dans les deux cas, c'est ce qui contribue au pire cas en O(n) : en moyenne, si la fonction de hash est correcte, on est sur du Θ(1), mais plus il y a de collisions, moins les performances sont bonnes, jusqu'au pire cas où toutes les clés vont au même index, ce qui donne O(n)

Une table de hash est donc fondée sur plusieurs compromis :

- Le choix de la taille du tableau est un compromis entre temps et espace : statistiquement, plus il y a de place, moins il y aura de collisions, mais plus il y aura de cases vides
	- Il y a aussi le problème de la croissance de la table : au bout d'un moment, il peut être plus intéressant de prendre du temps pour agrandir le tableau et réassigner les éléments existants plutôt que de pourrir les performances en continuant à les empiler les uns sur les autres dans un tableau trop petit.
	- La solution typique, c'est d'avoir un paramètre de charge maximale : arrivé à un certain nombre d'éléments par rapport à la taille du tableau, on augmente la taille du tableau (en la doublant par exemple). Par exemple, agrandir quand 75% des cases sont occupées (ou quand le nombre d'éléments dépasse 75% de la capacité du tableau).
- La fonction de hash est un élément très important mais aussi très compliqué à bien concevoir : il est parfaitement impossible d'empêcher totalement les collisions, mais il faut que les hashes soient distribués de façon aussi uniforme que possible : tous les hashes doivent avoir à peu près la même probabilité d'apparaître, il ne faut pas que la moitié des clés possibles finissent au même index
	- C'est un problème très compliqué sur lequel il y a des milliers d'articles — la vérité c'est que c'est très dépendant des caractéristiques exactes de vos clés.
	- Si vous cherchez à hasher des nombres entiers quelconques, il suffit d'utiliser le nombre comme hash, c'est déjà uniforme par définition.
	- Souvent, on cherche à hasher des chaînes de caractères — pour ça vous pouvez prendre à peu près n'importe quoi qui utilise tout le contenu de la chaîne de caractères, ça fera souvent une fonction tout à fait correcte. Par exemple, beaucoup de librairies et de langages utilisent [SipHash](https://github.com/veorq/SipHash), mais si vous n'avez pas besoin de quelque chose de parfaitement sûr et bien distribué, une congruence linéaire ou quelques bidouilles bit par bit sont bien suffisantes. Par exemple :

	```c
	unsigned int hash_string_Kernighan_Ritchie(const char* string) {
		unsigned int result = 0;
		for (int i = 0; string[i] != '\0'; i++)
			result = result * 13131 + string[i];
		return result;
	}

	unsigned int hash_string_Knuth(const char* string) {
		size_t length = strlen(string);
		unsigned int result = length;
		for (int i = 0; i < length; i++)
			result = ((result << 5) ^ (result >> 27)) ^ string[i];
		return result;
	}
	```
- Le troisième compromis est sur la gestion des collisions :
	- Listes chaînées : plus lourd en mémoire et en traitements, mais pas de propagation des collisions
	- Case suivante : plus performant, mais la table se remplit plus vite et les collisions peuvent se propager
