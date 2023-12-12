//// title = "Fonctions"
//// description = "Définition et utilisation de fonctions en C"

# {=title}

;;; code
```c/result/linenos
#include <stdio.h>
#include <ctype.h>

// Donne la version en majuscule d’une chaîne de caractères dans `sortie`
// La fonction est définie plus bas que son utilisation ou dans un fichier
// différent, donc il faut la déclarer avant avec un prototype
void majuscules(const char entree[], char sortie[]);

// Pas de valeur de retour, pas d’arguments
void print_source_file(void) {
	printf("%s\n", __FILE__);
}

// Prend un entier comme argument, et retourne un entier
int carre(int x) {
	return x*x;
}

// Prend un tableau et sa taille en argument, et le modifie sur place
void carre_tableau_sur_place(int tableau[], int taille) {
	for (int i = 0; i < taille; i++) {
		tableau[i] *= tableau[i];
	}
}

// Sur la plupart des systèmes, la fonction main prend comme paramètres le nombre d’arguments donné au programme en ligne de commandes (argc),
// et les arguments sous forme de tableau de chaînes de caractères (argv)
// Avec la plupart des compilateurs, si vous ne vous en servez pas, vous pouvez les omettre
int main(int argc, const char** argv) {
	char chaine_sortie[30];
	majuscules("test DE mise EN mAjUsCuLeS", chaine_sortie);
	printf("%s\n", chaine_sortie);
	return 0;  // Dans `main`, un code de retour de 0 est une fin normale, un code différent de 0 est un code d’erreur
}

// Prend une chaîne de caractères en argument, et met ses résultats dans la chaîne de caractères de sortie donnée
void majuscules(const char entree[], char sortie[]) {
	// On rappelle qu’une chaine de caractère est terminée par un caractère nul
	int i;
	for (i = 0; entree[i] != '\0'; i++) {
		 sortie[i] = toupper(entree[i]);
	}
	sortie[i] = '\0';  // Il faut bien terminer la chaîne qu’on remplit
}
```
;;;

Par défaut, les arguments des types de base sont passés par valeur, donc leur valeur est copiée : les modifier dans la fonction ne les modifiera pas dans la fonction appelante. Un **tableau** ne peut se passer comme argument que **par référence** : le modifier dans la fonction appelée le modifiera dans la fonction appelante. Pour interdire la modification du tableau, indiquez-le comme `const` dans la déclaration des arguments.

Il est **impossible de retrouver la taille d’un tableau**, donc pour passer un tableau comme argument, vous devez **donner sa taille** avec. Pas besoin pour une chaîne de caractères vu que la fin est déterminée par le caractère nul.

Pour des raisons historiques, c’est considéré comme une bonne pratique de mettre `void` quand une fonction ne prend pas d’argument (`int fonction (void);`), mais de nos jours ce n’est plus du tout nécessaire.

Pour pouvoir passer une chaîne de caractères littérale à une fonction (comme `majuscules("test", c)`), il faut impérativement que l’argument soit constant (`const char entree[]`), sinon il faudra la mettre dans une variable d’abord.

Depuis C99, il est aussi possible de donner des **tableau ou des structures littérales** à une fonction. Pour cela, mettez `(type){initialisation}` comme argument. Par exemple :

;;; example
```c/result/linenos; options=["-lm"]
#include <stdio.h>
#include <math.h>

typedef struct {
	double x, y;
} point_t;

int somme(int* valeurs, int taille) {
	int resultat = 0;
	for (int i = 0; i < taille; i++)
		resultat += valeurs[i];
	return resultat;
}

double distance(point_t p1, point_t p2) {
	return sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2));
}

int main() {
	int res_somme = somme((int[5]){2, 3, 5, 7, 11}, 5);
	double res_dist = distance((point_t){.x = 1.2, .y = -2.16},
	                           (point_t){.x = 4,   .y = 6.171});
	printf("Somme : %d, distance : %lf\n", res_somme, res_dist);
	return 0;
}
```
;;;
