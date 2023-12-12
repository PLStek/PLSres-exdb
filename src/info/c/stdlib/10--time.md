//// title = "#include <time.h>"
//// description = "La manipulation du temps en C avec le header time.h"

# {=title}

Le temps est un sujet (très) vaste et (très) compliqué, la librairie standard C offre quelques options pour le mesurer et le manipuler.

## Types

Le module définit plusieurs types pour stocker une information temporelle sous différentes formes :

- `time_t` : Représente une information temporelle sous forme d'un nombre, donc soustraire deux `time_t` a un sens. En théorie le sens réel du contenu de ce type est défini par l'implémentation, mais c'est très souvent un *timestamp UNIX* (même sous Windows), donc un nombre de secondes, écoulées depuis le 1er janvier 1970 à 00h00 UTC. Donc dans l'immense majorité des cas, vous pouvez soustraire deux `time_t` et vous aurez le nombre de secondes entre les deux. Si vraiment vous voulez être à 100% certain d'être parfaitement portable, il faudra faire la différence avec la fonction `difftime`, ou d'abord le convertir avec `localtime` ou `gmtime`, mais en général ça marche bien comme ça.
- `clock_t` : Autre type pour représenter une information temporelle, mais cette fois venant d'une **horloge système**, généralement beaucoup plus précise que le `time_t`, mais totalement dépendante du système et de l'implémentation. Du coup, n'utilisez pas sa valeur brute. C'est ce que retourne la fonction `clock()`.
	- Soustraire deux `clock_t` entre eux donnera le nombre de *ticks* d'horloge écoulés entre les deux, que vous pouvez convertir en une durée utile grâce à la constante `CLOCKS_PER_SEC` qui donne le nombre de *ticks* par seconde (`(double)(clock2 - clock1) / CLOCKS_PER_SEC` donne un nombre de seconde avec des décimales).
- `struct tm` : Structure contenant les informations sur un point du temps, avec toutes les informations calendaires pertinente. Vous pouvez convertir un `time_t` en `struct tm` avec `localtime` et `gmtime`, et reconstruire un `time_t` à partir d'une `struct tm` avec `mktime`. Ses champs sont les suivants :
	- `int tm_sec` : Nombre de secondes suivant la minute, dans l'intervalle [0, 60] (Si vous avez vraiment pas de bol, vous pouvez avoir un horaire du type 23:59:60 si vous tombez pile sur une [*leap second*](https://fr.wikipedia.org/wiki/Seconde_intercalaire), mais normalement ce n'est pas le genre de choses qui vous préoccuperont trop pour le moment)
	- `int tm_min` : Nombre de minutes suivant l'heure, dans l'intervalle [0, 59]
	- `int tm_hour` : Nombre d'heures suivant le jour, dans l'intervalle [0, 23]. 00h00 dénote bien la première minute du jour.
	- `int tm_mday` : Numéro du jour dans le mois, dans l'intervalle [1, 31]
	- `int tm_mon` : Numéro du mois dans l'année, dans l'intervalle [0, 11] (0 = janvier, 11 = décembre)
	- `int tm_year` : Nombre d'années **depuis 1900** (donc `1900 + temps->tm_year` pour la vraie année)
	- `int tm_wday` : Numéro du jour dans la semaine, dans l'intervalle [0, 6]. Ça suit la convention américaine, donc 0 est le **dimanche**, 6 le samedi.
	- `int tm_yday` : Numéro du jour dans l'année, dans l'intervalle [0, 365] (0 = 1er janvier, 364 = 31 décembre normal, 365 = 31 décembre dans une année bissextile)
	- `int tm_isdst` : Indique si c'est en *Daylight Saving Time*, **heure d'été** par chez nous, donc +1h par rapport à l'heure normale (d'hiver). Si `tm_isdst` vaut 0, on est à l'heure d'hiver, si c'est un nombre positif on est à l'heure d'été, et si c'est un nombre négatif l'information est indisponible.

## Mesurer le temps

Il y a deux façon de mesurer le temps : en `time_t` avec la fonction `time()`, ou en `clock_t` avec la fonction `clock()`

;;; code ```c
time_t time(time_t* timer)```
;;; doc
Retourne le temps actuel, en général sous forme d'un *timestamp UNIX*, donc le nombre de secondes depuis le 1er janvier 1970 00h00 UTC.
Vous pouvez éventuellement donner un pointeur sur un `time_t` en argument, la fonction y stockera la valeur retournée ; ou donner un pointeur `NULL`, ce qu'on fait généralement. Dans les deux cas, la fonction retourne le temps actuel.
;;; example
```c
char buffer1[10000] = {0};
char buffer2[10000] = {1};
char buffer3[10000];
time_t start = time(NULL);
for (int i = 0; i < 10000000; i++) {
	memcpy(buffer3, buffer1, 10000);
	memcpy(buffer3, buffer2, 10000);
}
time_t end = time(NULL);
printf("Temps d'exécution : %.1lf secondes\n", difftime(end, start));

// Temps d'exécution : 3.0 secondes
```
;;;

;;; code ```c
clock_t clock()```
;;; doc
Retourne le temps processeur consommé par le programme. C'est aussi une valeur entière, mais mesurée à partir d'un moment totalement défini par l'implémentation (c'est souvent quelque chose lié au programme, comme le moment du lancement, mais pas toujours), en intervalles définis par l'implémentation comme spécifié par la constante `CLOCKS_PER_SEC`, et en **temps processeur**, donc ce n'est pas en temps réel comme `time()`, c'est le temps activement utilisé par le programme seul. C'est donc beaucoup mieux pour mesurer un temps d'exécution.
;;; example ```c
char buffer1[10000] = {0};
char buffer2[10000] = {1};
char buffer3[10000];
clock_t start = clock();
for (int i = 0; i < 10000000; i++) {
	memcpy(buffer3, buffer1, 10000);
	memcpy(buffer3, buffer2, 10000);
}
clock_t end = clock();
printf("Précision de l'horloge : %lf secondes\n", (double)1.0 / CLOCKS_PER_SEC);
printf("Temps d'exécution : %lf\n", (double)(end - start) / CLOCKS_PER_SEC);

// Précision de l'horloge : 0.000001 secondes
// Temps d'exécution : 2.432179 secondes```
;;; warning
Cette horloge dépend totalement de l'implémentation, donc ne vous attendez pas à une précision particulière. Sur les systèmes POSIX, `CLOCKS_PER_SEC` vaudra toujours 1 000 000 (donc en théorie, une précision à la microseconde), mais les autres plateformes font ce qu'elles veulent. Et sur les plateformes POSIX, même si la *valeur* de l'horloge est en microsecondes, l'horloge peut s'incrémenter différemment (par exemple toutes les 100μs).
;;;

## Conversion et calculs

;;; code ```c
double difftime(time_t fin, time_t début)```
;;; doc
Calcule la différence entre deux `time_t`, et retourne la durée écoulée entre les deux en secondes. C'est mieux pour calculer des durées avec des `time_t`, vu que c'est parfaitement portable et que vous êtes certain de récupérer le résultat en secondes.
;;;

;;; code ```c
struct tm* localtime(const time_t* timer)```
;;; doc
Convertit un `time_t` en `struct tm*` à l'heure locale. La `struct tm` donnera l'heure locale chez l'utilisateur correspondant au moment donné. Notez bien que la fonction prend un pointeur sur un `time_t` et retourne un pointeur sur une `struct tm`.
;;; example ```c/result/wrapmain; includes=["stdio.h", "time.h"]
time_t moment = time(NULL);
struct tm* info = localtime(&moment);
printf("Au moment où cette page a été compilée, nous sommes le %d/%d/%d à %dh%d en France\n",
		info->tm_mday, info->tm_mon, info->tm_year + 1900, info->tm_hour, info->tm_min);```
;;; alert
Attention, il est possible que la valeur de retour soit un pointeur sur un **objet interne partagé**. Ça veut dire qu'un appel de `localtime` ou `gmtime` peut modifier une `struct tm` renvoyée préalablement. La `struct tm` est donc **invalidée au prochain appel de `localtime` ou `gmtime`**. Et vous ne pouvez pas juste la garder, rappeler `localtime` et vous servir de l'ancienne, vu que certaines implémentations peuvent faire autrement. Si vous voulez conserver les informations d'une `struct tm`, créez une `struct tm` à vous et copiez-y le contenu de la structure.
;;; example ```c
struct tm* temp = localtime(&moment);
struct tm conservée;
memcpy(&conservée, temp, sizeof(struct tm));```
;;;

;;; code ```c
struct tm* gmtime(const time_t* timer);```
;;; doc
Convertit un `time_t` en `struct tm*` contenant la date et l'heure UTC correspondant au moment donné, hors de toute considération de fuseau horaire et d'heure d'été. La fonction prend un pointeur sur le moment à convertir, et renvoie un pointeur sur une `struct tm`.
;;; example ```c/result/wrapmain; includes=["stdio.h", "time.h"]
time_t moment = time(NULL);
struct tm* info = gmtime(&moment);
printf("Au moment où cette page a été compilée, il est %d:%d:%d UTC\n",
		info->tm_hour, info->tm_min, info->tm_sec);```
;;; alert
Tout comme `localtime`, la valeur de retour peut être un pointeur sur un objet interne partagé, donc le prochain appel à `localtime` ou `gmtime` invalide l'objet renvoyé. Pour conserver les informations, créez une `struct tm` à vous et copiez-y les informations (voir l'exemple ci-dessus).
;;;

;;; code ```c
time_t mktime(struct tm* timeptr)```
;;; doc
Convertit un objet `struct tm`, facile à construire vous-même avec la date et l'heure voulue, en timestamp `time_t` plus opaque. Ça fait l'opération opposée de `localtime`, donc **ça part du principe que l'heure donnée est en heure locale chez l'utilisateur**.
Les valeurs des champs `tm_wday` (jour de la semaine) et `tm_yday` (jour de l'année) ne sont pas pris en compte pour la conversion.
Cette fonction **peut modifier le contenu de la structure donnée** : elle recalcule et remet en ordre les champs de la structure. Ça remet intelligemment les valeurs dans leur intervalle respectif, et ça recalcule correctement `tm_wday` et `tm_yday`. Donc en principe, vous pouvez juste donner un nombre de secondes et la date et `mktime` reconstruira l'heure correcte à partir de ça.
;;; example ```c/result/wrapmain; includes=["stdio.h", "time.h"]
struct tm info = {
	.tm_sec = 75, .tm_min = 59, .tm_hour = 14,
	.tm_mday = 34, .tm_mon = 1, .tm_year = 2022 - 1900,
	.tm_isdst = 0,
};
time_t timestamp = mktime(&info);

// Par exemple ici, mktime a corrigé 14h59 75s en 15h00 15s et le 34 février en 6 mars, et ça a calculé le jour de la semaine et de l'année
printf("%02d/%02d/%04d (jour %d de l'année) à %02d:%02d:%02d\n", info.tm_mday, info.tm_mon, info.tm_year + 1900, info.tm_yday, info.tm_hour, info.tm_min, info.tm_sec);
```
;;;

## Représentation

;;; code ```c
size_t strftime(char* destination, size_t taille_max, const char* format, const struct tm* timeinfo)```
;;; doc
Formate une structure `struct tm` (date et heure complète) en une chaîne de caractères selon un format. La fonction ressemble pas mal à `snprintf` sur le principe.
Cette fonction utilise la {> info.c.advanced.locale: localisation} pour les formats où la langue ou les notations locales s'appliquent, comme les noms des jours et des mois, les formats de dates locaux, …

- `destination` : tableau où sera écrite la chaîne de caractères
- `taille_max` : nombre maximal de caractères qui peuvent être écrits dans `destination`, caractère nul inclus (la taille de `destination`)
- `format` : Format de la date. C'est du même genre que les `printf`, avec les formats suivants :
	- `%S` : **Secondes**, alignées avec des zéros (00-60)
	- `%M` : **Minutes**, alignées avec des zéros (00-59)
	- **Heure** :
		- `%H` : Heure au format 24h, aligné avec des zéros (00-23)
		- `%I` : Heure au format 12h, aligné avec des zéros (01-12)
		- `%p` : Indicateur de demi-journée localisé (AM ou PM en anglais, ça n'existe pas en français)
	- **Timezone** :
		- `%Z` : Nom ou abréviation locale de la timezone (ex. CEST)
		- `%z` : Décalage horaire par rapport à l'UTC (ex UTC+2h -> +0200)
	- **Jour de la semaine** :
		- `%u` : Numéro ISO 8601 du jour de la semaine (1 = lundi, 7 = dimanche)
		- `%w` : Numéro du jour de la semaine d'après l'usage américain (0 = dimanche, 1 = lundi, 6 = samedi)
		- `%a` : Nom abrégé du jour de la semaine (ex. Sun, dim.)
		- `%A` : Nom complet du jour de la semaine (ex. Sunday, dimanche)
	- **Jour du mois** :
		- `%d` : Numéro du jour dans le mois, sur deux chiffres (2 -> 02, 23 ->_23)
		- `%e` : Numéro du jour dans le mois, aligné avec des espaces (2 -> " 2", 23 -> "23")
	- `%j` : Numéro du jour dans l'année, aligné avec des zéros (001 = 1er janvier, 365 = 31 décembre normal, 366 = 31 décembre dans une année bissextile)
	- **Semaine** :
		- `%V` : Numéro ISO 8601 de la semaine dans l'année (01-53). Pour ISO 8601, la semaine 01 est la première semaine de l'année qui contient le 4 janvier et le premier jeudi de l'année. La semaine précédente est la dernière semaine de l'année précédente (52 ou 53 selon l'année)
		- `%W` : Numéro de la semaine dans l'année d'après l'usage européen (00-53). La semaine 01 est la semaine qui commence le premier lundi de l'année. La fin de la semaine précédente (du 01/01 au dimanche suivant) est numérotée 00
		- `%U` : Numéro de la semaine dans l'année d'après l'usage américain (00-53). La semaine 01 est la semaine qui commence le premier dimanche de l'année. La fin de la semaine précédente (du 01/01 au samedi suivant) est numérotée 00
	- **Mois** :
		- `%m` : Numéro du mois, aligné avec des zéros (01 = janvier, 12 = décembre)
		- `%b` : Nom abrégé du mois (ex. Jul, juil.)
		- `%B` : Nom complet du mois (ex. July, juillet)
	- **Année** :
		- `%Y` : Numéro de l'année (ex. 2022)
		- `%y` : Les deux derniers chiffres du numéro de l'année (2022 -> 22)
		- `%G` : Année basée sur la semaine d'après ISO 8601 (la première semaine de l'année qui contient le 4 janvier et le premier jeudi de l'année, par exemple si on est le dimanche 2 janvier on considère que c'est une semaine de l'année précédente donc `%G` donnera l'année précédente)
		- `%g` : Comme `%G` mais ne donne que les deux derniers chiffres de l'année
	- `%C` : Année divisée par 100 et tronquée à l'entier inférieur (donc siècle + 1, ex. 2022 -> 20)
	- `%c` : Représentation locale de la **date et de l'heure** (ex. `Sun Jul  3 23:04:46 2022`, `dim. 03 juil. 2022 23:04:46`)
	- **Date complète** :
		- `%x` : Représentation locale de la date (ex. 07/17/22, 17/07/2022)
		- `%F` : Raccourci pour la représentation ISO 8601 de la date (aaaa-mm-jj), équivalent à `%Y-%m-%d`
		- `%D` : Raccourci pour la représentation américaine de la date (mm/jj/aa), équivalent à `%m/%d/%y`
	- **Heure complète** :
		- `%X` : Représentation locale de l'heure (ex. 23:42:51)
		- `%T` : Raccourci pour la représentation ISO 8601 de l'heure (HH:MM:SS), équivalent à `%H:%M:%S`
		- `%R` : Raccourci pour l'heure au format heure:minutes 24h, équivalent à `%H:%M` (ex. 23:28)
		- `%r` : Heure au format 12h local (ex. 11:26:03 PM, 11:26:03 en français)
	- **Autres** :
		- `%n` : Saut de ligne (`'\n'`)
		- `%t` : Tabulation ('`\t`')
		- `%%` : Vrai symbole `%`

Pour certaines localisations avec des langues, représentations et/ou systèmes d'écritures très différents (japonais, …), vous avez accès à des formats particuliers qui font l'équivalent des formats normaux mais dans la représentation du pays :

- `%Ec`, `%EC`, `%Ex`, `%EX`, `%Ey`, `%EY` donnent l'année dans le calendrier local
- `%Od`, `%Oe`, `%OH`, `%OI`, `%Om`, `%OM`, `%OS`, `%Ou`, `%OU`, `%OV`, `%Ow`, `%OW`, `%Oy` écrivent les nombres dans le système d'écriture local
;;; example ```c/result/wrapmain; locale; includes=["stdio.h", "time.h", "locale.h"]
char buffer[500];
time_t timestamp = time(NULL);
struct tm* info = localtime(&timestamp);

strftime(buffer, 500, "%A %d %B %Y (%x), %H:%M:%S UTC%z", info);
printf("%s\n", buffer);

setlocale(LC_ALL, "");  // Localisation de la machine de l'utilisateur, ici française
strftime(buffer, 500, "%A %d %B %Y (%x), %H:%M:%S UTC%z", info);
printf("%s\n", buffer);
```
;;; note
Sur les systèmes compatibles POSIX, il existe la fonction `char* strptime(const char* chaine, const char* format, struct tm* résultat)` pour parser une date écrite dans `chaine` vers `résultat` en fonction du `format`. Ça fait exactement l'inverse de `strftime`, avec les mêmes formats. Cette fonction n'est pas disponible sous Windows.
;;; warning
`strftime` ne recalcule pas tout, et utilise judicieusement les champs redondants de `struct tm` (`tm_wday`, `tm_yday`, …), donc s'ils ne sont pas calculés correctement, les résultats ne seront pas bons. Si vous avez modifié vous-même des champs de la structure, vous pouvez utiliser `mktime(&structure)` pour tout remettre en ordre avant de la donner à `strftime`.
;;;
