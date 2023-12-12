//// title = "Variables"
//// description = "Les variables en Python"

# {=title}

En Python, il n'y a pas de déclaration à faire, ou de type à déclarer : une variable est juste un nom, avec une valeur au bout. Donc pas de fioritures, c'est juste `nom = valeur`, où vous voulez.

;;; example ```python
ligne = 112
nom_fichier = "donnees.csv"```
;;;

Depuis Python 3.8 vous avez aussi l'opérateur *walrus* (morse, comme l'animal) qui permet d'assigner des valeurs à des variables même au milieu d'une expression : `nom := valeur`. En gros c'est comme mettre la valeur dans l'expression, sauf que la variable a sa valeur après. Pensez bien à mettre des parenthèses autour, cet opérateur a une très basse priorité.

;;; example ```python/result/stdin="5\n96\n\n"
résultat = 1 + 2 + (sousrésultat := 3 + 4 + 5)
print(f"{résultat=}, {sousrésultat=}")

# Tant que l'utilisateur n'entre pas une chaîne vide, et en gardant l'entrée
# utilisateur dans une variable pour l'utiliser après
while len(entrée := input("Nombre à doubler, ou rien pour quitter : ")) > 0:
	nombre = int(entrée)
	print(nombre * 2)
print("Fin")```
;;;

Par ailleurs, vous pouvez extraire les éléments des tuples et des listes directement dans des variables, ce qui permet à certaines fonctions de renvoyer plusieurs valeurs à la fois par exemple.

;;; example ```python/result
chaîne = "10003511:Jean-Claude Desfossés:50"
print(f"{chaîne.split(':')=}")
id, nom, âge = chaîne.split(":")
print(f"{id=}, {nom=}, {âge=}")```
;;;


Attention, en Python les objets sont toujours passés par référence — pour des objets non-modifiables comme des nombres, des chaînes de caractères ou des tuples ça ne change rien, mais pour les autres ça a son importance.

;;; example ```python/result
maliste = [1, 2, 3, 4, 5, [10, 11, 12]]
simple_reference = maliste
simple_reference[0] = 100  # C'est un autre nom qui pointe sur le même objet, donc ça modifie maliste avec
print(f"maliste          : {maliste}")
print(f"simple_reference : {simple_reference}")

# Les types standard ont souvent une méthode `.copy()`
# qui fait une « copie superficielle » (shallow copy) : les deux listes sont différentes,
# mais les objets qu'elles contiennent sont les mêmes,
# donc par exemple si on modifie la liste imbriquée dedans, ça la modifiera pour les deux
copie = maliste.copy()
copie[1] = 101
copie[5][0] = 1000
print(f"maliste : {maliste}")
print(f"copie   : {copie}")```
;;;

Quand vous voulez faire des copies ou passer des objets par valeur, c'est une petite habitude à prendre.

{!svg: info/python/1-copie.svg}

## Affichage

Vous avez la simple fonction `print(…)` qui affiche ce que vous lui donnez, en ajoutant toujours un saut de ligne à la fin. Vous pouvez même lui donner plusieurs valeurs, qu'elle affichera séparées par des espaces.

;;; example ```python/result
print("Une valeur")
print("Autre valeur :", 5)```
;;;

`print` a quelques paramètres nommés pour changer un peu son comportement :

- `file` permet de donner un fichier où écrire. Ça peut être n'importe quel fichier, mais il y a la sortie standard et la sortie d'erreur (`stderr`) dans le module `sys`
- `end` donne ce qui est ajouté à la fin, par défaut c'est le saut de ligne, mais vous pouvez le remplacer (par exemple une chaine vide)

;;; example ```python/result
import sys

print("Erreur : ", file=sys.stderr, end="")
print("Quelque chose s'est mal passé", file=sys.stderr)```
;;;

## Entrée utilisateur

Pour récupérer une entrée utilisateur, vous avez simplement la fonction `input()`, qui renvoie la chaîne de caractères à l'utilisateur. Ça renvoie seulement la chaîne de caractères brutes (sans saut de ligne), vous vous occupez de son traitement, donc de son éventuelle conversion ou traitement.

;;; example ```python/result/stdin="5\n6\n"
nombre1 = int(input("Entrez le premier nombre entier  : "))  # On convertit la valeur en entier. On verra plus tard pour traiter les erreurs
nombre2 = int(input("Entrez le deuxième nombre entier : "))
print(f"{nombre1} + {nombre2} = {nombre1 + nombre2}")```
;;;

## Types simples
### Entiers

Un nombre entier se définit juste avec sa valeur entière (`151`), et donne un objet de type `int`. Python supporte aussi les définitions en binaire avec le préfixe `0b` (`0b10010111`), en octal avec `0o` (zéro puis o minuscule, `0o227`), et hexadécimal avec `0x` (`0x97`)

;;; example ```python/result
nombre = 151
print(nombre == 0b10010111 and nombre == 0o227 and nombre == 0x97)```
;;;

### Réels

Les nombres réels (`float`) se définissent avec un point pour séparer les décimales :

;;; example ```python
réel = 1.608```
;;;

### Complexes

Si un jour vous en avez besoin, Python supporte nativement les nombres complexes. `1j` correspond à la racine carrée de -1, pour écrire votre nombre complexe c'est juste `5+16.5j`.

;;; example ```python/result
complexe = 5.5 + 4.5j
imaginaire = 12j
print(complexe.conjugate())  # Conjugué
print(imaginaire.imag, complexe.real)  # Partie imaginaire et partie réelle
print(abs(complexe))  # Module```
;;;

### Booléens

Les booléens (valeurs vraies / fausses) utilisent les constantes `True` et `False` (notez la majuscule). Une condition renverra un objet de type `bool`, qui se comporte à peu près comme un entier qui vaut 0 (`False`) ou 1 (`True`), mais c'est mieux de bien séparer ces deux types.

;;; example ```python/result
booléen = True
nombre = 11
print(nombre == 10 or booléen)```
;;;

### None

`None` est là pour dénoter une valeur qui n'existe pas (comme un `null`). Quand vous cherchez à savoir si une variable vaut `None` ou pas, vous devez tester avec l'opérateur `is` plutôt que `==`. On y reviendra sur la page des {> info.python.reference.operateurs: opérateurs}, mais en gros comme None est une valeur particulière, globale et unique, il faut utiliser `is` pour déterminer si c'est vraiment `None`, et pas un objet qui se considérerait égal à `None` par accident à cause d'une surcharge d'opérateur définie bizarrement. Donc on testera avec `variable is None` ou `variable is not None`.

;;; example ```python
tempval = None
if tempval is not None:
	print("tempval contient quelque chose")```
;;;

## Collections

En Python, *collection* est un terme générique pour tout ce qui s'apparente de près ou de loin à une liste. Pour obtenir la taille d'une collection (liste, dictionnaire, …), utilisez la fonction `len(objet)`

;;; example ```python/result
chaine = "test"
liste = [1, 2, 3]
print(f"Longueur de {chaine !r} : {len(chaine)}")
print(f"Longueur de {liste !r} : {len(liste)}")```
;;;

Pour vérifier si une valeur est dans une collection, vous avez l'opérateur `in` :

;;; example ```python
if élément in maliste:
	# Si l'élément est présent dans la liste
if élément not in maliste:
	# Si l'élément n'est pas dans la liste```
;;;


### Chaines de caractères

En Python, une chaîne de caractères (type `str`) se comporte plus ou moins comme une liste de caractères, mais il n'y a pas de type caractère en Python, que des chaînes de caractères, comme ça l'interface est la même. Les chaînes de caractères ont aussi plein de méthodes utiles dont on reparlera sur la {> info.python.recettes.texte: page appropriée}. Une chaîne de caractères se définit soit entre guillemets, soit entre apostrophes, soit entre triples guillemets, soit entre triples apostrophes. Les triples guillemets et triples apostrophes permettent de faire des chaînes de caractères de plusieurs lignes.

;;; example ```python/result
chaine1 = "Cette chaîne est entre guillemets et peut contenir des 'apostrophes'"
chaine2 = 'Cette chaîne est entre apostrophes et peut contenir des "guillemets"'
chaine3 = """
Cette chaîne est entre triple guillemets
et peut contenir des "guillemets" et des 'apostrophes'
"""

# Vous pouvez ajoutez des chaines entre elles ou multiplier une chaîne par un nombre
concaténée = chaine1 + "\n" + chaine2 + "\n" + chaine3
multipliée = "0" * 8
print(concaténée)
print(multipliée)```
;;;

Il faut bien noter qu'en Python 3, **les chaînes de caractères sont en Unicode** : un caractère est un caractère, pas bêtement un octet comme en C. Donc vous pouvez utiliser tous les caractères que vous voulez, accents, autres systèmes d'écriture, symboles, tout, et sans aucune bidouille de votre part, la seule limite est l'éventuelle police d'écriture qui affichera ces caractères. En fait tout est en Unicode, vous pouvez même utiliser des accents dans vos noms de variables si vous voulez.

Il existe des *escape sequences* pour mettre des caractères que vous ne pouvez pas taper facilement dans une chaîne de caractères :

- `\n` : Saut de ligne
- `\t` : Tabulation
- `\r` : Retour au début de la ligne
- `\b` : Retour en arrière d'un caractère (comme un appui sur la touche effacer du clavier)
- `\"` : Guillemets (même dans une chaîne entre guillemets, pas besoin pour les autres)
- `\'` : Apostrophe (même dans une chaîne entre apostrophes, pas besoin pour les autres)
- `\xHH` : Octet de valeur hexadécimale 0xHH
- `\uHHHH` ou `\uHHHHHHHH` : Caractère unicode de code hexadécimal HHHH
- `\\` : Backslash

Vous pouvez préfixer la chaîne littérale avec `r` pour que ses caractères ne soient pas échappés : `"\\\n"` correspond au caractère `\` suivi d'un saut de ligne, mais `r"\\\n"` donne réellement les caractères `\\\n`. C'est notamment pratique pour les chemins Windows et les expressions régulières

#### Formatage de chaînes de caractères

Pour formater des valeurs dans une chaîne de caractères, un peu comme `printf`, il y avait autrefois deux méthodes :

- Les formats avec `%` : `"Bonjour %s, vous avez %d nouveaux messages" % (nom, nbmessages)` -> `"Bonjour Eric, vous avez 99 nouveaux messages"`
- La méthode `.format()` : `"Bonjour {}, vous avez {} nouveaux messages".format(nom, nbmessages)` -> `"Bonjour Eric, vous avez 99 nouveaux messages"`

Vous pouvez toujours les croiser dans les codes écrits avant Python 3.6. Mais depuis Python 3.6, on a une option beaucoup plus rapide, beaucoup plus claire et beaucoup plus puissante : les ***f-strings***. Elles se définissent avec le préfixe `f`.

;;; example ```python/result
nom = "Eric"
nbmessages = 99
bienvenue = f"Bonjour {nom}, vous avez {nbmessages} nouveaux messages"
print(bienvenue)```
;;;

C'est très simple, vous écrivez votre chaîne de caractères, et là où vous voulez insérer une valeur, vous mettez une expression entre accolades `{}`. Vous pouvez y mettre n'importe quelle expression, même des opérations plus complexes et des appels de fonctions, et n'importe où dans la chaîne.

;;; example ```python
# Note : là on abuse un peu pour la démonstration, mais essayez de garder ça propre
print(f"Bonjour {user.nom}, vous avez {nbmessages := nb_messages(user)} nouveau{'x' if nbmessages != 1 else ''} message{'s' if nbmessages != 1 else ''}")

# Bonjour Eric, vous avez 99 nouveaux messages
# Bonjour Kevin, vous avez 1 nouveau message```
;;;

Au cas où ça change quelque chose, les expressions dans la f-string sont évaluées dans l'ordre, de gauche à droite. Pour mettre de vrais caractères accolades `{}` dans votre f-strings, vous avez juste à les doubler (`f"{expression} {{caractères accolades}}"`). Attention, si vous utilisez des chaînes de caractères dans les expressions à l'intérieur d'une f-string, n'utilisez pas les mêmes guillemets que la chaîne principale : par exemple, comme ci-dessus, des guillemets doubles pour la chaîne, et des apostrophes dans les expressions. Vous n'avez pas le droit d'utiliser des backslashes dans les expressions.

Pour aider au débuggage, vous pouvez mettre un `=` après l'expression pour afficher l'expression avec

;;; example ```python/result
print(f"Résultat : {11*11 + 11=}")```
;;;

Pour un formatage plus précis, vous pouvez mettre un format ressemblant à ceux de `printf` après l'expression : `{expression :format}`. Le format se présente sous la forme `:[remplissage][alignement][modificateur][signe][groupement][longueur][type]`. Tous ces éléments sont optionnels, même le type — s'ils ne sont pas spécifiés, ça fera une présentation par défaut selon le type de la valeur.

Les caractères de formatage sont les suivants :

- Le caractère de remplissage est un caractère au choix que vous mettez avant l'option d'alignement, et qui remplira les espaces vides. Par défaut, ça remplira avec des espaces.
- **Alignement** :
	- `<` : Aligne à gauche dans l'espace demandé (par défaut pour tout ce qui n'est pas un nombre)
	- `>` : Aligne à droite (par défaut pour les nombres)
	- `^` : Centrage de la valeur
- **Modificateur** :
	- `#` : Demande la « forme alternative » du format, l'effet dépend du type
	- `=` : Quand la valeur numérique est plus courte que la longueur demandée, place le remplissage entre le signe et la valeur (Par exemple, `:+6d` donne `"  +145"` alors que `:=+6d` donne `"+  145"`)
- **Signe**
	- `+` : Force à donner le signe du nombre, même s'il est positif
	- ` ` (espace) : Met un espace devant les nombres positifs, là où le signe `-` serait devant un nombre négatif. Ça permet de bien aligner les nombres positifs et négatifs.
- **Groupement**
	- `,` : Met des virgules comme séparateurs de milliers, à l'américaine. Pour faire des séparateurs de milliers appropriés à l'endroit, il faudra utiliser le format `:n` avec la bonne localisation
	- `_` : Utilise des underscores comme séparateurs de milliers, et comme séparateurs de blocs pour les types `x` (hexadécimal), `o` (octal) et `b` (binaire)
- **Longueur et précision**
	- Donnez juste un nombre pour la longueur minimale du champ : ex. `:8d` -> `"      76"`. Si la longueur d'origine de la valeur dépasse, elle ne sera pas coupée.
	- Pour la précision d'un réel, ce sera avec `.` suivi de la précision : ex. `:.2f` -> `345.67`
	- Notez bien que si vous donnez quelque chose du type `5.2f`, le premier nombre est la taille de la valeur complète, et pas juste de la partie entière
	- Vous pouvez utiliser des expressions pour la largeur et la précision : par exemple, `f"Valeur : {valeur :{largeur}.{precision}f}`
- **Type**
	- Nombres entiers
		- `d` : Nombre entier simple (par défaut pour les nombres entiers)
		- `c` : Caractère, donne le caractère unicode correspondant au nombre entier
		- `b` : Conversion en binaire. La forme alternative (`:#b`) écrit `0b` devant la valeur
		- `o` : Conversion en octal. La forme alternative (`:#o`) écrit `0o` devant la valeur
		- `x` : Conversion en hexadécimal. La forme alternative (`:#x`) écrit `0x` devant la valeur
		- `X` : Conversion en hexadécimal, mais avec les lettres en majuscule
		- `n` : Écriture locale du nombre entier (avec les séparateurs de milliers locaux, par exemple)
	- Nombres réels
		- `g` et `G` : Par défaut pour les `float`, choisit entre les notations normale et scientifique en fonction de la taille du nombre
		- `f` et `F` : Taille fixe. Si vous ne donnez pas de précision, ça donnera 6 décimales. `F` est pareil que `f` mais `inf` et `nan` seront en majuscules
		- `e` et `E` : Notation scientifique. `E` mettra le `e`, `inf` et `nan` en majuscules
		- `n` : Écriture locale du nombre (avec les séparateurs de milliers et le bon séparateur de décimales)
		- `%` : Pourcentage, multiplie par 100 et ajoute un `%` à la fin

Par défaut, tous les autres types seront simplement convertis en chaîne de caractères, comme avec la fonction `str(objet)`. Vous pouvez éventuellement mettre `!r` à la place du format pour utiliser `repr()` (en général une représentation comme ce que vous écrivez dans le code pour créer l'objet), ou `!a` pour `ascii()` (comme `repr()` mais en échappant les caractères non-ascii)

;;; example ```python/result/linenos
import locale
locale.setlocale(locale.LC_ALL, "fr_FR.UTF8")

largeur = 10
precision = 2
entier = 65456
flottant = 65.456
chaine = "chaîne de caractères"
objet = [largeur, precision, entier, flottant, chaine]

print(f"Ligne  9 : |{entier}|")
print(f"Ligne 10 : |{entier :n}|")     # Entier localisé
print(f"Ligne 11 : |{entier :#x}|")    # Hexadécimal avec 0x au début
print(f"Ligne 12 : |{entier :08X}|")   # Hexadécimal en majuscules, d'au moins 8 chiffres remplis par des zéros
print(f"Ligne 13 : |{entier :^+10}|")  # Entier par défaut, avec signe, centré sur 10 caractères
print(f"Ligne 14 : |{entier :+^10}|")  # Entier par défaut, centré sur 10 caractères, les espaces vides sont remplis par des +
print(f"Ligne 15 : |{entier :c}|")     # Caractère unicode correspondant
print(f"Ligne 16 : |{flottant}|")
print(f"Ligne 17 : |{flottant :.2f}|")      # 2 décimales
print(f"Ligne 18 : |{flottant :·<10.2%}|")  # Pourcentage à 2 décimales, aligné à gauche, et rempli par des `·` jusqu'à remplir 10 caractères
print(f"Ligne 19 : |{flottant :·<{largeur}.{precision}%}|")  # Pareil mais avec des expressions pour la largeur et la précision
print(f"Ligne 20 : |{chaine}|")
print(f"Ligne 22 : |{objet}|")         # Affiche la liste
print(f"Ligne 23 : |{objet !a}|")      # Affiche la liste avec échappement des caractères non-ASCII
```
;;;

### Listes et tuples

Une **liste** est une simple liste ordonnée d'objets, où vous pouvez ajouter, retirer, itérer, rechercher et modifier à votre guise. En Python il n'y a pas de typage strict, donc vous pouvez y mettre ce que vous voulez, dans tous les types que vous voulez. C'est un objet de type `list`, qui se définit en listant les objets entre crochets `[]`. Une liste vide s'écrit `[]`, `[1]` est une liste à un élément, `[1, 2, 3]` a plusieurs éléments.

Un **tuple** est à peu près pareil, sauf que vous ne pouvez **pas le modifier** après sa création. Il se définit en listant les éléments entre parenthèses. `()` est un tuple vide, `(1, 2, 3)` est un tuple à plusieurs éléments, par contre pour faire un tuple à un seul élément ce sera `(1, )`, parce que `(1)` serait juste la valeur entre parenthèses dans un calcul.

Vous pouvez accéder aux éléments d'une liste en mettant l'index entre crochets, ex. `maliste[2]`. Comme d'habitude, les indices commencent à 0.

;;; example ```python/result
maliste = [16, 12.345, "chaîne", ["autre", "liste"],
		   {"ou": "même", "n'importe quoi": "d'autre"}]
print(maliste[0], maliste[1])
maliste[0] = 116
maliste[1] *= 4
print(maliste[0], maliste[1])```
;;;

Pour ajouter des éléments, c'est avec les méthodes `.append(objet)` pour ajouter à la fin, ou `.insert(index, objet)` pour l'insérer ailleurs. Vous avez aussi `.extend(liste)` pour ajouter les éléments d'une autre collection à la fin. Vous pouvez ajouter des listes entre elles avec l'opérateur `+`, et prendre `n` fois le contenu de la liste avec `* n`

;;; example ```python/result
maliste = []
maliste.extend((1, ) * 3)   # Un tuple avec 3 fois l'élément `1`
maliste.append("fin")
maliste.insert(0, "début")  # Insère à l'index 0 = juste avant l'objet actuellement à l'index 0
print(maliste)```
;;;

Vous avez `.pop(index)` qui supprime et renvoie l'élément à l'index donné, `.remove(valeur)` qui supprime les éléments avec la valeur donnée de la liste, et `.clear()` qui vide la liste. Vous pouvez aussi supprimer un élément avec `del liste[index]`

;;; example ```python/result
maliste = ["début", 1, 1, 1, "fin"]
print(maliste.pop(0))
maliste.remove("fin")
print(maliste)
maliste.clear()
print(maliste)```
;;;

Vous pouvez trier une liste avec `.sort()` et inverser l'ordre de ses éléments avec `.reverse()`

;;; example ```python/result
maliste = [1, 5, 3, 4, 2]
print(maliste)
maliste.sort()
print(maliste)
maliste.reverse()
print(maliste)```
;;;

Il y a des pelletées d'autres méthodes qu'on verra sur une page dédiée, mais d'ici là c'est la base.

#### Indexation avancée

En Python, vous pouvez non seulement prendre un élément d'une liste par son index partant du début, mais aussi en partant de la fin, et prendre plusieurs éléments à la fois.

Pour indexer en partant de la fin, il suffit d'utiliser des indices négatifs. `maliste[-1]` donne le dernier élément de la liste, `maliste[-2]` l'avant-dernier et ainsi de suite.

Pour prendre plusieurs éléments, on utilise ce qu'on appelle des tranches (*slices*). Pour ça, on donne l'index sous la forme `maliste[debut:fin:pas]`. Comme pour tous les intervalles en Python, c'est `début` inclus, `fin` exclus. Du coup finir à `-1` exclura le dernier élément. Tous ces éléments sont facultatifs, ne pas spécifier le début commencera la tranche au début de la liste, ne pas mettre la fin finira la tranche à la fin de la liste, et ne pas donner de pas donnera tous les éléments entre `début` et `fin` (pas de 1)

;;; example ```python/result
maliste = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"Liste d'origine :                              {maliste=}")
print(f"Dernier élément :                              {maliste[-1]=}")
print(f"3 premiers éléments :                          {maliste[:3]=}")
print(f"Éléments à partir du 3ème :                    {maliste[2:]=}")
print(f"Sans le premier et le dernier :                {maliste[1:-1]=}")
print(f"Éléments d'index pair :                        {maliste[::2]=}")
print(f"Éléments d'index impair :                      {maliste[1::2]=}")
print(f"Tous les 3 éléments entre le 2ème et le 8ème : {maliste[1:8:3]=}")
print(f"Copie superficielle moins lisible :            {maliste[:]=}")```
;;;

Tout ça marche bien sûr partout où vous pouvez utiliser des index, que ce soit une liste, un tuple, une chaîne de caractères, …

### Dictionnaire

Un **dictionnaire**, de type `dict`, est ce qu'on appelle en algorithmique une *table d'association* : ça associe des clés à des valeurs. Ça se définit entre crochets : `{}` est un dictionnaire vide, pour y mettre des choses c'est `{"clé": "valeur", 1: 3}`. On y accède avec les `crochets["clé"]`, sauf que cette fois on ne met pas un index mais la clé entre les crochets. Pour ajouter un élément ou modifier la valeur d'un élément existant, affectez juste la valeur à la clé que vous voulez, ça créera l'élément.

;;; example ```python/result
mondictionnaire = {"user-001": "Jean-Pierre Dupont", "user-002": "Jean-Patrick Dumont"}
print(mondictionnaire["user-001"])
print(mondictionnaire["user-002"])

mondictionnaire["user-003"] = "Jean-Christophe Dubois"  # On crée un élément
print(mondictionnaire["user-003"])```
;;;

Notez que les clés doivent être d'un type dit *hashable*. On verra ça plus tard, mais en gros ce sont les types qui ne peuvent pas changer d'état après leur création, ce qui inclut notamment les nombres, les chaînes de caractères, les tuples, …

Vous avez toujours `len(objet)` pour avoir le nombre de paires clé-valeur dans le dictionnaire. Vous pouvez utiliser `clé in dictionnaire` / `clé not in dictionnaire` pour trouver si la clé existe dans le dictionnaire. Vous pouvez fusionner des dictionnaires avec la méthode `dic1.update(dic2)`, ou l'opérateur `dic1 | dic2` à partir de Python 3.9.

;;; example ```python/result
dictionnaire1 = {"user-001": "Jean-Pierre Dupont", "user-002": "Jean-Patrick Dumont"}
dictionnaire2 = {"user-001": "Jean-Paul Durand", "user-010": "Jean-Barnabé Duval"}

print(f"Dictionnaire 1 : {len(dictionnaire1)} éléments, dictionnaire 2 : {len(dictionnaire2)} éléments")
dictionnaire1 |= dictionnaire2
print(dictionnaire1)```
;;;

### Ensemble

Les **ensembles** sont des collections qu'on utilise plus rarement, de type `set`. Ce sont des ensembles d'objets non ordonnés, donc où vous ne pouvez pas récupérer un objet par un index — par contre ils sont beaucoup plus efficaces que les listes pour la recherche (savoir si un élément est dans l'ensemble ou pas). Un ensemble ne peut pas contenir d'objets en double, donc c'est aussi utile pour la suppression des doublons.

;;; example ```python/result
ensemble1 = set()  # {} ce serait un dictionnaire, pas un ensemble. Pour créer un ensemble vide c'est avec set()
ensemble1.add(5)   # Ajoute un élément à l'ensemble
ensemble1.add(10)
ensemble1.add(20)
ensemble1.add(5)   # Cet ajout sera ignoré vu que 5 est déjà dans l'ensemble
print(ensemble1)

ensemble2 = {50, 100, 200}   # {clé1: valeur1, clé2: valeur2} c'est un dictionnaire, mais {val1, val2} c'est un ensemble
ensemble1.update(ensemble2)  # Fusionne les deux ensembles, marche aussi avec |=
ensemble1.remove(50)         # Supprime un objet
print(ensemble1)

print(100 in ensemble1, 200 in ensemble1, 110 in ensemble1)```
;;;

Il y a aussi des ensembles figés, qui ne peuvent pas être modifiés après construction, qui s'appellent des `frozenset`, et qui se créent avec `frozenset(collection).`

## Conversions

C'est très facile de convertir entre les types, il suffit d'appeler la fonction correspondante.

;;; example ```python
entier = 16
réel = 3.8551

tronqué = int(réel)    # Convertit le float en int, par troncature (ici 3)
arrondi = round(réel)  # Arrondit au plus proche (ici 4)
arrondi_décimales = round(réel, 2)  # Arrondit au nombre de décimales demandé (ici 3.86)
entier_float = float(entier)  # Donne juste 16.0
booléen = bool(entier)  # Évaluation booléenne : 0, une chaîne vide ou une collection vide est fausse, tout le reste est vrai. En théorie None est faux aussi, mais la doc dit qu'il faut pas se reposer dessus et toujours tester x is / is not None

chaine1 = "12321"
entier_converti = int(nombre_chaine)  # Donne le nombre écrit dans la chaîne de caractères (ici 12321)

chaine2 = "1.608"
réel_converti = float(réel_chaine)    # float() peut aussi convertir les chaînes de caractères (ici 1.608)

# str() marche avec absolument tout et donne une représentation de l'objet sous forme de chaîne de caractères
entier_chaine = str(entier)
réel_chaine = str(réel)

liste_caractères = list(chaine1)      # Convertit en liste (ici des caractères ["1", "2", "3", "2", "1"])
tuple_caractères = tuple(chaine1)     # Convertit en tuple à la place ("1", "2", "3", "2", "1")
ensemble_caractères = set(chaine1)    # Donne l'ensemble des caractères utilisés {"1", "2", "3"}
ensemble_caractères = set(liste_caractères)```
;;;

## Portée des variables

Comme d'habitude, il faut parler de la *portée* des variables, c'est-à-dire quand vous déclarez une variable, où vous pouvez l'utiliser ensuite. Sur ce point Python est plus simple que des langages plus stricts comme C/C++ : pour le moment, le seul bloc de code important ici est la fonction. Il y a quelques cas particuliers qu'on verra plus tard mais rien de problématique.

Une variable (ou une fonction, ou quoi que ce soit d'autre) est utilisable à partir du moment (dans le temps) où elle a été définie pour la première fois, dans la fonction où elle a été définie, ou dans le fichier si elle est dans l'espace global. Il faut voir ça comme une pile : d'abord on regarde dans les variables locales, si la variable n'est pas définie localement on cherche dans le contexte immédiatement supérieur, et ainsi de suite. Les sous-blocs (conditions, boucles, …) n'ont aucune importance, une variable déclarée dans une condition ou une boucle, ou un compteur de boucle par exemple, peuvent être utilisées après en être sorti.

;;; example ```python/result
CONSTANTE = 10

def fonction1():  # 2 – On exécute la fonction1
	fonction2()   # 3 – fonction2 est définie plus bas mais pas de problème, quand on l'appelle l'interpréteur est déjà passé dessus

def fonction2():
	variable = CONSTANTE - 1  # On peut lire une constante globale
	for i in range(5):
		variable += i
	print(i, variable)  # i est accessible hors de la boucle

# 0 – À ce stade, l'interpréteur est passé sur tout ce qui est plus haut, donc CONSTANTE, fonction1 et fonction2 sont définies
fonction1()  # 1 – La fonction1 a été déclarée plus haut, on l'appelle```
;;;

### Variables globales

;;; alert
Une variable globale qui n'a pas une *très* bonne raison d'exister est généralement signe d'une mauvaise conception. Utiliser des variables globales empêche d'utiliser certaines fonctionnalités dans plusieurs contextes, peut faire que plusieurs parties du programme peuvent entrer en conflit, et ça rend le code plus confus vu qu'on voit plus difficilement d'où viennent les valeurs.
Idéalement, une fonction ne devrait pas avoir d'état, ou si elle en a besoin, il devrait être passé en argument, ou la fonction devrait être une méthode d'objet.
En théorie, vous ne devriez pas avoir de variables globales à moins de devoir communiquer des choses entre des parties du programme qui n'ont rien à voir entre elles, ce qui est rarement le cas tant que vous ne faites pas de l'interface utilisateur ou du multi-thread.
Bien sûr, les **constantes** globales ne posent aucun problème et sont très courantes pour paramétrer un programme.
;;;

Les variables globales se comportent d'une façon un peu particulière. Ci-dessus, vous avez vu une *constante* globale. Ça pas de problème, comme on l'a dit, quand on cherche à lire une valeur, l'interpréteur cherche dans les contextes de plus en plus larges comme une pile et finit par tomber sur le contexte global. Par contre, pour utiliser des *variables*, il faut pouvoir écrire et là c'est plus compliqué. Par défaut, quand vous assignez une valeur à une variable, la variable sera locale. S'il y a une variable du même nom dans l'espace globale, elle sera juste masquée par la variable locale : toutes les opérations se feront sur la variable locale sans aller cherchez la globale du tout.

;;; example ```python/result
variable = 0

def fonction():
	variable = 4
	print("Locale :", variable)

print("Avant :", variable)
fonction()
print("Après :", variable)```
;;;

Pour utiliser la variable globale et ne pas en redéclarer une nouvelle locale, il faut le dire explicitement avec le mot-clé `global` :

;;; example ```python/result
variable = 0

def fonction():
	global variable
	variable = 4
	print("Locale :", variable)

print("Avant :", variable)
fonction()
print("Après :", variable)```
;;;
