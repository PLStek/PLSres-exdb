//// title = "Les mots magiques"
//// description = "Les variables, attributs et méthodes magiques en Python"

# {=title}

Le titre vous a sûrement un peu interpellé : en Python, il existe ce qu'on appelle souvent les variables, attributs ou méthodes magiques, qui sont des variables, attributs et méthodes qui ont un sens particulier par rapport au langage ou à l'interpréteur, et qui servent à implémenter des comportements particuliers et très utiles. En général, ils ont des noms qui commencent et finissent par deux underscore, comme la méthode `__init__` par exemple. Il y en a des pelletées, on va en voir la plupart ici.

## Objets standard

Vous avez toujours accès à quelques constantes et attributs sur les objets que vous créez, qui donnent des infos dessus ou permettent de l'introspection du code.

### Attributs du module

Vous avez accès à ces attributs dans tous les modules que vous importez. Vous y avez aussi accès en tant que constantes globales, qui donnent alors des infos sur le module où elles se trouvent.

- `__name__` : Nom du module (tel qu'on l'utiliserait pour `import module`). Si le module a été lancé directement comme un script, ce nom vaut `"__main__"`, d'où la recette du `if __name__ == "__main__"` pour tester si on lance comme un script ou si on importe.
- `__file__` : Chemin du fichier
- `__doc__` : Documentation du module (c'est la docstring qui est en haut du fichier)

;;; example ```python/result
if __name__ == "__main__":
    print("Ce fichier a été lancé comme un script !")
else:
    print(f"Ce fichier a été importé comme le module {__name__}")```
;;;

### Attributs de classe

Ces attributs sont accessibles sur toutes les classes (qui sont aussi utilisables comme des objets, on rappelle)

- `__name__` : Nom de la classe (tel que vous l'avez défini dans `class NomDeLaClasse:`)
- `__qualname__` : Nom *qualifié* de la classe (incluant le chemin qui y mène, par exemple `module.MaClasse`)
- `__doc__` : Documentation de la classe (c'est la docstring qui est en haut de la définition de la classe)
- `__bases__` : Liste des classes dont la classe hérite directement

### Attributs de fonction

Ces attributs sont définis sur toutes les fonctions et méthodes (en tout cas celles écrites en Python)

- `__name__` : Nom de la fonction ou de la méthode
- `__qualname__` : Nom qualifié (incluant le chemin qui y mène, comme `module.MaClasse.méthode`)
- `__doc__` : Documentation de la fonction (la docstring)
- `__code__` : L'objet qui contient le code compilé et les infos dessus, si ça vous intéresse

### Attributs d'objet

- `__class__` : Classe d'où l'objet a été défini

## Méthodes magiques

L'intérêt réel est ici : les méthodes magiques permettent d'implémenter tous les comportements « spéciaux » possibles et imaginables sur vos objets, pour les rendre utilisables plus facilement et plus intuitivement par exemple.

;;; warning
N'utilisez jamais ces méthodes pour faire quelque chose qui n'est pas immédiatement évident. On parle d'intégration directe dans la syntaxe du langage, il faut que le comportement aille de soi rien qu'en voyant un signe ou une fonction générique sur l'objet, sans nom de méthode ni aucune explication.

Par exemple, définir `.__complex__()` sur une classe qui représente un point en 2D permet de faire `complex(point)`, ce qui est plutôt pertinent vu qu'un point dans le plan peut se voir comme un nombre sur le plan complexe. Mais n'allez pas faire retourner le module du point à `.__int__()` comme raccourci, parce qu'il n'y a aucun moyen de le savoir juste en voyant juste `int(point)`. Faites plutôt une méthode `point.module()`, ou mieux, utiliser la bonne méthode `.__abs__()` qui est utilisé par `abs(point)` (qui est la valeur absolue / module)
;;;

### Création et destruction des objets

;;; code ```python
def __new__(cls, ...)```
;;; doc
Méthode de classe qui crée un objet. En gros, le processus de construction d'un nouvel objet de la classe `MaClasse` est le suivant :

- Le code appelant utilise `objet = MaClasse(arg1, arg2)`
- La méthode de classe `MaClasse.__new__(arg1, arg2)` est appelée
- `__new__` *crée* l'objet
- Si l'objet est une instance de `MaClasse`, `__new__` ne *doit pas* l'initialiser. Elle doit retourner l'objet et `.__init__(arg1, arg2)` sera appelée automatiquement.
- Si l'objet est une instance d'autre chose, `__init__` ne sera pas appelée automatiquement, c'est à `__new__` d'utiliser le constructeur de l'autre classe correctement
- L'objet est retourné et mis dans la variable `objet`

Vous ne devriez pas avoir à vous préoccuper souvent de cette méthode. On s'en sert surtout pour personnaliser la création d'objets dérivés des types de base, ou dans la création de métaclasses.
;;;

;;; code ```python
def __init__(self, ...)```
;;; doc
Celle-là vous la connaissez bien, c'est le **constructeur**, qui est appelé automatiquement au moment d'initialiser un objet.
La méthode `__init__` récupère les arguments qui sont donnés à la création de l'objet, et ne doit rien retourner.
Si elle n'est pas définie, la classe aura un constructeur vide par défaut.
Quand on initialise une sous-classe, il est généralement nécessaire d'appeler le constructeur de la superclasse pour qu'il initialise correctement le reste de l'objet.
;;;

;;; code ```python
def __del__(self)```
;;; doc
Méthode appelée quand l'objet est sur le point d'être détruit. En principe vous ne devriez jamais avoir à vous préoccuper de ça à moins d'avoir des ressources à libérer explicitement qui traînent dans l'objet — et encore, même dans ces cas-là, on préfère définir une méthode pour les libérer explicitement (`.close()`, …). L'état du programme au moment de la destruction d'un objet est assez imprévisible, donc ne vous reposez sur rien d'extérieur.
;;;

### Représentation de l'objet

Les différentes méthodes de représentation et de conversion de l'objet. Ces méthodes permettent la conversion de l'objet en différents types, et sa compatibilité avec certaines fonctions fondamentales du langage.

;;; code ```python
def __str__(self)```
;;; doc
Convertit l'objet en chaîne de caractères. C'est ce qui est appelé quand vous utilisez `str(objet)` ou `print(objet)`.
Par défaut, si `.__str__()` n'est pas définie, ça renverra le résultat de `.__repr__()`.
Traditionnellement, `.__str__()` est faite pour être écrite et/ou affichée, donc on peut s'attendre à une représentation affichable à un utilisateur par exemple.
;;;

;;; code ```python
def __repr__(self)```
;;; doc
Donne la représentation d'un objet. C'est ce qui est appelé quand vous utilisez `repr(objet)`, avec `{objet !r}` dans une f-string, ou quand l'objet est affiché dans une exception par exemple.
Traditionnellement, on s'attend à ce que `.__repr__()` renvoie plus ou moins une expression en code Python qui puisse recréer l'objet, ou du moins une représentation qui soit utile au débuggage, donc claire et informative pour celui qui débugge.
Si cette méthode n'est pas implémentée, ça donnera une représentation par défaut.
;;; example ```python/result/exception
class Point:
    def __init__(self, nom, x, y):
        self.nom = nom
        self.x = x
        self.y = y

    # Représentation formelle, on peut faire une expression reconstructible donc on le fait
    def __repr__(self):
        return f"{self.__class__.__name__}({self.nom !r}, {self.x}, {self.y})"

    # Représentation propre et affichable
    def __str__(self):
        return f"{self.nom}({self.x}, {self.y})"

A = Point("A", 1, 1.5)
B = Point("B", 2, -1)
print(A)
print(repr(A))```
;;;

;;; code ```python
def __bool__(self)```
;;; doc
Donne la valeur de vérité de l'objet (s'il doit être considéré vrai ou faux). Cette méthode est utilisée quand vous utilisez `bool(objet)` ou quand vous utilisez sa valeur de vérité (`if objet`, `while objet`, l'utiliser avec un opérateur logique `and`, `or` ou `not`, …).
En général, on s'attend à ce que l'objet soit faux quand il est vide ou nul.
Par défaut, si cette méthode n'existe pas, la méthode `.__len__()` sera utilisée pour savoir si l'objet aurait une longueur nulle — et si elle non plus n'est pas là, il sera toujours considéré vrai.
;;; example ```python/result
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __bool__(self):
        """Renvoie faux seulement si les coordonnées du point sont nulles, vrai sinon"""
        return self.x != 0 or self.y != 0

A = Point(0, 0)
B = Point(0, -1)
if not A:
    print("A est faux")
if B:
    print("B est vrai")```
;;;

;;; code ```python
def __index__(self)```
;;; doc
Donne la représentation de l'objet sous forme d'un nombre entier. C'est ce qui est appelé quand vous utilisez l'objet comme index (`liste[objet]`), par les fonctions `bin(objet)`, `oct(objet)`, `hex(objet)`, et par `int(objet)` si la méthode `.__int__()` n'est pas définie.
;;;

;;; code ```python
def __int__(self)```
;;; doc
Donne la représentation de l'objet sous forme d'un nombre entier. C'est ce qui est appelé en priorité quand vous utilisez `int(objet)`.
Par défaut, si cette méthode n'est pas définie, les méthodes `.__index__()` et `.__trunc__()` seront essayées, et si aucune n'existe, l'opération échouera.
Cette méthode ne sert *pas* pour utiliser l'objet comme index, ou pour les méthodes `bin`, `oct` et `hex`
;;;

;;; code ```python
def __float__(self)```
;;; doc
Convertit l'objet en nombre réel (renvoie un `float`). C'est ce qui est appelé par `float(objet)`.
Si cette méthode n'est pas définie, la conversion n'est pas possible.
;;;

;;; code ```python
def __complex__(self)```
;;; doc
Convertit l'objet en nombre complexe (renvoie un `complex`). C'est ce qui est appelé par `complex(objet)`
Si cette méthode n'est pas définie, la conversion n'est pas possible.
;;;

### Surcharger les opérateurs

;;; code ```python
def __eq__(self, objet)  # self == objet
def __ne__(self, objet)  # self != objet
def __lt__(self, objet)  # self < objet
def __le__(self, objet)  # self <= objet
def __gt__(self, objet)  # self > objet
def __ge__(self, objet)  # self >= objet```
;;; doc
Ces méthodes implémentent les opérateurs de comparaison de vos objets avec d'autres.
Elles peuvent retourner trois valeurs :

- `True` si la relation est vraie, `False` si elle ne l'est pas
- `NotImplemented` si vous ne supportez pas la comparaison avec l'autre objet.

Donc `True` veut dire que c'est vrai, `False` veut dire que vous **savez avec certitude que c'est faux**, et `NotImplemented` veut dire que vous ne savez pas comparer avec l'autre objet. Si la méthode renvoie `NotImplemented`, la méthode symétrique sera tentée sur l'autre objet. Si vous utilisez `x < y`, ça tentera d'abord `x.__lt__(y)`, puis `y.__gt__(x)`. Si les deux renvoient `NotImplemented`, ça donnera `False` dans le cas de `__eq__` (on part du principe que si aucun des deux ne sait se comparer à l'autre, il y a peu de chances qu'ils soient égaux), `True` dans le cas de `__ne__` (l'inverse de `__eq__`), et pour tous les autres ce sera une `TypeError` (l'opération n'est pas supportée entre les deux objets).
Par défaut, vous n'êtes pas obligé de définir `__ne__` si vous avez défini `__eq__`, Python prendra juste l'inverse du résultat de `__eq__`.
Notez que définir `__eq__` a des implications au niveau de la *hashabilité* et de l'utilisation comme clé de dictionnaire, voir {> info.python.recettes.magic#hash} pour plus d'infos.
;;; example ```python/result
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Ici, un Point est égal à un autre Point avec les mêmes coordonnées x et y,
    # ou à une liste de deux coordonnées avec les mêmes valeurs
    def __eq__(self, point):
        # Si c'est un autre Point, pas de problème : on sait si c'est vrai ou faux
        if isinstance(point, Point):
            return self.x == point.x and self.y == point.y
        # Si c'est bien une collection de 2 coordonnées, on peut comparer aussi
        # Dans tous les autres cas, on ne sait pas faire la comparaison donc on
        # retourne NotImplemented, au cas où l'autre objet sache faire.
        try:
            if len(point) == 2:
                return self.x == point[0] and self.y == point[1]
            else:
                return NotImplemented
        except (TypeError, LookupError):
            return NotImplemented
    # Ici l'inverse de __eq__ est très bien pour l'opérateur !=, et les autres
    # comparaisons n'ont pas grand sens entre des points.

A = Point(1, 1)
print(f"{A == Point(0, -1)=}")
print(f"{A == Point(1, 1)=}")
print(f"{A == (1, 1)=}")```
;;;

;;; code ```python
@functools.total_ordering```
;;; doc
Décorateur de classe qui permet de réduire le travail quand vous implémentez les opérateurs de comparaisons.
Avec ça, vous pouvez n'implémenter que `__eq__` et une méthode de comparaison (`__lt__`, `__le__`, `__gt__` ou `__ge__`), et ça définit tout seul toutes les autres.
;;; example ```python/result
import functools

@functools.total_ordering
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    def __eq__(self, node):
        if isinstance(node, Node):
            return self.value == node.value
        else:
            return NotImplemented

    def __lt__(self, node):
        if isinstance(node, Node):
            return self.value < node.value
        else:
            return NotImplemented

right = Node(10)
left = Node(6)
top = Node(7, left, right)
print(f"{left} == {right} : {left==right}")
print(f"{left} < {right} : {left<right}")
print(f"{left} <= {right} : {left<=right}")
print(f"{left} > {right} : {left>right}")
print(f"{left} >= {right} : {left>=right}")
print(f"{left} != {right} : {left!=right}")```
;;;

;;; code ```python
def __neg__(self)  # -self
def __pos__(self)  # +self
def __abs__(self)  # abs(self) (valeur absolue ou module)
def __invert__(self)  # ~self (inversion bit par bit)```
;;; doc
Ces méthodes implémentent les opérateurs unaires du langage, c'est-à-dire ce que doivent renvoyer le résultat de `+obj`, `-obj`, `~obj` et `abs(obj)`.
Si ces méthodes ne sont pas définies, ces opérations ne seront pas possibles
;;; example ```python/result
import math

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def __pos__(self):
        # À moins d'y mettre un comportement particulier (rare), on renvoie le même objet
        # Cependant, quand on utilise un opérateur sur un objet, on ne s'attend pas à recevoir
        # une référence sur l'objet d'origine (si j'avais A = Point(1, 1); B = +A; B.x = 0, ça mettrait aussi A.x à 0)
        # Donc il vaut mieux renvoyer une copie. Comme ça ça peut en plus servir de moyen facile de copier un objet.
        # De toute façon c'est un opérateur qu'on n'utilise que très rarement,
        # vous pouvez aussi bien ne pas l'implémenter du tout et ça ne gênerait probablement personne.
        return Point(self.x, self.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __abs__(self):
        # Opérateur valeur absolue ou module, donc ici le module
        return math.sqrt(self.x**2 + self.y**2)

A = Point(1, -1)
print(f"{+A=}, {-A=}, {abs(A)=}")```
;;;

;;; code ```python
def __add__(self, obj)       # self + obj
def __sub__(self, obj)       # self - obj
def __mul__(self, obj)       # self * obj
def __truediv__(self, obj)   # self / obj
def __floordiv__(self, obj)  # self // obj
def __matmul__(self, obj)    # self @ obj (produit matriciel)
def __mod__(self, obj)       # self % obj
def __divmod__(self, obj)    # divmod(self, obj)
def __pow__(self, obj[, mod])  # self ** obj, pow(self, obj) ou pow(self, obj, modulo)
def __lshift__(self, obj)    # self << obj
def __rshift__(self, obj)    # self >> obj
def __and__(self, obj)       # self & obj (pas `self and obj`)
def __or__(self, obj)        # self | obj (pas `self or obj`)
def __xor__(self, obj)       # self ^ obj```
;;; doc
Vous l'aurez compris, ces méthodes permettent d'utiliser les différents opérateurs mathématiques du langage avec vos objets. Vous avez accès à tous les opérateurs habituels, plus deux un peu spéciaux : `a @ b` qui est là depuis Python 3.5 pour les produits matriciels (le langage de base ne s'en sert pas mais ça facilite pas mal la vie des utilisateurs de toutes les grosses librairies de mathématiques et data science comme numpy, scipy, pandas, etc.). L'autre opérateur c'est `.__divmod__()`, qui est en fait utilisé par la fonction `divmod(a, b)`, et qui retourne deux valeurs : le résultat de `a // b`, et celui de `a % b`.

Il y a aussi l'opérateur puissance, qui est appelé par `a ** b`, mais aussi `pow(a, b, mod)`, où `mod` est un argument optionnel qui permet de faire a^b mod c de façon plus efficace. Si vous ne voulez pas supporter la puissance avec le modulo, vous n'êtes même pas obligés de mettre l'argument dans votre méthode.

Toutes ces méthodes sont appelées quand un objet de votre classe est à gauche de l'opérateur, et un autre est à droite. Il peuvent retourner ce que vous voulez (ce qui est pertinent de renvoyer selon l'opération). Dans tous les cas, si l'opération n'est pas supportée pour les arguments donnés, **ces méthodes doivent retourner la valeur spéciale `NotImplemented`. C'est parce que comme ça, si *votre* objet ne supporte pas l'opération avec l'autre, on peut tenter avec l'autre plutôt que de foirer immédiatement. Donc pensez à bien vérifier que l'opération est supportée, et à renvoyer `NotImplemented` dans le cas contraire plutôt que de laisser l'opération donner une exception.
;;; note
Essayez de respecter au maximum le duck typing : pour tester le support des opérations, on est souvent tentés d'utiliser `isinstance()` à tour de bras pour ne sélectionner que les types qu'on reconnaît, mais ce n'est pas du tout le principe de Python. Si c'est possible, il vaut mieux tenter le coup dans un `try-except`, voir si l'objet supporte l'opération, et renvoyer `NotImplemented` si ça foire, plutôt que rejeter direct sous prétexte que vous ne connaissez pas l'autre type. Par exemple, si vous voulez supporter une opération avec des listes et des tuples vous pouvez utiliser `isinstance(obj, (list, tuple))`, mais dans ce cas exit les tableaux du module `array`, de `numpy`, et de sûrement plein d'autres librairies de géométrie. Si Python est un environnement aussi agréable à utiliser c'est parce que tant que les librairies sont conçues autour de ce principe, tout le monde est compatible avec tout le monde, au lieu de devoir convertir et reconvertir en permanence comme en Java ou C++.

Cela dit attention à ne pas accepter n'importe quoi non plus : par exemple pour notre point en 2D, il ne vaut mieux pas accepter d'additionner avec n'importe quoi qui a des attributs `x` et `y` car s'il s'agit d'une autre classe qui représente un point en 3D avec `x`, `y` et `z`, on renverra un mauvais résultat, il vaut mieux alors renvoyer `NotImplemented` et laisser le point en 3D s'en charger. En général :

- Si l'opération se base sur des méthodes ou des capacités de l'autre objet, l'approche duck typing est mieux parce que ce sont des méthodes qui encapsulent le bon comportement
- Si l'opération se base plutôt sur les attributs ou des méthodes d'usage interne de l'objet, il vaut mieux vérifier le type parce que vous ne pouvez pas prendre les attributs bruts (sans encapsulation donc) de l'autre objet et espérer que tout se passe bien.

Notez d'ailleurs que si l'opération a un sens évident, ce n'est pas du tout obligé d'être le rôle d'origine de l'opérateur : par exemple, les objets `Path` du module `pathlib`, qui représentent des chemins sur le système de fichiers, permettent de créer des chemins dérivés avec l'opérateur `/`, comme un chemin qui utilise des `/` (ex. `chemin_base / "temp" / "plstek_result.py"`).
;;; example ```python/result/exception
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    def __add__(self, point):
        # Ici on se base sur les attributs, il vaut mieux vérifier pour être sûr de ne pas faire n'importe quoi
        if isinstance(point, Point):
            return Point(self.x + point.x, self.y + point.y)
        # On veut aussi que ça marche avec des listes de 2 nombres
        # Le critère de validité, c'est que ce soit un conteneur ordonné (où on peut piocher avec un index)
        # qui contient deux éléments qu'on peut additionner à des nombres
        # Tout ça c'est des qualités de l'objet, donc on utilise l'approche duck typing
        try:
            if len(point) == 2:
                return Point(self.x + point[0], self.y + point[1])
            else:
                return NotImplemented  # S'il n'y a pas 2 coordonnées comme Point, on ne supporte pas
        # TypeError si len(point) a échoué (pas de taille = pas un conteneur fini, ça passe pas)
        # TypeError si point ne supporte pas l'opérateur d'indexation `objet[x]`
        #     dans ce cas ce n'est pas un conteneur ordonné donc c'est pas bon
        # LookupError c'est la superclasse de IndexError et KeyError, c'est levé quand objet[x] n'existe pas
        #     ici ce serait parce que l'objet n'utilise pas les index 0 et 1 pour récupérer ses éléments,
        #     donc on ne peut rien en faire
        # TypeError si une addition a échoué, donc si le contenu de l'objet ne peut pas s'additionner à des nombres
        # Quand vous faites ça, il faut être à la fois complet et aussi spécifique que possible dans les erreurs que vous interceptez,
        # car il faut intercepter toutes les causes d'échec possible sans pour autant intercepter des véritables erreurs de programmation
        except (TypeError, LookupError):
            return NotImplemented

    def __sub__(self, point):
        # Ici tout marche à peu près pareil que dans __add__
        # On pourrait truander en faisant return self.__add__(-point), mais les listes n'aimeraient pas
        if isinstance(point, Point):
            return Point(self.x - point.x, self.y - point.y)
        try:
            if len(point) == 2:
                return Point(self.x - point[0], self.y - point[1])
            else:
                return NotImplemented
        except (TypeError, LookupError):
            return NotImplemented

    def __mul__(self, obj):
        # Support de la multiplication avec un scalaire
        # Ici le critère de validité, c'est que l'objet puisse être multiplié par un nombre
        # On se base sur une capacité de l'objet, donc on lui fait confiance et on essaie
        # avant d'invalider l'opération. Mais on n'est pas aveugles non plus,
        # les coordonnées de nos points doivent être des nombres, donc on reconvertit après
        # pour être sûr
        try:
            return Point(float(self.x * obj), float(self.y * obj))
        # TypeError si une multiplication a échoué (l'objet ne la supporte pas)
        # ValueError si les résultats des multiplications n'étaient pas convertibles en float
        except (TypeError, ValueError):
            return NotImplemented

    def __matmul__(self, point):
        # On utilise l'opérateur @ pour le produit scalaire, il est fait pour ça
        # Pareil que pour l'addition, il nous faut un autre objet qui se comporte comme un point avec deux coordonnées
        # donc soit un Point, soit une liste de deux coordonnées
        if isinstance(point, Point):
            return self.x*point.x + self.y*point.y
        try:
            if len(point) == 2:
                return self.x*point[0] + self.y*point[1]
            else:
                return NotImplemented
        except (TypeError, LookupError):
            return NotImplemented

import array

A = Point(1, 2)
B = Point(0, 4)
C = (4, 5)
# D est un tableau d'octets du module array, donc un conteneur qui ressemble à une liste ou un tuple sans en être vraiment un,
# mais comme on a respecté le duck typing ça marchera quand même
D = array.array("b", (-1, 3))

print(f"{A+B=}, {A+C=}, {A+D=}")
print(f"{A-B=}, {A-C=}, {A-D=}")
print(f"{A@B=}, {A@C=}, {A@D=}")

# Tout ça fonctionne normalement
print(f"{A*2=}, {A*2.7=}, {A*False=}")
# Mais comme on a bien fait attention que les résultats soient convertibles en float,
# Ceci échoue (comme il se doit) plutôt que de donner un point ("X", "XX")
# D'ailleurs vous verrez dans l'exception qu'après avoir retourné NotImplemented,
# Python a bien essayé de demander à la chaîne de caractère de faire la multiplication
print(f"{A*'X'=}")```
;;;

;;; code ```python
def __radd__(self, obj)       # obj + self
def __rsub__(self, obj)       # obj - self
def __rmul__(self, obj)       # obj * self
def __rtruediv__(self, obj)   # obj / self
def __rfloordiv__(self, obj)  # obj // self
def __rmatmul__(self, obj)    # obj @ self (produit matriciel)
def __rmod__(self, obj)       # obj % self
def __rdivmod__(self, obj)    # divmod(obj, self)
def __rpow__(self, obj[, mod])  # self ** self, pow(obj, self) ou pow(obj, self, modulo)
def __rlshift__(self, obj)    # obj << self
def __rrshift__(self, obj)    # obj >> self
def __rand__(self, obj)       # obj & self (pas `self and self`)
def __ror__(self, obj)        # obj | self (pas `self or self`)
def __rxor__(self, obj)       # obj ^ self```
;;; doc
On rajoute juste un `r` devant (pour right). C'est exactement pareil, mais dans l'autre sens. Quand vous utilisez un opérateur comme `gauche + droite` en Python, ça se passe comme ça :

- Ça tente d'abord `gauche.__add__(droite)`. Si ça renvoie un résultat, c'est terminé
- Si `gauche.__add__(droite)` n'existe pas ou a renvoyé `NotImplemented`, ça essaie `droite.__radd__(gauche)`
- Si `droite.__radd__(gauche)` renvoie un résultat c'est parfait, si elle n'existe pas ou renvoie `NotImplemented`, c'est que l'opération n'est pas possible et ça se termine en `TypeError`.

Il y a une exception à ça, c'est si `droite` vient d'une sous-classe de `gauche`. Pour être sûr que le comportement de la sous-classe peut bien s'exprimer par-dessus de celui de la super-classe même si elle est à droite, dans ce cas-là on inverse : ça essaie d'abord `droite.__radd__(gauche)` puis `gauche.__add__(droite)`.
;;; example ```python/result
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    # Les opérateurs de base sont les mêmes que ci-dessus
    def __add__(self, point):
        if isinstance(point, Point):
            return Point(self.x + point.x, self.y + point.y)
        try:
            if len(point) == 2:
                return Point(self.x + point[0], self.y + point[1])
            else:
                return NotImplemented  # S'il n'y a pas 2 coordonnées comme Point, on ne supporte pas
        except (TypeError, LookupError):
            return NotImplemented

    def __radd__(self, point):
        # L'addition est commutative, donc on peut recycler notre méthode existante
        return self.__add__(point)

    def __sub__(self, point):
        if isinstance(point, Point):
            return Point(self.x - point.x, self.y - point.y)
        try:
            if len(point) == 2:
                return Point(self.x - point[0], self.y - point[1])
            else:
                return NotImplemented
        except (TypeError, LookupError):
            return NotImplemented

    def __rsub__(self, point):
        # Par contre la soustraction il va falloir se la retaper
        if isinstance(point, Point):
            return Point(point.x - self.x, point.y - self.y)
        try:
            if len(point) == 2:
                return Point(point[0] - self.x, point[1] - self.y)
            else:
                return NotImplemented
        except (TypeError, LookupError):
            return NotImplemented

    def __mul__(self, obj):
        try:
            return Point(float(self.x * obj), float(self.y * obj))
        except (TypeError, ValueError):
            return NotImplemented

    def __rmul__(self, obj):
        # La multiplication est commutative, on peut recycler
        return self.__mul__(obj)

    def __matmul__(self, point):
        if isinstance(point, Point):
            return self.x*point.x + self.y*point.y
        try:
            if len(point) == 2:
                return self.x*point[0] + self.y*point[1]
            else:
                return NotImplemented
        except (TypeError, LookupError):
            return NotImplemented

    def __rmatmul__(self, point):
        # Ici on utilise cet opérateur comme produit scalaire de deux vecteurs,
        # qui est commutatif, donc on réutilise notre méthode existante
        # Mais bien sûr, un vrai produit matriciel ne serait pas commutatif
        return self.__matmul__(point)

import array

A = Point(1, 2)
B = Point(0, 4)
C = (4, 5)
D = array.array("b", (-1, 3))

# Maintenant, ça marche avec tous les objets compatibles, même quand notre Point est à droite
print(f"{B+A=}, {C+A=}, {D+A=}")
print(f"{B-A=}, {C-A=}, {D-A=}")
print(f"{B@A=}, {C@A=}, {D@A=}")
print(f"{2*A=}, {2.7*A=}, {False*A=}")```
;;;

;;; code ```python
def __iadd__(self, obj)       # self += obj
def __isub__(self, obj)       # self -= obj
def __imul__(self, obj)       # self *= obj
def __itruediv__(self, obj)   # self /= obj
def __ifloordiv__(self, obj)  # self //= obj
def __imatmul__(self, obj)    # self @= obj (produit matriciel)
def __imod__(self, obj)       # self %= obj
def __ipow__(self, obj)       # self **= obj
def __ilshift__(self, obj)    # self <<= obj
def __irshift__(self, obj)    # self >>= obj
def __iand__(self, obj)       # self &= obj
def __ior__(self, obj)        # self |= obj
def __ixor__(self, obj)       # self ^= obj```
;;; doc
Ces méthodes servent à implémenter les opérations sur place (du type `a += b` par exemple, le `i` veut dire *in-place*).
En théorie, si vous implémentez ces méthodes, elles devraient modifier l'objet sur place (donc faire les modifs directement sur `self` plutôt que de créer un nouvel objet), et renvoyer `self` (ou autre chose, mais si c'est pour créer un nouvel objet quand même ça sert à rien)
En réalité, quand ces méthodes ne sont pas implémentées, ça fera juste `a = a+b` avec les méthodes habituelles — ces méthodes permettent surtout des optimisations, pour éviter de recréer un objet intermédiaire. En principe ça fait aussi que l'objet reste le même, donc si vous avez une autre référence sur l'objet ça reste le même au lieu d'en faire un nouveau, mais c'est déjà pas un comportement qui devrait être important dans un programme bien fait à la base.
Ces méthodes permettent des optimisations substantielles si elles sont utilisées souvent donc c'est bien de les avoir si vous écrivez une librairie supposée être distribuée ou si vous avez besoin de performances, mais à part ça c'est parfaitement optionnel.
Pour des raisons évidentes, il n'y a que la version où votre objet est à gauche de l'opérateur.
;;; example ```python/result
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    # Les opérateurs de base sont les mêmes que ci-dessus
    def __iadd__(self, point):
        if isinstance(point, Point):
            self.x += point.x
            self.y += point.y
            return self
        try:
            if len(point) == 2:
                self.x += point[0]
                self.y += point[1]
                return self
            else:
                return NotImplemented  # S'il n'y a pas 2 coordonnées comme Point, on ne supporte pas
        except (TypeError, LookupError):
            return NotImplemented

A = Point(1, 2)
print(f"{A=}")
A += Point(1, -1)
print(f"{A=}")
A += (-1, -4)
print(f"{A=}")```
;;;

;;; code ```python
def __trunc__(self)
def __floor__(self)
def __ceil__(self)
def __round__(self, décimales=0)```
;;; doc
Méthodes utilisées pour implémenter les différents types d'arrondis : troncature, arrondi à l'entier inférieur, arrondi à l'entier supérieur et arrondi à l'entier le plus proche ou à un certain nombre de décimales. C'est ça qu'utilisent les fonctions `math.trunc(objet)`, `math.floor(objet)`, `math.ceil(objet)` et `round(objet)`.
À part éventuellement `__round__` quand on lui donne un nombre de décimales, tout ça doit retourner un entier.
`__trunc__` est aussi utilisée en dernier recours par la fonction `int(objet)` si les méthodes `.__int__()` et `.__index__()` n'existent pas.
Si ces méthodes ne sont pas définies, les fonctions qui les utilisent échoueront.
;;;

### Méthodes de conteneur

Vous pouvez aussi implémenter vos propres collections et conteneurs avec des méthodes magiques.

;;; code ```python
def __len__(self)```
;;; doc
Donne le nombre d'éléments dans le conteneur. C'est ce qui est appelé par la fonction `len(objet)`.
Si votre classe ne définit pas la méthode `.__bool__()`, la valeur de vérité de l'objet sera fausse si `.__len__()` renvoie 0 et vrai autrement.
Donc quand vous implémentez un conteneur, à moins d'avoir une bonne raison de faire autrement, pas la peine d'implémenter `.__bool__()`, la longueur le fait très bien.
;;;

;;; code ```python
def __contains__(self, obj)```
;;; doc
Implémente l'opérateur `obj in conteneur`. Doit renvoyer `True` si le conteneur contient l'objet (d'après l'opérateur `==` en principe), `False` s'il n'y est pas.
Notez que si votre conteneur implémente les autres méthodes de conteneur (`__iter__` et/ou `__getitem__`), Python peut se débrouiller tout seul pour itérer sur votre conteneur et rechercher l'objet, et il le fait d'ailleurs mieux que vous. Donc si vous avez moyen d'implémenter ça plus efficacement que par une recherche naïve, ou si juste itérer sur le conteneur ne donnera pas le bon résultat, implémentez `__contains__` — sinon laissez faire l'interpréteur. Si votre classe est un wrapper autour d'un conteneur existant, faites passer au conteneur interne (`return obj in self.conteneur`)
;;;

;;; code ```python
def __iter__(self)```
;;; doc
Renvoie un **itérateur** sur votre conteneur. Cette méthode est appelée par la fonction `iter(objet)`, et chaque fois que vous itérez dessus par une boucle `for`, ou par quoi que ce soit qui demande un objet itérable (compréhensions, `map()`, `filter()`, …). C'est aussi utilisé quand vous convertissez en une autre collection (`list(objet)`, `tuple(objet)`, `set(objet)`, …). C'est nécessaire pour pouvoir itérer dessus, et il faut bien renvoyer un nouvel itérateur à chaque fois qu'on itère sur l'objet. Si vous créez un conteneur associatif (clé -> valeur, comme `dict`), l'itérateur par défaut doit itérer sur les clés.
Un itérateur est un objet particulier qui implémente plusieurs méthodes (magiques, elles aussi) :

- `def __next__(self)` : Avance l'itération d'un élément et renvoie l'élément à cet endroit, ou lève une exception `StopIteration` quand il a épuisé les éléments à itérer.
- `def __iter__(self)` : Un itérateur doit être lui-même itérable, en général on fait juste `return self`.

Il y a en gros trois techniques pour créer un itérateur pour votre conteneur :

- La méthode à l'ancienne, créer une classe exprès, ça on ne le fait plus trop à moins d'avoir des besoins extrêmement spécifiques qui ne permettent pas les autres solutions (pour itérer sur les nœuds d'un graphe par exemple)
- Faire de la méthode `.__iter__()` un générateur, qui `yield` les éléments au fur et à mesure, c'est la façon moderne de le faire. Comme un générateur implémente l'interface d'un itérateur, tout marche parfaitement.
- Si votre conteneur est juste un *wrapper* autour d'un conteneur existant, utiliser `iter()` sur l'objet wrappé.
;;; example ```python
class Masque:
    def __init__(self, nom_options):
        self.options = {nom: False for nom in nom_options}

    # Autres méthodes...

    def __iter__(self):
        # Cas trivial ici : notre conteneur est un wrapper autour d'un conteneur existant
        # (ici un dictionnaire), donc on peut juste renvoyer l'itérateur du dictionnaire
        return iter(self.options)```
;;; example ```python/result
import heapq

# Cas un peu plus complexe : on implémente un wrapper pour faciliter l'utilisation d'un tas
# (en gros une structure qui reste toujours triée de façon efficace, c'est la base du tri par tas),
# et on veut qu'itérer dessus donne les éléments triés
# Mais réellement triés, pas direct dans l'ordre de la liste interne, c'est pas pareil
# On doit donc implémenter notre propre itérateur
class Heap:
    def __init__(self, content):
        self.heap = list(content)
        heapq.heapify(self.heap)

    def push(self, item):
        heapq.heappush(self.heap, item)

    def pop(self):
        return heapq.heappop(self.heap)

    def __len__(self):
        return len(self.heap)

    def __contains__(self, obj):
        return obj in self.heap

    def __iter__(self):
        # Du coup cette fois on doit créer notre propre itérateur
        # Un générateur fait très bien l'affaire
        copy = self.heap.copy()
        for i in range(len(copy)):
            yield heapq.heappop(copy)

heap = Heap([16, 74, 51, 10, 1, 55])
heap.push(14)
heap.push(80)
print(f"{heap.pop()=}")
print(f"\nOrdre interne de la liste : {heap.heap}")
print(f"Par l'itérateur :           [", end="")
for item in heap:
    print(item, end=", ")
print("]")```
;;;

;;; code ```python
def __getitem__(self, index)
def __setitem__(self, index, valeur)
def __delitem__(self, index)```
;;; doc
Ces méthodes sont utilisées pour indexer votre conteneur : `conteneur[index]` est équivalent à `conteneur.__getitem__(index)`, `conteneur[index] = valeur` est équivalent à `conteneur.__setitem__(index, valeur)`, et `del conteneur[index]` est équivalent à `conteneur.__delitem__(index)`.
L'index est un objet quelconque, qui sera utilisé pour identifier un élément de votre conteneur. Ça peut être ce que vous voulez, par exemple les listes utilisent des nombres entiers, les dictionnaires des objets hashables, et les ensembles ne supportent pas l'indexation du tout : vous n'êtes absolument pas obligé de supporter l'indexation, vous pouvez même supporter certaines de ces méthodes et pas les autres.

Cependant, il y a un cas particulier : les *slices* (tranches). Concrètement, quand vous indexez avec la syntaxe `conteneur[début:fin:pas]`, ça appelle la méthode `.__getitem__()` avec un objet `slice` qui contient ces informations dans ses attributs `.start`, `.stop` et `.step`. Ces attributs valent `None` s'ils n'étaient pas précisés (par exemple `conteneur[:5]` donnera `5` dans `.stop` et `None` pour le reste). Si vous voulez supporter ce type d'indexation, il faudra bien séparer le cas où vous obtenez un objet simple, et le cas des slices. Notez qu'en principe, des valeurs absurdes dans une `slice` ne devraient pas causer d'erreur, et marcher comme on s'y attendrait. Par exemple, utiliser `liste[:10]` sur une liste de 3 éléments renverra juste toute la liste sans poser de question, même si `liste[10]` est une erreur. Pensez aussi à supporter les index négatifs si vous voulez un comportement qui ressemble aux conteneurs habituels.

Notez bien que `liste[3:6] = [1, 2, 3]` est tout à fait possible et le cas où le conteneur donné ne correspond pas à la taille de la tranche peut se traiter de différentes manières :

- Les conteneurs standard acceptent que le conteneur donné n'ait pas la même taille que la tranche, et vont juste insérer ce qu'il faut. Par exemple, `liste = [1, 2, 3]; liste[1:2] = [10, 11, 12]` donnera `[1, 10, 11, 12, 3]`. C'est un cas souvent tordu à traiter, qui peut être pratique mais qui est rarement utilisé parce que même à utiliser c'est un peu confus. Si vous écrivez quelque chose de sérieux qui doit être aussi générique que possible, et si c'est pertinent, c'est bien de supporter ça, mais absolument pas une obligation
- Ou alors vous pouvez juste en faire une erreur, ça ne gênera pas non plus grand monde.
;;; example ```python/result
# Ici on définit une classe qui permet d'enchaîner plusieurs listes,
# mais en gardant les listes originales, qui peuvent donc être modifiées individuellement
class Chaine:
    def __init__(self, *listes):
        self.listes = listes

    def __repr__(self):
        return "Chain(" + ", ".join([str(item) for item in self.__iter__()]) + ")"

    def __iter__(self):
        for liste in self.listes:
            yield from liste

    def __len__(self):
        return sum(map(len, self.listes))

    def _index(self, index):
        """Retourne l'index de la liste et l'index dans la liste où se trouve l'élément demandé
        La gestion des index et des slices sera pratiquement toujours la même entre __getitem__
        et __setitem__, donc si c'est un traitement un peu complexe (et ce sera sûrement le cas
        si vous bidouillez des slices), ne vous répétez pas"""
        # Traitement des index négatifs : ils partent de la fin
        if index < 0:
            index = self.__len__() + index

        début_actuel = 0
        index_liste = 0
        while index - début_actuel >= len(self.listes[index_liste]):
            début_actuel += len(self.listes[index_liste])
            index_liste += 1
        return index_liste, index - début_actuel

    def _index_slice(self, index):
        """Retourne un itérateur qui donne l'index de la liste et l'index dans la liste
        de chaque élément demandé par la slice donnée."""
        longueur = self.__len__()

        if index.start is None:  # Début pas défini, on part de 0 par défaut
            start = 0
        elif index.start < 0:  # Index négatif
            start = longueur + index.start
        elif index.start >= longueur:  # Début plus loin que la fin du conteneur, ça retournera rien
            return []
        else:
            start = index.start

        if index.stop is None:
            stop = longueur
        elif index.stop < 0:
            stop = longueur + index.stop
        elif index.stop <= start:  # Fin avant le début, ça ne retournera rien
            return []
        else:
            stop = min(index.stop, longueur)  # Pour ne pas aller plus loin que la fin du conteneur

        step = 1 if index.step is None else index.step
        résultat = []
        début_actuel = 0
        index_liste = 0
        for i in range(start, stop, step):
            while i - début_actuel >= len(self.listes[index_liste]):
                début_actuel += len(self.listes[index_liste])
                index_liste += 1
            yield index_liste, i - début_actuel

    def __getitem__(self, index):
        # On teste le cas des slices. C'est une syntaxe particulière qui donnera
        # toujours un objet de type `slice`, ici pas de duck typing qui tienne
        # (par contre, on fait confiance aux bornes pour être des entiers ou équivalents)
        # C'est beaucoup de traitement pour s'occuper des slices,
        # mais ça rend les conteneurs pour lesquels c'est pertinent beaucoup plus pratiques
        if isinstance(index, slice):
            résultat = []
            for index_liste, index_élément in self._index_slice(index):
                résultat.append(self.listes[index_liste][index_élément])
            # En général, quand on tranche, on s'attend à recevoir un conteneur du même
            # type que l'objet qu'on vient de trancher. Ici ça sert pas à grand chose,
            # mais si c'est possible il vaut mieux éviter les comportements incohérents
            return Chaine(résultat)
        # Cas d'un simple index
        else:
            index_liste, index_élément = self._index(index)
            return self.listes[index_liste][index_élément]

    def __setitem__(self, index, valeur):
        # Cas des slices : ici on n'accepte que les tranches de la bonne taille
        # Si on voulait être parfaitement rigoureux il faudrait beaucoup plus de
        # vérifications d'erreur ici
        if isinstance(index, slice):
            for i, (index_liste, index_élément) in enumerate(self._index_slice(index)):
                self.listes[index_liste][index_élément] = valeur[i]
        else:
            index_liste, index_élément = self._index(index)
            self.listes[index_liste][index_élément] = valeur

    def __delitem__(self, index):
        if isinstance(index, slice):
            indices = list(self._index_slice(index))
            for index_liste, index_élément in reversed(indices):
                del self.listes[index_liste][index_élément]
        else:
            index_liste, index_élément = self._index(index)
            print(index_liste, index_élément)
            del self.listes[index_liste][index_élément]

chaine = Chaine([1, 2, 3], [10, 11, 12, 13], [100, 101], [1000, 1001, 1002, 1003, 1004])
print(f"{list(chaine)=}")  # list(chaine) utilise .__iter__()

print("\n======== Utilisation de __getitem__")
# Indexation simple
print(f"{chaine[4]=}")
print(f"{chaine[8]=}")
# Slices, en vérifiant par exemple les indices négatifs
print(f"{chaine[6:10]=}")
print(f"{chaine[1:-1]=}")
print(f"{chaine[-5:]=}")  # 5 derniers éléments
print(f"{chaine[:10:3]=}")

print("\n======== Utilisation de __setitem__ et __delitem__")
chaine[4] = 99
chaine[:10:3] = [5, 55, 555, 5555]
del chaine[-1]
print(chaine)```
;;;

;;; code ```python
def __reversed__(self)```
;;; doc
Doit renvoyer un itérateur qui itère sur les éléments du conteneur dans l'ordre inverse. C'est ce qui est utilisé par la fonction `reversed(objet)`.
Par défaut, si cette méthode n'est pas définie, `reversed()` se débrouille en utilisant `.__len__()` et `.__getitem__()`. Donc n'implémentez cette méthode que si c'est pertinent, et si vous êtes capable d'être plus efficace que ça ou si vous ne supportez pas l'indexation (pas de méthode `__len__` ou `__getitem__`).
Au niveau technique, cette méthode fonctionne exactement comme `.__iter__()`, l'itérateur doit juste donner les éléments dans l'ordre inverse.
;;;

;;; code ```python
def __length_hint__(self)```
;;; doc
Cette méthode est destinée à donner un indice sur la taille d'un itérable quand la taille réelle ne peut pas être déterminée exactement. En principe, ça devrait renvoyer une taille supérieure ou égale à la véritable taille finale du conteneur. Par exemple c'est le cas de classes qui se comportent comme des générateurs de valeurs : on sait qu'elles vont s'arrêter, mais pas exactement quand. Ça sert d'optimisation pour quelques opérations, par exemple quand vous faites `list(objet)` ça permet d'aider à dimensionner la liste à l'avance plutôt que de l'étendre au fur et à mesure, ce qui accélère pas mal la gestion de la mémoire.
Ce n'est qu'une optimisation, qui plus est assez rare. Ça ne sert à rien si `.__len__()` est définie et fiable. Si vous êtes dans la situation décrite, essayez d'implémenter cette méthode, sinon pas la peine.
;;;

### Gestion des attributs

;;; code ```python
def __getattr__(self, nom)
def __getattribute__(self, nom)```
;;; doc
Ces méthodes sont appelées quand vous demandez un attribut de l'objet (`objet.attribut` est équivalent à `objet.__getattribute__("attribut")`, puis `objet.__getattr__("attribut")`).
Il faut bien avoir leur fonctionnement en tête quand vous les utilisez :

- D'abord, `__getattribute__` est utilisé sans condition dès qu'un attribut est demandé. Si vous ne l'avez pas réimplémenté, c'est le comportement par défaut.
- Si `__getattribute__` a levé une `AttributeError`, `__getattr__` est appelée.

Autrement dit :

- `__getattribute__` capture toutes les demandes d'attribut quelles qu'elles soient
- `__getattr__` capture seulement les demandes où le vrai attribut du nom demandé n'existe pas

Faites attention avec `__getattribute__`, car c'est une méthode qui écrase toutes les demandes d'attribut (d'ailleurs vous ne pouvez pas utiliser `self.attribut` ou `self.méthode()` dans `__getattribute__` car ça rappellerait `__getattribute__` récursivement, il faut utiliser `object.__getattribute__(self, "méthode")()`. En principe vous ne devriez pratiquement jamais en avoir besoin à part pour ajouter des choses autour de la demande d'attribut sans l'altérer. Si le but c'est de faire des traitements particuliers en fonction de l'attribut demandé, utilisez plutôt des propriétés (`@property`).

De l'autre côté, si vous voulez vraiment bricoler des attributs spéciaux comme ça, c'est `__getattr__` qu'il faut utiliser, qui elle ne masque pas les attributs existants. C'est assez simple, la méthode prend en paramètre le nom de l'attribut comme une chaîne de caractères, et doit renvoyer une valeur (ou `AttributeError` si l'attribut ne doit pas exister).
;;;

;;; code ```python
def __setattr__(self, nom, valeur)```
;;; doc
Cette méthode est utilisée quand vous assignez une valeur à un attribut (`objet.attribut = valeur` est équivalent à `objet.__setattr__("attribut", valeur)`). Cette fois rien de spécial, cette méthode est appelée dans tous les cas. Pareil, si c'est pour avoir un comportement particulier sur certains attributs, utilisez plutôt des propriétés. Notez bien que cette méthode est appelée chaque fois qu'un attribut ou une méthode est demandée, même au sein même de la classe, donc prévoyez bien les cas où un vrai attribut ou une vraie méthode est demandé.
;;;

;;; code ```python
def __delattr__(self, nom, valeur)```
;;; doc
Cette méthode est appelée quand vous essayez de supprimer un attribut (`del objet.attribut` est équivalent à `objet.__delattr__("attribut")`). Bien sûr, ne l'implémentez que si ça a du sens. C'est très rare d'utiliser ça, en tout cas en dehors de la classe.
;;;

;;; code ```python
def __dir__(self)```
;;; doc
Retourne la liste des noms des attributs et des méthodes. C'est ce qui est appelé quand `dir(objet)` est utilisé. Si vous bricolez avec `__getattr__`, `__setattr__` et compagnie, ça peut être intéressant de donner ici les attributs utilisables. La doc indique que comme `dir()` est plutôt un utilitaire pour les sessions interactives, c'est plus utile de donner ce qui est intéressant que d'être parfaitement exhaustif.
;;;

### Rendre un objet appelable

;;; code ```python
def __call__(self, ...)```
;;; doc
Vous pouvez même rendre un objet appelable comme un fonction avec cette méthode. En réalité, tout ce qui demande plus ou moins une fonction demande en fait n'importe quel objet *callable* (appelable), donc qui implémente cette méthode. `objet(arg1, arg2)` est équivalent à `objet.__call__(arg1, arg2)`.  
Vous pouvez donner le comportement que vous voulez à cette méthode.
En général, ça peut servir quand vous voulez donner un objet avec un état à quelque chose qui prendrait d'habitude une fonction. Si c'est juste pour faire un genre de foncteur à la C++, une simple fonction ou une closure font le job en 2 fois moins de code. Ça peut aussi servir pour utiliser une classe comme décorateur par exemple. Ça peut aussi permettre des architectures un peu particulières, comme des « fonctions » qui héritent les unes des autres.
;;; example ```python/result
# Note : c'est pour l'exemple, mais ce n'est pas une très bonne façon de faire ça
# (en théorie on ferait ça avec itertools.accumulate)
# En fait il y a peu d'exemples d'utilisation pratique qui seraient assez simples,
# l'utilisation de __call__ est souvent soit très spécifique, soit un sucre syntaxique
# pour quelque chose qui se fait très bien autrement
class Accumulateur:
    def __init__(self):
        self.somme = 0

    def __call__(self, x):
        self.somme += x
        return self.somme

liste = [1, 2, 3, 4, 5]
accumulation = list(map(Accumulateur(), liste))
print(liste)
print(accumulation)```
;;;

### Utiliser un objet comme clé de dictionnaire //// hash

;;; code ```python
def __hash__(self)```
;;; doc
Un dictionnaire demande des objets *hashables* comme clé. Si on peut vouloir utiliser vos objets comme clés de dictionnaires (ou les mettre dans un `set`), il faudra traiter la question du hash. C'est aussi ce qu'appelle la fonction `hash(objet)`. Il y a un comportement assez compliqué pour la méthode `.__hash__()` par défaut :

- Si votre classe ne définit ni `__hash__`, ni `__eq__`, elle a le comparateur et le hash par défaut (qui sont équivalents à `a is b`).
- Si votre classe définit `__eq__` et pas `__hash__`, elle ne sera pas hashable, donc pas utilisable comme clé de dictionnaire
- Si votre classe ne définit pas `__eq__`, elle ne doit pas définir `__hash__` non plus
- Si vous ne définissez pas `__eq__` mais que vous ne voulez pas que l'objet soit hashable, utilisez `__hash__ = None` pour l'interdire

Ceci dit, le *hash* d'un objet doit être un nombre entier qui doit pouvoir (idéalement) identifier l'objet sans ambiguïté. La valeur de retour de `__hash__` doit répondre à quelques propriétés :

- Si `a == b`, alors `hash(a) == hash(b)`. La réciproque n'est techniquement pas obligatoire, mais c'est mieux.
- Le hash ne doit **jamais changer pendant la vie de l'objet**. Ça veut dire qu'un objet *mutable* (dont on peut changer l'état après sa création) ne devrait pas avoir de hash, car comme son hash serait basé sur ses attributs, son hash pourrait changer.

Globalement, on ne définit le hash que sur les objets immutables, donc dont l'état ne change pas après leur création (vous pouvez faire des `+=` ou des trucs comme ça mais ça crée un nouvel objet sans changer l'ancien). C'est pour ça par exemple qu'on peut utiliser des nombres, des chaînes de caractères, des tuples comme clés de dictionnaires, mais pas une liste.

En général, on définit le hash d'un objet par rapport au hash de ses attributs — une technique courante est de faire un tuple avec les attributs et de hasher ce tuple. Si ça n'utilise pas tous les attributs, pensez bien à utiliser les mêmes attributs que ceux qui servent à établir l'égalité (dans `__eq__`), pour respecter la première règle.
;;; example ```python/result
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"

    # Ici, un Point est égal à un autre Point avec les mêmes coordonnées x et y,
    # ou à une liste de deux coordonnées avec les mêmes valeurs
    def __eq__(self, point):
        if isinstance(point, Point):
            return self.x == point.x and self.y == point.y
        try:
            if len(point) == 2:
                return self.x == point[0] and self.y == point[1]
            else:
                return NotImplemented
        except (TypeError, LookupError):
            return NotImplemented

    # Donc ici pareil, on rend équivalent à un autre Point avec les mêmes valeurs,
    # ou à un tuple avec les mêmes valeurs. On ne contrôle pas ce que les autres
    # éventuelles collections ordonnées immutables font, mais si elles ont aussi
    # ce même hash, elles seront compatibles aussi.
    def __hash__(self):
        return hash((self.x, self.y))

valeurs = {Point(x, y): (x+y)/2 for x in range(-2, 3) for y in range(-2, 3)}
print(f"{valeurs=}")
print(f"{Point(1, -1) == (1, -1)=}")
print(f"{valeurs[Point(2, 1)]=}")
print(f"{valeurs[(2, 1)]=}")```
;;;

### Gestionnaires de contexte

;;; code ```python
def __enter__(self)
def __exit__(self, type_exception, exception, traceback)```
;;; doc
Ces méthodes sont appelées en entrant et en sortant d'un contexte avec `with`, en permettant à l'objet de servir de gestionnaire de contexte.

```python
with objet as contexte:
    # opérations
```

est équivalent à

```python
context = objet.__enter__()
try:
    # opérations
except BaseException as exc:
    if not objet.__exit__(type(exc), exc, exc.__traceback__):
        raise exc
else:
    objet.__exit__(None, None, None)
```

La méthode `__enter__` est appelée en entrant dans le contexte, et peut retourner un objet quelconque qui sera renvoyé par la clause `as` qui peut aller avec `with`. À moins de gestion plus complexe qui implique que le contexte n'est pas le gestionnaire du contexte, on fait retourner à `.__enter__()` l'objet lui-même, pour pouvoir l'utiliser facilement dans le contexte.
La méthode `__exit__` est appelée en sortant du contexte, et sera **toujours** appelée avant d'en sortir, que ce soit avant de continuer ou avant de quitter. Cette méthode prend trois arguments, qui sont la classe de l'exception, l'exception elle-même, et l'objet traceback associé à l'exception. S'il n'y a pas eu d'exception, ces trois arguments vaudront `None`. S'il y a eu une exception dans le contexte, `.__exit__()` peut retourner `True` pour ignorer l'exception et poursuivre normalement le programme, ou `False` pour faire son traitement puis laisser l'exception être levée. En aucun cas il faut vous-même relever l'exception.
;;; example ```python
import threading

# Une sous-classe de Lock, qui ajoute les fonctionnalité d'un gestionnaire de
# contexte pour être sûr qu'il soit toujours bien relâché pour éviter les
# deadlocks même en cas d'erreur
class ContextLock (threading.Lock):
    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
        return False

socket_lock = ContextLock()

def run_thread():
    # ...
    with socket_lock:
        # Opérations sur le socket
    # ...```
;;;
