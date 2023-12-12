//// title = "Piles et files"
//// description = "Les structure FIFO et LIFO"

# {=title}

Les piles et les files sont des structures qui fonctionnent un peu comme des listes, mais où on ne manipule que les extrémités d'une façon particulière.

Des piles et des files bien implémentées on des complexités en O(1) pour l'empilement/enfilement et le dépilement/défilement d'un élément. Même si vous pouvez utiliser n'importe quelle liste comme une de ces structures, selon l'implémentation de la liste les performances peuvent être plus faibles.

## Piles

Une pile (stack en anglais) est une structure dite *LIFO* : Last In, First Out (dernier arrivé, premier sorti). Ça fonctionne comme une pile d'objets : on ne peut rajouter ou retirer des éléments qu'en haut de la pile.

{!svg: info/algo/stack.svg}

La pile est une structure très importante mais qu'on manipule rarement directement : en fait, tous les algorithmes récursifs s'appuient implicitement sur une pile (dont le rôle est joué par la pile d'appels).

Implémentations dans différents langages :

- C : Implémentation manuelle
- C++ : `std::stack` ou `std::deque`
- Java : Soit `Stack` (qui peut être plus lente parce qu'elle est synchronisée), ou les implémentations de l'interface `Deque` (`ArrayDeque`, `LinkedList`, …)
- Python : `collections.deque`, en utilisant juste les méthodes `.append()` et `.pop()`
- JavaScript : Il faudra bidouiller avec les tableaux de base du langage.

## Files

Une file (queue en anglais) est une structure *FIFO* : First In, First Out (premier arrivé, premier sorti). C'est comme une file d'attente : les éléments sortent dans l'ordre où ils arrivent. Concrètement, on rajoute les nouveaux éléments d'un côté, et on en sort de l'autre.

{!svg: info/algo/queue.svg}

Les files sont très importantes aussi, peut-être moins en algorithmique, mais partout où il y a besoin de mettre des choses en attente (typiquement des tâches à effectuer ou des évènements à traiter). D'un point de vue purement algorithmique, ça sert par exemple au parcours en largeur des arbres.

- C : Implémentation manuelle
- C++ : `std::queue` ou `std::deque`
- Java : Les classes qui implémentent l'interface `Queue` (`ArrayDeque`, `LinkedList`, …)
- Python : `collections.deque`, avec par exemple `.appendleft()` pour enfiler et `.pop()` pour défiler

## Deque

Ce qu'on appelle un *deque* (pour Double-Ended QUEue), est une généralisation d'une file, sur laquelle insérer et retirer des éléments aux deux extrémités a une complexité en O(1). Ça fait que vous pouvez utiliser un deque à la place des structures dédiées pour les piles et les files (d'ailleurs en C++, `std::stack` et `std::queue` sont juste des wrappers autour d'un deque).

{!svg: info/algo/deque.svg}

- C : Implémentation manuelle
- C++ : `std::deque`
- Java : Les classes qui implémentent l'interface `Deque` (`ArrayDeque`, `LinkedList`, …)
- Python : `collections.deque`

## File à priorités

Une file à priorité est un peu comme une file (on met en file et on récupère des éléments), sauf que chaque élément est associé à une *priorité*, et les éléments sont défilés dans l'ordre de leurs priorités. C'est notamment utile pour les files d'attentes de tâches avec des priorités différentes, ou bien pour optimiser certains algorithmes (comme l'algorithme A*, pour trouver le plus court chemin dans un graphe).

{!svg: info/algo/priority-queue.svg}

Il y a diverses implémentations pour les files à priorités, vu qu'une simple liste aurait des performances désastreuses. Par exemple :

- Un *tas* (une structure basée sur des arbres) donnera généralement du O(1) pour lire le prochain élément et O(log n) pour défiler et insérer
- Une *skip list* (une structure probabiliste basée sur des listes) aura du O(log n) pour rechercher, défiler et insérer. Habituellement, les tas sont plus pratiques, mais la skip list permet l'accès en lecture et écriture en parallèle de façon beaucoup plus efficace.

- C : Implémentation manuelle
- C++ : `std::priority_queue`
- Java : `PriorityQueue`
- Python : Le module `heapq` permet de gérer une liste classique comme un tas
- JavaScript : Implémentation manuelle ou librairie tierce
