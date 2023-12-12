//// title = "Boucles"
//// description = "Les différents types de boucles en Python"

# {=title}

Python a plusieurs types de boucles, pour certaines très différentes de ce que vous avez pu voir.

## Boucles while

Une boucle `while` tourne tant que la condition est vraie, tout comme ce que vous avez pu voir en C par exemple.

;;; code ```python
while condition:
    # Code à exécuter tant que la condition est vraie```
;;; example ```python/result/stdin="5\n3\n10\n2\n\n"
somme = 0
# On exécute tant que l'utilisateur entre des choses
# quand il donne une chaîne vide ou que des espaces la condition est fausse et on sort de la boucle
while len(entrée := input("Entrez un nombre, ou rien pour terminer : ").strip()) > 0:
    somme += int(entrée)
print(f"Somme : {somme}")```
;;;

### Contrôle de boucle

Il existe deux mots-clés pour contrôler de façon plus radicale ce qui se passe dans la boucle :

- `break` casse la boucle, donc ça sort immédiatement de la boucle et ça continue juste après la boucle
- `continue` saute le reste de l'itération en cours : le reste du passage de boucle en cours n'est pas exécuté et ça passe directement au tour suivant

;;; code ```python/result/joinfiles=[("lignes.txt", "Ligne 1\n\n  \nLigne 4\nLigne 5\n--fin--\nLigne 7")]
with open("lignes.txt", "r") as fichier:
    for ligne in fichier:
        ligne = ligne.strip()

        # On ne lit pas la ligne si elle est vide ou s'il n'y a que des espaces,
        # donc on saute le reste du traitement et on passe de suite à la ligne suivante
        if len(ligne) == 0:
            continue

        # Le reste du code n'est exécuté que si la boucle n'a pas été cassée et
        # si l'itération n'a pas été sautée avant
        print(ligne)

        # Si le contenu de la ligne est "--fin--", on arrête tout
        if ligne == "--fin--":
            break```
;;;

Ça permet aussi d'évaluer les conditions plus tard dans la boucle, par exemple avec une boucle infinie, qu'on casse avec une condition plus loin dans le code

;;; example ```python
# True est toujours vrai, donc c'est une boucle infinie
# On verra la gestion des exceptions plus tard,
# mais par exemple ici on casse la boucle dès qu'on tombe sur une erreur dans
# la méthode self._unpack_file
while True:
    try:
        subgroup = self._unpack_file(data, token.content, refdata)
    except OperationError:
        break
    sublist.append(subgroup)```
;;;

## Boucles for

Les boucles `for` en Python sont un peu différentes de ce que vous avez pu voir en C / VB. En Python, une boucle `for` itère sur les éléments d'un *itérateur* (un objet sur lequel on peut itérer). Typiquement, sur une collection. Les boucles `for` peuvent bien sûr être manipulées avec `break` et `continue` également.

Pour itérer un certain nombre de fois, on utilise la fonction `range()`, qui donne un itérateur sur les nombres d'un intervalle (ce n'est *pas* une liste, mais `list(range(x))` le convertira). La fonction `range` a trois configurations :

- `range(fin)` : Donne les entiers de l'intervalle [0, fin[. Donc `for i in range(nb_itérations)` itèrera `nb_itérations` fois et `i` ira de 0 à `nb_itérations - 1` inclus
- `range(début, fin)` : Donne les entiers de l'intervalle [début, fin[
- `range(début, fin, pas)` : Donne les entiers de l'intervalle [début, fin[ avec un pas : par exemple `range(1, 10, 2)` donnera tous les nombres impairs entre 1 et 10. Notez que si le pas n'est pas parfaitement aligné avec la `fin`, ça n'ira jamais après la `fin` : `range(2, 10, 3)` donnera (2, 5, 8)

Notez bien que pratiquement partout en Python, les intervalles sont du type `[a, b[` : **début inclus, fin exclue**. Donc `range(2, 5)` donnera (2, 3, 4), `liste[2:5]` donnera les éléments d'indices 2, 3 et 4, etc.
Et pour toujours être cohérent et éviter les maux de têtes, **conformez-vous toujours à cette règle**. Si vous manipulez des intervalles, à moins d'une impossibilité majeure, arrangez-vous pour respecter cette règle du début inclus, fin exclue, ça aide tout le monde à avoir les idées claires

;;; code ```python
for variable in itérateur:
    # Code à exécuter pour chaque élément```
;;; example ```python/result
# Pour simplement itérer un certain nombre de fois
print("     ", end="")
for i in range(11):
    print(f"{i :2}", end=" ")
print("")
print("—" * (3*11 + 5))

for i in range(11):
    print(f"{i :2} |", end=" ")
    for j in range(11):
        print(f"{i*j :2}", end=" ")
    print("")```
;;; example ```python/result
# On itère sur une liste, dans l'ordre.
# Vous pouvez itérer comme ça sur les éléments de n'importe quelle collection,
# liste, tuple, ensemble, chaîne de caractères, …
liste = [2, 3, 5, 7, 11, 13, 17, 19, 23]
produit = 1
for premier in liste:
    produit *= premier
print(f"{produit=}")```
;;; example ```python/result
# Pour itérer sur une liste tout en gardant l'index, la fonction enumerate() est très pratique
# Vous notez que vous pouvez extraire des variables de la structure des éléments itérés
# enumerate() renvoie des tuples (index, valeur), donc il suffit de reporter ça dans les variables d'itération
liste = [2, 3, 5, 7, 11, 13, 17, 19, 23]
résultat = liste.copy()
for i, valeur in enumerate(liste):
    résultat[(i-1) % len(liste)] += valeur
print(liste)
print(résultat)```
;;; example ```python/result
# Sur un dictionnaire, ça itère par défaut sur les clés
# Depuis Python 3.7, itérer sur un dictionnaire donnera les éléments dans l'ordre où ils ont été insérés
dictionnaire = {10004324: "Jean-Paul Duval", 10003561: "Jean-Patrick Dumont", 10003674: "Jean-Christophe Dubois"}
for clé in dictionnaire:
    print(clé, end=", ")
print("")

# On peut aussi itérer sur les valeurs seules avec la méthode .values()
for valeur in dictionnaire.values():
    print(valeur, end=", ")
print("")

# Et sur clé et valeur en même temps avec .items()
for clé, valeur in dictionnaire.items():
    print(f"{clé} : {valeur}", end=", ")
print("")```
;;;

Tout comme la simple affectation, `for` peut extraire les valeurs des tuples, donc si vous avez un itérateur du type `[(1, 2, 3), (3, 4, 5), …]`, vous pouvez faire `for a, b, c in itérateur` pour extraire facilement les variables. Depuis quelques temps, vous pouvez même extraire des valeurs encore plus profondes: `[(1, (2, 3)), (4, (5, 6)), …]` peut s'extraire par `for a, (b, c) in itérateur`.

### Condition for-else

Il y a une syntaxe très peu connue et qui sert pas souvent mais qui est bien pratique quand on en a besoin : `for-else`.
En gros, c'est une boucle `for` à peu près normale, et le bloc `else` ne sera exécuté **que si la boucle s'est exécutée jusqu'au bout**, donc si vous n'en êtes pas sorti avant par un `break`. C'est pratique dans tous les cas où vous allez tester des choses jusqu'à trouver la bonne, pour traiter le cas où vous ne la trouvez pas.

;;; example ```python/result
# Par exemple ici on cherche où se trouve une librairie
import os
import sys

for path in sys.path:
    if os.path.exists(os.path.join(path, "numpy")):
        print(f"NumPy se trouve dans le répertoire {path}")
        break
else:
    print("NumPy n'est pas installé (ou pas correctement)")```
;;;


## Compréhensions

Python a aussi ce qu'on appelle des *compréhensions de collection*, qui sont en gros un moyen compact de générer, traiter et/ou filtrer des collections. Ce sont des expressions qui renvoient la collection ainsi construites. Ça se présente toujours plus ou moins sous cette forme :

- Un crochet ouvrant quelconque (`[` pour les listes, `{` pour les ensembles et dictionnaires)
- L'expression pour chaque élément
- Une boucle `for` : c'est exactement une boucle `for variables in itérateur`, comme serait une boucle `for` normale
- Un prédicat facultatif : seuls les éléments pour lesquels la condition est vraie seront conservés
- Le crochet fermant correspondant

Le tout donnant quelque chose du style `[os.path.join("temp", filename) for filename in file_list if not filename.endswith(".log")]`, qui est techniquement équivalent à ceci en plus concis et efficace :

;;; code ```python
résultat = []
for filename in file_list:
    if not filename.endswith(".log"):
        résultat.append(os.path.join("temp", filename))```
;;;

Et dans cet ordre, donc à chaque élément l'ordre d'exécution est tout à fait logiquement boucle -> condition -> expression.

Il est aussi possible d'itérer sur plusieurs dimensions à la fois en mettant plusieurs boucles :

;;; code ```python/result
résultats = [i*j for i in range(1, 6) for j in range(1, 11)]
print(f"{résultats=}")```
;;;

Cela dit, certes c'est plus compact, mais n'abusez pas non plus, il ne faut pas que ça devienne illisible. Ne faites pas ça (la compréhension de ce code est laissée en exercice)

;;; counterexample ```python
[((t:=__import__("pickle").load(open("todo.dat","rb")) if __import__("os").path.exists("todo.dat") else {}),print("\n".join([f"{i} [{'x' if t[i][0] else ' '}] : {t[i][1]}" for i in t.keys()])+"\n1- Add\n2- Toggle\n3- Edit\n4- Delete"),(t.__setitem__(max(t.keys())+1 if len(t)>0 else 0,[False,input("TODO : ")]) if (o:=int(input(": ")))==1 else (t[(x:=int(input("ID : ")))].__setitem__(0,t[x][0]^1) if o==2 else (t[int(input("ID : "))].__setitem__(1,input("New name : ")) if o==3 else (t.__delitem__(int(input("ID : "))) if o==4 else None)))),__import__("pickle").dump(t,open("todo.dat","wb"))) for i in iter(int, 1)]```
;;;

### Compréhension de liste

Une compréhension de liste renvoie une liste, et se présente comme une liste. Elle s'écrit entre crochets `[]`

;;; example ```python/result
import math

vecteurs = [(0, 5), (1, 4), (4, 3), (1, 3), (2, 0)]

# Calcule la liste des modules de chaque vecteur
modules = [math.sqrt(x**2 + y**2) for x, y in vecteurs]

# Ne garde que les vecteurs qui ont un module plus élevé que le précédent
filtré = [vecteur for i, vecteur in enumerate(vecteurs) if modules[i] > modules[(i-1) % len(vecteurs)]]

print(f"{vecteurs=}")
print(f"{modules=}")
print(f"{filtré=}")```
;;;

Attention, utiliser des parenthèses `(expression for variable in itérateur)` n'est pas une quelconque compréhension de tuple, c'est une *genexpr* qu'on verra juste après. Si vous voulez un tuple comme ça convertissez-le explicitement (`tuple([expression for variable in itérateur])`)

### Compréhension d'ensemble

C'est pareil que les listes, mais entre accolades.

;;; example ```python/result
document = """
Maître Corbeau, sur son arbre perché, tenait en son bec un fromage
Maître Renard, par l'odeur alléché, lui tint à peu près ce langage :
« Hé, bonjour, Monsieur du Corbeau.
Que vous êtes joli ! Que vous me semblez beau !
Sans mentir, si votre ramage se rapporte à votre plumage,
Vous êtes le phœnix des hôtes de ces bois. »
"""

# On éclate le texte au niveau des espaces,
# on ne garde que les mots, donc ce qui reste une fois éliminés tous les symboles, la ponctuation, les chiffres, …
# Et enfin on met tout en minuscules
# On peut se permettre la bidouille avec (mot := ...) pour ne pas réécrire `élément.strip(...)` vu que la condition
# est exécutée avant l'expression
mots_uniques = {mot.lower() for élément in document.split() if (mot := élément.strip(" \n,?!:;.…;")).isalpha()}
print(mots_uniques)```
;;;

### Compréhension de dictionnaire

La compréhension de dictionnaire génère un dictionnaire, c'est aussi entre accolades sauf que cette fois vous donnez deux expressions pour chaque élément, `clé: valeur`

;;; example ```python/result
import pprint

doclist = ("info.python.reference.variables", "info.python.reference.operateurs", "info.python.reference.conditions", "info.python.reference.boucles")
linktable = {docpath: "/" + docpath.replace(".", "/") + ".html" for docpath in doclist}
pprint.pprint(linktable)```
;;;

### Genexprs //// genexpr

Une *genexpr* (generator expression) est quelque chose qui ressemble à une compréhension de liste, mais qui crée un générateur à la place. On verra ça après, mais en gros c'est un itérateur qui génère ses éléments à la demande plutôt que de créer la liste d'un coup. Du coup pour itérer sur beaucoup d'éléments générés, ça permet d'épargner l'espace mémoire qu'aurait occupé la liste de tous les éléments (et de rendre possible un éventuel itérateur infini). En fait, `range()`, `reversed()`, `enumerate()`, … sont des générateurs, ça ne renvoie pas vraiment des listes.

;;; example ```python/result
impairs = (2*i+1 for i in range(100))

# On peut juste récupérer le prochain élément avec la fonction next()
print(f"Premier nombre impair : {next(impairs)}")

# Et on peut itérer dessus tout à fait normalement
print("Le reste des nombres impairs :")
for nombre in impairs:
    print(nombre, end=", ")```
;;;

Jusque là, à part avoir plus de flexibilité sur la génération des éléments ça n'a pas grand intérêt par rapport à une bête boucle `for`. Par contre c'est tout de suite beaucoup plus efficace avec des fonctions d'aggrégation comme `sum()`, `min()`, `max()`, `all()`, `any()`, … qui du coup consomment les éléments comme ils sont générés plutôt que de vous obliger à construire des listes immenses en mémoire avant de leur donner

;;; example ```python/result
import math

somme_impairs = sum(2*i + 1 for i in range(100))
max_cos = max(math.cos(i) for i in range(1, 100))

print(f"{somme_impairs=}, {max_cos=}")```
;;;
