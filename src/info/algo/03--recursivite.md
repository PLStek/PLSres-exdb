//// title = "Récursivité"
//// description = "Le concept et l'utilisation de la récursivité"

# {=title}

Une fonction **récursive** est une fonction qui s'appelle elle-même. C'est une conception très différente des algorithmes, qui permet de rendre certains algorithmes beaucoup plus naturels, notamment ceux qui parcourent des structures de données récursives (arbres, graphes). Ça peut aussi permettre d'isoler l’étape de traitement elle-même, ce qui peut avoir ses avantages en termes de modularité.

## Utilisation

La récursivité est une façon différente de concevoir un algorithme.

Déjà, à moins de travailler sur un langage qui nécessite ce genre de représentation (langages fonctionnels, typiquement), il faut réfléchir à la **pertinence** d'un algo récursif — pas la peine de se casser le tronc si la version itérative est plus simple. Ça se voit très vite quand un algorithme est plus naturel en récursif, quand l'itératif semble inutilement compliqué, avec une pile explicite, ou pour parcourir une structure de données récursive (arbres, …).

Et ensuite, il y a deux choses à assurer :

- Que l'algo **fait** bien **ce que vous voulez**. Pour cela, il faut réussir à le découper en étapes similaires, et bien se rendre compte de quelles infos vont où pour bien faire ce que vous comptez faire
- Que l'algo se **termine**. Vous faites une fonction qui s'appelle elle-même, il faut bien arriver à un point où elle retourne sans s'appeler elle-même, sinon ça fera une récursion infinie. Il faut donc identifier le **cas terminal**, souvent trivial, qui termine le processus.

;;; example ```
# Cas d'école : la version récursive de la factorielle
Fonction factorielle(opérande:entier positif) -> entier
	# Cas terminal : on est tombé à zéro, la factorielle vaut 1
	Si opérande = 0:
		Renvoyer 1
	# Cas général : on multiplie par le résultat de la factorielle de l'opérande - 1
	Sinon:
		Renvoyer opérande * factorielle(opérande - 1)```
;;; example ```
# Cas plus réel : quicksort
# Ici les modifications sont faites sur place, donc pas de valeur de retour
Fonction triRapide(valeurs:tableau d'objets comparables)
	# Le cas terminal c'est quand indexFin = indexDébut, où on ne fait rien
	# Cas général : on trie un segment
	Si indexFin - indexDébut > 1:
		pivot <- tableau[indexFin-1]
		indexPivot <- indexDébut - 1
		Pour i allant de indexDébut à indexFin-2:
			Si tableau[i] <= pivot:
				indexPivot <- indexPivot + 1
				échanger tableau[indexPivot] avec indexPivot[i]
		indexPivot <- indexPivot + 1
		échanger tableau[indexPivot] avec tableau[indexFin-1]
		triRapide(tableau, indexDébut, indexPivot)
		triRapide(tableau, indexPivot+1, indexFin)```
;;;

{!exercise: info.algo.iterative-to-recursive}

{!exercise: info.algo.flood-fill}

## Performance

Il existe un théorème simple en informatique théorique :

;;; doc
Pour tout algorithme récursif, il existe un algorithme itératif équivalent au moins aussi efficace.
Pour tout algorithme itératif, il existe un algorithme récursif équivalent au plus aussi efficace.
;;;

En fait, un algorithme récursif exploite ce qu'on appelle la **pile d'appel**. Un algorithme récursif peut donc être converti en itératif simplement en utilisant une pile explicite au lieu d'utiliser implicitement la pile d'appel, et un algorithme itératif peut être converti en récursif vu que l'itération implique toujours plus ou moins une séquence, qui peut être implicitée dans une fonction récursive.

Ça veut aussi dire qu'un algorithme récursif aura une performance inférieure ou égale à son équivalent itératif — en fait, dans l'immense majorité des cas, la complexité algorithmique est strictement la même entre les deux, à part pour les algos où il faut vraiment beaucoup bidouiller pour les passer en récursif. Le seul cas courant, c'est dans les algos à accumulateur (on a une seule variable qui stocke le résultat, où chaque itération écrase le résultat de la précédente). Ça fait une complexité en espace de O(1) en itératif, mais comme le récursif doit déployer une pile et mettre la variable dessus, ça étendra la complexité en espace à O(n) — encore que les compilateurs C/C++ peuvent parfois optimiser ça.

En fait le principal problème est l'exécution elle-même. Dans le monde de la réalité véritable, appeler une fonction, allouer son espace sur la pile, l'exécuter, désallouer l'espace et revenir à la fonction appelante prend du temps. De plus trop de récursions peut dépasser la taille maximale de la pile (le fameux *stack overflow*).
Il faudra donc faire attention à ces détails.

- En C/C++, ces choses-là peuvent être largement optimisées à la compilation. En particulier, la *récursion en queue* (où l'appel récursif est la dernière opération dans la fonction) sera optimisée très efficacement, autant qu'en itératif. Même si ce n'est pas problématique en général, la taille de la pile est limitée (sous Linux c'est typiquement 8 Mio d'après `ulimit -s`, sous OSX souvent moins), donc si vous faites trop d'appels récursifs, en particulier avec beaucoup de données locales dans la fonction, le programme crashera avec une erreur `stack overflow`. Par exemple, si vous avez 100 octets de variables locales, 8 Mio de pile autorise grand maximum 83 000 appels récursifs.
- En Java, les appels récursifs ne sont jamais optimisés, donc ça peut causer une légère perte de temps. La taille de la pile est aussi limitée, mais vous avez quand même quelques milliers d'appels récursifs avant la `StackOverflowException`.
- En Python, les appels récursifs ne sont pas optimisés, et peuvent causer une légère perte de temps (qui peut chiffrer s'il y en a beaucoup). Le nombre d'appels récursifs est limité, par défaut c'est une valeur très sécuritaire (typiquement 1000 appels récursifs). Vous pouvez la changer avec `sys.setrecursionlimit(nb_appels)`, mais à vos risques et périls (ça peut causer un vrai *stack overflow* si vous allez trop loin)
