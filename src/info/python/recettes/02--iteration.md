//// title = "La puissance des itérateurs"
//// description = "Exploiter les itérateurs et l'itération avancée pour des programmes plus courts et plus efficaces"

# {=title}

Une bonne partie de la puissance de Python vient de tous les itérateurs qu'il propose. Ici on utilisera surtout des fonctions disponibles de base, et le module `itertools`.
Pour cette section il est impératif de comprendre le concept d'*itérateur* : certaines fonctions renvoient une conteneur, mais la plupart renvoient un *itérateur*, un objet sur lequel vous pouvez seulement itérer. Ce n'est pas un vrai conteneur, plutôt une référence sur un conteneur qui avance et fait des traitements au fur et à mesure plutôt que de faire les traitements à l'avance et gaspiller de la mémoire pour stocker les résultats entre-temps. Si vous voulez récupérer un itérateur sous forme d'un conteneur, vous pouvez juste faire `list(iterateur)` ou `tuple(iterateur)`.

## Appliquer un traitement

Pour itérer sur un seul conteneur, il y a la technique habituelle de la compréhension de liste

;;; example ```python
liste = [2, 3, 5, 7, 11]
traitée = [élément * 2 for élément in liste if élément > 5]```
;;;

Pour faire des traitements en même temps que vous itérez, ne sous-estimez pas les *genexpr*, en faisant attention à la lisibilité. Contrairement à une compréhension de liste, une expression génératrice génère à la demande, donc il n'y a pas de stockage intermédiaire en mémoire, ce qui peut avoir son importance — par contre le temps d'exécution est pratiquement identique.

;;; example ```python/result
tableau = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]]

for élément in ((x + y) * tableau[y][x]
                    for y in range(len(tableau)) for x in range(len(tableau[0]))
                    if x != y):
    print(élément)```
;;;

### Traitement fonctionnel

Python propose aussi les fonctions `map(fonction, itérable)` et `filter(fonction, itérable)`, respectivement pour appliquer une fonction sur tous les éléments du conteneur, et pour filtrer les éléments selon un prédicat.
L'utilisation est très simple : vous donnez une fonction, un itérable, et vous obtenez un itérateur qui appliquer la fonction au fur et à mesure (ou `list(map(…))` pour une liste).

;;; example ```python/result
liste = [2, 3, 5, 7, 11]
print("map() : éléments au carré")
for valeur in map(lambda n: n**2, liste):
    print(valeur)

print("filter() : élément inférieurs à 6")
for valeur in filter(lambda n: n < 6, liste):
    print(valeur)

# Et vous pouvez bien sûr combiner les deux, qui travailleront toujours élément par élément
print("Combinaison !")
for valeur in map(lambda n: n**2, filter(lambda n: n < 6, liste)):
    print(valeur)```
;;;

Cela dit, l'exemple ci-dessus est très mauvais. En effet, pour ce type de traitement, `map()` et `filter()` sont nettement moins performants que des compréhensions de listes ou des genexpr, simplement parce qu'ils font beaucoup d'appels de fonction, et qu'un appel de fonction est lourd en Python. Si vous voulez juste appliquer un traitement simple à une liste, une compréhension de liste peut être jusqu'à 15% plus rapide que `map` et `filter`. Dans tous les cas, `map`, `filter`, les genexprs et les compréhensions de listes sont toutes plus rapides que le code équivalent avec une simple boucle `for`.

Cependant, `map` et `filter` ont deux avantages. Le premier, c'est que si vous travaillez avec des fonctions, ils seront plus efficaces parce que le code de l'itération est en C :

;;; code ```python
# Juste pour un traitement qui se fait bien sans passer par une fonction :
# la compréhension de liste peut être ~15% plus rapide
traitée_plus_lent = list(map(lambda x: x**2, liste))
traitée_plus_rapide = [x**2 for x in liste]

# Utilisation d'une fonction existante :
# map/filter peuvent être ~15% plus rapides
traitée_plus_rapide = list(map(fonction, liste))
traitée_plus_lent = [fonction(x) for x in liste]```
;;;

Et le deuxième, c'est que `map()` peut nativement travailler sur plusieurs itérables à la fois (pas `filter`, ça n'aurait pas grand sens). Si vous donnez plusieurs itérables, et une fonction qui prend autant d'arguments, ça donnera les arguments à partir de tous les itérables à la fois (le premier appel prendra `liste1[0]` et `liste2[0]`, le suivant `liste1[1]` et `liste2[1]`, etc.). Vous pouvez donner autant d'itérables que vous voulez du moment que la fonction a le bon nombre d'arguments.

;;; example ```python/result
def moyenne_harmonique(a, b):
    print(f"Arguments : {a=}, {b=}")
    return 1 / ((1/a) + (1/b))

liste1 = [1, 2, 3, 4, 5]
liste2 = [6, 5, 4, 3, 2]
moyennes = list(map(moyenne_harmonique, liste1, liste2))
print("Map :", moyennes)

# Ce serait plus ou moins équivalent à ça (en plus efficace) :
moyennes = [moyenne_harmonique(a, b) for a, b in zip(liste1, liste2)]
print("Compréhension de liste :", moyennes)
```
;;; example ```python/result
liste1 = list(range(10))
liste2 = [(x-1)**2 for x in range(10)]
liste3 = [2*x for x in range(10)]
liste4 = [10-x for x in range(10)]
# Maximum des éléments correspondants des listes
print(list(map(max, liste1, liste2, liste3, liste4)))```
;;;

Le module `itertools` propose quelques autres fonctions du même style

;;; code ```python
itertools.filterfalse(prédicat, itérable)```
;;; doc
Marche exactement comme `filter`, sauf qu'au lieu de garder les éléments pour lesquels `prédicat(élément)` est vrai, ça garde les éléments où c'est faux.
;;;

;;; code ```python
itertools.takewhile(prédicat, itérable)```
;;; doc
Garde les éléments tant que le prédicat est vrai, et coupe au premier élément pour lequel le prédicat est faux (élément faux exclus)
;;; example ```python/result
import itertools

# Convertit une chaîne de caractères en nombre entier, en s'arrêtant quand un
# caractère n'est pas un nombre (comme atoi en C) plutôt que de lever une exception
def int_safe(string):
    value = 0
    for char in itertools.takewhile(str.isdigit, string):
        value = 10*value + int(char)
    return value

print(int_safe("100"))
print(int_safe("23 aller-retours"))
print(int_safe("245€"))```
;;;

;;; code ```python
itertools.dropwhile(prédicat, itérable)```
;;; doc
Inverse de `takewhile`, élimine les éléments tant que le prédicat est vrai et garde tous les éléments à partir du premier où le prédicat est faux.
;;; example ```python/result
import itertools

log = """
INFO    | Combobulating discombobulator
INFO    | Coupling decouplers
WARNING | Remembering ladders
ERROR   | Waking Kraken
WARNING | Amending laws of physics
WARNING | Negociating gravity
ERROR   | Rapid unplanned disassembly"""

# N'affiche le log qu'à partir de la première erreur
for line in itertools.dropwhile(lambda line: not line.startswith("ERROR "), log.splitlines()):
    print(line)```
;;;

;;; code ```python
itertools.compress(itérable, sélecteur)```
;;; doc
Ne garde que les éléments de l'`itérable` pour lesquels l'élément correspondant des `sélécteurs` est vrai. En gros, c'est comme `filter` sauf que la sélection est précalculée.
;;; example ```python/result
import random
import itertools

sélecteur = [random.randint(0, 1) for _ in range(100)]
# On itère sur un intervalle, mais en ne gardant que les nombres sélectionnés
# (ici au hasard)
for i in itertools.compress(range(100), sélecteur):
    print(i, end=" ")```
;;;

### Accumulation

Il est aussi possible de réaliser facilement une *accumulation*, ou *réduction*. C'est quelque chose avec un paradigme plutôt fonctionnel, très en phase avec ce qu'on fait en LO21 :

- `résultat = fonction(liste[0], liste[1])`
- `résultat = fonction(résultat, liste[2])`
- `résultat = fonction(résultat, liste[3])`
- `...`

En utilisant chaque fois la fonction avec le résultat précédent et l'élément suivant, jusqu'à avoir entièrement réduit la liste à une simple valeur. Pour ça il y a deux fonctions :

- `functools.reduce(fonction, itérable[, valeur_initiale])` : Fait exactement ce qui est décrit ci-dessus. La fonction doit prendre deux arguments et l'itérable doit bien sûr avoir au moins deux éléments. Vous pouvez donner une valeur initiale, optionnelle, qui fera que le premier résultat sera `fonction(valeur_initiale, liste[0])` au lieu de `fonction(liste[0], liste[1])`.
- `itertools.accumulate(itérable[, fonction])` : Ça fait pareil, sauf que vous obtenez un itérateur sur tous les résultats intermédiaires, du premier qui est juste le premier élément de l'itérable, au dernier qui est le résultat final. Ici l'itérable n'est pas obligé d'être fini. La fonction est optionnelle parce que si vous ne la donnez pas, ça fait la somme.

Par exemple, pour faire le produit d'un itérable (sans `math.prod` qui existe depuis Python 3.8) :

;;; example ```python/result
import functools
import itertools

liste = [2, 3, 5, 7, 11, 13]
produit = functools.reduce(lambda x, y: x*y, liste)
print(f"functools.reduce : {produit}")

print("itertools.accumulate : ", end="")
for résultat in itertools.accumulate(liste, lambda x, y: x*y):
    print(résultat, end=" ")
print("")```
;;;

### Utiliser des méthodes comme des fonctions

Parfois, on veut utiliser une méthode sur chaque objet d'une liste, et on a bien envie de faire ça avec map, filter ou autres fonctions qui demandent une fonction de traitement.
Vous savez que quand vous définissez une méthode, la définition ressemble à ça :

;;; code ```python
def méthode(self, arg1, arg2):
    # ...```
;;;

En réalité, quand vous appelez `objet.méthode(arg1, arg2)` c'est du sucre syntaxique pour `classe.méthode(objet, arg1, arg2)`. Donc vous pouvez parfaitement utiliser les méthodes comme ça, en donnant juste `classe.méthode` : `map`, `filter` et autre donneront l'objet en argument comme `classe.méthode(objet)` et ce sera exactement comme faire `objet.méthode()`

;;; example ```python/result
mots = ["kiwi", "annulation", "millicochrane", "entomologie", "dévidoir"]
print(list(map(str.upper, mots)))  # Comme appeler mot.upper() sur chaque mot```
;;;

## Itérer sur un conteneur

Il y a des méthodes pour itérer sur un conteneur différemment.

;;; code ```python
enumerate(iterable, start=0)```
;;; doc
Itère sur l'itérable en donnant l'index en même temps. Ça donne des couples `(index, élément)` pour chaque élément.
L'argument `start` permet de donner une valeur de départ, si vous voulez partir d'autre chose que 0.
;;; example ```python/result/joinfiles=[("lignes.dat", "2 3 4\n3 5 1\n\n5 4 7\naaaaaaa\n7")]
entrées = {}
with open("lignes.dat", "r") as fichier:
    for i, ligne in enumerate(fichier, start=1):
        ligne = ligne.strip()
        if len(ligne) == 0:
            continue
        try:
            entrées[i] = [int(élément) for élément in ligne.split()]
        except ValueError:
            print(f"ERREUR : Entrée invalide dans `lignes.dat`, ligne {i} : {ligne}")
print(entrées)```
;;; example ```python
# Cas où l'itérable d'origine contenait déjà des tuples (word, position, hint)
for i, (shelfword, shelfpos, shelfhint) in enumerate(shelf_words.tokens()):
		for j, (entryword, entrypos, entryhint) in enumerate(entry_words.tokens()):
			similarity_matrix[i, j] = word_similarity(shelfword, shelfpos, entryword, entrypos, entryhint, wiktionary)```
;;;

;;; code ```python
reversed(itérable)```
;;; doc
Permet d'itérer sur un itérable en sens inverse
;;;

;;; code ```python
sorted(itérable, /, key=None, reverse=False)```
;;; doc
Trie un itérable.
Vous pouvez spécifier l'argument nommé `key` pour donner une fonction clé. Ça doit être un objet appelable qui retourne un objet comparable (entier, chaîne de caractères, … N'importe quoi tant que c'est des objets qui peuvent être comparés entre eux avec les opérateurs `<` et `>`). Si vous donnez une clé, elle sera utilisée sur chaque élément et les éléments seront triés en fonction de ça.
L'argument nommé `reverse` permet éventuellement de trier en sens inverse.
Ça donne bien le conteneur trié complet, pas juste un itérateur.
;;; example ```python/result
mots = ["Villeneuve", "fourre-tout", "variable", "La Racineuse", "lampion"]

# Tri normal
print(sorted(mots))
# Tri sans mettre les majuscules d'abord, et en sens inverse
print(sorted(mots, key=str.lower, reverse=True))```
;;;

;;; code ```python
itertools.cycle(itérable)```
;;; doc
Tourne indéfiniment sur l'itérable (donc `itertools.cycle([1, 2, 3])` donnera `1, 2, 3, 1, 2, 3, 1, …`)
;;; example ```python/result
import itertools

# Chiffrement par XOR
def xor_cipher(message, key):
    result = bytearray(len(message))
    for i, (msg_byte, key_byte) in enumerate(zip(message, itertools.cycle(key))):
        result[i] = msg_byte ^ key_byte
    return bytes(result)

key = b"LLPA38@Gch2"
message = """Dans un grand bol de strychnine
Délayez de la morphine
Faites tiédir a la casserole
Un bon verre de pétrole...

- Ho Ho, je vais en mettre deux."""

ciphered = xor_cipher(message.encode("utf-8"), key)
print(f"Ciphered :\n{ciphered}")
deciphered = xor_cipher(ciphered, key).decode("utf-8")
print(f"\nDeciphered :\n{deciphered}")```
;;;


## Combiner plusieurs itérables
### Itérer sur plusieurs conteneurs en même temps

;;; code ```python
zip(*itérables, strict=False)```
;;; doc
Permet d'itérer sur plusieurs itérables en même temps. En gros, si vous itérez sur `zip(it1, it2, it3)`, ça va donner des tuples `(it1[0], it2[0], it3[0]), (it1[1], it2[1], it3[1]), …`. Ça donne donc l'effet de transposition d'une matrice (les lignes deviennent les colonnes, les colonnes deviennent les lignes). Vous pouvez donner autant d'itérables que vous voulez comme ça.
Par défaut, ça s'arrête dès que l'itérable le plus court est épuisé, ce qui peut être pratique dans certaines situations, mais cacher des bugs dans d'autres. Si tous les itérables sont doivent être de la même taille, donnez l'argument `strict=True`, qui lèvera une exception si les itérables de taille différente, ce qui vous fera détecter les problèmes immédiatement plutôt que de causer des bugs difficiles à remonter.
;;; example ```python/result
noms = ["Jean-Baptiste Duval", "Jean-Christophe Dumont", "Jean-Barnabé Dupied"]
codes_postaux = ["71310", "70110", "87160"]
utilisateurs = {}
for i, (nom, code_postal) in enumerate(zip(noms, codes_postaux, strict=True)):
    print(f"{i} : {nom}, {code_postal}")
    utilisateurs[i] = {"nom": nom, "code_postal": code_postal}```
;;;

;;; code ```python
itertools.zip_longest(*itérables, fillvalue=None)```
;;; doc
Ça fonctionne comme `zip(*itérables)`, mais plutôt que de demander des itérables de la même taille ou de s'arrêter au plus court, ça va jusqu'au bout du plus long en remplissant les trous avec `fillvalue`.
;;; example ```python/result
import itertools

def somme_vecteurs(vecteur1, vecteur2):
    return [coord1 + coord2 for coord1, coord2 in itertools.zip_longest(vecteur1, vecteur2, fillvalue=0)]

print(f"{somme_vecteurs([1, 3], [4, 5, 5, 0])=}")
print(f"{somme_vecteurs([0, 4, 4], [4, 0, 4])=}")
print(f"{somme_vecteurs([3, 2, 2, 3], [1, 5])=}")```
;;;

### Enchaîner des itérateurs

;;; code ```python
itertools.chain(*itérables)```
;;; doc
Itère de façon transparente sur plusieurs itérables à la suite
;;; example ```python/result
import itertools

liste = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# On enchaîne la liste, puis un itérateur qui répète le dernier élément de la
# liste jusqu'à avoir passé 20 éléments
for x in itertools.chain(liste, itertools.repeat(liste[-1], 20-len(liste))):
    print(x, end=" ")```
;;;

;;; code ```python
itertools.chain.from_iterable(itérable)```
;;; doc
Pareil que `itertools.chain`, mais ça utilise une liste d'itérables au lieu de les enchaîner comme arguments (en gros, `itertools.chain.from_iterable(itérables)` est équivalent à `itertools.chain(*itérables)`)
;;; example ```python/result
import itertools

listes = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14]]
for x in itertools.chain.from_iterable(listes):
    print(x, end=" ")```
;;;
