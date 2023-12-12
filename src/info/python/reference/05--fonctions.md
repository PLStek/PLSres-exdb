//// title = "Fonctions"
//// description = "Définition et utilisation des fonctions en Python"

# {=title}

## Arguments

Pour utiliser une fonction c'est très simple, c'est `fonction(arguments)`. En Python il y a trois types de paramètres:

- Les paramètres positionnels, donc déterminés par leur position dans la liste d'arguments. C'est ce que vous connaissez bien comme `fonction("arg1", "arg2")`
- Les paramètres optionnels, ce sont des arguments situés à la fin des arguments positionnels, que vous n'êtes pas obligé de donner, ex. `range(10)`, `range(1, 11)`, `range(1, 11, 2)`
- Les paramètres nommés, ce sont des arguments que vous passez en donnant leur nom avec pour les identifier, ex. `print("ERREUR", end=" ", file=sys.stderr)`

En fait tous les arguments peuvent être donnés avec leur nom si vous le connaissez. Par exemple, si vous avez une fonction avec 3 arguments optionnels et que vous voulez juste donner le 3ème, vous utiliserez son nom. Si vous donnez le nom vous n'êtes pas obligé de donner les arguments dans l'ordre. On verra comment utiliser tout ça très vite.

## Définition de fonction

À la base, une fonction se définit avec `def`, un nom, et une liste de paramètres. Une fonction peut retourner une valeur avec `return`. Vous n'avez pas de types à déclarer.

;;; code ```python
def norme(x, y):
    return math.sqrt(x**2 + y**2)```
;;;

### Valeurs de retour

Une fonction peut, ou pas, retourner une valeur. Pour retourner une valeur, c'est juste `return valeur`, qui quitte la fonction immédiatement et retourne la valeur donnée.

;;; example ```python/result
import math
def norme(x, y):
    return math.sqrt(x**2 + y**2)

résultat = norme(1, 1)
print(f"{résultat=}, {norme(2, 2)=}")```
;;;

Si vous voulez juste quitter la fonction immédiatement sans retourner de valeur, utilisez juste `return` sans valeur de retour

;;; example ```python
def load_documents(self):
    """Load the sub-sections of this document"""
    self.documents = []

    # Ici, si un document n'a pas de sous-section, il n'y a rien à charger donc on ressort directement
    if not self.has_subdocuments():
        return

    if self.attributes is None or "sections" not in self.attributes:
        filenames = sorted([filename for filename in os.listdir(self.sourcepath) if filename.endswith(".md")])
        for filename in filenames:
            if "--" in filename:
                docname = os.path.splitext(filename)[0].partition("--")[-1]
            else:
                docname = os.path.splitext(filename)[0]
            self.documents.append(self.load_document(self.sourcepath, docname, filename=filename))
    else:
        for docname in self.attributes["sections"]:
            self.documents.append(self.load_document(self.sourcepath, docname))```
;;;

Notez qu'une fonction à qui vous ne faites pas retourner de valeur retournera toujours `None` par défaut.

Vous pouvez aussi retourner plusieurs valeurs d'une fonction, elles seront alors retournées sous forme d'un tuple, qu'il est facile d'extraire avec la notation `a, b = fonction(…)`.

;;; example ```python/result
import cmath  # Comme math mais qui traite aussi les complexes

def résoudre_second_degré(a, b, c):
    """Résous un polynôme du second degré de la forme ax² + bx + c"""
    delta = b**2 - 4*a*c
    solution1 = (-b + cmath.sqrt(delta)) / (2*a)
    solution2 = (-b - cmath.sqrt(delta)) / (2*a)
    return solution1, solution2

print(f"x² + x + 1 : {résoudre_second_degré(1, 1, 1)}")
solution1, solution2 = résoudre_second_degré(1, -1, 0)
print(f"x² - x : {solution1=}, {solution2=}")```
;;;

### Liste de paramètres

À la base, une fonction peut avoir autant de paramètres que vous voulez.

;;; code ```python
def fonction():
    pass  # Pas de paramètres
fonction()

def fonction(argument):
    pass  # Un paramètre
fonction(1)

def fonction(arg1, arg2, arg3):
    pass
fonction(1, 2, 3)
fonction(arg1=1, arg2=2, arg3=3)  # Vous pouvez toujours donner les arguments par nom```
;;;

Pour avoir des paramètres optionnels, ils faut leur donner une valeur par défaut.

;;; code ```python/result
def fonction(arg1, arg2=2, arg3=3):
    print(f"{arg1=}, {arg2=}, {arg3=}")

fonction(1)  # Les arguments optionnels ont leurs valeurs par défaut
fonction(1, 10)  # On spécifie la valeur de arg2 mais pas arg3
fonction(1, 10, 100)  # On spécifie tous les arguments
fonction(1, arg3=100)  # Pour donner un argument optionnel mais pas ceux d'avant il faut passer par le nom```
;;;

Il est aussi possible de demander un nombre indéfini d'arguments positionnels en mettant `*nom` en paramètres. Ces arguments seront alors rendus sous la forme d'un tuple. Tous les arguments après ça devront être nommés : il ne pourront être passés qu'avec `nom=valeur` et doivent avoir une valeur par défaut.

;;; code ```python/result
import sys

# La définition de `print()` quelque chose comme ça par exemple
def print_args(name, *items, file=sys.stdout):
    file.write(f"{name} = {items}\n")

print_args("test1", 1, 2, 3, 4)
print_args("test2", 5, file=sys.stderr)
print_args("test3", file=sys.stderr)```
;;;

Il est aussi possible d'accepter des arguments nommés indéfinis avec `**nom`. Vous les aurez alors dans le dictionnaire `nom`. Il ne peut y avoir aucun autre paramètre après ça. On l'appelle souvent `**kwargs`, pour *keyword arguments*

;;; code ```python/result
def print_all(*args, **kwargs):
    print(f"{args=}, {kwargs=}")

print_all(1, 2, 3, arg4=4, arg5=5, arg6=6)
print_all(arg=7)
print_all(8, 9)
print_all()```
;;;

Vous pouvez d'ailleurs utiliser la même syntaxe pour extraire une liste ou un dictionnaire en arguments pour une fonction.

;;; example ```python/result
import math

def norme(x, y, z):
    return math.sqrt(x**2 + y**2 + z**2)

# Notre fonction norme prend les arguments x, y, z, pas un vecteur d'un bloc sous forme d'un tuple
# Mais on peut extraire notre vecteur directement comme liste d'arguments
vecteur = (4, 6, -1)
print(f"{norme(*vecteur)=}")
# Ici c'est équivalent à norme(4, 6, -1) au lieu de norme((4, 6, -1))
```
;;; example ```python/result
import sys

# On fait souvent ça quand on doit juste transmettre des arguments
# dont on n'a pas à savoir la nature
def log_wrapper(function, *args, **kwargs):
    print(f"Appel à {function.__name__}()\n\tArguments positionnels : {args}\n\tArguments nommés : {kwargs}", file=sys.stderr)
    return function(*args, **kwargs)

log_wrapper(print, 1, 2, 3, end=";\n", sep=", ")
# Ici, au final le `function(*args, **kwargs)` sera comme `print(1, 2, 3, end=";\n", sep=", ")`
```
;;;

Si vous voulez rendre le tout un peu plus clair et strict, il est possible d'imposer l'utilisation d'arguments positionnels (pas par nom) ou nommés (pas positionnels).

;;; code ```python
def fonction(pos1, pos2, pos3, pos4, nom1=5, nom2=6, nom3=7):
    pass

fonction(1, 2, 3, 4)                              # Valide
fonction(1, 2, 3, 4, nom1=5, nom2=6, nom3=7)      # Valide
fonction(1, 2, 3, 4, 5, 6, 7)                     # Valide
fonction(pos2=2, pos1=1, pos3=3, pos4=4, nom1=5)  # Valide```
;;;

Tout ça peut être un peu confus, donc dans les appels de fonction un peu complexes, il est possible de forcer plus d'ordre et de lisibilité en obligeant à donner les arguments sous forme positionnelle ou nommée. On a ainsi le symbole `/` qui fait que tous les arguments avant lui doivent être positionnels, et `*` qui fait que tous les arguments après lui doivent être nommés

;;; code ```python
def fonction(pos1, pos2, /, tout1, tout2, *, nom1, nom2=6):
    pass

fonction(1, 2, 3, 4, nom1=5)                                # Valide
fonction(1, 2, 3, tout2=4, nom1=5, nom2=6)                  # Valide
fonction(nom1=5, nom2=6, pos1=1, pos2=2, tout1=3, tout2=4)  # Invalide (pos1 et pos2 doivent être positionnels)
fonction(1, 2, 3, 4, 5, nom2=6)                             # Invalide (nom1 et nom2 doivent être nommés)```
;;; code ```python
# On a toutes les combinaisons comme ça
# / contraint juste tous ceux avant lui à être positionnels
# * contraint juste tout ceux après lui à être nommés
# Ce qui n'est pas contraint peut s'utiliser comme vous voulez
def fonction(tout1, tout2, *, nom1, nom2):
    pass

def fonction(pos1, pos2, /, tout1, tout2):
    pass

def fonction(pos1, /):
    pass

def fonction(*, nom1):
    pass```
;;;

## Expressions lambda

Les *expressions lambdas*, concept venu tout droit du lambda-calcul et du paradigme fonctionnel, sont de courtes fonctions anonymes qui prennent des paramètres et les associe à une expression. Elles se définissent sous la forme `lambda paramètres: expression` et se manipulent comme n'importe quelle autre objet. Elles s'utilisent comme n'importe quelle autre fonction.

;;; code ```python/result
import math

carré = lambda x: x**2
norme = lambda x, y: math.sqrt(x**2 + y**2)

print(f"{carré(14)=}")
print(f"{norme(1, 1)=}")```
;;; code ```python
# C'est à peu près équivalent à ça
def carré(x):
    return x**2

def norme(x, y):
    return math.sqrt(x**2 + y**2)```
;;;

Sous cette forme ça n'apporte pas grand chose, mais comme c'est des expressions, vous pouvez les utiliser facilement comme callbacks ou prédicats.

## Prédicats, clés et callbacks

En Python, tout est objet, *absolument tout*, même les fonctions, modules, classes, tout ce que vous voulez. Donc vous pouvez très bien manipuler une fonction comme n'importe quelle variable, ce qui rend très simple de passer des fonctions en argument d'autres fonctions, généralement pour donner un comportement spécifique à une autre fonction.

Pour le vocabulaire, on appelle *prédicat* une fonction qui prend des paramètres et renvoie une valeur booléenne, généralement pour dire s'il faut procéder ou pas. Une *callback* (fonction de rappel) est une fonction qu'on donne et qui sera rappelée à un moment choisi (par exemple, si vous faites une interface graphique, vous allez très souvent donner des callbacks pour qu'elles soient rappelées quand l'utilisateur clique quelque part).

C'est bien là que les lamba-expressions brillent, parce qu'elles permettent de définir des fonctions simples directement sans s'encombrer d'une définition de fonction complète.

;;; example ```python
import asyncio

# Exemple de callback : on appelle la fonction après un certain temps
# Les histoires de async/await sont pour de l'exécution asynchrone, on verra ça plus tard
async def délai(durée, fonction):
    await asyncio.sleep(durée)
    # On rappelle la fonction donnée au bon moment
    fonction()```
;;; example ```python/result
# Pour trier sur un critère personnalisé, on utilise le paramètre `key` de `.sort()` ou `sorted()`
# C'est une fonction qui doit prendre un élément de l'itérable et donner une valeur, et ça triera ces valeurs dans l'ordre croissant
# Ici, on trie les mots par ordre croissant de longueur
liste = ["anticonstitutionnellement", "corbeau", "burin", "aluminium", "passiflore", "ontologie"]
triée = sorted(liste, key=lambda élément: len(élément))
print(liste)
print(triée)

# Ou alors par l'ordre alphabétique inverse de leur dernière lettre
liste.sort(reverse=True, key=lambda élément: élément[-1])
print(liste)```
;;; example ```python/result
import itertools

# La fonction itertools.takewhile(prédicat, itérable) garde les éléments de la collection
# tant que le prédicat est vrai et s'arrête dès qu'il est faux
# Ici on garde jusqu'à ce qu'on trouve un mot de moins de 8 lettres
liste = ["ostensiblement", "capybara", "balle", "molybdène", "hortensia", "stoïcisme"]
coupée = list(itertools.takewhile(lambda élément: len(élément) >= 8, liste))
print(liste)
print(coupée)```
;;;

## Générateurs

Un *générateur* est un objet qui ressemble à une fonction, mais qui va générer des valeurs à la demande. On pourrait croire que ça fait comme une fonction qui renverrait une liste, sauf que d'une, un générateur peut être infini, et de deux les valeurs sont générées dynamiquement et à la demande, donc pas besoin de les stocker entre-temps d'où de fortes économies de mémoire, et aucun calcul superflu.

Pour définir un générateur, soit on passe par une {> info.python.reference.boucles#genexpr: *genexpr*}, soit par une fonction qui utilise le mot-clé `yield` au lieu de `return`

;;; example ```python/result/joinfiles=[("users.csv", "prénom,nom,age,codepostal\nJean-Paul,Duchesne,54,23000\nJean-Pierre,Duval,41,70110\nJean-Claude,Dumont,60,71310")]
import csv

# Lit et décode successivement les lignes d'un fichier CSV
# Comme on n'a jamais plus d'une ligne en mémoire à la fois,
# pas de risque de surcharge avec des gros fichiers
def read_csv_rows(filename):
	with open(filename, "r", encoding="utf-8") as f:
		reader = csv.DictReader(f)
		for i, row in enumerate(reader):
			yield (i, row)  # On génère une valeur (ici un couple index, ligne)
    # Quand la fonction "retourne", la génération est terminée et l'itération s'arrête

for index, row in read_csv_rows("users.csv"):
    print(f"Ligne {index} : {row['prénom']} {row['nom']}")
```
;;; example ```python/result
# Il est aussi possible de récupérer des valeurs manuellement avec next(générateur).
# Ici le générateur est infini, mais s'il est fini et que vous utilisez next(),
# ça lèvera une exception de type StopIteration
import math

def cercle(pas_radians, sens_trigo=True):
    angle = 0
    while True:  # Générateur infini, on tourne sur notre cercle aussi longtemps qu'il y a besoin
        yield math.cos(angle), math.sin(angle)
        if sens_trigo:
            angle += pas_radians
        else:
            angle -= pas_radians

gen_cercle = cercle(math.pi / 24)
for i in range(10):
    print(f"{next(gen_cercle)=}")
# On n'est pas obligé, mais quand on a fini d'utiliser un générateur alors
# qu'il n'est pas réellement fini (la fonction n'est pas terminée),
# c'est toujours bien de le fermer
gen_cercle.close()```
;;;

### Générateurs paramétrés dynamiquement

Il est également possible d'envoyer des données à un générateur pendant son fonctionnement (traditionnellement on appellerait ça une coroutine mais comme en Python moderne il y a autre chose de nettement plus commun qui s'appelle une coroutine on évite). Pour cela, on utilise la méthode `.send(arguments)` pour envoyer des choses au générateur, et `arguments = (yield valeur)` pour les récupérer dans le générateur

;;; example ```python/result
def moyenne_glissante(fenêtre):
    valeurs_précédentes = []
    while True:
        if len(valeurs_précédentes) > 0:
            nouvelle_valeur = (yield sum(valeurs_précédentes) / len(valeurs_précédentes))
        else:
            nouvelle_valeur = (yield None)
        if nouvelle_valeur is not None:  # Si on utilise next() et pas .send() ça donnera None
            valeurs_précédentes.append(nouvelle_valeur)
            if len(valeurs_précédentes) > fenêtre:
                valeurs_précédentes.pop(0)

températures = [10, 11, 14, 18, 31, 30, 20, 16, 14, 13, 12, 2, 11, 16, 10, 24, 13]
gen_moyenne = moyenne_glissante(7)
gen_moyenne.send(None)  # On doit envoyer None la première fois parce qu'il faut que le générateur s'exécute jusqu'au premier yield. C'est une bizarrerie du langage, c'est juste comme ça.
for température in températures:
    gen_moyenne.send(température)
    print(f"Il fait {température}°C. La moyenne sur les 7 derniers jours est de {next(gen_moyenne)}°C")
gen_moyenne.close()```
;;;

Ce type de structuration est souvent un peu confuse et très prise de tête, donc on utilise souvent d'autres solutions, comme une classe ou une closure (la version closure de la moyenne glissante est ci-dessous)

### Enchaînement de générateurs

Il est parfois utile d'enchaîner des générateurs, ou du moins de faire qu'un générateur donne les valeurs renvoyées par un autre générateur. Pour cela, il y a la syntaxe `yield from`. Par exemple, dans cet exemple, on a un système de combat au tour par tour qui génère des évènements qui seront affichés sur l'interface, pour cela c'est un modèle très pratique :

;;; example ```python/result
# Exemple ressemblant à itertools.chain qui donne les éléments de plusieurs collections à la suite
def chain(*collections):
    for collection in collections:
        yield from collection  # On génère les éléments du générateur ou de l'itérateur donné

for item in chain([1, 2, 3], (5, 6, 7), [9, 10, 11, 12]):
    print(item, end=" ")
print("")```
;;; example ```python/result
# Cette fois on trouve tous les arrangements possibles d'une liste, un peu comme itertools.permutations
# Ici yield from permet de rendre facilement notre générateur récursif
def arrangements(éléments, longueur=None, intro=[]):
    éléments = set(éléments)  # Ça nous arrange pour les opérations d'ensemble
    if longueur is None:
        longueur = len(éléments)
    if longueur == 0:
        return []
    elif longueur == 1:
        for élément in éléments:
            yield intro + [élément]
    else:
        for élément in éléments:
            yield from arrangements(éléments - {élément}, longueur-1, intro=intro+[élément])

for arrangement in arrangements([1, 2, 3, 4]):
    print(arrangement)```
;;;

`yield from` est essentiellement un raccourci de ceci :

;;; code ```python
for élément in autre_générateur:
    yield élément```
;;;

Mais c'est aussi beaucoup plus puissant, parce que tout est géré comme une fusion parfaite des générateurs : les résultats sont passés directement, les exceptions et arrêts sont transmis, les valeurs envoyées par `.send(paramètre)` sont aussi transmises au second générateur, etc.

## Fonctions imbriquées

En Python tout est objet, donc rien n'empêche une fonction de prendre une fonction en argument… ni de retourner une autre fonction. Ça permet pas mal de choses bien pratiques.

### Closure

En programmation, ce qu'on appelle une *closure* (apparemment « fermeture » en français mais je n'ai jamais vu ce terme nulle part), c'est une fonction qui retourne une autre fonction en lui donnant un contexte par ses variables. Un exemple sera plus parlant que ce genre de définition :

;;; example ```python/result
import pprint

def tri_champs(champs):
    def clé(élément):
        return élément[champs]
    return clé

utilisateurs = [
    {"prénom": "Jean-Paul", "nom": "Duchesne", "age": 54, "codepostal": "23000"},
    {"prénom": "Jean-Pierre", "nom": "Duval", "age": 41, "codepostal": "70110"},
    {"prénom": "Jean-Claude", "nom": "Dumont", "age": 60, "codepostal": "71310"},
]

print("Tri par prénom")
pprint.pprint(sorted(utilisateurs, key=tri_champs("prénom")))

print("\nTri par nom")
pprint.pprint(sorted(utilisateurs, key=tri_champs("nom")))

print("\nTri par âge")
pprint.pprint(sorted(utilisateurs, key=tri_champs("age")))

print("\nTri par code postal")
pprint.pprint(sorted(utilisateurs, key=tri_champs("codepostal")))```
;;;

Ici, on a une liste de dictionnaires, qu'on veut trier selon leurs différents champs. Pour cela, il faut créer une fonction qui prenne à la fois des paramètres du contexte « extérieur » (là où on écrit `key=qqch`), et le paramètre que la fonction de tri lui donne (un élément à évaluer). Et c'est précisément à ça que servent les closures.

Plutôt que de réécrire `sorted(utilisateurs, key=(lambda élément: return élément["prénom"]))` 4 fois, on utilise une closure qui va « générer » ces fonctions clés en fonction du champs à utiliser. On définit donc une fonction `tri_champs(champs)`, qui retourne une fonction (appelée `clé` en interne) qui fait ça, en utilisant le paramètre `champs`. Comme le paramètre `champs` est dans le contexte supérieur, `clé()` peut l'utiliser.

La sous-fonction peut aussi modifier l'état de la closure, ce qui permet de faire des fonctions qui gardent leur état entre deux appels de façon beaucoup plus propre qu'avec des variables globales. Pour cela, on utilise le mot-clé `nonlocal variable`.

;;; counterexample ```python/result
# Très, très mauvaise solution avec une variable globale

valeurs_précédentes = []
def moyenne_glissante(val):
    valeurs_précédentes.append(val)
    if len(valeurs_précédentes) > 3:
        valeurs_précédentes.pop(0)
    return sum(valeurs_précédentes) / len(valeurs_précédentes)

print(f"{moyenne_glissante(1)=}")
print(f"{moyenne_glissante(2)=}")
print(f"{moyenne_glissante(3)=}")
print(f"{moyenne_glissante(2)=}")
# Plus tard (ou juste au même moment ailleurs dans le programme)
print("\nPlus tard")
print(f"{moyenne_glissante(1473)=}")
print(f"{moyenne_glissante(1882)=}")
# Oups ! Nos résultats sont pourris par les restes des calculs précédents alors qu'on s'y attendait pas```
;;; example ```python/result
# Bien meilleure version avec une closure (qui permet en plus de paramétrer proprement la fenêtre glissante)
def créer_moyenne_glissante(fenêtre):
    valeurs_précédentes = []
    def moyenne_glissante(val):
        valeurs_précédentes.append(val)
        if len(valeurs_précédentes) > fenêtre:
            valeurs_précédentes.pop(0)
        return sum(valeurs_précédentes) / len(valeurs_précédentes)
    return moyenne_glissante

# Ici même pas de problème pour les entrelacer vu qu'on peut en avoir deux indépendantes
moyenne_glissante_1 = créer_moyenne_glissante(3)
moyenne_glissante_2 = créer_moyenne_glissante(3)
print(f"{moyenne_glissante_1(1)=}")
print(f"{moyenne_glissante_1(2)=}")
print(f"{moyenne_glissante_2(1474)=}")
print(f"{moyenne_glissante_1(3)=}")
print(f"{moyenne_glissante_2(1182)=}")
print(f"{moyenne_glissante_1(2)=}")```
;;;

### Décorateur

En Python, un **décorateur** est une fonction qui modifie le comportement d'une autre fonction (en général en lui ajoutant une fonctionnalité particulière). Il y a une syntaxe spécifique pour *décorer* une fonction :

;;; code ```python
@décorateur
def fonction_décorée(arguments):
    # contenu```
;;;

Par exemple, mettons qu'on veut optimiser notre programme en donnant un *cache* à une fonction, c'est-à-dire conserver ses résultats précédents pour que si on retombe sur les mêmes arguments, on puisse juste prendre ceux du cache plutôt que de tout recalculer. Bien sûr, on peut faire ça directement dans la fonction :

;;; example ```python
import math
import time
import random

def facteurs_premiers_sans_cache(nombre):
    facteurs = []
    for i in range(2, int(math.sqrt(nombre))+1):
        while nombre % i == 0:
            nombre //= i
            facteurs.append(i)
    if nombre > 1:
        facteurs.append(nombre)
    return facteurs

# Ici il n'y a pas de raison que ça parasite quoi que ce soit donc la variable globale est ok tant qu'on ne fait pas d'accès parallèles
_cache_facteurs_premiers = {}
def facteurs_premiers_avec_cache(nombre):
    if nombre in _cache_facteurs_premiers:
        return _cache_facteurs_premiers[nombre]
    facteurs = []
    quotient = nombre
    for i in range(2, int(math.sqrt(nombre))+1):
        while quotient % i == 0:
            quotient //= i
            facteurs.append(i)
    if nombre > 1:
        facteurs.append(quotient)
    _cache_facteurs_premiers[nombre] = facteurs
    return facteurs

valeurs_test = [random.randrange(2, 1000) for _ in range(1000000)]

début = time.time()
for val in valeurs_test:
    facteurs = facteurs_premiers_sans_cache(val)
fin = time.time()
print(f"Sans cache : {fin - début} secondes")

début = time.time()
for val in valeurs_test:
    facteurs = facteurs_premiers_avec_cache(val)
fin = time.time()
print(f"Avec cache : {fin - début} secondes")

# Sans cache : 1.5370118618011475 secondes
# Avec cache : 0.20984220504760742 secondes```
;;;

C'est super, sauf que maintenant si on veut faire ça pour d'autres fonctions, on va devoir répéter l'opération partout, faire plein de caches et la moitié de notre code va servir à gérer des caches. Au lieu de ça, vous remarquez ici que `facteurs_premiers_avec_cache` est en gros pareil que `facteurs_premiers_sans_cache`, mais entouré par quelques opérations de gestion du cache. Et ça, c'est exactement ce que permet un décorateur.

À la base, un décorateur est une fonction qui prend une fonction en paramètre, et renvoie une fonction. Ça donnera ça :

;;; code ```python
@décorateur
def fonction(paramètres):
    # contenu```
;;; code ```python
# Équivalent à
def fonction(paramètres):
    # contenu
fonction = décorateur(fonction)```
;;;

Donc au final, la fonction sera remplacée par ce que le décorateur renverra. Souvent, l'idée sera donc de définir une fonction (le décorateur), qui renvoie une fonction qui ajoute des fonctionnalités (la fonction de remplacement), qui appelle la fonction originale (on l'étend mais sans la remplacer complètement). Comme c'est une fonction dans une fonction, on a toutes les possibilités des closures à portée de main. Dans le cas présent, notre gestion de cache peut se présenter comme ceci :

;;; example ```python/result
import math
import time
import random

def avec_cache(fonction):
    cache = {}
    def remplacement(*args):
        if args in cache:
            return cache[args]
        else:
            résultat = fonction(*args)
            cache[args] = résultat
            return résultat
    return remplacement

@avec_cache
def facteurs_premiers(nombre):
    facteurs = []
    for i in range(2, int(math.sqrt(nombre))+1):
        while nombre % i == 0:
            nombre //= i
            facteurs.append(i)
    if nombre > 1:
        facteurs.append(nombre)
    return facteurs

@avec_cache
def produit_scalaire(vec1, vec2):
    résultat = 0
    for coord1, coord2 in zip(vec1, vec2):
        résultat += coord1 * coord2
    return résultat


valeurs_test = [random.randrange(2, 1000) for _ in range(1000000)]

début = time.time()
for val in valeurs_test:
    facteurs = facteurs_premiers(val)
fin = time.time()
print(f"Avec cache : {fin - début} secondes")```
;;;

Et voilà, le cache est bien appliqué, et en plus c'est totalement réutilisable pour toutes les fonctions que vous voulez en ajoutant juste `@avec_cache` au-dessus. En réalité, cette fonctionnalité existe déjà en plus efficace avec le décorateur `@cache` ou `@lru_cache` définis dans le module [`functools`](https://docs.python.org/fr/3/library/functools.html) de la librairie standard. D'ailleurs ce module définit d'autres fonctions et décorateurs utiles pour pas mal de choses, comme `@singledispatch` pour faire des surcharges de fonction en fonction du type d'un argument par exemple.
