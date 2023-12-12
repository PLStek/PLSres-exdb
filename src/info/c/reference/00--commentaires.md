//// title = "Commentaires"
//// description = "Les commentaires en C"

# {=title}

En C, vous avez en gros 2 types de commentaires + une bidouille pour éliminer du code :

;;; code
```c
// Ceci est un commentaire sur une ligne
int x = 1729;  // Que vous pouvez mettre seul sur une ligne ou à la fin de la ligne

/* Ceci est un commentaire terminé explicitement
   Ça veut dire que vous choisissez vous même où vous l’arrêtez,
   soit sur la même ligne, soit après plusieurs lignes */

for (int i = 0; chaine[i] != '\0' /* fin de chaîne */; i++) {
	/* Même au milieu d’une ligne
	   Mais n’en abusez pas non plus, ça alourdit pas mal le code */
}

/* Les commentaires servent à commenter,
   mais aussi à éliminer temporairement du code */

int resultat = 0;
for (int i = 0; i < TAILLE; i++) {
	// printf("%d ", tableau[i]);
	resultat += tableau[i];
}

/* Il y a des situations où vous voulez commenter
   des gros bouts de codes, comme une fonction entière si vous voulez
   la réécrire en gardant l’ancienne pour référence
   Sauf que s’il y a des commentaires en /* comme celui-ci dans la fonction,
   leur fin de commentaire */ va terminer le commentaire complet */
//                           /                                    \
//                  Tout ceci n’est pas dans le commentaire et est donc invalide

#if 0
Pour cela, vous pouvez éliminer ce bout de code avec le préprocesseur
Ça ne sera pas un vrai commentaire mais le préprocesseur l’éliminera
avant la compilation donc c’est tout comme
D’ailleurs une bonne coloration syntaxique comme ici l’affichera comme un commentaire

int somme(int* tableau, int taille) {
	int resultat = 0;
	/* Ceci est une boucle pour ajouter
	   chaque élément du tableau au résultat */
	for (int i = 0; i < taille; i++)
		resultat += tableau[i];
	return resultat;
}
#endif
```
;;;
