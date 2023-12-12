//// title = "Tests et contrats"
//// description = "Comment ne pas programmer par coïncidence"

# {=title}

Naturellement, on a tendance à écrire du code, qu'on suppose fonctionner, puis on l'essaie, et on corrige ce qui ne marche pas. Quand on fait des petits projets c'est pas un souci, mais pour des trucs sérieux c'est particulièrement scabreux. Prenons quelques problèmes avec ça :

- Vous n'êtes pas fiable *du tout*. Un humain est parfaitement incapable d'assurer que du code est juste simplement en le regardant, surtout s'il l'a écrit. Vous laisserez toujours passer des problèmes. Vous pouvez même louper des problèmes un peu discrets en testant manuellement.
- Même si vous testez manuellement votre code, vous n'allez sans doute pas tester chaque valeur pour chaque fonction (pas le temps). Vous allez donc en loupez
- Quand vous changer des choses, comment être sûr que ça n'a rien cassé ? En testant manuellement, ça frise l'impossible.

Ça a peut-être l'air méchant, mais il faut être pragmatique : vous êtes intelligent mais pas fiable, et votre ordinateur est con mais très fiable. Donc si on est pragmatique, plutôt que de faire reposer la fiabilité de votre code sur vous, on va la faire reposer sur celle de votre ordinateur.

## Automatiser les tests

La solution, c'est bien sûr de faire les tests automatiquement. C'est très fastidieux, mais quand on fait du sérieux, on n'y coupe pas. Vous allez peut-être passer une journée à écrire vos tests, mais vous ne passerez pas les 3 semaines suivantes à vous arracher les cheveux sur des bugs obscurs.

Il y a en gros deux types de tests :

- Un **test unitaire** teste *un* comportement de votre code. En règle générale, un test unitaire lance une fonction avec certaines valeurs, et vérifie que la fonction se comporte comme il faut.
- Un **test d'intégration** teste le fonctionnement général de l'application. C'est un sujet plus complexe, et c'est très dépendant de l'application : pour un outil en console, ça peut être juste le lancer avec certaines données et vérifier que ça ressort bien ce qu'on attend ; pour une grosse application, ça peut impliquer d'automatiser des actions sur l'interface graphique, il y a des langages de script exprès pour ça.

Ici, on parlera surtout des tests unitaires, les tests d'intégration sont importants aussi mais très spécifiques au projet.

### Tests unitaires

Un test unitaire est donc un test qui vérifie *un* comportement d'*une* fonction (d'où le terme *unitaire*). Et par *comportement*, on veut bien sûr dire autant les bons résultats que les erreurs. Si la fonction n'échoue pas alors qu'elle devrait, c'est un gros problème pour la suite.

C'est important d'être unitaire : il faut tester *une* fonction (idéalement), pour que si le test échoue, on sache exactement où c'est (dans la fonction, donc) ; et *un* comportement, pour ne pas que différents comportements se parasitent entre eux. C'est plus facile de débugger les tests ratés quand ce qui teste les bons résultats et ce qui teste les erreurs n'est pas dans le même test.

Il y a souvent des librairies ou des outils qui permettent de faciliter et d'automatiser les tests unitaires : le module `unittest` en Python, JUnit en Java, etc. En général, on a une suite d'assertions, pour vérifier chaque comportement. En général, on vérifie au minimum les cas normaux, les cas limite (limite des intervalles, cas un peu bizarres qui pourraient avoir des raisons de rater, extrémités des listes, etc.), et les cas d'erreur.

Par exemple, mettons qu'on a une fonction en Python qui calcule la moyenne d'une liste de nombres. Pour intégrer ça dans un projet ou une librairie, il nous faut une spécification un peu plus complète :

- La fonction renvoie la moyenne arithmétique d'une liste de nombres
- La fonction lève une exception de type `ValueError` si la liste est vide

On écrit donc notre fonction :

;;; code ```python/keep/name="moyenne.py"; next=1
def moyenne(nombres):
	if len(nombres) == 0:
		raise ValueError("La liste de nombres est vide")
	return sum(nombres) / len(nombres)```
;;;

Et les tests associés (ici avec le module standard `unittest`) :

;;; example ```python/result
import unittest
from moyenne import moyenne

class MoyenneTestCase (unittest.TestCase):
	results = [
		([0], 0),   ([0, 0], 0),  # On vérifie les zéros
		([1], 1),                 # Test avec une seule valeur
		([2, 2, 2, 2, 2], 2),     # Test avec plusieurs fois la même valeur
		([1, 2, 3], 2),           # Test normal, résultat entier
		([1, 2], 1.5),            # Test normal, résultat décimal
		([1, 10, 100, 1000], 277.75),
		([-1, 0, 1], 0),   ([-5, -2, -1], -8/3),  # Nombres négatifs
		((5, 6, 5, 6), 5.5),      # Avec d'autres types de conteneur
		({6, 2, 4, 8}, 5),
	]

	def test_moyenne_résultats(self):
		for nombres, résultat_attendu in self.results:
			résultat_obtenu = moyenne(nombres)
			# Fonction utilitaire de `unittest` : vérifie si les deux valeurs sont égales
			self.assertEqual(résultat_obtenu, résultat_attendu)

	def test_moyenne_erreur_liste_vide(self):
		# On vérifie que ça lève bien une erreur, et du bon type
		with self.assertRaises(ValueError):
			moyenne([])
		with self.assertRaises(ValueError):
			moyenne(())
		with self.assertRaises(ValueError):
			moyenne(set())

if __name__ == "__main__":
`!!!
	unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(MoyenneTestCase))
!!!`
`///
	unittest.main(verbosity=2)
///`
```
;;;

### Maintenir les tests

Bien sûr, les tests d'un bout de code doivent évoluer avec lui : il faut répercuter tous les changements de spécification sur les tests, pour continuer à tester correctement.

Surtout, parfois, il arrive qu'un bug passe entre les mailles du filet. C'est souvent oublié, mais quand ça arrive, **vous devez mettre à jour les tests en conséquence**. Un bug ne doit pouvoir arriver qu'une fois. Quand un bug arrive, vous ajoutez des tests pour le dépister, et il ne repassera plus.

### Programmation dirigée par les tests

La programmation dirigée par les tests (*test-driven development*) est une méthode pour assurer la fiabilité du code et son adhésion à la spécification, en évitant au maximum les pertes de temps. En gros, ça revient à écrire les tests *avant* le code lui-même. À partir de là, les tests deviennent la **spécification** du code : en principe, un code qui passe ces tests fait exactement ce qu'on lui demande. Pour ça, il faut bien sûr que les tests soient aussi complets que possible. Une fois les tests écrits, donc une fois les spécifications écrites en dur, on écrit le code et on le teste immédiatement.
