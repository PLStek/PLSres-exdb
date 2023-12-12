//// title = "Exceptions"
//// description = "Les exceptions et leur gestion en Python"

# {=title}

## Principe des exceptions

Python, comme la plupart des langages plus haut niveau que C, permet de traiter les problèmes par un système d'exceptions. En C, une erreur va soit crasher le programme immédiatement sans espoir de guérison, ou renvoyer une valeur spéciale pour signifier que c'est une erreur. Ici, on utilise ce qu'on appelle des *exceptions*.

Une **exception** est ce qui arrive quand quelque chose dans le programme rencontre une erreur. Une exception peut alors être rattrapée par une fonction appelante pour traiter l'anomalie correctement, soit en arrangeant la situation, soit pour avertir l'utilisateur proprement et nettoyer avant de quitter.

En Python, une exception est un objet descendant du type `Exception`, qui a au moins un *type* et un *message d'erreur*, plus éventuellement d'autres attributs selon le type d'exception. Quand une exception n'est pas rattrapée, elle termine le programme en affichant un *traceback*, la pile des appels de fonctions qui y ont mené, avec chaque fois la ligne exacte en faute. Lisez bien ça, c'est là que vous aurez le plus d'infos sur les causes de l'exception.

;;; example ```python/result/exception
def lire(nom_fichier):
    with open(nom_fichier, "r") as fichier:
        return fichier.read()

def lire_données():
    contenu = lire("données.dat")
    données = {}
    for ligne in contenu.splitlines():
        clé, valeur = [élément.strip() for élément in ligne.split("=")]
        données[clé] = valeur
    return données

lire_données()```
;;;

## Rattrapage des exceptions

Pour rattraper des exceptions, on utilise un bloc `try-except`.

;;; code ```python
try:
    # Code où il peut y avoir une exception
except:
    # Code à exécuter s'il y a une exception```
;;; counterexample ```python/result
try:
    with open("fichier.dat", "r") as fichier:
        données = fichier.read()
    print(données)
except:
    print("ERREUR : `fichier.dat` n'existe pas ou n'est pas accessible")
print("Fini")```
;;;

Le code du `try` s'exécute normalement, jusqu'à tomber sur une exception. S'il n'y a pas d'exception c'est super, le bloc `try` va jusqu'au bout puis l'exécution reprend après le bloc `try-except`. S'il y a une exception, on laisse tomber toute la suite du `try`, on saute directement au bloc `except` qui est alors exécuté normalement, puis ça reprend après le bloc. Par exemple ici, il y a une erreur à la première ligne du `try` donc ça a sauté au `except` immédiatement sans exécuter la suite du `try`.

Un `except` simple comme ça rattrape absolument n'importe quelle exception. À moins d'avoir une très bonne raison de le faire, c'est généralement une **mauvaise pratique**. Premièrement, le traitement de l'exception est souvent spécifique à l'exception, donc il faut bien filtrer sur le type de l'exception pour que ce soit pertinent ; deuxièmement, ça rattrapera toutes les exceptions, même des exceptions qui ont de bonnes raisons d'être levées (qui signaleraient des erreurs de programmation pas prévues par exemple) ; et troisièmement, il y a parfois des exceptions qu'il ne faut justement pas rattraper. Par exemple, pour récupérer une entrée utilisateur de façon sûre, on peut être tenté de faire ça :

;;; counterexample ```python
while True:
    try:
        valeur = int(input("Entrez un nombre : "))
        break
    except:
        print("    Vous devez entrer un nombre entier !")```
;;;

Mais c'est en fait très mauvais, parce que quand l'utilisateur appuie sur `Ctrl+C`, la commande pour quitter immédiatement un programme en cours, Python le traduit en exception de type `KeyboardInterrupt`… qui est alors rattrapée par le `except` qui donne un mauvais message d'erreur et qui bloque l'utilisateur sans espoir de sortie tant qu'il n'a pas entré un nombre. Un `except` générique est donc généralement réservé aux cas où on veut juste rattraper toute erreur qui arrive pour appliquer des étapes spécifiques avant de quitter le programme (pour ne pas perdre ce qu'a fait l'utilisateur par exemple).

Il faut donc **toujours être spécifique dans le traitement de ses exceptions**. Pour cela, on utilise `except TypeDException:`

;;; example ```python/result/stdin="aaaaaa\n\n42\n"
while True:
    try:
        valeur = int(input("Entrez un nombre : "))
        break
    except ValueError:
        print("    Vous devez entrer un nombre entier !")
print(valeur)```
;;;

Pour savoir quels types d'exception peut lever une fonction, référez-vous à sa documentation. Par exemple ici, si vous donner une valeur inconvertible à une fonction de conversion (par exemple quelque chose qui ne représente pas un entier à `int()`), ça lèvera une `ValueError`.

Notez que les exceptions sont organisées sous forme de hiérarchie, par héritage. `except TypeDException` rattrapera le type demandé **et toutes ses sous-classes**. Par exemple, `OSError` est la superclasse d'un certain nombre d'exceptions liées au traitement du système de fichiers, comme `FileNotFoundError` (le fichier n'existe pas), `IsADirectoryError` (vous essayez d'ouvrir un répertoire comme un fichier), `PermissionError`, etc. Vous pouvez traiter toutes ces exceptions séparément, ou bien utiliser `OSError`, qui les rattrapera toutes à la fois.

À la base de cette hiérarchie, il y a `BaseException` et `Exception`. `except Exception` rattrape toutes les *erreurs*, et c'est ce que vous devriez utiliser si vous voulez faire un traitement générique. `except BaseException` est équivalent à juste `except` et rattrape en plus les exceptions d'origine extérieure comme `KeyboardInterrupt` (l'utilisateur utilise Ctrl+C pour quitter) ou `SystemExit` (le gestionnaire de tâches a dit stop), c'est vraiment juste pour nettoyer avant de quitter le programme, vous ne devriez pas empêcher la fin du programme avec ça sans une très, très bonne raison.

Vous avez la hiérarchie des exceptions standard ici : [https://docs.python.org/3/library/exceptions.html#exception-hierarchy](https://docs.python.org/3/library/exceptions.html#exception-hierarchy)

Il est possible de traiter plusieurs exceptions, soit avec le même traitement, soit avec des traitements séparés en fonction du type d'erreur.

;;; example ```python/result/joinfiles=[("fichier.dat", "valeurs:1,10,100,1000")]
# Ici le fichier doit être sous la forme 1,2,3,10 (des entiers séparés par des virgules).
# On tente de l'ouvrir, le lire et récupérer les nombres sous forme d'une liste d'entiers
try:
    # Lève une OSError (ou une sous-catégorie de OSError) si le fichier n'a pas pu être ouvert
    # Ou une sous-classe de ValueError si le contenu n'est pas Unicode
    with open("fichier.dat", "r") as fichier:
        données = list(map(int, fichier.read().split(",")))  # ValueError si ce n'est pas convertible en `int`
except (OSError, ValueError):
    print("Erreur de chargement du fichier `fichier.dat`, sauvegarde…")
    # Sauvegarde...```
;;; example ```python/result/joinfiles=[("fichier.dat", "valeurs:1,10,100,1000")]
# Pareil, mais on rattrape chaque erreur plus précisément
try:
    with open("fichier.dat", "r") as fichier:
        données = list(map(int, fichier.read().split(",")))
except FileNotFoundError:
    print("Le fichier `fichier.dat` n'existe pas")
except PermissionError:
    print("Le programme n'a pas la permission d'accéder à `fichier.dat`")
# Les `except` sont vérifiés dans l'ordre : si c'est une OSError autre que FileNotFoundError ou PermissionError ça tombera ici
except OSError:
    print("Le fichier `fichier.dat` existe et est accessible mais n'a pas pu être ouvert")
except UnicodeDecodeError:
    print("Le fichier `fichier.dat` n'est pas un fichier texte donc n'est probablement pas dans le bon format")
except ValueError:
    print("Le fichier `fichier.dat` n'est pas dans le bon format")```;;;

### Clause else

Ici aussi il y a une clause `else` optionnelle. On a souvent tendance à mettre tout ce qui a besoin de ne pas rencontrer l'exception dans le `try` :

;;; counterexample ```python/result/joinfiles=[("fichier.dat", "")]
try:
    with open("fichier.dat", "r") as fichier:
        données = [int(valeur.strip()) for valeur in fichier.read().split(",") if valeur.strip() != ""]
    minimum = min(données)
    maximum = max(données)
    somme = sum(données)
    moyenne = somme / len(données)
    print(f"{somme=}, {moyenne=}, {minimum=}, {maximum=}")
except (OSError, ValueError):
    print("Erreur de chargement du fichier `fichier.dat`")```
;;;

Maintenant prenez quelques secondes pour chercher ce qui ne va pas dans ce code.

Si vous avez trouvé bravo, mais dans le monde de la réalité véritable où vous codez rapidement sans faire attention à tout, c'est le genre de choses que vous louperez facilement. Ici, si le fichier est vide, vous avez une division par zéro dans la moyenne (`ZeroDivisionError`, qui n'est pas rattrapée ici), mais surtout des `ValueError` dans `min()` et `max()` ! Or ces `ValueError` sont traitées par le bloc `except ValueError` qui n'était pas fait pour. Résultat, au mieux elles n'ont pas le bon message d'erreur, au pire ces erreurs passent complètement sous le radar. En plus, la vraie origine des erreurs traitées est moins explicite (c'est le `open("fichier.dat", "r")` mais en rajoutant des choses c'est pas évident de savoir si vous avez voulu traiter toutes les `ValueError` de tout le bloc ou juste celles de la lecture du fichier).

Pour ça, vous pouvez mettre un bloc `else`, qui sera exécuté si et seulement si il n'y a pas eu d'exceptions dans le `try`, mais sans être parasité par le `except`.

;;; example ```python/result/exception; joinfiles=[("fichier.dat", "")]
try:
    with open("fichier.dat", "r") as fichier:
        données = [int(valeur.strip()) for valeur in fichier.read().split(",") if valeur.strip() != ""]
except (OSError, ValueError):
    print("Erreur de chargement du fichier `fichier.dat`")
else:
    minimum = min(données)
    maximum = max(données)
    somme = sum(données)
    moyenne = somme / len(données)
    print(f"{somme=}, {moyenne=}, {minimum=}, {maximum=}")```
;;;

C'est bien différent de juste mettre ce code à la suite du bloc `try-except` : du code à la suite sera exécuté même si c'est le `except` qui a été exécuté, alors que le `else` ne sera exécuté que si le `except` ne s'est *pas* exécuté.

### Clause finally

Encore un autre bloc, c'est l'une des constructions les plus complexes du langage — `finally`. Vous pouvez mettre un bloc `finally` pour définir du code qui doit être exécuté quoi qu'il arrive : pas d'exception, exception traitée, exception qui fait quitter le programme, sortie de la fonction (`return`) ou de la boucle (`break`, `continue`) au milieu du `try`, du `except` ou du `else`, etc. — quoi qu'il arrive, le `finally` sera exécuté avant de partir.

Ça sert par exemple dans tous les cas où vous devez nettoyer quelque chose avant de finir.

;;; example ```python
# Ici on redirige la sortie d'erreur standard vers un fichier journal
# Il faut absolument remettre le flux standard à la normale et
# fermer le fichier avant de partir, sinon les erreurs suivantes ne
# s'afficheront pas sans raison apparente
import sys

task_manager = TaskManager()
logfile = open("errors.log", "w")
sys.stderr = logfile
try:
    task_manager.run_tasks()
except:
    print("Tasks interrupted, saving the current task state", file=sys.stderr)
    task_manager.save_state()
finally:
    sys.stderr = sys.__stderr__
    logfile.close()```
;;;

Vous pouvez d'ailleurs faire un `try-finally` sans `except`, pour que l'étape de nettoyage soit exécutée même en cas de problème mais sans traiter d'exceptions particulières.

;;; example ```python
def run_tasks(self):
    try:
        self.task1()
        if not self.task2_possible():
            return False
        self.task2()
        self.task3()
        return True
    finally:
        # Ça sera exécuté avant les return ou si une exception est levée
        self.save_results()```
;;;

Au final, voici un diagramme général de ce qui peut se passer dans un bloc `try` :

{!svg: info/python/6-tryblock.svg}

### Récupérer l'objet exception

Dans le bloc `except`, il est possible de récupérer l'objet exception rattrapé, par exemple pour gérer vous-même l'affichage de l'erreur. Certains types d'exception contiennent aussi des attributs donnant plus d'information sur l'erreur qu'un simple message, et ça permet de les récupérer. On utilise pour ça la syntaxe `except TypeDException as variable` (ou `except (Type1, Type2) as variable` pour pouvoir récupérer plusieurs types)

;;; example ```python
try:
    task_manager.load_state()
except OSError as exc:
    print(f"Impossible de charger l'état des tâches (fichier {exc.filename})")
    print(exc)  # Affiche le message d'erreur associé à l'exception, sans le traceback
task_manager.run_tasks()```
;;;

## Lever une exception

Parfois, vous pouvez avoir besoin de lever vous-même, pour traiter les erreurs irrécupérables, typiquement dans un module ou une librairie. Ça se fait avec le mot-clé `raise`, suivi de l'objet exception à lever. Essayez si possible de donner le type d'erreur le plus précis possible, un `raise Exception("Erreur !")` n'aide pas beaucoup à savoir ce qui se passe. En général une exception se crée avec le type et un simple message d'erreur.

;;; example ```python
def moyenne(nombres):
    if len(nombres) == 0:
        raise ValueError("Impossible de calculer la moyenne d'une liste vide")
    return sum(nombres) / len(nombres)```
;;;

## Créer vos propres types d'exception

Quand vous écrivez une librairie, vous pouvez avoir besoin de définir vos propres types d'exceptions, pour les cas spécifiques à votre librairie qui ne rentrent pas dans les types prédéfinis. Pour cela, vous devrez définir une classe héritant de `Exception` (ou d'une classe d'exception plus précise si c'est pertinent). Si c'est juste pour faire un type d'exception particulier avec un simple message d'erreur, vous n'avez pas besoin de faire plus, tout est déjà défini dans `Exception` :

;;; example ```python/result/exception
class StructuralError (Exception):
    pass

raise StructuralError("Erreur dans la structure")```
;;;

Si vous voulez quelque chose de plus complexe, vous devrez au minimum définir le constructeur et la méthode `.__str__()` qui permettra de récupérer le message d'erreur quand l'erreur s'affichera, tout le reste est à votre discrétion, du moment que la classe dérive de `Exception`. Par exemple, vous pouvez mettre d'autres attributs pour construire un message d'erreur formaté et/ou permettre de récupérer plus d'information au moment de traiter l'exception.

;;; example ```python
class StructuralError (Exception):
    def __init__(self, message, format, position):
        self.message = message
        self.format = format
        self.position = position

    def __str__(self):
        return f"In structure {self.format}, position {self.position} : {self.message}"

format = input("> ")
try:
    struct = Struct(format)
except StructuralError as exc:
    print(f"Erreur : {exc.format}")
    print(f"         {exc.position*' '}^")```
;;;
