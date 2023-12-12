//// title = "Comparatif des complexités"
//// description = "Petit comparatif rapide de quelques structures de données courantes"

# {=title}

## Listes

Structures de données comparées :

- **Tableau** : Valeurs contiguës en mémoire, impossible d'étendre directement la zone mémoire sans la réallouer. Ici on parlera d'un tableau dynamique, donc qui double de taille et recopie dans la nouvelle zone mémoire quand la capacité est dépassée. Un tableau fixe a les mêmes complexités, sauf qu'on ne peut pas insérer ou supprimer.
	- C : simple tableau (`int tableau[TAILLE];`)
	- C++ : `std::vector`
	- Java : `ArrayList`
	- Python : `list` (`[1, 2, 3]`)
- **Liste chaînée** : Chaque élément pointe sur le suivant. Pour ces opérations, que la liste soit simplement ou doublement chaînée ne change rien, c'est surtout pour les algorithmes où on a besoin de naviguer dans la liste que ça change beaucoup.
	- C++ : `std::list`
- **Liste doublement terminée** : Une liste doublement chaînée, où on garde les pointeurs vers le premier et le dernier élément au lieu de seulement le premier. Principale implémentation du *deque*. Les pires cas ont le même big-O, mais concrètement les complexités sont divisées par 2
	- C++ : `std::deque`
	- Java : `LinkedList`
	- Python : `collections.deque`

| Opération             | Tableau | Liste chaînée  | Liste doublement terminée |
| --------------------- | ------- | -------------- | ------------------------- |
| Accès par index       | O(1)    | Meilleur : O(1) (en tête)\ Moyen/Pire : O(n) | Meilleur : O(1) (en tête ou en queue)\ Moyen/Pire : O(n) (pire cas au milieu) |
| Insertion en tête     | O(n) (décalage de tout le tableau) | O(1) | O(1) |
| Insertion en queue    | Amorti : O(1)\ Pire : O(n) (quand il faut augmenter la capacité) | O(n) | O(1)
| Insertion par index   | O(n)    | O(n) | O(n) |
| Suppression en tête   | O(n) (décalage de tout le tableau) | O(1) | O(1) |
| Suppression en queue  | O(1)    | O(n) | O(1) |
| Suppression par index | O(n)    | O(n) | O(n) |

## Ensembles et tables associatives

- **Table de hash** : Tableau dans lequel on trouve les index avec une fonction de hash. Les implémentations avec listes chaînées et sans listes chaînées ont les mêmes complexités asymptotiques, celles avec listes chaînées sont un peu plus lourdes en temps et en mémoire mais demandent d'augmenter la capacité moins souvent. À la base, une table de hash n'est *pas* ordonnée.
	- Java : `HashSet`, `HashMap`
	- Python : `dict`, `set`, `frozenset`
- **Arbre binaire de recherche naïf** : Arbre binaire de recherche simple, sur lequel on n'applique aucune stratégie pour le garder équilibré. Un arbre binaire de recherche donne un ensemble ordonné.
- **Arbre binaire de recherché équilibré** : Arbre binaire de recherche qu'on garde équilibré. Ça élimine les pires cas et ça améliore le cas moyen, mais n'oubliez pas que ça fait plus de maintenance quand on insère des éléments
	- C++ : `std::set`, `std::map`
	- Java : `TreeSet`, `TreeMap`
- **Liste chaînée** : Pour comparer, une implémentation naïve qui utiliserait une liste chaînée comme un ensemble. Ne faites pas ça en vrai.

| Opération         | Table de hash | Arbre naïf | Arbre équilibré | Liste chaînée |
| ----------------- | ------------- | ---------- | --------------- | ------------- |
| Accès / Recherche | Moyen : O(1)\ Pire cas : O(n) (table complètement dégénérée, insignifiant en pratique si la fonction de hash est correcte) | Moyen : O(log n)\ Pire : O(n) (arbre dégénéré) | Moyen/Pire : O(log n) | Moyen/Pire : O(n) |
| Suppression       | Moyen : O(1)\ Pire cas : O(n) (table totalement dégénérée) | Moyen : O(log n)\ Pire : O(n) (arbre dégénéré) | Moyen/Pire : O(log n) | Moyen/Pire : O(n) |
| Insertion         | Moyen : O(1)\ Pire cas : O(n) (table totalement dégénérée) | Moyen/Pire : O(log n) | Moyen/Pire : O(log n) | O(1) |
