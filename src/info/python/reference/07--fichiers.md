//// title = "Fichiers"
//// description = "L'utilisation des fichiers en Python"

# {=title}
## Ouvrir un fichier

L'utilisation des fichiers est très facile en Python, et repose globalement sur la fonction `open()`, qui s'utilise comme ceci :

;;; code ```python
with open("nom-du-fichier", "r") as fichier:
    # Faire des choses avec le fichier
# Fini d'utiliser le fichier```
;;;

De nos jours, `open` peut s'utilise comme un *gestionnaire de contexte* avec le mot-clé `with` : on reverra ça, mais c'est en gros l'équivalent d'un `try-finally` avec des instructions prédéfinie. Ici, quoi qu'il arrive (exception, `return`, `break`, …), le fichier sera fermé avant de sortir du bloc `with`.

;;; code ```python
# C'est équivalent à ça
try:
    fichier = open("nom-du-fichier", "r")
    # Faire des choses avec le fichier
finally:
    fichier.close()
# Fini d'utiliser le fichier```
;;;

Cela dit, vous pouvez toujours l'utiliser normalement, même si c'est rarement pertinent en Python moderne. Dans ce cas-là, il faut bien penser à le fermer avant de partir.

;;; code ```python
fichier = open("nom-du-fichier", "w")
fichier.write(contenu)
fichier.close()```
;;;

La fonction `open` a quelques arguments :

;;; code ```python
open(chemin, mode, encoding=None) -> objet fichier```
;;; doc
Ouvre un fichier et renvoie l'objet associé.

- `nom` : Chemin vers le fichier. Le chemin peut être relatif ou absolu, sous la forme d'une chaîne de caractères ou d'une objet *path-like* (on verra ça plus bas)
- `mode` : Mode d'ouverture, c'est comme en C
    - `"r"` : Lecture seule, le fichier doit exister au préalable
    - `"w"` : Écriture seule, crée le fichier en écrasant l'ancien s'il existait déjà
    - `"a"` : Écriture seule, crée le fichier s'il n'existe pas ou reprend à la fin du fichier s'il existe déjà
    - `"x"` : Écriture seule, crée le fichier, échoue s'il existe déjà
    - À tous ces modes, il est possible de rajouter le caractère `"b"` pour ouvrir le fichier en mode binaire. Par défaut, les fichiers sont ouverts en mode texte, donc seront décodés comme du texte (typiquement unicode) et s'utilisent avec des chaînes de caractères. En mode binaire, aucun traitement intermédiaire n'est fait, et le fichier s'utilisera avec des objets *bytes-like* (`bytes` ou `bytearray`).
    - Dans tous les cas, on peut ajouter un `+` pour ouvrir à la fois en lecture et écriture (`r+`, `wb+`, …)
- `encoding` : Argument optionnel, encodage du texte dans le fichier. Par défaut, ça prend l'encodage préféré d'après le système, **qui peut être un truc bizarre du genre cp1252 sous Windows**, donc si vous voulez forcer vos fichiers sous Windows à être en UTF-8, mettez `encoding="utf-8"` (ou l'encodage que vous voulez)

En cas d'échec, la fonction lèvera une sous-classe de `OSError`, différente selon l'erreur (`FileNotFoundError`, `PermissionError`, `FileExistsError`, …)
;;; note
Pour éviter tout accident, mettez le mode d'ouverture avec le moins de permissions possibles, inutile d’utiliser `r+` si vous n’allez que lire. En réalité, on a très rarement besoin des modes `+`.
;;;

## Fonctionnement d'un fichier

Ça va être un peu le même laïus que sur la {> info.c.stdlib.stdio#fileuse: page équivalente en C} : les fichiers ont un fonctionnement un peu particulier qu'il faut bien comprendre.
En Python, un fichier est un objet qui offre diverses méthodes pour accéder à son contenu. Il contient un **curseur** qui indique la position où vous en êtes dans le fichier. Quand vous lisez ou écrivez dans le fichier, ce curseur se déplace : par exemple, si le curseur est au début du fichier (position 0), et que vous lisez 10 caractères, ça retournera les 10 premiers caractères et le curseur sera à la position qui suit la partie que vous venez de lire (ici 10). Donc si vous lisez de nouveau 10 caractères, ça retournera les 10 suivants (de 10 à 19) et ça mettra le curseur à 20. Pareil pour l'écriture, ça place le curseur à la fin de l'opération que vous venez de faire, donc vous écrirez à la suite.

On se rappelle aussi que Python utilise le *duck typing*, c'est-à-dire que tout ce qui ressemble à un fichier peut être utilisé comme un fichier. La doc appelle ça *file-like object*, un objet qui se comporte comme un fichier. Il y en a quelques autres différents des fichiers normaux, mais vous pouvez les utiliser exactement de la même façon.

D'ailleurs les flux standard (entrée, sortie et sortie d'erreur standard) sont des objets *file-like*, auxquels vous pouvez accéder comme des fichiers dans le module `sys`, ce sont `sys.stdin`, `sys.stdout` et `sys.stderr`.

;;; example ```python
# L'argument `file` de print() demande un objet file-like ouvert en écriture,
# donc vous pouvez donner n'importe quoi, flux standard, fichier à vous, autres, …
with open("fichier.dat", "w") as sortie:
    print("Hello World !", file=sortie)```
;;; example ```python/result
# Exemple d'objet file-like qui n'est pas un vrai fichier : io.StringIO
# C'est un objet qui se comporte comme un fichier mais qui n'est pas lié à un
# vrai fichier, qui sert à récupérer ce que font des fonctions qui demandent
# un fichier directement dans une chaîne de caractères
import io
import csv

with io.StringIO() as filelike:
    writer = csv.writer(filelike)
    writer.writerow([10004324, "Jean-Patrick Duval", 65])
    writer.writerow([10003712, "Jean-Barnabé Duchemin", 56])
    content = filelike.getvalue()
print(content)```
;;;

## Les méthodes utilisables sur les fichiers
### Lecture

Une façon privilégiée de manipuler un fichier texte est d'itérer sur ses lignes : il suffit d'utiliser `for ligne in fichier`. Les sauts de ligne restent dans les chaînes de caractères.

;;; example ```python/result/joinfiles=[("fichier.txt", "1 2 3 4\n5 6 7 8\n9 10 11\n")]
with open("fichier.txt", "r") as fichier:
    for ligne in fichier:
        valeurs = [int(élément.strip()) for élément in ligne.split()]
        print(f"Somme de {valeurs} : {sum(valeurs)}")```
;;;

Autrement, il y a les méthodes plus classiques :

;;; code ```python
fichier.read()
fichier.read(nb_caractères)```
;;; doc
Lit depuis le fichier : l'intégralité du contenu du fichier si vous ne donnez pas d'argument, ou un certain nombre de caractères si vous le donnez.
;;; example ```python/result/joinfiles=[("fichier.txt", "Hello World !")]
with open("fichier.txt", "r") as fichier:
    print(fichier.read())  # Tout le fichier d'un coup

with open("fichier.txt", "r") as fichier:
    print(fichier.read(5))  # 5 caractères```
;;;

;;; code ```python
fichier.readline()```
;;; doc
Lit une ligne du fichier (terminée par un saut de ligne). Le caractère saut de ligne (`\n`) reste dans la chaîne de caractères.
;;; example ```python/result/joinfiles=[("fichier.txt", "Hello\nWorld\n!")]
with open("fichier.txt", "r") as fichier:
    print(repr(fichier.readline()))
    print(repr(fichier.readline()))
    print(repr(fichier.readline()))```
;;;

### Écriture

Là rien de compliqué : quoi que vous vouliez écrire, il n'y a que la méthode `.write(texte)`. C'est pas comme `print()`, vous devez lui donner une chaîne de caractères. N'oubliez pas les éventuels sauts de ligne, ils ne sont pas insérés pour vous. La méthode renvoie le nombre de caractères réellement écrits.

;;; example ```python/result
# Pour la démo, ici on utilise le module tempfile qui permet d'utiliser des
# fichiers temporaires sans prise de tête. Pareil, c'est du file-like.
import tempfile

with tempfile.TemporaryFile(mode="w+") as fichier:
    fichier.write(f"2 + 2 = {2+2}\n")
    fichier.write(f"3 + 3 = {3+3}\n")
    # Là le curseur est à la fin, on doit revenir au début du fichier
    fichier.seek(0)
    contenu = fichier.read()
print(contenu)```
;;;

### Déplacement

Pour se déplacer dans le fichier (déplacer le curseur donc), vous avez les méthodes `.seek()` et `.tell()`, un peu comme en C. Notez que certains objets *file-like* ne permettent pas de vous déplacer comme vous voulez (par exemple vous ne pouvez pas déplacer le curseur dans les flux standards ou certains fichiers spéciaux comme `/dev/urandom` sous UNIX).

;;; code ```python
fichier.seek(décalage, référence=0)```
;;; doc
Déplace le curseur dans le fichier en fonction du `décalage` donné par rapport au point de `référence`.

- `décalage` : Nombre de caractère pour le déplacement.
- `référence` : Point de référence. Ce paramètre peut prendre 3 valeurs :
    - `0` (par défaut) : Par rapport au début du fichier (`fichier.seek(10)` met le curseur sur le caractère d'index 10 (le 11ème donc)). Le `décalage` doit être positif.
    - `1` : Par rapport à la position actuelle. Décale le curseur du nombre de caractères demandé (`fichier.seek(-10, 0)` recule le curseur de 10 caractères). Le `décalage` peut être positif (avance dans le fichier) ou négatif (recule)
    - `2` : Par rapport à la fin du fichier (`fichier.seek(-10, 2)` met le curseur 10 caractères avant la fin). Le `décalage` doit être négatif vu qu'on recule par rapport au point de référence.

Du coup, `fichier.seek(0)` revient au début du fichier et `fichier.seek(0, 2)` va directement à la fin par exemple
;;;

;;; code ```python
fichier.tell() -> int```
;;; doc
Renvoie la position du curseur par rapport au début du fichier (donc si `fichier.tell()` renvoie 10, le prochain caractère que vous lirez est celui d'index 10, donc le 11ème)
;;;
