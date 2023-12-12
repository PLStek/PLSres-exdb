//// title = "Gestion des erreurs"
//// description = "La gestion des erreurs en C"

# {=title}

Il y a plusieurs moyens de gérer les erreurs en C, et aucun de haut niveau comme vous pouvez en avoir dans d'autres langages (aka des exceptions). Il faut donc un peu de bidouille

## Quitter le programme

Jusque là rien de bien complexe : quand vous tombez sur une erreur irrécupérable, vous allez souvent afficher un message d'erreur et quitter (ou si vous êtes un sac, quitter sans message d'erreur, mais svp ne faites jamais ça).

Dans ces cas-là, trois choses qui peuvent faciliter le traitement par l'utilisateur :

- Rendre le message d'erreur le plus descriptif possible ("Le fichier `fichier.dat` n'existe pas ou n'a pas pu être ouvert" est mieux que "Échec d'ouverture du fichier")
- Écrire les messages d'erreur sur `stderr` et non `stdout`, ça aide à séparer les erreurs des vrais résultats quand on veut logger
- Quitter avec un code d'erreur, donc différent de zéro

;;; example ```c
FILE* fichier = fopen(nom_fichier, "rb");
if (fichier == NULL) {
	fprintf(stderr, "ERREUR : Le fichier `%s` n'existe pas ou n'a pas pu être ouvert\n", nom_fichier);
	exit(EXIT_FAILURE);  // Ou un autre nombre supérieur à 0 si vous voulez faire des codes d'erreurs plus spécifiques
}```
;;;

Vous pouvez, très éventuellement, vous amuser à utiliser `abort()`, sauf que ça fera littéralement comme si le système avait crashé le programme, donc ça ne nettoie rien et ça sera considéré comme un crash forcé par le système. Il vaut mieux faire ça proprement avec `exit()`.

## Errno

Quand une fonction de la librairie standard échoue, elle va souvent vous signifier explicitement qu'elle a échoué (par une valeur particulière de la valeur de retour par exemple, pour ça référez-vous à la doc). En plus de ça, pour un peu plus de précision, elle va souvent écrire une valeur particulière dans ce qu'on appelle *`errno`* (error n°).

`errno` est une variable globale définie dans `<errno.h>`, qui peut être modifiée n'importe où et n'importe quand dans un programme, et qui peut contenir des codes d'erreur eux aussi définis dans `<errno.h>`. Le standard C n'impose que très peu de valeurs :

- `EDOM` : Erreur de domaine mathématique (par exemple donner un nombre négatif à une fonction logarithme, …)
- `ERANGE` : Un argument est trop grand pour que le résultat soit correct ou significatif
- `EILSEQ` : Séquence d'octets invalide dans une chaîne de caractères à encodage multi-octets

Cependant, les différentes implémentations de la bibliothèque standard donnent généralement beaucoup plus de codes d'erreurs, dont vous pouvez trouver des listes [ici pour les systèmes compatibles POSIX](https://en.cppreference.com/w/cpp/error/errno_macros) (Linux, OSX, Android, iOS, UNIX-like divers) [ici chez Microsoft](https://docs.microsoft.com/en-us/cpp/c-runtime-library/errno-constants?view=msvc-170), et potentiellement encore d'autres selon les implémentations spécifiques et les versions. Ça rend le tout un peu pénible à utiliser vous-même, vu que traiter les codes d'erreurs directement sera moyennement portable. Cela dit, les fonctions `perror` et `strerror` permettent de gérer ça facilement.

### Les fonctions perror et strerror

Ces deux fonctions donnent un message d'erreur lisible en fonction de la valeur actuelle de `errno`.

;;; code ```c
void perror(const char* intro)```
;;; doc
Défini dans `stdio.h`
Écrit un message d'erreur sur `stderr` en fonction du code d'erreur dans `errno`.

- `intro` permet de donner un message à écrire avant la description de l'erreur elle-même. `perror` insèrera automatiquement un `:` entre votre intro et le message d'erreur.
;;; example ```c/result/wrapmain; includes=["stdio.h", "stdlib.h"]
FILE* fichier = fopen("jexiste.pas", "r");
if (fichier == NULL) {
	perror("ERREUR à l'ouverture du fichier `jexiste.pas` ");
	exit(EXIT_FAILURE);
}```
;;;

;;; code ```c
char* strerror(int errno);```
;;; doc
Défini dans `string.h`
Donne la description d'un code d'erreur. L'argument est la valeur de `errno` dont vous voulez le message d'erreur.
;;; example ```c/result/wrapmain; includes=["stdio.h", "string.h", "errno.h"]
if (fprintf(stdin, "Message associé au code EOWNERDEAD : %s\n", strerror(EOWNERDEAD)) < 0) {
	fprintf(stderr, "Écrire sur stdin n'a pas marché : %s\n", strerror(errno));
}```
;;;

En principe, ça donnera des messages dans la langue choisie si vous changez la {> info.c.advanced.locale: localisation}.
