//// title = "Séquences"
//// descriptions = "Les structures de données séquentielles"

# {=title}

## Abstraction

Il est parfois possible de s'absoudre totalement des différents types de séquence — cependant, dans l'implémentation, les performances sont très différentes, et certains types manquent de certaines opérations (insertion dans un tableau par exemple)

Une **liste** (au sens générique) est une séquence d'éléments. Elle a un **sens** (elle commence d'un bout et continue jusqu'à la fin), et un **ordre** (les éléments sont organisés d'une certaine façon, sans ambigüité). Une liste a donc plusieurs propriétés :

- On peut **accéder** à un élément particulier par sa **position** dans la liste : c'est le concept d'**indexation**.
- On peut **itérer** dessus (effectuer une opération sur chaque élément de la liste successivement)

On définit généralement un certain nombre d'opérations sur une liste abstraite, mais il faut être conscient qu'elles sont *très différentes* selon la vraie structure de données qui sera utilisée.

- **Lire** un élément par sa **position** (son index)
- **Écrire** un élément par sa **position**
- **Insérer** un élément (souvent en tête ou en queue de la liste, mais ça peut être n'importe où du moment qu'on sait la position où on veut insérer)
- **Supprimer** un élément (idem)

Il y a deux conceptions possibles de la liste :

- La conception « itérative » : la liste est une suite d'éléments les uns après les autres, accessibles par leur position. Cette conception est prédominante dans les langages impératifs.
- La conception « récursive » : la liste est constituée de son premier élément (la « tête »), et du reste. Pour la traiter, on appelle une fonction qui traite la tête, et qui s'appelle récursivement sur le reste de la liste (donc qui traite la tête du reste, et ainsi de suite). Cette conception est prédominante dans les langages déclaratifs (notamment fonctionnels).

{!svg: info/algo/concepts-list.svg}

## Tableaux

Un **tableau** est une séquence **fixe**. Il est représenté par une **zone mémoire unique** où les éléments sont écrits de façon **contigüe**. Les opérations ont ces spécificités :

- L'**accès par index** est en **temps constant** O(1). Comme tout est contigu en mémoire, il suffit de faire `début du tableau + taille d'un élément × index` quel que soit l'index.
- L'**insertion** et la **suppression** sont soit **impossibles**, soit lourdes. En effet, si on veut insérer ou supprimer un élément, il faut décaler d'une place tous ceux qui se trouvent après. De plus, la zone mémoire allouée est généralement fixe, donc pour changer sa taille, il faut en **allouer une nouvelle et recopier le contenu** dans la nouvelle, ce qui vient avec une complexité en O(n) et beaucoup de temps perdu en gestion de la mémoire. Il est possible de réduire cet effet en allouant du rab et en gardant la taille effective du tableau en plus de la taille allouée, pour supporter quelques insertions et délétions avant d'avoir à réallouer, au prix d'un peu de gaspillage de mémoire.

{!svg: info/algo/array.svg}

Implémentations dans quelques langages :

- C : Simples tableaux (`type[taille]`). Gestion de la mémoire manuelle
- C++ : Simples tableaux, ou `std::vector` qui gère la mémoire automatiquement et permet les insertions/délétions
- Java : `ArrayList`, gère tout automatiquement
- Python : Les listes de base du langage (`list`) ont toutes les opérations possibles et imaginables sur une liste (insertion, délétion, extension, retournement, …) mais ont à peu près les complexités algorithmiques d'un tableau. `array.array` et les tableaux numpy sont plus nettement des tableaux typés.
- JavaScript : Les *typed arrays* et `ArrayBuffer` permettent ce genre de trucs mais ne sont pas vraiment faits pour, c'est plutôt pour la manipulation de buffers binaires

## Listes chaînées

Une **liste chaînée** est une structure où chaque élément est séparé en mémoire et **pointe sur le suivant**. Ça prend un peu plus de mémoire et ça rallonge certaines opérations, mais ça rend la liste entièrement dynamique, donc l'insertion et la délétion deviennent nettement plus simple.

- L'accès par index dépend de l'index : il faut parcourir toute la liste jusqu'à l'index pour obtenir l'élément, donc ça devient du O(n) en moyenne
- L'insertion et la suppression deviennent possibles sans problème de mémoire vu que tout est dynamique. Si vous avez déjà l'élément précédent, c'est du O(1), sinon il faudra remonter la liste avant. Les opérations en tête de liste sont triviales.

{!svg: info/algo/linked-list.svg}

Implémentations :

- C : Implémentation manuelle
- C++ : `std::list`
- Java : `LinkedList`
- Python : `collections.deque` (les listes de base peuvent faire tout ce que font les listes chaînées mais ont bien la performance d'un tableau)
- JavaScript : `Array` (les listes de base du langage)

### Types de chaînage

Il y a aussi un choix à faire dans le chaînage de la liste. Une liste peut être :

- **Simplement chaînée** : le chaînage n'est que dans un sens. Dans une liste classique chaque élément pointe seulement sur l'élément avant lui (ou éventuellement sur l'élément précédent dans des cas particuliers comme une pile)

;;; code ```c
typedef struct _element_s {
	type valeur;
	struct _element_s* suivant;
} element_t;```
;;;

- **Doublement chaînées** : chaque élément pointe sur les éléments avant et après lui. Ça rend possible la navigation dans les deux sens et simplifie certaines opérations (recherche binaire et certains tris par exemple). Ça échange de la mémoire pour du temps. Toutes les implémentations standard listées ci-dessus sont doublement chaînées.

;;; code ```c
typedef struct _element_s {
	type valeur;
	struct _element_s* precedent;
	struct _element_s* suivant;
} element_t;```
;;;
