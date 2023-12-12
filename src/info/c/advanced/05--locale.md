//// title = "Localisation"
//// description = "L'internationalisation standard en C"

# {=title}

Par défaut, à peu près tout ce que vous faites en C utilise des paramètres linguistiques plus ou moins américains (en anglais, avec une présentation telle qu'on la trouverait aux US). Cependant, la librairie standard peut s'adapter et vous permettre de vous adapter à différents pays, langues et cultures internationales. Pour cela, on utilise ce qu'il y a dans le header `<locale.h>`.

## Localisation

Une *localisation* (*locale*) est un ensemble de paramètres qui définissent comment sont présentées les informations dans un pays ou une culture particulière. Par exemple, dans le monde anglo-saxon, on utilise des points pour les nombre décimaux, et les dates sont en format `mm/jj/aaaa`, alors que par chez nous on met des virgules et des dates en `jj/mm/aaaa`. Pour choisir une localisation, on utilise la fonction `setlocale`

;;; code ```c
char* setlocale(int mode, const char* locale)```
;;; doc
Change les paramètres de localisation

- `mode` indique quels paramètres changer
	- `LC_ALL` : Applique l'intégralité des paramètres de la localisation donnée
	- `LC_COLLATE` : Change la *collation*, c'est-à-dire l'ordre alphabétique utilisé pour le tri des chaînes de caractères par `strcoll` (voir ci-dessous). Par exemple, l'ordre alphabétique entre majuscules et minuscules, ou par rapport aux accents, ou juste pour les langues avec des systèmes d'écritures différents, n'est pas toujours le même selon les langues et les pays.
	- `LC_CTYPE` : Pour les classes de caractères et leur conversion
	- `LC_MONETARY` : Change le symbole de la monnaie locale
	- `LC_NUMERIC` : Règles d'écriture des nombres, dont le séparateur de décimales
	- `LC_TIME` : Formatage des dates et des heures
	- `LC_MESSAGES` : Change la langue des messages (comme les messages d'erreur par `perror` par exemple)
- `locale` est la chaîne de caractère identifiant la localisation (voir ci-dessous)

;;; example
```c/result
#include <stdio.h>
#include <locale.h>

int main() {
	printf("Par défaut  : %f\n", 12.34);

	char* locale = setlocale(LC_ALL, "");
	printf("\nLocalisation locale : %s\n", locale);
	printf("En français : %f\n", 12.34);
	perror("perror ");

}
```
;;;

Il existe 2 localisations imposées par le standard en C :

- `"C"` : La localisation par défaut de la bibliothèque standard, qui est plus ou moins américaine à part que les dates sont normales
- `""` (chaine vide) : Utilise les paramètres du système, définis par des variables d'environnement (c'est ça que vous voyez dans la localisation ci-dessus).

Vous aurez rarement besoin de plus que ça : ne changez rien pour garder vos paramètres par défaut, utilisez la localisation système en donnant une chaîne vide pour utiliser la localisation de l'utilisateur. Si le système de l'utilisateur ne définit pas sa localisation, vous n'êtes pas magicien.

Cela dit, vous pouvez parfois vouloir être plus précis et distinguer des localisations particulières, en particulier si vous traduisez votre programme dans plusieurs langues spécifiques.

;;; shell ```bash
~plstek$ # Ici sous Linux
~plstek$ # Localisation actuelle
~plstek$ locale
LANG=fr_CH.UTF-8
LANGUAGE=fr_CH
LC_CTYPE="fr_CH.UTF-8"
LC_NUMERIC=fr_FR.UTF-8
LC_TIME=fr_FR.UTF-8
LC_COLLATE="fr_CH.UTF-8"
LC_MONETARY=fr_FR.UTF-8
LC_MESSAGES="fr_CH.UTF-8"
LC_PAPER=fr_FR.UTF-8
LC_NAME=fr_FR.UTF-8
LC_ADDRESS=fr_FR.UTF-8
LC_TELEPHONE=fr_FR.UTF-8
LC_MEASUREMENT=fr_FR.UTF-8
LC_IDENTIFICATION=fr_FR.UTF-8
LC_ALL=
~plstek$ # Liste les localisations installées sous Linux
~plstek$ locale -a
C
C.UTF-8
en_AG
en_AG.utf8
en_AU.utf8
en_BW.utf8
en_CA.utf8
en_DK.utf8
en_GB.utf8
en_HK.utf8
en_IE.utf8
en_IL
en_IL.utf8
en_IN
en_IN.utf8
en_NG
en_NG.utf8
en_NZ.utf8
en_PH.utf8
en_SG.utf8
en_US.utf8
en_ZA.utf8
en_ZM
en_ZM.utf8
en_ZW.utf8
fr_BE.utf8
fr_CA.utf8
fr_CH.utf8
fr_FR.utf8
fr_LU.utf8
POSIX```
;;;

J'ai donc la localisation `C` par défaut, la localisation `POSIX` qui jusqu'à nouvel ordre est la même, vous remarquez `C.UTF-8` qui est pareil mais en UTF-8 plutôt qu'en pur ASCII, et surtout, toutes les autres sont pour des langues et pays spacifiques. En général, ça se présente sous la forme `ll_PP` avec `ll` la langue et `PP` le pays. Par exemple, `fr_FR` donne la localisation française de France, `fr_CA` donne la localisation française du Canada, et `en_CA` la localisation canadienne anglophone.

Si besoin, vous pouvez installer de nouvelles localisation. Toujours sous Linux :

;;; shell ```bash
~plstek$ sudo locale-gen de_DE
~plstek$ sudo locale-gen de_DE.UTF-8
~plstek$ sudo update-locale```
;;;

Désormais, vous avez accès à la localisation allemande (`de_DE`)

;;; example ```c/result/wrapmain; includes=["stdio.h", "locale.h"]
printf("Locale : %s\n", setlocale(LC_ALL, "de_DE"));```
;;;

## Utilité de la localisation

Diverses fonctions utilisent la localisation que vous appliquez.

- Les fonctions de texte formaté (familles de `printf` et `scanf`) sont localisées, notamment avec les séparateurs de décimales (par exemple, avec la localisation en français ça écrira `12,5`, et il faudra entrer `12,5` si `scanf` demande un `float`).
- Toujours avec les fonctions de la famille `printf`, vous avez le modificateur `'` pour mettre les séparateurs de milliers localisés (avec la localisation C par défaut, ça ne sert à rien). Par exemple `%d` -> 12345678, `%'d` -> 12 345 678).
- Dans la fonction de formatage de date et heure {> info.c.stdlib.time: `strftime`}, tous les formats qui peuvent dépendre de la langue ou du format de date local sont localisés (les noms des jours et des mois (`%a`, `%A`, `%b`, `%B`), le format de date et/ou heure complet `%c`, `%r`, `%x`, `%X`, et le nom de la timezone `%Z`)
- Sur les systèmes POSIX, vous avez éventuellement le header `<monetary.h>`, qui contient la fonction `strfmon` qui formate des valeurs monétaires en fonction de la localisation, voir ci-dessous.

;;; code ```c
int strcoll(const char* chaine1, const char* chaine2)```
;;; doc
Défini dans `string.h`.
Compare deux chaînes de caractères en fonction de la collation (ordre alphabétique local) appliquée (localisation appliquée avec le mode `LC_ALL` ou `LC_COLLATE`), contrairement à `strcmp` qui n'utilise que le code ASCII. Ça marche exactement comme `strcmp`, ça retourne 0 si les deux sont égales, un nombre **négatif** si `chaine1` est avant dans l'ordre alphabétique, et un nombre **positif** si `chaine2` passe avant.
C'est aussi un comparateur standard, donc vous pouvez vous en servir pour trier des chaînes de caractères avec `qsort`
;;; example ```c/result
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <locale.h>

int comparateur_strcmp(const void* str1, const void* str2) {
	return strcmp((const char*)str1, (const char*)str2);
}

int comparateur_strcoll(const void* str1, const void* str2) {
	return strcoll((const char*)str1, (const char*)str2);
}

void afficher_chaines(char* chaines[], int taille) {
	for (int i = 0; i < taille; i++)
		printf("%s ", chaines[i]);
	printf("\n");
}
int main() {
	char* chaines[] = {"notre", "nôtre", "Notre", "Nôtre"};

	setlocale(LC_COLLATE, "C.utf8");
	qsort(chaines, 4, sizeof(char*), comparateur_strcmp);
	printf("Localisation C, strcmp      : "); afficher_chaines(chaines, 4);
	qsort(chaines, 4, sizeof(char*), comparateur_strcoll);
	printf("Localisation C, strcoll     : "); afficher_chaines(chaines, 4);

	setlocale(LC_COLLATE, "fr_FR.utf8");
	qsort(chaines, 4, sizeof(char*), comparateur_strcmp);
	printf("Localisation fr_FR, strcmp  : "); afficher_chaines(chaines, 4);
	qsort(chaines, 4, sizeof(char*), comparateur_strcoll);
	printf("Localisation fr_FR, strcoll : "); afficher_chaines(chaines, 4);
}
```
;;; warning
En théorie, vous pouvez juste donner `strcmp` ou `strcoll` directement à `qsort`, le compilateur vous sortira des warnings parce que vous donnez des `void*` à une fonction qui prend des `char*`. Ça marche quand même, mais il vaut mieux faire ça proprement, c'est rapide.
;;;

;;; code ```c
ssize_t strfmon(char* buffer, size_t taille_max, const char* format, ...)```
;;; doc
Défini dans `<monetary.h>`, sur les systèmes compatibles POSIX
Formate une valeur monétaire selon la localisation actuelle. La fonction ressemble à `snprintf` :

- `buffer` : Chaîne de caractères où la valeur sera écrite
- `taille_max` : Nombre maximal de caractères à écrire, caractère nul non inclus (donc la taille du `buffer` - 1)
- `format` : Un format du même type que ceux de `printf`, mais avec d'autres caractères de formatage :
	- Une valeur monétaire sera insérée là où vous mettrez un format. À la base, ces formats sont `%n` pour le format national, et `%i` pour le format national. Utilisez `%%` pour écrire un vrai caractère `%`.
	- Entre le `%` et `n/i`, vous pouvez insérer un certain nombre de modificateurs :
		- `=f` : Caractère de remplissage, si vous spécifiez une taille de champ (ci-dessous), et que la valeur est plus petite, ça remplira avec le caractère que vous avez mis à la place du `f`
		- `^` : Ne pas faire de groupes de chiffres (milliers, typiquement)
		- `(` : Mettre les valeurs négatives entre parenthèses
		- `+` : Écrire les signes mathématiquement (du type `-100`), plutôt que comme la localisation l'impose
		- `!` : Ne pas écrire le symbole de la devise
		- `-` : Aligne à gauche (par défaut c'est aligné à droite)
	- Ensuite, vous pouvez éventuellement mettre une taille minimum pour le champ complet (valeur, décimales, symbole, signe, espaces, …). Si le champ complet est plus court, ça remplira avec des espaces à gauche
	- Ensuite, vous pouvez spécifier la largeur minimale de la partie entière (~~USD ~~**__12,345__**~~.34~~) avec `#` suivi de la largeur (ex. `#8`)
	- Ensuite, vous pouvez spécifier la largeur exacte de la partie décimale (point exclus), avec `.` suivi du nombre de décimales (ex. `.2`). Utilisez `.0` pour ne pas écrire de décimales du tout, par défaut ça prendra le nombre défini dans la locale.

Les arguments restants sont les valeurs monétaires à formater, sous forme de `double`. La fonction retourne le nombre de caractères réellement écrits (caractère nul exclus), ou `-1` si elle n'a pas pu tout écrire pour cause de dépassement.
;;; example ```c/result/wrapmain; linenos; linux; includes=["stdio.h", "locale.h", "monetary.h"]
setlocale(LC_MONETARY, "");
char buffer[100];
strfmon(buffer, 99, "%n", 1234.56);
printf("Ligne 3  : %s\n", buffer);
strfmon(buffer, 99, "%i", 1234.56);
printf("Ligne 5  : %s\n", buffer);
strfmon(buffer, 99, "%#6.3n", 1234.56);
printf("Ligne 7  : %s\n", buffer);
strfmon(buffer, 99, "%=.#8i", 1234.56);
printf("Ligne 9  : %s\n", buffer);
strfmon(buffer, 99, "%=.(-10n", -1234.56);
printf("Ligne 11 : %s\n", buffer);
strfmon(buffer, 99, "%^-#10n", 1234.56);
printf("Ligne 13 : %s\n", buffer);```
;;;

;;; code ```c
struct lconv* localeconv()```
;;; doc
Défini dans `locale.h`.
Renvoie un pointeur sur une structure `struct lconv`, qui contient les principales infos de localisation pour les utiliser manuellement.
Vous ne devez pas modifier le contenu de cette structure (c'est un comportement indéterminé)
Les membres de la structure sont les suivants. Notez que les `char*` sont des chaînes de caractères, sauf `grouping` qui est un tableau d'entiers terminé par un zéro, et les valeurs de type `char` sont juste des nombres, pas des caractères. Pour ces derniers, la valeur `CHAR_MAX` (définie dans `<limits.h>`) indique que la localisation ne permet pas cette fonctionnalité. Pour les valeurs monétaires (formatées avec `strfmon`), il y a un format locale (`%n`) et un format *international* (`%i`), qui ont des paramètres séparés ici (les noms commençant par `int_` sont pour le format international).

- `char* currency_symbol` : Symbole local de la monnaie (par exemple `$`, `€`, …)
- `char* decimal_point` : Séparateur de décimales des nombres (ex. `.` par défaut, `,` en français)
- `char* int_curr_symbol` : symbole international de la monnaie locale (en principe le code ISO-4217, par exemple `USD`, `EUR`, …)
- `char* mon_decimal_point` : Séparateur de décimales pour les valeurs monétaires
- `char* mon_thousands_sep` : Séparateur de milliers pour les valeurs monétaires
- `char* negative_sign` : Signe à utiliser pour les valeurs monétaires négatives
- `char* positive_sign` : Signe à utiliser pour les valeurs monétaires positives ou nulles
- `char* thousands_sep` : Séparateur de milliers, notamment utilisé par le format `%'d` et similaires par `printf`
- `char* grouping` : Règle de regroupement des milliers chiffres. C'est un tableau de nombres terminé par un 0 qui donnent le nombre de chiffres dans chaque groupe de droite à gauche. Le dernier élément avant le 0 concernera tous les groupes suivants. Par exemple, `{3, 0}` fait toujours regrouper par 3 chiffres, `{3, 2, 0}` fait un groupe de 3 à droite puis des groupes de 2 chiffres (`1 00 00 000`).
- `char* mon_grouping` : Même chose que `grouping`, mais pour les valeurs monétaires
- `char frac_digits` : Nombre de chiffres à conserver pour la partie décimale des valeurs monétaires
- `char n_cs_precedes` : Si ce champ vaut 1, le symbole de la devise doit être devant les valeurs négatives, s'il vaut 0 il doit être derrière
- `char n_sep_by_space` : Si ce champ vaut 1, le symbole de la devise doit être séparé des valeurs négatives par une espaces
- `char n_sign_posn` : Indique la position du signe (`+` / `-`) par rapport aux autres éléments pour les valeurs monétaires négatives :
	- `0` : Devant le reste, la valeur et le symbole de la devise sont entre parenthèses
	- `1` : Le signe est tout devant
	- `2` : Le signe est tout derrière
	- `3` : Le signe est juste devant le symbole de la devise
	- `4` : Le signe est juste derrière le symbole de la devise
- `char p_cs_precedes` : Si ce champ vaut 1, le symbole de la devise doit être devant les valeurs non-négatives, s'il vaut 0 il doit être derrière
- `char p_sep_by_space` : Si ce champ vaut 1, le symbole de la devise doit être séparé des valeurs non-négatives par une espace
- `char p_sign_posn` : Pareil que `n_sign_posn` pour les valeurs non-négatives
- `char int_frac_digits`, `char int_n_cs_precedes`, `char int_n_sep_by_space`, `char int_n_sign_posn`, `char int_p_cs_precedes`, `char int_p_sep_by_space`, `char int_p_sign_posn` : Équivalents de ces champs pour le format international
;;;
