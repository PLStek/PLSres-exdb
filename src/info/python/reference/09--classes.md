//// title = "Orienté objet"
//// description = "La programmation orientée objet en Python"

# {=title}

On l'a dit et redit, tout est objet en Python. On va maintenant voir comment faire vos propres objets.

## Rappels d'usage

On ne va pas refaire un cours sur l'OOP en général parce que c'est un sujet vaste et compliqué, mais globalement :

- Un objet est quelque chose qui a des **attributs** (propriétés qui lui sont associées, comme des variables liées à l'objet), et des **méthodes** (des fonctions qui s'y appliquent)
- Un objet est modelé par rapport à une **classe**, qui sert de « patron de construction » en définissant les méthodes et les attributs de ses **instances** (objets crées d'après une classe)

Et pour ce qui est spécifique à Python :

- Il n'y a pas besoin de déclarer les attributs à l'avance, tout est totalement dynamique, vous pouvez donner les attributs que vous voulez à l'objet que vous voulez quand vous voulez
- Python utilise le *duck typing*, donc du moment qu'un objet a les attributs et méthodes qu'il faut pour être utilisé quelque part, il peut être utilisé quelles que soient ses origines. Par exemple, un objet *file-like* peut implémenter l'interface d'un fichier (les méthodes pour lire, écrire, se déplacer, vérifier le statut, …), sans pour autant avoir rien à voir avec un vrai fichier, ni même en dériver. Dans les langages plus stricts (C++, Java) le polymorphisme est un sujet vaste et compliqué — en Python on l'utilise sans même le faire exprès.
- Il n'y a pas de concept de droits d'accès aux propriétés d'un objet (public, privé, …). Pour citer Guido van Rossum, « on est entre adultes consentants ». Ce qui veut dire que la définition de ce qui est privé est conventionnelle et à la bonne volonté des programmeurs. En général, on préfixe le nom de ce qui est privé par un underscore pour bien faire savoir que ce n'est pas fait pour être utilisé depuis l'extérieur (`def _méthode(self): …`)

## Créer une classe

Pour créer une classe c'est très simple, il suffit de déclarer un bloc de code `class MaClasse:` et d'y mettre les méthodes. Le **constructeur** (la méthode appelée quand un objet est créé) doit s'appeler `__init__`. Il y a une particularité en Python : le premier paramètre de toutes les méthodes doit être l'objet manipulé, qu'on appelle par convention `self`. Dans la plupart des langages, pour manipuler l'objet, soit on peut utiliser directement les méthodes et attributs de l'objet manipulé sans préfixe, soit on a un mot-clé `this` ou quelque chose du genre pour le désigner — en Python ce serait le bazar en plus d'être ambigu, donc on rend tout explicite.

;;; example ```python/result
import math

class Vecteur3D:
    """Vecteur géométrique en 3 dimensions

    La docstring pour la classe entière se place au tout début du bloc.
    Par convention, les classes sont nommées en CamelCase
    """

    def __init__(self, x, y, z):
        """Le constructeur doit s'appeler __init__
        Notez bien le paramètre `self`, qui représente l'objet qu'on manipule
        Toutes les opérations sur l'objet manipulé passeront par `self`"""
        self.x = x  # Assignation d'attributs à l'objet
        self.y = y
        self.z = z

    # La méthode ne prend pas d'arguments depuis l'extérieur,
    # mais on met quand même `self` qui est donné implicitement quand on appelle la méthode
    def norme(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

# Instanciation : on crée un objet, ce qui appelle le constructeur.
# Les trois arguments sont passés à la méthode __init__
u = Vecteur3D(1, -1, 0)
v = Vecteur3D(2, 2, -1)

# `u` et `v` sont des objets de la classe Vecteur3D.
# On peut utiliser leurs attributs et leurs méthodes avec un `.`
# L'objet manipulé est passé implicitement par l'argument `self`
# Ici on récupère les attributs x, y et z des objets,
# et on appelle la méthode .norme() sur chacun d'entre eux.
print(f"||u({u.x}, {u.y}, {u.z})|| = {u.norme()}")
print(f"||v({v.x}, {v.y}, {v.z})|| = {v.norme()}")```
;;;

Et voilà. C'est souvent comme ça que tout marche, avec des objets qui interagissent entre eux.

### Héritage

Et comme dans tout langage orienté objet, il y a la possibilité de faire hériter une classe d'une autre. Autrement dit, la classe fille aura tous les attributs et méthodes de la classe mère, en ajoutant ses propres particularités. Pour ça, on ajoute juste la classe mère entre parenthèses après le nom.

;;; example ```python/result
import math

# Exemple trivial : cette classe fera tout exactement comme Exception,
# mais est bien une sous-classe de Exception
class StructuralError (Exception):
    pass

# Classe de base pour des formes géométriques
class Forme:
    def aire(self):
        NotImplemented
    def périmètre(self):
        NotImplemented

# Une classe point qui dérive de Forme
class Point (Forme):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def aire(self):
        return 0
    def périmètre(self):
        return 0

# Classe pour un polygone générique qui dérive de Forme
class Polygone (Forme):
    def __init__(self, *points):
        print("Appel du constructeur de Polygone")
        self.points = points

    def aire(self):
        print("Calcul de l'aire par Polygone.aire")
        résultat = 0
        for i, point in enumerate(self.points):
            suivant = self.points[(i+1) % len(self.points)]
            résultat += (point.x * suivant.y - suivant.x * point.y) / 2
        return abs(résultat)

    def périmètre(self):
        print("Calcul du périmètre par Polygone.périmètre")
        return sum(self.longueurs())

    # Nouvelle fonctionnalité spécifique aux polygones : la liste des longueurs des côtés
    def longueurs(self):
        résultat = []
        for i, point in enumerate(self.points):
            suivant = self.points[(i+1) % len(self.points)]
            résultat.append(math.sqrt((point.x-suivant.x)**2 + (point.y-suivant.y)**2))
        return résultat

# Triangle, qui dérive de Polygone en contraignant plus le constructeur
class Triangle (Polygone):
    def __init__(self, point1, point2, point3):
        print("Appel du constructeur de Triangle")
        # On appelle le constructeur de la superclasse
        super().__init__(point1, point2, point3)

    # On change le calcul de l'aire pour le rendre plus efficace spécifiquement pour les triangles, mais le périmètre reste le même
    def aire(self):
        print("Calcul de l'aire par Triangle.aire")
        A, B, C = self.points
        return abs((B.x-A.x)*(C.y-A.y) - (C.x-A.x)*(B.y-A.y)) / 2

    # Nouvelle fonctionnalité spécifique aux triangles : la liste des mesures des angles
    def angles(self):
        a, b, c = self.longueurs()  # On appelle sans problème une méthode de la superclasse sur l'objet Triangle
        alpha = math.acos((b**2 + c**2 - a**2) / (2*b*c))
        beta = math.acos((c**2 + a**2 - b**2) / (2*c*a))
        gamma = math.acos((a**2 + b**2 - c**2) / (2*a*b))
        return alpha, beta, gamma

print("======== Manipulation d'un Triangle")
triangle = Triangle(Point(0, 0), Point(1, 1), Point(0, 1))
print(f"\n{triangle.aire()=}, {triangle.périmètre()=}")
# Fonctionnalité spécifique à Triangle, qui n'est pas dans Polygone
print(f"{triangle.angles()=}")
# Juste pour montrer que Triangle dérive bien de Polygone et de Forme
print(f"\n{isinstance(triangle, Triangle)=},\n{isinstance(triangle, Polygone)=},\n{isinstance(triangle, Forme)=}")

print("\n======== Manipulation d'un Polygone")
# Cette fois c'est un polygone, donc ça utilise juste les méthodes de Polygone
carré = Polygone(Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0))
print(f"\n{carré.aire()=}, {carré.périmètre()=}")
# C'est un Polygone, qui est une Forme, mais ce n'est pas un triangle
print(f"\n{isinstance(carré, Triangle)=},\n{isinstance(carré, Polygone)=},\n{isinstance(triangle, Forme)=}")```
;;;

Voilà en gros l'idée. On crée une sous-classe qui hérite des méthodes de la superclasse, et qui peut définir ses propres fonctionnalités

## TODO : Héritage multiple
