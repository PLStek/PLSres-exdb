//// title = "Les conditions"
//// description = "Conditionner du code en Python"

# {=title}
## Conditions logiques

Ça évalue simplement les conditions dans l'ordre et exécute le bloc de la première condition vraie.

;;; code ```python
# Première condition : ça n'exécute ce bloc que si la condition est vraie
if len(résultat) == 0:
    print("Erreur : le résultat est vide")
# Autres conditions : si la condition précédente était fausse et que celle-ci est vraie, le bloc est exécuté
elif sum(résultat) == 0:
    print("Erreur : Le résultat est nul")
# Encore une : si toutes les conditions précédentes sont fausses et que celle-ci est vraie, le bloc est exécuté
elif résultat[0] == 0:
    print("Erreur : Le résultat commence par un zéro")
# Ne s'exécute que si toutes les conditions sont fausses
else:
    print("Erreur : On ne sait pas quoi faire de ce résultat")
# N'importe quelle combinaison marche : if seul, if-elif-elif-… seuls, if-else sans elif, …

if len(résultat) > 0:
    if sum(résultat) > 10:
        print("Très beau résultat")
    # C'est un nouveau if, donc totalement indépendant du précédent, ils ne sont pas mutuellement exclusifs
    if len(résultat) > 10:
        print("Très long résultat")```
;;;

## Expressions conditionnelles

Python autorise des *expressions conditionnelles*, qui sont un peu comme les ternaires du C mais en plus naturel. C'est une expression (donc qui peut s'utiliser dans d'autres expressions), et qui donne une valeur en fonction d'une condition. Ça s'écrit simplement `valeur_si_condition_est_vraie if condition else valeur_si_condition_est_fausse`

;;; code ```python/result
attributes = {"hidden": False, "relevantCourses": ("LO21", "IF3")}
# ...

print("relevantCourses : ", attributes["relevantCourses"] if "relevantCourses" in attributes else '—')
print(f"description : {attributes['description'] if 'description' in attributes else '—'}")```
;;;

N'en abusez pas non plus, si vous commencez à les empiler il ne faut pas que ça devienne illisible.

## Reconnaissance de motif

**— Seulement à partir de Python 3.10**

Depuis Python 3.10, on a enfin quelque chose qui ressemble à un `switch`, comme dans la majorité des autres langages, avec la syntaxe `match - case`.

;;; code ```python/result/stdin="5\n"
# C'est pour l'exemple, par pitié ne faites pas ça
nombre = int(input("Nombre à tester : "))
match nombre:
    case 0:  # S'exécute si nombre == 0
        print("Pair !")
    case 1:  # S'exécute si nombre == 1
        print("Impair !")
    case 2:  # ...
        print("Pair !")
    case 3:
        print("Impair !")
    case other:  # Toutes les autres valeurs possibles
        print("Oh la barbe")```
;;;

Sauf que c'est beaucoup plus puissant que la majorité des autres langages. Déjà, vous pouvez capturer pour plusieurs expressions différentes en les séparant par des `|` :

;;; code ```python
match file.read(4):
    case b"CLYT" | b"FLYT":
        filetype = "layout"
    case b"CLIM" | b"FLIM" | b"BNTX":
        filetype = "texture"
    case b"CSTM" | b"RSTM" | b"CWAV":
        filetype = "audio"
    case other:
        filetype = "unknown"```
;;;

Ensuite, ça permet aussi de reconnaître la structure, et même le type en plus des valeurs. Vous pouvez aussi ajouter des conditions supplémentaires pour chaque `case`. Vous pouvez même en extraire des variables.

;;; code ```python/result
def compute_node(node):
    match node:
        # Capture selon le type et récupère la valeur dans `value`
        case int() | float() as value:
            return value
        # Capture les séquences (listes, tuples) de deux éléments, si le premier est égal à "LITERAL"
        # Le deuxième élément va dans la variable `value`
        case ("LITERAL", value):
            return value
        # Pareil avec 3 éléments
        case ("PLUS", left, right):
            return compute_node(left) + compute_node(right)
        case ("MINUS", left, right):
            return compute_node(left) - compute_node(right)
        case ("TIMES", left, right):
            return compute_node(left) * compute_node(right)
        case ("DIVIDE", left, right):
            return compute_node(left) / compute_node(right)
        case other:
            raise KeyError(f"Invalid node type {node[0]}")

# (10 + 12*4) - (10 / (11 - 2*3)) = 56
tree = ["MINUS",
    ("PLUS",
        ("LITERAL", 10),
        ("TIMES", 12, 4)
    ),
    ("DIVIDE",
        ("LITERAL", 10),
        ("MINUS",
            ("LITERAL", 11),
            ("TIMES", 2, 3)
        )
    )
]
print(f"Résultat : {compute_node(tree)}")
```
;;; code ```python/result
user = {"id": 10004324, "name": "Jean-Paul Duval", "type": "client", "age": 66}

# Ça marche aussi très bien avec des dictionnaires
# Notez que pour les dictionnaires ça capture les dictionnaires qui ont *au moins* les clés / clés-valeurs demandées
# Ici il y a `name` en plus mais ça capture quand même
match user:
    # On ne rentrera ici que si le motif correspond, et si la condition est vraie
    case {"type": "client", "age": age, "id": clientid} if age >= 18:
        print(f"Client n°{clientid} : ok (age {age})")
    # Ça teste successivement comme un if-elif-else: la précédente n'est pas passée, mais celle-ci passera
    case {"type": "client", "age": age, "id": clientid}:
        print(f"Client n°{clientid} : minor")
    case {"type": "manager", "department": department, "name": name}:
        print(f"{name} is manager of the {department} department")
    # Pas de case other : il ne se passera rien si ça ne correspond à rien```
;;;
