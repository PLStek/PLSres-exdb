//// title = "Syntaxe et documentation"
//// description = "Les particularités de la syntaxe de Python et les moyens de le commenter et de le documenter"

# {=title}
## La syntaxe du langage

La syntaxe de Python est assez particulière. Beaucoup de langages (Javascript, Java, C++, …) ont une syntaxe dérivée de C :

;;; example ```cpp
// Get the value at the given relative address
uint8_t InterruptRegisterMapping::get(uint16_t address) {
	uint8_t result = 0x00;
	for (int i = 0; i < 5; i++)
		result |= interrupts[i] << i;

	// IE can retain any value in its unused bits
	if (m_holdUpperBits)
		result |= m_upperBits;
	else
		result |= 0xE0;
	return result;
}```
;;;

D'autres ont une syntaxe inspirée par Fortran (Pascal, BASIC et ses désespérément existants dérivés, Ada, Matlab, …)

;;; example ```vbnet
'** Dévoile une cellule et transmet à ses voisines le cas échéant (Algorithme de flood-fill, version récursive)
' * @param grid : La grille du jeu
' * @param x : Abscisse de la case cliquée, en partant du haut à gauche
' * @param y : Ordonnée de la case cliquée, en partant du haut à gauche
' * @return : True si c'est une mine, False sinon (donc si la cellule est dévoilée)
Public Function activateCells(grid As Range, ByVal x As Integer, ByVal y As Integer) As Boolean
    showCell grid, x, y
    If grid.Cells(y, x).value = "@" Then  ' Mine
        activateCells = True
    ElseIf grid.Cells(y, x).value >= 1 Then  ' Chiffre
        activateCells = False
    Else  ' Vide (0)
        Dim nx, ny As Integer  ' (x, y) pour la cellule voisine en cours
        Dim neighbors() As Integer
        neighbors = neighboring(grid, x, y)
        For i = 1 To UBound(neighbors) / 2
            nx = neighbors(i * 2 - 1)
            ny = neighbors(i * 2)
            If grid.Cells(ny, nx).Interior.ColorIndex = hidingColor Then  ' La cellule n'a pas été dévoilée. Sale, mais on ne peut pas mettre de métadonnées aux cellules
                ' Debug.Print nx & " " & ny
                activateCells grid, nx, ny
            End If
        Next i
        activateCells = False
    End If
End Function```
;;;

Et encore d'autres ont des syntaxes encore plus exotiques, mais bref — tous ces langages se basent sur des parseurs à base relativement simple, et ont besoin chaque fois d'ouvrir et de fermer chaque bloc, petit ou grand. En Python, il n'y a rien de tout ça : les blocs de codes sont déterminés par l'indentation. Ça a deux avantages : pas d'accolade, de parenthèses ou de `end` partout, donc un code plus léger, plus lisible et plus facile à écrire (exit les point-virgules oubliés) ; et ça force à avoir la bonne indentation, donc aussi un code plus propre.

;;; example ```python
# Create an independent file for the book – author relationship
def process_wrote(log, author_books, wrote_out):
	log.title("Writing author - book relationships")
	starttime = time.time()
	with open(wrote_out, "w", encoding="utf-8", newline="") as outfile:
		writer = csv.DictWriter(outfile, fieldnames=["author_id", "book_id"])
		writer.writeheader()
		written = 0
		for i, (author_id, books) in enumerate(author_books.items()):
			for book_id in books:
				writer.writerow({"author_id": author_id, "book_id": book_id})
				written += 1

			if (i+1) % 1000 == 0:
				log.status(f"Written {written} rows from {i+1} authors")
	log.print(f"Written {written} rows from {i+1} authors")

	endtime = time.time()
	log.section(f"Section accomplished in {endtime - starttime :.3f} seconds")
	log.close()```
;;;

Globalement, en Python, tous les blocs de code commencent par une ligne terminée par `:`, a un niveau d'indentation supplémentaire par rapport à ce qui est en-dehors, et s'arrête quand l'indentation redescend, sans plus de fioritures. **L'indentation est donc primordiale**, c'est pas comme ailleurs où vous pouvez faire n'importe quoi. Pour les caractères d'indentation à utiliser, la PEP8 dit d'utiliser 4 espaces et de faire des lignes de code de 80 caractères max (parce que le retour à la ligne dans l'éditeur à cause d'une ligne trop longue casse la structure visuelle du code) — mais les tabulations permettent de s'adapter aux préférences de chacun, donc ça peut être préférable pour certains, et la longueur de la ligne dépend des outils de votre équipe. Ultimement ça reste au choix.

## Commentaires

En Python, vous avez 3 types de commentaires. Le premier est le commentaire monoligne, similaire au `//` en C/C++, et qui commence par `#`. Le commentaire commence au `#` et se termine à la fin de la ligne

;;; example ```python
# Ce bloc de code fait quelque chose d'intéressant
if parametres["themeColor"] is not None:
	faire_qqch()  # Cette fonction fait le quelque chose intéressant```
;;;

Le deuxième permet les commentaires multiligne, et se met entre triples guillemets `"""` (ou `'''`)

;;; example ```python
"""similarity = (sum(max(lines[i])) + sum(max(columns[i]))) / (len(lines) + len(columns))
   subclass = (sum(max(lines[i])) + sum(max(columns[i]))) / (len(lines) + len(columns where max(columns[i]) is considered))"""

for shelfindex in range(similarity_matrix.shape[0]):
	rowmax = similarity_matrix[shelfindex].max()
	if rowmax > 0:
		maxsum += rowmax
		subclass_denominator += 1```
;;;

Et le troisième s'appelle une **docstring**, et est très important parce qu'il permet d'écrire la documentation de vos fonctions directement dans le code. Ces docstrings peuvent être extraites et sont utilisées par l'aide interactive (fonction `help()` dans l'interpréteur), et par les générateurs de documentation comme Pydoc et Docutils. En réalité, c'est juste un commentaire comme ci-dessus, mais situé juste en-dessous de la définition qu'il documente, donc au début d'un fichier ou juste après la ligne `class X:` ou `def x():`

;;; example ```python
"""Création d'objets parfaitement inutiles"""

class ObjetInutile:
	"""Définit un objet inutile tout à fait quelconque"""

	def methode(self, x, y):
		"""Prends deux arguments, et n'en fais rien de spécial.

		Comme vous pouvez le voir, la PEP 257 dit que c'est mieux de mettre
		une description courte de la fonction sur la première ligne,
		un saut de ligne, puis la description longue. Et de garder les
		ligne en-dessous de 72 caractères de large si vous pouvez, pour les
		terminaux plus étroits.

		Vous noterez l'impératif : c'est généralement une bonne pratique
		de rendre sa documentation prescriptive, c'est-à-dire de l'écrire
		comme un ordre qu'on donnerait à la fonction. Ça fait des phrases
		plus concises, moins complexes et plus compréhensibles pour ceux
		qui comprennent moins bien la langue utilisée.

		Arguments :
		x -- Un argument inutile
		y -- Un autre argument qui n'ira nulle part
		"""

		print("Je suis une méthode et je ne fais rien !")```
;;;

Ce que ça donne dans l'aide interactive :

;;; example ```python
>>> import module_inutile
>>> help(module_inutile)
``` ```
Help on module module_inutile:

NAME
    module_inutile - Création d'objets parfaitement inutiles

CLASSES
    builtins.object
        ObjetInutile

    class ObjetInutile(builtins.object)
     |  Définit un objet inutile tout à fait quelconque
     |  
     |  Methods defined here:
     |  
     |  methode(self, x, y)
     |      Prends deux arguments, et n'en fais rien de spécial.
     |      
     |      Comme vous pouvez le voir, la PEP 257 dit que c'est mieux de mettre
     |      une description courte de la fonction sur la première ligne,
     |      un saut de ligne, puis la description longue. Et de garder les
     |      ligne en-dessous de 72 caractères de large.
     |      
     |      Vous noterez l'impératif : c'est généralement une bonne pratique
     |      de rendre sa documentation prescriptive, c'est-à-dire de l'écrire
     |      comme un ordre qu'on donnerait à la fonction. Ça fait des phrases
     |      plus concises, moins complexes et plus compréhensibles pour ceux
     |      qui comprennent moins bien la langue utilisée.
     |      
     |      Arguments :
     |      x -- Un argument inutile
     |      y -- Un autre argument qui n'ira nulle part```
;;;

## Import de modules

Python a une librairie standard immense et énormément de librairies tierces, donc on va très souvent utiliser ce qui est déjà dispo sans se prendre la tête. Pour ça il faut *importer* des *modules* (ou *packages*). Il y a plusieurs moyens d'importer un module.

;;; code ```python/result
# Ici on importe simplement le module.
# C'est généralement le moyen le plus recommandé car ça garde tout bien rangé
import math

# Pour utiliser le contenu du module, c'est `module.élément`
angle_rad = math.acos(math.pi / 4)
print(angle_rad)```
;;; code ```python/result
# On peut aussi utiliser un alias avec `as`
import datetime as dt

maintenant = dt.datetime.now()
print(f"{maintenant}")```
;;; code ```python/result
# Ici on importe un seul élément du module
# L'objet sera alors dispo comme n'importe quel autre dans le fichier
# C'est l'autre méthode d'import recommandée
# Il est possible d'importer un seul, ou plusieurs éléments à la fois
from decimal import Decimal, getcontext

# Les objets importés sont disponibles directement sans préfixe
context = getcontext()
context.prec = 50
a = Decimal(1)
b = Decimal(1) / context.sqrt(Decimal(2))
t = Decimal(1/4)
p = Decimal(1)
for k in range(6):
	next_a = (a + b) / 2
	b = context.sqrt(a * b)
	t -= p * (a - next_a)**2
	p *= 2
	a = next_a
	print(f"Itération {k} : π ≃ {(a + b)**2 / (4*t)}")```
;;; counterexample ```python/result
# Import tout le contenu du module directement dans l'espace global
# Cette méthode n'est pas recommandée car elle bourre tout le contenu du module
# dans le vôtre, donc ça peut créer des conflits de noms avec des trucs dont vous
# ne connaissez même pas l'existence.
# C'est aussi mieux d'être explicite, comme ça on sait ce que vous utilisez dans le module
from hashlib import *

# Maintenant tout le contenu du module est dans l'espace global (ici on utilise sha256, mais il y a énormément d'autres choses)
hash = sha256("m0tD€pa$$e".encode("utf-8")).hexdigest()
print(hash)
```
;;;

Pour choisir la bonne méthode, si ça n'alourdit pas trop le reste du code on préfère largement utiliser `import module` (donc ensuite `module.élément`), c'est plus organisé et on sait d'où vient chaque chose. Si on est sûr que rien est ambigu, la version `from module import élément` est bien aussi. Par exemple, `from hashlib import sha512` ne pose pas de problème car on voit bien ce que `sha512()` fait et d'où ça vient rien qu'à son nom, pareil pour des choses comme `from xml.sax.xmlreader import XMLReader` où c'est assez clair et répéter `xml.sax.xmlreader.XMLReader` serait pénible. Par contre il y a des situations où c'est une très mauvaise idée.

;;; counterexample ```python
from json import dump

users = [
	{"id": 10004323, "name": "Jean-Baptiste Dubout", "postcode": "87160"},
	{"id": 10007541, "name": "Jean-Félix Dubalai", "postcode": "50800"},
]
with open("users.json", "w") as backup:
	dump(backup, users)```
;;;

Ici, on a une fonction `dump()` au nom très générique. On ne sait pas d'où elle sort au premier coup d'œil, et pire, si on a d'autres modules importés de la sorte il peut facilement y avoir plusieurs fonctions `dump()` qui seraient écrasées les unes par les autres. Dans ces cas-là, il faut garder le préfixe.

;;; example ```python
import json

users = [...]
with open("users.json", "w") as backup:
	json.dump(backup, users)  # Là on sait que c'est du JSON, et pas de confusion```
;;;

## Organisation d'un fichier de code Python

Généralement, un fichier de code Python a une certaine structure :

;;; code ```python
"""Tout en haut, l'éventuelle docstring du module.

Pour un script, on y met généralement le message d'aide du programme,
pour un module on décrit ce qu'il fait et généralement son interface.
"""

# Ensuite, les imports de modules
import os
import math

# Puis les constantes et éventuelles variables globales
PARAMETRE_MIN = 0
PARAMETRE_MAX = 100

# Ensuite, les fonctions et classes
class MaClasse:
	def __init__(self):
		pass

	def methode1(self, x, y):
		pass

def fonction1():
	pass

def fonction2(x, y):
	pass

# Et tout en bas, l'éventuel point d'entrée du script
# Le if __name__ == "__main__" sert à vérifier si le script est bien exécuté
# directement (`python3 monscript.py`), et pas importé (`import monmodule` dans
# un autre fichier). En effet, importer exécute le code du fichier, donc sans
# cette vérification l'autre fichier exécutera le fichier comme un script
# alors qu'il veut juste ses fonctions et classes.
# Dans un script, c'est là qu'il y aura le code principal, comme une fonction main()
# Dans un module, vous pouvez y mettre du code de test par exemple
if __name__ == "__main__":
	print("Ce fichier a été exécuté comme un script !");```
;;;
