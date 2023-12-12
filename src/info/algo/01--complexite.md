//// title = "Complexité algorithmique"
//// description = "Description rapide du concept de complexité algorithmiques et notations"

# {=title}

La **complexité algorithmique** est un concept vaste et compliqué, mais qui est essentiel pour comprendre l'algorithmique en général. En effet, si on utilise un algorithme ou une structure de données plutôt qu'une autre, c'est parce qu'elle est plus performante dans notre cas d'utilisation — mais pour ça il faut savoir ce qu'on appelle la *complexité algorithmique*

## Concept

On distingue deux complexités différentes :

- La **complexité en temps**, le temps que prend l'algorithme à s'exécuter
- La **complexité en espace**, la quantité de mémoire qu’il occupe.

Fondamentalement, la complexité en temps d'un algorithme est le nombre d'opérations élémentaires nécessaires pour le mener à bien.
Par contre compter les opérations c'est pas pratique (c'est quoi une « opération élémentaire » ?) et c'est pas si utile que ça pour comparer des algos entre eux.
Donc ce qu'on fait généralement, c'est calculer la complexité *asymptotique*.

En général, quand on cherche à comparer des algorithmes, ce sont des algorithmes qui prennent des **données en entrée**, et qui les **traitent**. Et en général, la complexité est une **fonction** directe de la **taille des données** en entrée : par exemple, un algorithme qui trie une liste de `n` éléments aura une complexité qui est fonction de cette longueur `n`. Pareil pour la complexité en espace (l'espace mémoire occupé en fonction des données en entrée). Souvent, on peut sacrifier de l'espace mémoire au profit du temps d'exécution, ou inversement.

De là, on a la complexité, qui est fonction de la taille des données en entrée. On étudie donc la croissance du temps ou de la mémoire pris quand la taille des données augmente. Du coup, on étudie la complexité *asymptotique*, qui élimine les paramètres négligeables quand $$n$$ augmente. Typiquement, un algorithme de tri efficace a une complexité en temps qui croît en $$n \cdot \log{n}$$ : ça peut être quelque chose comme $$14 \cdot n \cdot \log_{2}{n} + 144 \cdot \log_{2}{n} + 23$$, mais quand $$n$$ augmente, la partie $$144 \cdot \log_{2}{n}+23$$ devient parfaitement négligeable par rapport au reste. De plus, le facteur 144 est une question de point de vue, selon ce qu’on appelle une « opération élémentaire », donc on l’enlève aussi. La base du logarithme est aussi une constante multiplicative, donc pareil. Au final, notre complexité devient ainsi $$O(n \cdot \log{n})$$.

## Notations

À partir de là, on introduit plusieurs notations pour écrire ces complexités. C'est la notation *big-O* et ses dérivées, qui ont la signification suivante :

- $$O(f(n))$$ : la complexité asymptotique est inférieure ou égale à $$C \cdot f(n)$$ (où C est un facteur quelconque). Par exemple, un algorithme en $$O(n^2)$$ est un algorithme dont la complexité croît au plus aussi vite que $$n^2$$, à un facteur près.
- $$\Theta(f(n))$$ : la complexité asymptotique est comprise entre $$C_1 \cdot f(n)$$ et $$C_2 \cdot f(n)$$ (pour des facteurs C₁ et C₂ quelconques). Autrement dit, une complexité en $$\Theta(n \cdot \log{n})$$ signifie que tous les cas de figure ont une croissance en $$n \cdot \log{n}$$
- $$\Omega(f(n))$$ : la complexité asymptotique est supérieure ou égale à $$C \cdot f(n)$$. Un algorithme en $$\Omega(n)$$ est un algorithme dont le cas le plus favorable croît de façon linéaire.

En pratique, on parle surtout en $$O(f(n))$$, et éventuellement en $$\Theta(f(n))$$ quand on peut aussi dire que tous les cas suivent la même loi. Le reste se voit de temps en temps, mais moins. Par exemple, on dira que l'algorithme de tri rapide a une complexité moyenne en $$O(n \cdot \log{n})$$, un pire cas en $$O(n^2)$$ quand la liste est déjà triée ou presque, et un meilleur cas en $$O(n \cdot \log{n})$$ pour la plupart des implémentations.

Notez bien que ce n'est pas toujours pertinent pour de petites valeurs de *n*, vu que l'*overhead* (les coûts constants incompressibles, par exemple la préparation de l'algorithme, les traitements finaux) peuvent devenir plus longs que l'algorithme lui-même quand les données en entrée sont très petites.

### Classes de complexité

Comme on donne juste une version très réduite de la fonction de croissance, on retrouve toujours plus ou moins les mêmes complexités. Pour se rendre compte :

| Complexité | Nom                       | n = 5 | n = 10 | n = 50 | n = 100 | n = 1000 | Exemples                                                             |
| ---------- | ------------------------- | ----- | ------ | ------ | ------- | -------- | -------------------------------------------------------------------- |
| O(1)       | Complexité constante      |     1 |      1 |      1 |       1 |        1 | Accès à une case de tableau, dépilement d'une valeur sur une pile, … |
| O(log(n))  | Complexité logarithmique  | {=round(log2(5))} | {=round(log2(10))} | {=round(log2(50))} | {=round(log2(100))} | {=round(log2(1000))} | Recherche dichotomique, insertion dans un tas |
| O(n)       | Complexité linéaire       |     5 |     10 |     50 |     100 |    1000 | Parcours de liste, meilleur cas du tri à bulles                      |
| O(n·log(n))| Complexité linéarithmique | {=round(5*log2(5))} | {=round(10*log2(10))} | {=round(50*log2(50))} | {=round(100*log2(100))} | {=round(1000*log2(1000))} | Tri optimal, FFT (transformée de Fourier rapide)       |
| O(n²), O(n³), … | Complexité polynomiale | {=5**2} | {=10**2} | {=50**2} | {=100**2} | {=1000**2} | Parcours de tableau multi-dimensionnel, produit matriciel            |
| O(2ⁿ), O(eⁿ), … | Complexité exponentielle | {=2**5} | {=2**10} | {=2**50:g} | {=2**100:g} | *infini* | Décomposition en facteurs premiers, problème du voyageur de commerce (en gros la plupart des algos où on doit tester toutes les possibilités) |
| O(nᵃ·bⁿ)   |                           | {=2**5*5**2} | {=2**10*10**2} | {=2**50*50**2:g} | *infini* | *infini* | Beaucoup de problèmes dont l'approche naïve a une complexité factorielle (voyageur de commerce, distance de levenshtein, …) peuvent se réduire à quelque chose comme ça grâce à la programmation dynamique |
| O(n!)      | Complexité factorielle    | {=factorial(5)} | {=factorial(10)} | *infini* | *infini* | *infini* | Problèmes combinatoires, bogosort                |

(Quand c'est écrit *infini*, c'est que même si une unité correspond à une picoseconde ça fait plus long que l'âge de l'univers)

## Analyse de la complexité

Il y a différentes façon d'analyser la complexité d'un algorithme, et toutes ont leurs propres avantages et inconvénients :

- Le plus souvent, on parle du **pire cas**. Ce n'est pas déconnant vu qu'on doit souvent s'attendre au pire.
- On peut aussi parler du **meilleur cas**, le cas le plus favorable. C’est utile quand on en est généralement proche ou quand il y a des techniques pour être sûr de s’en approcher.

Le meilleur cas est rarement significatif pour la conception d'un programme, mais parfois, le **pire cas** est **très pessimiste** : par exemple, dans une table de hash, le pire cas est en O(n), mais c'est si absolument tous les éléments causent une collision, ce qui est parfaitement absurde dès lors que la fonction de hash est à peu près correcte – l'immense majorité des cas seront en temps constant ou presque. On a donc deux autres mesures, parfois plus représentatives :

- La complexité **moyenne** : on fait la moyenne de toutes les situations possibles. Autrement dit, pour des données parfaitement aléatoires en entrée, quelle est la complexité moyenne en fonction de la taille des données.
- La complexité **amortie** : on calcule la complexité moyenne des *suites d'opérations* qui peuvent arriver. Certaines structures de données peuvent avoir des situations de pire cas de temps en temps, mais avoir *un* pire cas rend très improbable un nouveau dans un avenir proche (ou pas, justement). Donc juste s'intéresser au pire cas est très pessimiste, et la complexité moyenne est très compliquée à calculer à cause de l'état qui se garde entre les opérations. En général, on va voir les séries d'opérations possibles, et prendre la moyenne sur ces séries.

La différence entre les deux, c'est que la complexité moyenne est *ponctuelle* (on prend chaque possibilité de façon isolée et on prend la moyenne de toutes), alors que la complexité amortie tient compte d'un *état* (on calcule sur une suite d'opérations)

;;; doctext
Pour comprendre la complexité amortie, prenons l'exemple d'un tableau extensible. Il y a deux cas possibles quand on ajoute un nouvel élément en queue du tableau :

- Soit la capacité actuelle est suffisante, et c'est juste un accès au tableau — O(1)
- Soit il faut étendre le tableau, donc généralement allouer une nouvelle zone mémoire et y recopier tout le contenu du tableau — O(n)

Le pire cas est donc en O(n), mais dire que l'insertion en queue se fait en O(n) serait un peu réducteur, on n'a pas à étendre le tableau à tous les coups. Alors quelle est la performance qu'on peut attendre d'un usage normal du tableau ? Et comment va-t'on augmenter la taille du tableau le moment venu de la façon la plus efficace possible ? Pour savoir ça, on va calculer la **complexité amortie**.

**Premier cas : incréments constants**

Mettons que quand le tableau est plein, on l'étend d'un nombre de cases constants qu'on appellera *T*. *p* peut être n'importe quel entier. La suite des complexités pour chaque opération est la suivante :

$$C_i = \left\{
	\begin{aligned}
		& i+1 \text{ si } i = T \times p \\
		& 1 \text{ sinon }
	\end{aligned}
\right.$$

La somme des Cᵢ est donc décomposable en deux sommes : la somme des 1 (1 opération par insertion, donc *n* en tout), plus la somme des recopies, qui font chacune *i* opérations toutes les *T* insertions. Autrement dit, quand $$(p-1) \times T < n \leq p \times T$$, il y a eu exactement $$p-1$$ extensions avant d'atteindre *n*, donc :

$$\begin{aligned}
\sum_{i=1}^n C_i & = n + \sum_{j=1}^{p-1} T \times j \\
                 & = n + T \times \sum_{j=1}^{p-1} j \\
                 & = n + T \times \frac{(p-1)((p-1)+1)}{2} \\
                 & = n + T \times p(p-1)
\end{aligned}$$

*p* est juste *n* à un facteur près, d’où :

$$\begin{aligned}
(p-1) \times T < n \leq p \times T & \Rightarrow (p-1) \times T + T < n + T \leq p \times T + T \\
                                   & \Rightarrow p \times T < n+T \leq (p+1) \times T \\
								   & \Rightarrow p < \frac{n+T}{T} \leq p+1
\end{aligned}$$

Et on avait déjà $$T \times (p-1) < n$$, donc on peut majorer $$n + T \times p(p-1)$$ par $$n + n \times p$$. On peut donc majorer notre somme :

$$\begin{aligned}
\sum_{i=1}^n C_i & = n + T \times p(p-1) \\
                 & < n + n \times p \\
				 & < n + n \times \frac{n+T}{T} \\
				 & < n + \frac{n^2}{T} + \frac{T \times n}{T} \\
				 & < \frac{n^2}{T} + 2n
\end{aligned}$$

Ce qu’on a là, c'est la somme sur toute la série d’opérations, on divise donc par *n* pour avoir la moyenne par opération :

$$\frac{\frac{n^2}{T} + 2n}{n} = \frac{n}{T} + 2 = O(n)$$

Ayayaïe : notre complexité amortie est en O(n), c'est pas terrible. Voyons donc une autre solution.

**Deuxième cas : doublement**

Cette fois, on double la taille du tableau chaque fois qu'on a besoin de l'étendre. *n* est toujours le nombre d'insertions qu'on veut réaliser, et *p* peut être n'importe quel entier :

$$C_i = \left\{
	\begin{aligned}
		& 2^p + 1 \text{ si } i = 2^p + 1 \\
		& 1 \text{ sinon }
	\end{aligned}
\right.$$

Donc si on fait la somme de 1 à n, on peut décomposer ça en deux sommes : les accès au tableau pour écrire la nouvelle valeur, qui valent tous 1, et qui sont à toutes les insertions, donc ça fait *n* en tout ; et les copies, qui sont quand *i* dépasse la taille du tableau, donc quand il vaut une valeur du type $$2^p + 1$$. Donc si on prend un entier *p* tel que $$2^(p-1) < n \leq 2^p$$, ça fait exactement p-1 doublements avant d'atteindre *n*, qui coûtent à chaque fois le nombre d'éléments dans le tableau, soit $$2^p$$. C'est donc la suite des puissances de 2, de 1 à p-1

$$\begin{aligned}
\sum_{i=1}^n C_i & = n + \sum_{j=1}^{p-1} 2^j \\
                 & = n + 2^p - 2
\end{aligned}$$

On a dit que $$2^{p-1} < n \leq 2^p$$, donc $$2 \times 2^{p-1} < n \leq 2 \times 2^p \Rightarrow 2^p < n < 2^{p+1}$$. D'où on tire :

$$\begin{aligned}
\sum_{i=1}^n C_i & = n + 2^p - 2 \\
                 & < n + 2n \\
				 & < 3n
\end{aligned}$$

On a donc un coût inférieur à 3n pour *n* opérations, soit un coût moyen par opération inférieur à 3 : la complexité amortie de nos insertions est en temps constant, O(1).
;;;

## Évaluer la complexité

Toute cette algèbre est très chouette, mais c'est des choses qu'on fait rarement nous-même, vu que ça s'applique plutôt à des structures de données qui existent déjà et qu'on ne fait qu'implémenter. Sur des algorithmes, il est souvent assez facile d'évaluer la complexité. En règle générale :

- Si vous itérez sur les données en entrée, c'est du O(n)
- Des boucles imbriquées font du polynomial (deux boucles imbriquées ⇒ O(n²), tableau en 3D ⇒ O(n³), …)
- Une approche « diviser pour régner » pertinente fera du O(log n) (quand on répète *n* fois une opération en O(log n), ça fait du O(n·log n), comme les tris)
- Si vous testez toutes les possibilités (bruteforce), c'est probablement exponentiel
- Tester toutes les combinaisons possibles des éléments fera du factoriel. Si vous ne pouvez pas suivre une approche **heuristique** (appliquer une stratégie qui nous donnera beaucoup plus efficacement un *bon* résultat, quitte à ne pas forcément avoir le *meilleur* résultat), regardez du côté de la *programmation dynamique* qui permet d'arranger un peu ça, au prix de plus de mémoire.

## Le bon sens

On fait plein de belles choses avec les analyses de complexité, mais il faut bien se rappeler de ce qu'on fait, de nos besoins, de nos contraintes, et de ce qu'on essaie de calculer.

Par exemple, il ne faut pas oublier qu'on parle de complexité *asymptotique*, donc quand *n* devient grand c'est très vite valable, mais si c'est juste pour trier des listes de 3 éléments, un quicksort perdra beaucoup de temps en manipulations incompressibles alors qu'un tri par insertion ou par sélection, malgré son cas moyen en O(n²) bien crade, sera en pratique bien plus efficace.

Autre situation : dans l'exemple du tableau extensible ci-dessus, on parle beaucoup de la complexité en temps, comme quoi doubler à chaque fois plutôt qu'étendre par incréments constants est plus rapide. Mais si on parle de complexité en espace, les deux solutions ont la même complexité spatiale en O(n), et pourtant il est évident qu'en général, doubler à chaque extension gaspillera nettement plus de mémoire. Si la mémoire est un problème, il y a une réflexion à avoir.

Il ne faut jamais perdre de vue ses contraintes et ses objectifs, et bien se dire que la complexité est un indice pour comparer des algorithmes entre eux, mais ce n'est ni une indication directe des performances de votre programme, ni une confirmation universelle qu'une méthode est plus efficace qu'une autre.
