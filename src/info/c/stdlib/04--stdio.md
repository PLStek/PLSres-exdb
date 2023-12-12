//// title = "#include <stdio.h>"
//// description = "Description du contenu du header standard stdio.h"

# {=title}

Interaction avec les flux standard et les fichiers.

## Définitions génériques
### Types

- **`FILE*`** : Objet opaque définissant un accès à un fichier. Le type réel est totalement dépendant de l’implémentation et du système, et pourrait être virtuellement n’importe quoi, donc n’essayez pas de l’utiliser autrement que via les fonctions de `stdio.h`.

### Constantes

- **`EOF`** : *End-Of-File*, valeur retournée par certaines fonctions pour signifier qu’elles ont atteint la fin du fichier.
- **`FILENAME_MAX`** : Définit la taille maximale d’un nom de fichier si elle existe, autrement une taille de tableau recommandée pour contenir un nom de fichier.
- **`FILE* stdin`** : **Flux d’entrée standard**, en lecture seule, typiquement l’entrée utilisateur dans la console ou la sortie de la commande précédente si vous utilisez des pipes en ligne de commande `(cmd1 | myprogram)`
- **`FILE* stdout`** : **Flux de sortie standard**, en écriture seule, typiquement la console ou la commande suivante si vous utilisez des pipes en ligne de commande `(myprogram | cmd2)`
- **`FILE* stderr`** : **Flux d’erreur standard**, en écriture seule, fonctionne par défaut comme `stdout`, mais il est possible de le rediriger à part, par exemple pour séparer les avertissements et le vrai résultat du programme

Vous noterez que les **flux standards** sont de type `FILE*`, donc vous pouvez les utiliser de façon **presque identique** à n’importe quels autres fichiers.

## Fonctionnement des fichiers //// fileuse

Les **fichiers** (ou **flux**, ***stream*** pour être plus générique), ont un fonctionnement un peu particulier qu’il faut comprendre pour bien les utiliser.

Quand on parle de « fichier » en C, ça correspond à n’importe quoi qui se comporte comme un fichier, ce qui inclut notamment les flux standard `stdin`, `stdout` et `stderr`. Ils fonctionnent donc de manière presque identique à n’importe quel autre fichier.

Un fichier peut être **ouvert** en **lecture**, **écriture**, ou les deux (selon le paramètre `mode` donné à `fopen`). On peut aussi dire « entrée » pour la lecture (les données entrent dans votre programme), et « sortie » pour l’écriture. `stdin` est ouvert en lecture, `stdout` et `stderr` en écriture. Vous ne pouvez faire que ce qui est permis par le mode d’ouverture (n’essayez pas d’écrire dans `stdin`, donc).

Dans le fichier, vous avez un curseur, qui pointe la position où vous vous situez dans le fichier. Quand vous lisez `n` caractères du fichier, vous avancez le curseur de `n` caractères, donc la prochaine lecture lira à la suite. Idem pour l’écriture. Vous pouvez éventuellement récupérer la position de ce curseur avec `fgetpos` ou `ftell`, et le déplacer manuellement avec `rewind`, `fsetpos` et `fseek` — mais pas dans les flux standard parce qu’ils ne sont pas des fichiers normaux, ils ne sont pas *seekable*.

Pour optimiser un peu les choses, le fichier n’est pas lu ou écrit caractère par caractère à la demande depuis le disque. En interne, chaque fichier a un buffer, toutes les lectures et écritures se feront d’abord dans ce buffer en mémoire, et ne seront reportées sur le disque que quand vous êtes arrivé au bout du buffer (quand vous lisez plus loin que le buffer de lecture, la suite du fichier sera lue depuis le disque ; quand vous avez rempli le buffer d’écriture il est écrit sur le disque puis vidé). Ça permet de faire ces opérations sur le disque par bloc, donc moins fréquemment, donc de façon plus efficace car l’accès au disque est lent par rapport à la mémoire.

Ça veut dire qu’une opération d’écriture ne sera pas toujours répercutée dans le fichier immédiatement. Si vous avez besoin de forcer l’écriture immédiatement, vous pouvez utiliser `fflush()`. Les opérations seront toujours répercutées sur le disque au moment de fermer le fichier.

Ça fait aussi que `stdin` a un buffer, si vous ne lisez pas tout ce que l’utilisateur a écrit dedans, le reste sera toujours disponible dans le buffer pour la prochaine fois que vous lirez.

## Entrée-sortie formatée

### Formats

Toutes les fonctions suivantes utilisent les mêmes formats. Un format pour une valeur aura toujours la forme `%[options][taille][.précision][longueur]type`.

**Options** :

* `-` : Aligne à gauche (par défaut c’est aligné à droite)
* `+` : Force à donner le signe, positif ou négatif (par défaut il n’est précisé que pour les nombres négatifs)
* `(espace)` : Met un espace à la place du signe pour les nombres positifs
* `#` : Pour un nombre flottant, force à mettre un point même sans décimales ; pour un nombre hexadécimal, ajoute le préfixe 0x devant le nombre
* `0` : Remplit l’espace vide avec des 0 au lieu d’espaces

**Taille** :

- `(nombre)` : longueur minimale du champ, si la valeur est plus courte, elle sera alignée avec des espaces (ou des zéros avec l’option 0) ; mais si elle est plus longue elle ne sera pas raccourcie
- `*` : La longueur est donnée par l’argument précédent : (5, 210) ⟶ 00210
**Précision** :
- `.(nombre)` : nombre maximal de décimales du nombre flottant à écrire
- `.*` : La précision est donnée par l’argument précédent : (3, 1.23456) ⟶ 1.234
**Longueur** :
- `h` : `short` (`hd` = `short`, `hu` = `unsigned short`)
- `l` : `long` (`ld` = `long`, `lld` = `long long`, `lu` = `unsigned long`, `llu` = `unsigned long long`, `lf` = `double`)
**Type** :
- `c` : `char` (en tant que caractère)
- `d` : entier signé (`d` = `int`, hd = `short`, ld = `long`, lld = `long long`)
- `u` : entier non signé (`u` = `unsigned int`, `hu` = `unsigned short`, `lu` = `unsigned long`, `llu` = `unsigned long long`)
- `f` : nombre flottant (`f` = `float`, `lf` = `double`)
- `s` : chaîne de caractères
- `e` : nombre flottant en notation scientifique (`E` pour un E majuscule)
- `g` : nombre flottant avec la représentation la plus courte entre `f` et `e` (normal / scientifique)
- `x` : entier non signé en notation hexadécimale (`X` pour les lettres majuscules)
- `p` : adresse mémoire (pour afficher un pointeur)
Vous pouvez utiliser `%%` pour avoir un vrai caractère `'%'`

;;; example
```c/result/includes=["stdio.h"]
int main() {
    short hd_pos = 456;
    short hd_neg = -176;
    printf(" 1 - |%s|\n", "test");
    printf(" 2 - |%hd|\n", hd_pos);
    printf(" 3 - |%hd|\n", hd_neg);
    printf(" 4 - |%+hd|\n", hd_pos);
    printf(" 5 - |% hd|\n", hd_pos);
    printf(" 6 - |%04hd|\n", hd_pos);
    printf(" 7 - |%04hd|\n", hd_neg);
    printf(" 8 - |%-5hd|\n", hd_pos);
    printf(" 9 - |%.3f|\n", 4.166853);
    printf("10 - |%+.*f|\n", 3, 4.1);
    printf("11 - |%04hx|\n", hd_pos);
}
```
;;;

### Fonction d’écriture formatée

;;; code ```c
int printf(const char* format, ...)```
;;; doc
**Écrit** du **texte formaté** sur la **sortie standard**

- `format` : chaîne de formatage utilisant les codes ci-dessus
- Les arguments suivants sont les valeurs à insérer dans le texte formaté, dans l’ordre des codes dans le `format`

Retourne le nombre de caractères réellement écrits, ou un nombre négatif en cas d’échec
;;; example
```c/result/wrapmain; includes=["stdio.h", "stdlib.h"]
const char nom[] = "Dupont";
int age = 46;
float prix_commande = 112.45;
printf("Nom : %s\n\tAge : %d\n\tPrix de la commande : %.2f\n", nom, age, prix_commande);
```
;;;

;;; code ```c
int fprintf(FILE* fichier, const char* format, ...)```
;;; doc
**Écrit** du **texte formaté** dans un **fichier**

- `fichier` : fichier (ou tout flux de sortie comme `stdout` et `stderr`) où écrire
- `format` : chaîne de formatage utilisant les codes ci-dessus
- Les arguments suivants sont les valeurs à insérer dans le texte formaté, dans l’ordre

Retourne le nombre de caractères réellement écrits, ou un nombre négatif en cas d’échec
;;; example
```c
fprintf(stderr, "ERROR : You fucked up %d times\n", fuckup_count);
```
;;;

;;; code ```c
int sprintf(char* resultat, const char* format, ...)```
;;; doc
**Écrit** du **texte formaté** dans une **chaîne de caractères**

-	`resultat` : chaîne de caractères où écrire le texte formaté (plus un caractère nul)
-	`format` : chaîne de formatage utilisant les codes ci-dessus
-	Les arguments suivants sont les valeurs à insérer dans le texte formaté, dans l’ordre

Retourne le nombre de caractères réellement écrits (caractère nul non inclus), ou un nombre négatif en cas d’échec
;;; example
```c/result/wrapmain; includes=["stdio.h"]
unsigned int id = 10012577;
char ligne[80];
sprintf(ligne, "%08u,%s\n", id, "Bureau RODULF");
puts(ligne);
```
;;; warning
Cette fonction ne vérifie pas la taille du tableau `résultat`, donc soyez sûr qu’il est assez grand pour contenir le texte formaté. Si vous pouvez, utilisez plutôt `snprintf()`
;;;

;;; code ```c
int snprintf(char* resultat, size_t taille_buffer, const char* format, ...)```
;;; doc
**Écrit** du **texte formaté** dans une **chaîne de caractères**, en **vérifiant la taille** du tableau `résultat`

-	`resultat` : chaîne de caractères où écrire le texte formaté (plus un caractère nul)
-	`taille_buffer` : nombre maximal de caractères à écrire dans `resultat` (caractère nul inclus)
-	`format` : chaîne de formatage utilisant les codes ci-dessus
-	Les arguments suivants sont les valeurs à insérer dans le texte formaté, dans l’ordre

Retourne le nombre de caractères écrits (caractère nul non inclus, donne le nombre de caractères qui auraient dû être écrit même si ça a été tronqué à moins), ou un nombre négatif en cas d’échec.
Cette fonction tronque le texte à `taille_buffer – 1` s’il dépasse cette taille, pour respecter la taille indiquée et bien ajouter un caractère nul à la fin.
;;; example
```c/result/wrapmain; includes=["stdio.h"]
unsigned int id = 10012577;
char ligne[12];
snprintf(ligne, 12, "%08u,%s\n", id, "Bureau RODULF");
puts(ligne);
```
;;; warning
Cette fonction est standard depuis C99, mais **Microsoft refuse d’implémenter** complètement le standard C99 donc ça ne **marchera pas avec MSVC** (Visual Studio). Sur cette implémentation il existe la fonction `sprintf_s`, qui a la même signature et la même utilité mais qui ne gère pas les dépassements correctement (pas de caractère nul à la fin, retourne `-1` même en cas de simple dépassement).

Dans **MinGW**, avant la version 8.0.0 (septembre 2020), `snprintf` utilisait aussi `sprintf_s`, depuis cette version ils ont remplacé l’implémentation de Microsoft pour respecter le standard donc avec une version récente c’est bon.

Donc faites attention avec cette fonction si vous devez pouvoir compiler **sous Windows**.
;;;

### Fonctions de lecture formatée

;;; code ```c
int scanf(const char* format, ...)```
;;; doc
**Lit** des **valeurs formatées** depuis l’**entrée standard**

-	`format` : chaîne de formatage utilisant les codes décrits plus haut (seuls les définitions de type sont supportées)
-	Les arguments suivants sont les pointeurs vers les variables où écrire les valeurs décodées, dans l’ordre

Retourne le nombre d’éléments réellement lus (moins que le nombre d’éléments attendus si certains n’étaient pas bien formatés), ou `EOF` en cas d’échec
;;; example
```c/result/wrapmain; includes=["stdio.h"]; stdin="8\n12"
int x, y;
printf("Entrez le premier nombre à additionner :\n");
scanf("%d", &x);
printf("Entrez le deuxième nombre à additionner :\n");
scanf("%d", &y);
printf("%d + %d = %d\n", x, y, x+y);
```
;;; note
En théorie vous pouvez mettre le format que vous voulez et autant de valeurs que vous voulez, mais quand on demande des choses à l’utilisateur, on préfère rendre ça aussi évident que possible
;;; warning
`scanf` coupe les éléments aux espaces (y compris les chaînes de caractères avec `%s`)
;;; alert
`scanf("%s")` ne **vérifie pas la taille du tableau**, une entrée utilisateur trop longue en **dépassera** donc : un utilisateur mal informé pourra donc planter le programme sans raison apparente, et un utilisateur malveillant pourra facilement en corrompre la mémoire. **Utilisez plutôt fgets()** pour récupérer des chaînes de caractères de l’utilisateur.
Si vous tenez absolument à quelque chose de formaté d’une certaine manière avec une chaîne de caractères (ce qu’il est généralement une **très mauvaise idée** de demander à l’utilisateur), `scanf("%30s")` avec la taille maximale de la chaîne tronquera si ça va trop loin, cependant le reste traînera dans le buffer pour la suite du format donc un problème ici fera probablement échouer tout le reste, et en plus ça coupe aux espaces ce qui est pas toujours ce qu’on attend d’une chaîne de caractères (et pareil, s’il y a un espace pas prévu, le reste traînera dans le buffer).
;;;

;;; code ```c
int fscanf(FILE* fichier, const char* format, ...)```
;;; doc
**Lit** des **valeurs formatées** depuis un **fichier** ouvert en lecture (`stdin` inclus)

- `fichier` : fichier où lire du texte
- `format` : chaîne de formatage utilisant les codes décrits plus haut (seuls les définitions de type sont supportées)
- Les arguments suivants sont les pointeurs vers les variables où écrire les valeurs décodées, dans l’ordre

Retourne le nombre d’éléments réellement lus, ou `EOF` en cas d’échec
;;; example
```c/result/wrapmain; includes=["stdio.h"]; joinfiles=[("nombre.txt", "6 9\n")]
int x, y;
FILE* fichier = fopen("nombre.txt", "r");
fscanf(fichier, "%d %d", &x, &y);
printf("%d + %d = %d\n", x, y, x+y);
fclose(fichier);
```
;;; alert
Même si c’est moins sensible aux simples utilisateurs naïfs, lire des chaînes de caractères depuis un fichier avec `fscanf` est tout aussi sensible aux exploitations malveillantes, à moins d’utiliser `%50s` qui fera rater toute la suite si ça dépasse. **Utilisez plutôt `fgets()` pour lire des chaînes de caractères**.
;;;

;;; code ```c
int sscanf(const char* texte, const char* format, ...)```
;;; doc
**Lit** des **valeurs formatées** depuis une **chaîne de caractères**

- `texte` : texte formaté à décoder
- `format` : chaîne de formatage utilisant les codes décrits plus haut

- Les arguments suivants sont les pointeurs vers les variables où écrire les valeurs décodées, dans l’ordre
Retourne le nombre d’éléments réellement lus, ou `EOF` en cas d’échec
;;; example
```c/result/wrapmain; includes=["stdio.h"]
int x, y;
sscanf("10 15", "%d %d", &x, &y);
printf("%d + %d = %d\n", x, y, x+y);
```
;;; alert
À moins que le texte de base ne soit jamais sorti de votre programme, c’est toujours aussi dangereux de lire des `%s` avec les fonctions `scanf`. Utilisez plutôt les fonctions de manipulations de chaînes de caractères si possible.
;;;

## Entrée-sortie texte non formatée
### Fonctions d’écriture non formatée

;;; code ```c
int putchar(char caractère)```
;;; doc
**Écrit** un **caractère** sur l’**entrée standard**

-	`caractère` : caractère à écrire

Retourne soit le caractère écrit, soit `EOF` en cas d’erreur
;;; example
```c/result/wrapmain; includes=["stdio.h"]
for (char c = 'A'; c <= 'Z'; c++)
	putchar(c);
```
;;;

;;; code ```c
int putc(char caractère, FILE* fichier)
int fputc(char caractère, FILE* fichier)
```
;;; doc
**Écrit un caractère** dans un **fichier** ouvert en écriture (dont `stdout` et `stderr`)

- `caractère` : caractère à écrire
- `fichier` : fichier où écrire
Retourne soit le caractère écrit, soit `EOF` en cas d’erreur
;;; example
```c/result/wrapmain; includes=["stdio.h"]
for (char c = 'A'; c <= 'Z'; c++)
    fputc(c, stderr);
```
;;; warning
Les deux fonctions ont le même effet, mais pour des raisons historiques `putc` peut être implémenté comme une macro et évaluer plusieurs fois le paramètre `fichier`, ce qui posera problème si ce n’est pas une simple variable. Il vaut donc mieux utiliser `fputc` à moins de savoir ce que vous faites.
;;;

;;; code ```c
int puts(const char* chaine)```
;;; doc
**Écrit** une **chaîne de caractère** sur la **sortie standard**, puis ajoute un **saut de ligne**

- `chaine` : chaîne de caractère à écrire

Retourne `EOF` en cas d’échec, autrement une valeur positive indéterminée
;;; example
```c/result/wrapmain; includes=["stdio.h"]
puts("Bonjour !");
puts("Au revoir !");
```
;;;

;;; code ```c
int fputs(const char* chaine, FILE* fichier)```
;;; doc
**Écrit** une **chaîne de caractère** dans un **fichier** ouvert en écriture (incluant `stdout` et `stderr`), **sans ajouter de saut de ligne** contrairement à `puts`

- `chaine` : chaîne de caractère à écrire
- `fichier` : fichier où écrire la chaîne de caractères

Retourne `EOF` en cas d’échec, autrement une valeur positive indéterminée
;;; example
```c/result/wrapmain; includes=["stdio.h"]
const char errmessage[] = "Quelque chose a foiré\n";
fputs("ERREUR : ", stderr);
fputs(errmessage, stderr);
```
;;;

### Fonctions de lecture non formatée

;;; code ```c
int getchar(void)```
;;; doc
**Lit** un **caractère** de l’**entrée standard**, ou `EOF` en cas d’échec.
;;; example
```c/result/wrapmain; includes=["stdio.h"]; stdin="Test\n"
char c;
while ((c = getchar()) != EOF && c != '\n') {
    putchar(c);
    putchar(' ');
}
putchar('\n');
```
;;;

;;; code ```c
int getc(FILE* fichier)
int fgetc(FILE* fichier)
```
;;; doc
**Lit** un **caractère** d’un **fichier** ouvert en lecture (incluant `stdin`), ou `EOF` s’il n’y a plus de caractères à lire.
;;; example
```c/result/wrapmain; includes=["stdio.h"]; joinfiles=[("texte.txt", "Un Grand Et Long Titre Avec Plein De Majuscules\n")]
FILE* fichier = fopen("texte.txt", "r");
int num_majuscules = 0;
char c;
while ((c = fgetc(fichier)) != EOF) {
    if ('A' <= c && c <= 'Z')
        num_majuscules += 1;
}
fclose(fichier);
printf("%d majuscules dans le fichier\n", num_majuscules);
```
;;; warning
Les deux fonctions ont le même effet, mais pour des raisons historiques `getc` peut être implémenté comme une macro et évaluer plusieurs fois le paramètre `fichier`, ce qui posera problème si ce n’est pas une simple variable. Il vaut donc mieux utiliser `fgetc` à moins de savoir ce que vous faites.
;;;

;;; code ```c
char* fgets(char* chaine, int taille_tableau, FILE* fichier)```
;;; doc
**Lit** une **ligne** d’un **fichier** ouvert en lecture (incluant `stdin`), en **vérifiant la taille** du tableau.

- `chaine` : chaîne de caractère où écrire la ligne lue
- `taille_tableau` : taille du tableau chaine (la chaîne de caractères peut donc aller jusqu’à `taille_tableau – 1`, pour compter le caractère nul
- `fichier` : fichier d’où lire la ligne

Retourne `chaine`, ou `NULL` en cas d’échec

La lecture s’arrête à la première condition qui arrive entre un **saut de ligne**, la **fin du fichier** ou le **dépassement** de `taille_tableau`.

- Si la lecture s’arrête à un **saut de ligne**, le saut de ligne sera **laissé** dans la chaîne de caractères
- Si la lecture s’arrête à la **fin du fichier**, il n’y aura **pas de saut de ligne** à la fin de la chaine (à moins bien sûr que le fichier se termine par un saut de ligne)
- Si la lecture s’arrête pour un **dépassement**, il n’y aura **pas de saut de ligne** non plus, et le reste de la ligne **restera** pour la prochaine fois où vous lirez dans le fichier.
;;; example
```c
#define TAILLE_CHAINE 10

char chaine[TAILLE_CHAINE];
fgets(chaine, TAILLE_CHAINE, stdin);
int position_saut_ligne = strcspn(chaine, "\n");
// S’il y a un saut de ligne dans la chaîne de caractères,
// c’est que la lecture s’est arrêtée à la fin de la ligne,
// donc on peut supprimer le saut de ligne en terminant la chaîne
// à la position du saut de ligne (toujours en dernier)
if (chaine[position_saut_ligne] != '\0') {
    chaine[position_saut_ligne] = '\0';
}
// S’il n’y a pas de saut de ligne, c’est qu’on est soit arrivé
// au bout du fichier, soit qu’on a dépassé la taille maximale
else {
    // On peut supprimer le reste de la ligne qui traîne dans le buffer
    char c;
    while ((c = getchar()) != '\n' && c != EOF);
}
```
;;; example
```c
// Si on veut juste virer le saut de ligne, on peut raccourcir :
chaine[strcspn(chaine, "\n")] = '\0';
```
;;; note
Cette fonction est la seule qui permet de récupérer une chaîne de caractères entrée par l’utilisateur de façon parfaitement maîtrisée. Ça peut être intéressant de vous faire une fonction pour ces manipulations si vous en avez besoin.
;;;

;;; counterexample ```c
char* gets(char* chaine)```
;;; doc
Lit une ligne depuis l’entrée standard, sans inclure le saut de ligne (qui reste donc dans le buffer).

- `chaine` : chaîne de caractères où écrire ce qu’a entré l’utilisateur

Retourne `chaine`, ou `NULL` en cas d’échec
;;; alert
Cette fonction est **dépréciée en C99** et **supprimée en C11**. On la met là pour que vous sachiez ce que c'est si vous la croisez mais **ne l'utilisez pas**. Utilisez `fgets()` à la place.
`gets()` ne vérifiait pas la taille du tableau, donc un utilisateur qui entrerait une ligne trop longue dépasserait de votre tableau et corromprait la mémoire de votre programme.
;;;

## Utilisation de fichiers

;;; code ```c
FILE* fopen(const char* nom_fichier, const char* mode)```
;;; doc
**Ouvre un fichier** dans le mode demandé

- `nom_fichier` : chemin vers le fichier à ouvrir
- `mode` : conditionne ce que vous pouvez faire avec le fichier :
	- `"r"` : lecture seule, le fichier doit exister au préalable
	- `"w"` : écriture seule, détruit et recrée le fichier s’il existe déjà
	- `"a"` : écriture seule, écrit à la fin du fichier s’il existe déjà
	- `"r+"` : lecture et écriture d’un fichier existant (le fichier doit exister)
	- `"w+"` : crée un nouveau fichier (et écrase le fichier s’il existe déjà) et l’ouvre en lecture et écriture
	- `"a+"` : ouvre ou crée le fichier en lecture et écriture, et place le curseur à la fin du fichier
	- Tous ces modes ont leur équivalent binaire en rajoutant un `b` (`rb`, `wb`, `ab`, `rb+`, `wb+`, `ab+`). Les modes textes peuvent faire un peu de prétraitement fait pour du texte (par exemple la traduction entre `\n` et `\r\n` sous Windows), qui parasiteraient la lecture et l’écriture de contenu qui n’est pas du texte.

Retourne le fichier ouvert, ou `NULL` si l’ouverture a échoué
;;; note
Pour éviter tout accident, mettez le mode d’écriture avec le moins de permissions possibles, inutile d’utiliser `r+` si vous n’allez que lire. En réalité, on a très rarement besoin des modes `+`.
;;; warning
Vérifiez toujours que le fichier est bien ouvert avant de l’utiliser ! La gestion du système de fichiers de l’utilisateur est totalement indépendante de votre volonté, à la fois la présence des fichiers et les permissions dessus.
;;;

;;; code ```c
int fclose(FILE* fichier)```
;;; doc
Vide les buffers et ferme le fichier
;;; example
```c
FILE* fichier = fopen("fichier.txt", "r");
if (fichier != NULL) {
    fscanf(fichier, "%d %d", &x, &y);
    printf("%d + %d = %d\n", x, y, x+y);
    fclose(fichier);
} else {
    fputs("ERREUR : Fichier inexistant\n", stderr);
}
```
;;; warning
Fermez bien le fichier dès que vous avez fini de l’utiliser. Si vous ne le faites pas il sera fermé automatiquement à la fin du programme, mais en attendant il ne pourra pas être utilisé par d’autres applications, ce qui peut parfois être pénible pour l’utilisateur.
;;;

;;; code ```c
FILE* freopen(const char* nom_fichier, const char* mode, FILE* fichier)```
;;; doc
Ferme le fichier, puis le réassocie à un autre fichier et le retourne

-	`nom_fichier` : nom du fichier à ouvrir. Si vous donnez `NULL`, ça essaiera juste de changer le mode d’ouverture du fichier sans le réassocier, mais ça peut ne pas marcher.
-	`mode` : mode d’ouverture du fichier (pareil que `fopen`)
-	`fichier` : fichier à réassocier

Retourne le fichier ouvert (en théorie le même que `fichier`), ou `NULL` si l’ouverture a échoué. Si l’ouverture a échoué, le fichier d’origine aura quand même été fermé.
Cette fonction peut notamment servir à rediriger les flux standard :
;;; example
```c
// Redirige le flux de sortie standard vers le fichier output.txt
FILE* newout = freopen("output.txt", "a", stdout);
if (newout != NULL) {
    printf("%d", 134);  // Écrit 134 dans output.txt au lieu de la console
    fclose(newout);
}
```
;;;

;;; code ```c
int fflush(FILE* fichier) ```
;;; doc
Écrit les données d’un flux ouvert en écriture vers le fichier (ou la console) sans attendre que le buffer soit plein, peut être utile si quelque chose n’est pas écrit immédiatement quand vous voulez.
Retourne 0 en cas de succès et `EOF` en cas d’erreur.
;;; alert
Beaucoup de tutos jamais testés hors de Visual Studio disent d’utiliser `fflush(stdin)` pour vider le buffer de l’entrée standard (quand il reste des caractères que vous n’avez pas lu et dont vous voulez vous débarrasser).
**Le standard ne définit `fflush` que sur des flux ouverts en écriture**, et POSIX l’ajoute sur les flux en lecture *seekable* (où vous pouvez vous déplacer librement), ce que `stdin` n’est pas ; du reste, les implémentations font ce qu’elles veulent.

`fflush(stdin)` est défini clairement sur les implémentations de Microsoft, ailleurs vous ne pouvez être sûr de rien et généralement ça ne marche pas (et ça peut autant ne rien faire que planter).
Une version portable serait quelque chose de ce type :

```c
while ((c = getchar()) != '\n');
```
Ou de s’arranger pour ne pas laisser traîner des choses problématiques dans le buffer (typiquement en n’utilisant pas `scanf` dans ces cas-là)
;;;

### Déplacement dans un fichier

Note : vous ne pouvez pas vous déplacer manuellement dans certains types de fichiers spéciaux. En particulier, les fonctions suivantes ne fonctionnent pas sur les flux standard `stdin`, `stdout` et `stderr` (entre autres [pour raisons de compatibilité avec les télétypes](https://www.youtube.com/watch?v=2XLZ4Z8LpEE) et les terminaux distants). Un fichier où vous pouvez vous déplacer librement est dit *seekable*.
Si vous utilisez un fichier normal sur le disque que vous avez ouvert avec `fopen`, en principe les fonctions de cette section n’échoueront jamais ; autrement faites attention à ce que vous utilisez.

#### Types

- `fpos_t` : Type opaque permettant de sauvegarder une position dans un fichier, à utiliser uniquement avec `fgetpos` et `fsetpos`

#### Fonctions

;;; code ```c
int feof(FILE* fichier) ```
;;; doc
Dit si le **curseur** est à la **fin du fichier** (donc si la prochaine lecture dessus renverrait `EOF`)
;;; example
*Voir plus bas*
;;;

;;; code ```c
int fgetpos(FILE* fichier, fpos_t* position)```
;;; doc
**Sauvegarde la position** actuelle du curseur de fichier dans `position`. Renvoie 0 si ça a réussi, une autre valeur en cas d’échec.
;;; example
*Voir plus bas*
;;;

;;; code ```c
int fsetpos(FILE* fichier, const fpos_t* position)```
;;; doc
**Ramène le curseur** à la position préalablement sauvegardée avec `fgetpos()`
;;; example
*Voir plus bas*
;;;

;;; code ```c
void rewind(FILE* fichier) ```
;;; doc
Ramène le curseur au **début du fichier**
;;; example
```c/result/wrapmain; includes=["stdio.h"]; joinfiles=[("fichier.csv", "   6,   2,   3\n  11,   2,   6\n  77,   7,  11\n  90,   8,  11")]
/* Les valeurs font toujours 4 caractères
   On veut corriger la première colonne si elle ne vaut pas le produit des deux autres */
FILE* fichier = fopen("fichier.csv", "r+");
if (fichier != NULL) {
    while (!feof(fichier)) {
        fpos_t debut_ligne, fin_ligne;
        unsigned int a, b, c;

        // Sauvegarde la position du début de la ligne
        fgetpos(fichier, &debut_ligne);
        fscanf(fichier, "%u,%u,%u", &a, &b, &c);
        // Sauvegarde la position à la fin de la lecture
        fgetpos(fichier, &fin_ligne);
        // On réécrit la première valeur si elle n’est pas celle qu’on attend
        if (a != b*c) {
            fsetpos(fichier, &debut_ligne);  // Retour au début de la ligne
            fprintf(fichier, "%4u", b*c);
            fsetpos(fichier, &fin_ligne);    // Retour où on en était
        }
        char caractere;
        while ((caractere = fgetc(fichier)) != '\n' && caractere != EOF);  // Passage à la ligne suivante
    }

	rewind(fichier);
	char line[100];
	while(!feof(fichier)) {
		fgets(line, 100, fichier);
		fputs(line, stdout);
	}
    fclose(fichier);
}
```
;;;

;;; code ```c
long ftell(FILE* fichier)```
;;; doc
Donne la **position actuelle** du curseur dans le fichier (nombre d’octets à partir du début du fichier)
;;;

;;; code ```c
int fseek(FILE* fichier, long deplacement, int reference)```
;;; doc
**Déplace le curseur** manuellement dans le fichier

- `fichier` : fichier où manipuler le curseur
- `deplacement` : nombre d’octets par rapport à la référence
- `reference` : position de référence d’où le déplacement est compté, en utilisant une de ces constantes :
 	- `SEEK_SET` : positionne le curseur à `déplacement` octets à partir du début du fichier
 	- `SEEK_END` : positionne le curseur à `déplacement` octets à partir de la fin du fichier (`déplacement` devra donc être négatif)
	- `SEEK_CUR` : déplace le curseur à `déplacement` octets à partir de sa position actuelle (`déplacement` peut être positif ou négatif)
;;; example
*Voir l’exemple de `fread` —*
;;;


### Utilisation de données brutes

Vous pouvez utiliser des fichiers textes, mais beaucoup de formats utilisent plutôt des données brutes, encodées en binaire. Pour lire un fichier binaire plutôt que de travailler avec du texte, vous avez les fonctions `fread` et `fwrite`.

;;; code ```c
size_t fread(void* destination, size_t taille_element, size_t num_elements, FILE* fichier)```
;;; doc
**Lit des données brutes** depuis un fichier

-	`destination` : pointeur vers la variable où mettre les données lues (peut être un pointeur autant sur une variable normale qu’un tableau, une structure ou n’importe quoi d’autre)
-	`taille_element` : taille d’un élément à lire
-	`num_elements` : nombre d’éléments à lire (si vous ne lisez pas un tableau, vous pouvez juste mettre la taille de la variable dans `taille_element` et 1 dans `num_elements`)
-	`fichier` : fichier d’où lire (de préférence en mode binaire, sinon les petits prétraitements du mode texte risquent de vous embêter)

Retourne le nombre d’éléments réellement lus (donc s’il est inférieur à `num_elements`, c’est qu’il y a eu un problème ou que vous avez atteint la fin du fichier)
;;; example
```c
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

// Détection d’exécutables Windows
int main(int argc, char** argv) {
    if (argc < 2) {
        printf("Usage : %s <file>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    FILE* fichier = fopen(argv[1], "rb");
    if (fichier == NULL) {
        printf("File %s not found\n", argv[1]);
        exit(EXIT_FAILURE);
    }

    char magic[4];
    uint32_t pointer;
    // Lecture du nombre magique DOS
    fread(magic, sizeof(char), 2, fichier);
    if (magic[0] == 'M' && magic[1] == 'Z') {
        // Lecture du pointeur vers l’en-tête PE (e_lfanew)
        fseek(fichier, 0x3A, SEEK_CUR);
        fread(&pointer, sizeof(uint32_t), 1, fichier);
        // Déplacement à l’adresse de l’en-tête PE
        fseek(fichier, pointer, SEEK_SET);
        // Lecture du nombre magique PE
        fread(magic, sizeof(char), 4, fichier);
        if (magic[0] == 'P' && magic[1] == 'E' && magic[2] == 0 && magic[3] == 0)
            printf("PE (Windows NT) executable found\n");
        else
            printf("DOS executable found\n");
    } else {
        printf("Not a DOS or Windows executable");
    }
    fclose(fichier);
}
```
;;;

;;; code ```c
size_t fwrite(void* source, size_t taille_element, size_t num_elements, FILE* fichier)```
;;; doc
**Écrit des données brutes** dans un fichier

- `source` : pointeur vers les données à écrire (peut être un pointeur autant sur une variable normale qu’un tableau, une structure ou n’importe quoi d’autre)
- `taille_element` : taille d’un élément à lire
- `num_elements` : nombre d’éléments à lire (si vous ne lisez pas un tableau, vous pouvez juste mettre la taille de la variable dans `taille_element` et 1 dans `num_elements`)
- `fichier` : fichier d’où lire (de préférence en mode binaire, sinon les petits prétraitements du mode texte risquent de vous embêter)

Retourne le nombre d’éléments réellement écrits (donc s’il est inférieur à `num_elements`, c’est qu’il y a eu un problème)
;;; example
```c
// C’est abrégé pour des raisons de place et de beaucoup de code peu pertinent
typedef enum {EVENT_ARRIVEE, EVENT_DEPART} event_type_t;
typedef struct {/* ... */} event_t;
typedef struct {/* ... */} event_queue_t;

int main() {
    FILE* fichier = fopen("events.dat", "rb");
    if (fichier == NULL)
        exit(EXIT_FAILURE);

    int num_events;
    event_t element;
    event_queue_t* file = creer_file();

    fread(&num_events, sizeof(int), 1, fichier);
    for (int i = 0; i < num_events; i++) {
        if (fread(&element, sizeof(event_t), 1, fichier) < 1) {
            printf("Erreur de lecture des events\n");
            fclose(fichier);
            exit(EXIT_FAILURE);
        }
        enfiler_event(file, element);
    }
    fclose(fichier);

    char action;
    do {
        printf("1 - Ajouter\n2 - Retirer \n3 - Sauvegarder et quitter\n> ");
        scanf("%c", &action);
        // ...
        if (action == '3') {
            fichier = fopen("events.dat", "wb");
            if (fichier == NULL) {
                printf("Échec de l’ouverture en écriture de events.dat\n");
                exit(EXIT_FAILURE);
            }

            num_events = taille_file(file);
            fwrite(&num_events, sizeof(int), 1, fichier);
            for (int i = 0; i < num_events; i++) {
                element = defiler_event(file);
                fwrite(&element, sizeof(event_t), 1, fichier);
            }
        }
    } while (action != '3');
    return 0;
}
```
;;;

Attention, une structure n’est pas toujours ce qu’elle paraît être, en particulier à cause de l’alignement en mémoire, et la taille des types peut varier entre les machines. Tant que vos fichiers ne changent pas de machine ça ne posera pas de problème, mais si vos fichiers doivent pouvoir être échangés entre des machines différentes, il faudra faire ça plus précisément.

;;; example
```c/result/includes=["stdio.h"]
typedef struct {
    int test1;
    char test2;
    int test3;
} test_struct;

int main() {
    printf("Structure        : %llu octets\n", sizeof(test_struct));
    printf("Composants seuls : %llu octets\n", sizeof(int) + sizeof(char) + sizeof(int));
}
```
;;;
