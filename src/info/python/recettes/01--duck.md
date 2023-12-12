//// title = "Duck typing"
//// description = "Comment respecter les canards et être un bon pythonneux"

# {=title}

Ça ne vous aura pas échappé, Python est un langage qui emploie le *duck typing*. Si un objet a la bonne interface ça fonctionne, sans poser de questions. Sauf que ça, ça dépend aussi pas mal de vous. On a régulièrement besoin de vérifier le type d'un objet. Et pour vérifier le type d'un objet, on est vite tenté de bourrer à coup de `isinstance(objet, type)`.

Le problème, c'est que ça c'est comme faire de la vérification de type statique, mais sans même le gain en clarté du code que c'est supposé apporter. Ça va totalement à l'encontre de tout le principe de Python, et ça bloque l'accès de vos fonctions aux objets qui ne sont pas exactement ceux que vous avez prévu.

Si Python est un environnement particulièrement agréable à utiliser, c'est parce que tant que les différentes librairies respectent le duck typing en restant aussi génériques que possible dans leur typage, tout le monde est compatible avec tout le monde, même entre des librairies qui n'ont rien à voir. On peut utiliser les images de PIL sous forme de tableaux numpy, utiliser sans problème les données d'une obscure librairie d'acquisition de GoPro avec une obscure bibliothèque de bioinformatique, tout est possible.

Dans un langage au typage statique et à la librairie standard limitée aux utilitaires comme Java ou C++, seul le développeur de la librairie contrôle ce qu'on peut faire avec. Ça fait que dès que vous voulez utiliser deux librairies ensemble, vous allez souvent vous coltiner une quantité absurde de code d'interfaçage juste pour faire plaisir aux types d'arguments de chacune des deux librairies. Ceux qui ont déjà dû faire des conversions entre le zillion de classes pour représenter le temps en Java et dans ses librairies savent de quoi je parle. Et ce modèle a tendance à mener à l'écrasante domination de quelques immenses frameworks (Apache Commons, Spring Framework en Java ; Boost, Qt en C++), qui sont seuls à pouvoir faire du tout-en-un de façon cohérente sans jamais avoir à (ni pouvoir) sortir de leur environnement.

Au contraire, avec le modèle de Python d'une librairie standard immense et le duck typing, des librairies de gens qui n'ont même pas ne serait-ce qu'imaginé l'utilisation avec l'autre sont compatibles entre elles, et vous pouvez créer vos propres objets pour utiliser des librairies d'une façon que personne d'autre n'aurait imaginé. Ça ouvre la voie à une puissance infinie dans un code qui reste léger et propre, et ça permet l'utilisation de plein de plus petites librairies plutôt que de s'enterrer dans un unique gros framework maintenu par une grosse structure, ce qui permet l'existence d'alternatives, d'un open source bien plus démocratique, et une flexibilité bien supérieure.

Du coup, ici on va voir les alternatives qui permettent de rester compatible avec le plus de monde possible.

;;; warning
Notez bien qu'on parle de faire des choses génériques, ce qui s'applique forcément plus quand vous faites des composants réutilisables voire une librairie. Il y a toujours une composante de bon sens là-dedans, pas la peine de se casser le tronc à être parfaitement générique pour un truc qui ne sera jamais utilisé qu'à un seul endroit dans un contexte très précis. Cependant, certaines techniques ici ne sont pas beaucoup plus lourdes que la version naïve, donc pensez-y.
;;;

## Goûtez avant de critiquer

### Exemple de conception

Le principe fondamental, c'est d'essayer et de rejeter *si* ça foire, plutôt que de vérifier à l'avance et de rejeter si ça ne correspond pas à vos critères. Par exemple, prenons une banale classe `Point`, qui représente un point en deux dimensions. On veut pouvoir additionner deux points. Que faire ?

- Seulement accepter les objets de la même classe ? Au temps pour la généricité.
- Du coup on peut accepter les listes de deux nombres. Pour ça on a envie de vérifier d'abord si l'objet additionné est bien une liste, mais on ne serait pas plus avancés : il y a plein de choses qui ont l'interface d'une `list` sans en être une
- Il faut donc une technique qui fonctionne avec tout ce qui ressemble à peu près à une collection de deux nombres.
- Et tant qu'à faire, si on cherche à être compatible avec les collections de deux nombres, autant nous aussi ressembler à une collection de deux nombres.

La solution est généralement de faire `try: opération — except: rejet` plutôt que `if ça_va_marcher: opération — else: rejet`. On n'applique aucun préjugé sur la situation : on tente, si ça marche tant mieux, et seulement si ça marche pas on rejette. Par exemple, ceci serait un très mauvais exemple :

;;; counterexample ```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, point):
        if isinstance(point, Point):
            return Point(self.x + point.x, self.y + point.y)```
;;;

Alors que ceci respecte beaucoup mieux le duck typing. D'ailleurs c'est aussi bien plus générique et permettrait un système d'héritage pour avoir différentes dimensions. Ici on implémente notre point comme un wrapper autour d'une liste (on pourrait d'ailleurs en faire une sous-classe de `list` mais ça pourrait être pénible de restreindre les opérations possible pour garder le même nombre de dimensions). Pour garder les attributs `x` et `y` qui sont bien pratiques, on en fait des propriétés qui redirigent vers la liste.

;;; example ```python/result
class Point:
    def __init__(self, x, y):
        self.coords = [x, y]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.coords[0]}, {self.coords[1]})"

    @property
    def x(self):
        return self.coords[0]
    @x.setter
    def x(self, valeur):
        self.coords[0] = valeur

    @property
    def y(self):
        return self.coords[1]
    @y.setter
    def y(self, valeur):
        self.coords[1] = valeur

    # On décide que nos points doivent être compatibles avec des collections,
    # donc autant les faire aussi se comporter comme des collections comme ça ils
    # seront aussi compatible avec le reste des choses qui acceptent des collections
    def __len__(self):
        return len(self.coords)

    def __iter__(self):
        return iter(self.coords)

    def __getitem__(self, index):
        return self.coords[index]

    def __setitem__(self, index, valeur):
        self.coords[index] = valeur

    def __contains__(self, valeur):
        return valeur in self.coords

    def __add__(self, point):
        try:
            # On restreint aux collections de 2 coordonnées
            # S'il y en a plus ou moins ça pourrait donner des faux résultats
            # (comme additionner un point en 2D avec un point en 3D qui donnerait un point en 2D)
            # Dans ces cas-là, il vaut mieux laisser faire l'autre objet
            if len(point) == 2:
                return Point(self.coords[0] + point[0], self.coords[1] + point[1])
            else:
                return NotImplemented
        # LookupError (IndexError ou KeyError) si l'objet n'utilise pas 0 et 1 comme index, dans ce cas on ne peut pas deviner
        # TypeError pour tout le reste (pas de len(), pas d'indexation)
        except (TypeError, LookupError):
            return NotImplemented

    def __radd__(self, point):
        return self.__add__(point)

import array
A = Point(0, 1)
B = Point(-1, 2)
C = (4, -2)
# Tableau d'octets signés du module array
# C'était pas forcément prévu, mais on a respecté le duck typing donc ça marche
D = array.array("b", (-2, 3))
print(f"{A=}")
print(f"{A.x=}, {A.y=}")
print(f"{A[0]=}, {A[1]=}")
print(f"{A+B=}")
print(f"{A+C=}")
print(f"{A+D=}")```
;;;

### La technique

Vous l'avez compris, la technique est donc double :

- Faire accepter les objets compatibles par votre code
- Si c'est pertinent, rendre votre objet compatible avec les autres, en implémentant les comportements pertinents, comme faire émuler une liste de coordonnées à notre point.

Pour accepter tout ce qui peut marcher, même ce qui est pas prévu, le principe est donc de tenter, et de ne rejeter qu'en cas d'erreur.
En général, c'est parfaitement trivial de faire ça, il suffit de ne rien vérifier. Laissez faire le code, et si ça marche pas, ça finira forcément par lancer une `TypeError` quelconque, et le programmeur qui utilise votre code lira le traceback et verra qu'il a fait une bêtise.

Si vous avez besoin d'un code parfaitement sûr, avec des messages d'erreur plus explicites, ou si à un endroit vous avez besoin de changer de comportement en fonction du type, vous allez tout de même avoir besoin d'un contrôle de type. Pour ça, on peut utiliser `isinstance()`, mais la solution est plutôt d'utiliser un `try-except` en rattrapant les exceptions que lèverait un objet du mauvais type. Pour ça regardez bien la doc, parce qu'il faut être à la fois complet et précis : il faut bien capturer toutes les erreurs qui invaliderait le type (sous peine d'erreurs inattendues), mais il ne faut pas non plus capturer des véritables erreurs de programmation pas prévues.

Par exemple, dans le cas de l'addition de points, on avait deux erreurs potentielles :

- `TypeError` si l'objet n'a pas de `len()` (pas une collection), ou s'il ne supporte pas l'indexation `point[0]`
- `LookupError`, la superclasse de `IndexError` et `KeyError`, si l'objet a une indexation, mais elle n'utilise pas des index classiques (`point[0]` échoue)

Autre exemple, mettons qu'on implémente une fonction clé de tri, pour une liste qui contient à la fois des chiffres et des itérables contenant des chiffres. Il faut donc séparer ces deux cas :

;;; example ```python/result
def clé(élément):
    try:
        return sum([chiffre * 10**i for i, chiffre in enumerate(reversed(élément))])
    # Si l'objet n'est pas itérable, on aura une TypeError
    except TypeError:
        return élément

liste = [1, 7, 6, (5, 4), [0, 0, 2], 9, 1, (5, 6), (6, 5)]
liste.sort(key=clé)
print(liste)```
;;;

;;; warning
Ne vous préoccupez **pas** d'éventuels objets qui auraient la bonne interface mais qui ne feraient pas ce que vous voulez. D'une part, c'est une situation rare qui ne vaut pas l'effort. Et d'autre part, ce n'est pas votre responsabilité. La responsabilité d'un programmeur sur son code est son bon fonctionnement, sa fiabilité, sa maintenabilité, son respect des éventuelles conventions comme le duck typing, et sa documentation. Ce n'est **pas** votre responsabilité de décider ce que d'autres personnes en feront.
Du moment que votre code est bien documenté et que les autres savent à quoi s'attendre, c'est *leur* responsabilité de s'assurer qu'ils utilisent votre code convenablement. Autrement dit, **vous n'avez pas à faire la police sur le code des autres**. Ne faites pas comme Java qui supprime des fonctionnalités sous prétexte qu'une mauvaise utilisation très précise en fait un risque de sécurité, sans donner d'alternative.
Il n'est jamais vraiment possible de distinguer une mauvaise utilisation d'une utilisation pas prévue mais intelligente, et vouloir un code à l'épreuve des ignorants n'est pas une raison pour tuer toute tentative d'utilisation originale.
;;;

## La documentation générique

Si votre objet est supposé être générique, vous pouvez bien sûr le dire, mais si vous mettez juste ce à quoi vous vous attendez, on saura quoi en faire. Cela dit il y a quelques termes à bien comprendre et utiliser s'ils sont pertinents :

- Un *iterable* désigne n'importe quel objet sur lequel il est possible d'itérer (donc qui a la méthode `__iter__`). Donc si vous avez juste une boucle `for` sur un argument, vous ne demandez pas une liste, vous demandez un itérable.
- Un objet appelable (*callable*) est n'importe quel objet qui peut être appelé comme une fonction (avec une méthode `__call__`). Ne demandez pas une fonction, demandez un *callable*.
- Un objet *file-like* (qui se comporte comme un fichier) est un objet qui implémente la même interface qu'un fichier, même si ce n'en est pas un. Si vous demandez un objet fichier, parlez plutôt d'objet *file-like*
