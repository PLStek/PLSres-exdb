//// title = "Pointeurs"
//// description = "Les pointeurs en C"

# {=title}

Un pointeur est : (choisissez la définition que vous comprenez le mieux)

-	Une variable qui **contient l’adresse mémoire** d’une autre
-	Une **référence** vers une autre variable
-	Une variable qui référence une case en mémoire

;;; code
```c/result/linenos
#include <stdio.h>

int changer_valeur(int x) {
	x = 2;
}

int changer_pointeur(int* x) {
	// Déréférencement : *x accède à la valeur référencée par le pointeur (pour la lire ou l’écrire)
	*x = 2;
}

int main() {
	int x = 5;
	printf("Début : %d\n", x);

	changer_valeur(x);
	printf("Après changer_valeur : %d\n", x);

	// L’opérateur & donne le pointeur sur la variable (donc son adresse)
	changer_pointeur(&x);
	printf("Après changer_pointeur : %d\n", x);

	return 0;
}
```
;;;

Un pointeur **référence** une valeur, donc l’action de récupérer la valeur pointée par un pointeur s’appelle le **déréférencement**.

Une variable de type **tableau** est implicitement un **pointeur** vers la zone mémoire contenant les éléments. Demander un tableau en argument est donc parfaitement équivalent à le demander comme un pointeur :

;;; example
```c
int somme(int tableau[], int taille);
int somme(int* tableau, int taille) {
	int resultat = 0;
	for (int i = 0; i < taille; i++)
		resultat += tableau[i];
	return resultat;
}
```
;;;

Donc `pointeur[2]` correspond à la valeur à l’adresse donnée par pointeur plus la taille de 2 éléments.

Si vous avez besoin qu’un pointeur soit **invalide** ou **vide**, ce qui arrive souvent, par exemple pour indiquer qu’une valeur est indéfinie, vous pouvez utiliser la constante **`NULL`**. Si vous déclarez un pointeur que vous n’initialisez pas immédiatement, c’est une bonne idée de **l’initialiser à `NULL`**. En cas d’erreur, déréférencer un pointeur nul crashera toujours le programme avec un comportement très identifiable (dans un débugger, vous verrez que le pointeur vaut `0`), alors qu’un pointeur non-initialisé peut pointer n’importe où en mémoire, y compris à des endroits qui ne crasheront pas immédiatement et peuvent causer des dysfonctionnement, vulnérabilités ou des comportements activement dangereux, et ça se verra beaucoup moins dans un debugger.

;;; example ```c
char* temp = NULL;```
;;;

Attention si vous voulez retourner un pointeur d’une fonction : **assurez-vous que la variable référencée sera toujours valide**. Mettons que vous tentez ceci :

;;; counterexample
```c
point2d_t* triangle_random() {
	point2d_t triangle[3] = {
		{.x = (float)rand() / RAND_MAX, .y = (float)rand() / RAND_MAX},
		{.x = (float)rand() / RAND_MAX, .y = (float)rand() / RAND_MAX},
		{.x = (float)rand() / RAND_MAX, .y = (float)rand() / RAND_MAX}};
	return triangle;
}
```
;;;

Vous allez **retourner l’adresse d’une variable locale**… qui sera **détruite** dès que la fonction se terminera. Le résultat sera inutilisable et crashera probablement votre programme si vous tentez de l’utiliser.

Un pointeur peut pointer sur n’importe quoi, y compris un autre pointeur : un pointeur sur pointeur aura alors deux étoiles (`int**`). On croise parfois cela quand on a besoin d’un pointeur sur un tableau, ou pour des tableaux multi-dimensions par exemple. Si un jour vous croyez avoir besoin d’aller plus loin (`int***`) en dehors des tableaux multi-dimensionnels, reconsidérez.

## Retourner plusieurs valeurs d’une fonction

Une fonction ne peut **retourner** qu’**une seule et unique valeur**. Vous pourriez plus ou moins contourner ça en retournant une structure, mais faire un type de structure exprès comme type de retour d’une seule fonction est une très mauvaise pratique. Pour ça, vous pouvez donner des **pointeurs comme arguments** de la fonction :

;;; example ```c
/** Lit une ligne `clé : valeur` d’un fichier dans les variables `key` et `value`
 *  Retourne 0 en cas de succès, un nombre négatif en cas d’échec */
int extract_line(FILE* stream, long* key, long* value) {
	char line[100];
	if (fgets(line, 100, stream) == NULL)
		return -1;

	while ((c = fgetc(stream)) != '\n' && c != EOF);

	char* value_start = strchr(line, ':') + 1;
	while (!isdigit(*value_start))
		value_start += 1;

	*key = strtol(line, NULL, 10);
	*value = strtol(value_start, NULL, 10);
	return 0;
}

int key, value;
if (extract_line(stream, &key, &value) < 0)
	ERROR("Failed to read a line");
printf("%d : %d\n", key, value);
```
;;;

Dans cet exemple, on a une fonction qui lit une ligne d’un fichier au format `clé : valeur`, donc qui doit retourner deux valeurs : la clé et la valeur. Pour ça, on fait passer des **pointeurs vers les variables qui vont accueillir les valeurs de retour**. La fonction modifie les variables pointées, elles seront alors utilisables dans la fonction appelante. Notez aussi qu’on fait retourner un **code d’erreur** à la fonction : la valeur de retour est un code qui sera négatif si la fonction échoue. Si vous faites ça, pensez bien à **documenter** à quoi correspondent les valeurs du code d’erreur.

Avant d’utiliser ça, réfléchissez avant. Dans beaucoup de situations, vous voulez retourner plusieurs valeurs parce que vous voulez faire plusieurs choses à la fois dans une même fonction. C’est une **très mauvaise pratique**. Pour être aussi générique que possible, une **fonction doit avoir un et un seul objectif**. Par exemple, vous pourriez être tenté de faire une fonction `int stats(int* tableau, int taille, double* moyenne, double ecarttype, double* q1, double* mediane, double* q3)`. Ça peut permettre de légères optimisations quand vous utilisez toujours toutes ces valeurs ensembles, si vraiment vous en êtes à ce point-là, mais en règle générale, ça ne fera qu’une seule fonction pour tout faire, résultat si vous avez besoin de la moyenne et de l’écart-type, ça gaspillera des ressources pour calculer les quartiles et la médiane qui ne servent à rien, et ça alourdira inutilement le code qui l’appelle vu qu’il faudra créer des variables poubelle pour les valeurs inutilisées. Il vaut mieux faire des fonctions individuelles pour chacun de ces calculs, pour rester plus générique, et ne pas mélanger autant de choses dans le code rendra le tout plus maintenable, plus lisible et mieux organisé.

En général, c’est une bonne pratique de ne **pas mélanger le code d’erreur avec les valeurs de retour** : soit vous faites `retour fonction(int* code_erreur)`, soit `code_erreur fonction(retour* var1, retour* var2)`, mais pas `retour* fonction(retour* var2, int* code_erreur)`. C’est plus clair si **toutes les valeurs de retour sont données de la même façon**, donc on évite d’en rendre une par la valeur de retour et d’autres par un pointeur en argument.

## L’arithmétique avec des pointeurs

En C, vous pouvez bricoler directement sur les pointeurs avec un peu d’arithmétique. Attention cependant : **c’est relativement dangereux**. Ça donne un peu plus de liberté, mais surtout la liberté de faire d’énormes boulettes. Assurez-vous toujours que vos pointeurs sont valides, qu’ils pointent toujours vers ce que vous pensez, de toujours faire des opérations qui ont du sens. C’est beaucoup moins propre et lisible que des syntaxes plus spécifiques comme `tableau[index]` plutôt que `*(tableau + index)`. Une erreur d’arithmétique sur pointeurs sera toujours catastrophique. Donc utilisez ça quand c’est pertinent et quand faire autrement serait encore pire.

;;; example
```c/result/wrapmain; includes=["stdio.h"]
int tableau[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
int* pointeur = &(tableau[0]);
printf("%d\n", *(pointeur + 3));
```
;;; doc
Additionner un pointeur et un nombre (ex. `ptr + 3`, `ptr + nb_elements`) donne le pointeur autant d’éléments plus loin. Donc dans le cas ci-dessus, `*(pointeur + 3)` donne la valeur 3 éléments = 3 entiers plus loin (vu que c’est un `int*`). Donc on additionne bien un nombre d’*éléments*, pas un nombre *d’octets*.
En gros, `*(pointeur + n)` correspond à `pointeur[n]`.
Ce type d’addition sert surtout à manipuler un pointeur pendant une boucle de façon plus complexe qu’avec un simple `for` avec un compteur. Par exemple, si on veut copier une chaîne de caractères en éliminant les espaces :
;;; example
```c/result/wrapmain; includes=["stdio.h"]
char chaine_base[50] = "Hello World !";
char resultat[50];

char* ptr_base = chaine_base;
char* ptr_resultat = resultat;
while (*ptr_base != '\0') {
	if (*ptr_base != ' ' && *ptr_base != '\t' && *ptr_base != '\n')
		*ptr_resultat++ = *ptr_base;
	ptr_base += 1;
}
*ptr_resultat = '\0';
printf("%s", resultat);
```
;;; doc
C’est pas forcément des plus lisibles, mais ici, on travaille avec les pointeurs plutôt que de garder des indices (notez que c’est pour l’exemple et que ça marche très bien avec des indices). À la ligne fatidique `*ptr_resultat++ = *ptr_base`, on atteint la ligne si le caractère doit être copié ; de là, la valeur pointée par `ptr_résultat`, donc la case actuelle de `resultat`, prend la valeur du caractère actuel de `chaine_base`, pointé par `ptr_base`. Ensuite, `ptr_resultat++` incrémente `ptr_resultat`, qui passe à l’élément suivant dans `resultat`.
Vous pouvez ainsi utiliser n’importe quel opérateur d’addition ou de soustraction entre un pointeur et un nombre entier : `pointeur + entier`, `pointeur++`, `++pointeur`, `pointeur += entier`, `pointeur - entier`, `pointeur--`, …. Notez bien qu’on parle d’additionner un pointeur avec un entier, additionner deux pointeurs n’a aucun sens.
;;;

;;; example
```c/result/wrapmain; includes=["stdio.h", "string.h"]
char chaine[] = "id:011A16";
int index_separateur = strchr(chaine, ':') - chaine;
printf("Index : %d\n", index_separateur);
```
;;; doc
Vous pouvez également **soustraire des pointeurs entre eux *s’ils pointent dans une même zone mémoire*** (dans un même tableau, une même structure).
Tout comme l’addition, la soustraction travaille sur les éléments et non sur des octets, donc ça renverra bien le nombre d’éléments entre les deux pointeurs (si c’est des `int*`, ça renverra le nombre de `int` entre les deux).
Par exemple, ci-dessus, `strchr` renvoie le pointeur vers la première occurence du caractère `':'` dans la chaîne, mais on veut son index — pour ça, il suffit de soustraire le pointeur sur le début du tableau (`chaine`) pour obtenir le nombre d’éléments entre les deux, donc l’index.
;;;

;;; example
```c/result/wrapmain; includes=["stdio.h", "string.h"]
char chaine[] = "id:011A16";
char titre[20];

char* separateur = strchr(chaine, ':');
char* pointeur = chaine;
int i = 0;
while (pointeur < separateur) {
	titre[i++] = *pointeur++;
}
titre[i] = '\0';
printf("Nom du champ : %s\n", titre);
```
;;; doc
Il est aussi possible de **comparer des pointeurs entre eux**.
Les opérateurs d’égalité `==` et d’inégalité `!=` sont toujours disponibles et fonctionnent comme on s’y attend, ça teste si les deux pointeurs pointent au même endroit ou pas.
Vous avez aussi accès aux opérateurs de comparaison `<`, `<=`, `>=`, `>` **si les deux pointeurs pointent dans la même zone mémoire** (dans un même tableau ou une même structure), sinon le résultat n’a aucun sens. Ça donnera alors si un pointeur est plus ou moins loin que l’autre dans la zone mémoire. Par exemple, ci-dessus la boucle continue tant que le pointeur de parcours n’a pas encore atteint le pointeur vers le caractère `':'`.
;;;

## Pointeurs sur type indéfini

Vous pouvez parfois (rarement si vous y réfléchissez) avoir besoin de pointeurs sur un type indéfini, autrement dit sur potentiellement n’importe quel type. Qu’on se le dise tout de suite : **dans 99% des cas c’est une mauvaise idée**. Les quelques fonctions de la bibliothèque standard qui en utilisent ont de très bonnes raisons de le faire, en général parce qu’elles définissent des opérations sur de la mémoire brute en assembleur.

En général, l’utilisation de mémoire brute est la seule utilisation vraiment 100% certaine de ce type de pointeurs. Si vous cherchez juste à bricoler des variables qui peuvent prendre différents types, regardez plutôt du côté des {> info.c.advanced.unions: unions}. Les pointeurs sont un nid à problèmes à la base, et les faire pointer sur quelque chose dont vous ne connaissez même pas le type en rajoute encore une bonne couche. De plus, ça détruit toute information de type pour les données pointées, il n’y a aucun moyen de connaître leur type réel, donc il faut vous assurer que votre gestion des types est parfaitement cohérente, sinon vous interpréterez mal les données pointées et ça pourrira toute la suite des opérations.

Bref, pour faire ça on utilise des *« pointeurs sur void »*, juste `void*` :

;;; code ```c
// Fonctions de la bibliothèque standard qui travaillent sur de la mémoire brute avec des void*
void* malloc(size_t taille);
int memcmp(const void* mem1, const void* mem2);

// qsort vous laisse interprétez vous-même vos éléments dans la fonction de comparaison,
// et ne les traite que par blocs de mémoire de la taille que vous donner,
// pour que ça marche avec n’importe quel type d’éléments.
// C’est un bon exemple de fonction qui utilise des void* pour être indépendant du type
void qsort(void* mem, size_t nb_elements, size_t taille_element, int (*comparateur)(const void*, const void*))```
;;;

Il y a quelques règles de base avec ces pointeurs :

- Un `void*` accepte n’importe quel type de pointeur, donc vous pouvez convertir n’importe quel pointeur en `void*` et donner n’importe quel type de pointeur à une fonction qui demande `void*`
- Un `void*` peut être converti en n’importe quel type de pointeur (donc peut se convertir de `n’importe quoi* -> void* -> n’importe quoi d’autre*`, d’où les gros problèmes si tout n’est pas parfaitement cohérent)
- Vous ne pouvez pas déréférencer un `void*`, vous devez le convertir en un vrai type avant toute utilisation.
