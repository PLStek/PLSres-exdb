//// title = "GDB, le débugger GNU"
//// description = "Utilisation du débugger GDB"

# {=title}

GDB est un **débugger**, qui permet donc de **manipuler** votre programme **pendant son exécution** pour mieux voir ce qui se passe. Il s’utilise essentiellement avec GCC, et la plupart des IDE l’intègrent dans leur environnement pour le rendre plus facile d’utilisation. Ici, on se concentrera sur son utilisation en console — sous un IDE, il y aura généralement les fonctionnalités de base en mode graphique.
Pour utiliser GDB de façon utile, vous devrez compiler votre programme avec les **symboles de débuggage** (option `-g`)

## Mise en situation

Faisons-nous un programme de test nul :

;;; counterexample
```c//linenos
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define TAILLE 10000000000


int generate(int* value1, int* value2) {
	*value1 = rand() % 1000;
	*value2 = *value1 + (rand()%1000) - (rand()%1000) + (rand()%1000) - (rand()%1000);
}

void fill(int* array1, int* array2, long taille) {
	for (int i = 0; i < taille; i++)
		generate(&(array1[i]), &(array2[i]));
}

long numequal(int* array1, int* array2, long taille) {
	long equal = 0;
	for (int i = 0; i < taille; i++)
		equal += (array1[i] == array2[i])? 1 : 0;
	return equal;
}

int main(int argc, char** argv) {
	srand(time(NULL));
	if (argc < 2) {
		printf("Usage : %s <size>\n", argv[0]);
		exit(EXIT_FAILURE);
	}

	long taille = atoi(argv[1]);

	int* array1 = calloc(sizeof(int), taille);
	int* array2 = calloc(sizeof(int), TAILLE);

	fill(array1, array2, TAILLE);
	long equal = numequal(array1, array2, taille);

	printf("%ld/%ld cells equal\n", equal, taille);
	return 0;
}
```
;;;

Et lançons-le :

;;; shell ```bash
~/plstek$ gcc -g -o test test.c
~/plstek$ ./test 1000000
Segmentation fault```
;;;

Oh non ! Notre programme est plein de problèmes ! Vite, débuggons ça proprement plutôt que passer 1h30 à utiliser des `printf` un peu partout ou que réfléchir 30 secondes :

;;; shell
```bash
~/plstek$ gdb ./test
~/plstek$ # Pour mettre des arguments à votre programme
~/plstek$ gdb --args ./test 1000000
```
;;; shell
```
GNU gdb (Ubuntu 9.2-0ubuntu1~20.04.1) 9.2
Copyright (C) 2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from ./test...

(gdb) `***run***`
Starting program: /home/tyulis/plstek/test 1000000

Program received signal SIGSEGV, Segmentation fault.
0x00005555555552fb in generate (value1=0x7ffff79fc010, value2=0x0) at test.c:10
10              *value2 = *value1 + (rand()%1000) - (rand()%1000) + (rand()%1000) - (rand()%1000);
```
;;; doc
**`run`**, **`r`** : Lance le programme du début
;;;

On a donc lancé GDB, et simplement lancé notre programme dedans avec la commande `run`. GDB a automatiquement suspendu l’exécution quand le programme a crashé. GDB nous dit donc que nous avons reçu un signal `SIGSEGV` (erreur de segmentation), et nous donne exactement la fonction et la ligne où ça a planté. C’est déjà mieux, mais on ne sait toujours pas pourquoi. Explorons l’état du programme quand il a planté :

;;; shell
```
(gdb) `***backtrace***`
#0  0x00005555555552fb in generate (value1=0x7ffff79fc010, value2=0x0) at test.c:10
#1  0x0000555555555358 in fill (array1=0x7ffff79fc010, array2=0x0, taille=10000000000) at test.c:15
#2  0x0000555555555497 in main (argc=2, argv=0x7fffffffdfd8) at test.c:37
```
;;; doc
**`backtrace`**, **`ba`**, **`bt`** : Affiche la pile d’exécution actuelle
Ça donne la pile d’exécution, avec les fonctions, leurs arguments, le fichier, et la ligne où on se situe dans chacune d’elles : ici, `main()` a appelé `fill()` à la ligne 37, puis `fill()` a appelé `generate()` à la ligne 15, et on est actuellement à la ligne 10 dans `generate()`
;;;

Inspectons les valeurs de nos variables :

;;; shell
```
(gdb) `***print***` *value1
$2 = 610
(gdb) `***print***` *value2
Cannot access memory at address 0x0
```
;;; doc
**`print`** : Affiche le résultat d’une expression
Vous pouvez calculer à peu près n’importe quelle expression en C : par exemple ici on a des `*pointeur`, on peut faire aussi bien `print variable` que `print structure->champ.souschamp[var1] + *(ptr + 5)`
;;;

Bizarre, on a un pointeur nul qui traîne. Regardons les valeurs de nos variables :

;;; shell
```
(gdb) `***backtrace full***`
#0  0x00005555555552fb in generate (value1=0x7ffff79fc010, value2=0x0) at test.c:10
No locals.
#1  0x0000555555555358 in fill (array1=0x7ffff79fc010, array2=0x0, taille=10000000000) at test.c:15
		i = 0
#2  0x0000555555555497 in main (argc=2, argv=0x7fffffffdfd8) at test.c:37
		taille = 1000000
		array1 = 0x7ffff79fc010
		array2 = 0x0
		equal = 0
```
;;; doc
**`backtrace full`** : Affiche la pile d’exécution avec les variables locales de chaque fonction
;;;

Notre `array2` est donc un pointeur nul (adresse `0x0`). Sortons pour recommencer avec de nouvelles options :

;;; shell
```
(gdb) `***quit***`
A debugging session is active.

        Inferior 1 [process 282] will be killed.

Quit anyway? (y or n) y
~/plstek$
```
;;; doc
**`quit`** : Tue le programme et quitte GDB (avec confirmation)
;;;

;;; shell ```bash
~/plstek$ gdb --args ./test 1000000```
```
GNU gdb (Ubuntu 9.2-0ubuntu1~20.04.1) 9.2

(gdb) `***break***` main
Breakpoint 1 at 0x13e5: file test.c, line 25.

(gdb) `***run***`
Starting program: /home/tyulis/plstek/test 1000000

Breakpoint 1, main (argc=21845, argv=0x7ffff7fbe2e8 <__exit_funcs_lock>) at test.c:25
``` ```c
25      int main(int argc, char** argv) {
```
;;; doc
**`break`** : Crée un **breakpoint**, quand l’exécution atteindra ce point, GDB interrompra le programme et vous pourrez l’explorer comme vous voulez. Vous pouvez donner le nom d’une fonction (comme ici `break main`) pour suspendre dès l’entrée dans la fonction, ou donner une ligne dans un fichier pour suspendre l’exécution quand elle sera atteinte (`break test.c:26` pour suspendre à la ligne 26 de `test.c`)
;;;

Notre programme s’est bien suspendu au début de la fonction, on peut maintenant installer des **watchpoints** sur ses variables :

;;; shell
```
(gdb) `***watch***` array1
Hardware watchpoint 2: array1
(gdb) `***watch***` array2
Hardware watchpoint 3: array2
(gdb) `***continue***``
Continuing.

Hardware watchpoint 2: array1

Old value = (int *) 0x555555555120 <_start>
New value = (int *) 0x7ffff79fc010
main (argc=2, argv=0x7fffffffdfd8) at test.c:35
``` ```c
35              int* array2 = calloc(sizeof(int), TAILLE);
``` ```
(gdb) `***c***`
Continuing.

Hardware watchpoint 3: array2

Old value = (int *) 0x7fffffffdfd0
New value = (int *) 0x0
main (argc=2, argv=0x7fffffffdfd8) at test.c:37
``` ```c
37              fill(array1, array2, TAILLE);
```
;;; doc
**`watch`** : Place un **watchpoint**, chaque fois que la valeur de l’expression donnée (là aussi ça peut être une simple variable ou une expression), le programme s’interrompt et GDB vous donne le changement de valeur. Attention, selon le système (par exemple ici), ça interrompt après le changement de valeur, donc généralement à la ligne d’après.
**`continue`**, **`c`** : Reprend l’exécution du programme après une interruption
;;;

Donc juste avant la ligne 37, la valeur `NULL` (`0x0`) a été assignée à `array2`. Allons donc voir :

;;; counterexample
```c
	int* array1 = calloc(sizeof(int), taille);
	int* array2 = calloc(sizeof(int), TAILLE);
```
;;;

Ô, rage et surprise : quand on a rendu l’allocation dynamique on a oublié de changer la constante `TAILLE` par la variable `taille` pour `array2` ! Du coup l’allocation a raté et `malloc` a retourné `NULL`. Changeons ça rapidement et testons de nouveau :

;;; shell
```bash
~/plstek$ vim test.c
~/plstek$ gcc -g -o test test.c
~/plstek$ ./test 1000000
Segmentation fault
```
;;;

C’est pas encore ça. Repassons notre programme par GDB :

;;; shell ```bash
~/plstek$ gdb --args ./test 1000000
``` ```
GNU gdb (Ubuntu 9.2-0ubuntu1~20.04.1) 9.2

(gdb) `***run***`
Starting program: /home/tyulis/plstek/test 1000000

Program received signal SIGSEGV, Segmentation fault.
0x0000555555555249 in generate (value1=0x7ffff7dcd000, value2=0x7ffff79fc000) at test.c:9
``` ```c
9               *value1 = rand() % 1000;
```
;;;

Ça ne plante pas au même endroit, on avance. Les valeurs des arguments `value1` et `value2` ont l’air normales à première vue, et comme tout à l’heure il n’y a pas de variables locales dans `generate()`. Plutôt que de refaire la même chose que la dernière fois et utiliser `backtrace full` pour voir les variables des fonctions appelantes, démontrons quelques autres commandes :

;;; shell
```
(gdb) `***ba***`
\#0  0x0000555555555249 in generate (value1=0x7ffff7dcd000, value2=0x7ffff79fc000) at test.c:9
\#1  0x0000555555555358 in fill (array1=0x7ffff79fc010, array2=0x7ffff762b010, taille=10000000000) at test.c:15
\#2  0x0000555555555494 in main (argc=2, argv=0x7fffffffdfd8) at test.c:37
(gdb) `***frame***` 1
\#1  0x0000555555555358 in fill (array1=0x7ffff79fc010, array2=0x7ffff762b010, taille=10000000000) at test.c:15
``` ```c
15                      generate(&(array1[i]), &(array2[i]));
``` ```
(gdb) `***info locals***`
i = 1000444
```
;;; doc
**`frame <n° donné par backtrace>`** : Passe dans le contexte d’une fonction plus basse dans la pile d’exécution, avec le numéro donné par la commande `backtrace`. Par exemple, ici, la frame n°1 est la fonction `fill`, donc `frame 1` vous passe dans le contexte actuel de `fill()` pour pouvoir l’explorer. Ça ne retourne pas vraiment, c’est juste pour l’exploration dans GDB.
**`info locals`** : Liste les variables locales de la fonction actuelle (`backtrace full` fait comme info locals sur chaque fonction de la pile)
;;;

Bizarre, notre taille fait 1’000'000 mais `i` est arrivé à 1’000'444 — et pour cause, l’argument `taille` est à 10’000’000'000. Encore un `TAILLE` pas modifié !

;;; counterexample ```c
	fill(array1, array2, TAILLE);
	long equal = numequal(array1, array2, taille);
```
;;;

Corrigeons et réessayons :

;;; shell
```bash
~/plstek$ vim test.c
~/plstek$ gcc -g -o test test.c
~/plstek$ ./test 1000000
696/1000000 cells equal
```
;;;

C’est gagné ! Récapitulons :

;;; doc
- **`run`**, **`r`** : Lance le programme du début
- **`continue`**, **`c`** : Continue le programme après une interruption
- **`kill`**, **`k`** : Termine le programme en cours d’exécution
- **`quit`**, **`q`** : Termine le programme et quitte GDB
- **`backtrace`**, **`ba`**, **`bt`** : Affiche la pile d’exécution actuelle
- **`backtrace full`**, **`ba full`**, **`bt full`** : Affiche la pile d’exécution avec les variables locales de chaque fonction
- **`frame <n° donné par backtrace>`** : Passe GDB dans le contexte d’une fonction appelante
- **`return`**, **`ret`** : Retourne de la fonction actuelle (réellement, dans l’exécution du programme)
- **`info locals`** : Liste les variables locales de la fonction en cours
- **`print <expression>`** : Calcule et affiche la valeur d’une expression C dans le contexte actuel (donc avec des variables, constantes, …)
- **`break <fonction>`** : Interrompt quand la fonction donnée est appelée
- **`break <fichier:ligne>`** : Interrompt quand le programme exécute la ligne donnée (ex : `break test.c:26`)
- **`watch <variable ou expression>`** : Interrompt quand la valeur de l’expression change et donne le changement de valeur
;;;

## Autres commandes

GDB offre des pelletées de commandes pour explorer en profondeur le fonctionnement de votre programme, que vous pouvez voir par la commande `help` dans gdb. En voici quelques-unes particulièrement utiles :

### Breakpoints et watchpoints

;;; shell
```
(gdb) `***break***` test.c:15 `***if***` i==100
Breakpoint 1 at 0x1325: file test.c, line 15.
(gdb) `***run***`
Starting program: /home/tyulis/plstek/test 1000000

Breakpoint 1, fill (array1=0x7ffff79fc010, array2=0x7ffff762b010, taille=1000000) at test.c:15
``` ```c
15                      generate(&(array1[i]), &(array2[i]));
``` ```
(gdb) `***print***` i
$1 = 100
```
;;; doc
**`break <position> if <condition>`** : Crée un breakpoint à la position donnée, mais qui interrompra seulement quand la condition (exprimée comme en C) est vraie.
**`watch <expression> if <condition>`** : Pareil pour créer un watchpoint conditionnel
;;;

;;; shell
```
(gdb) `***break***` test.c:16
Breakpoint 3 at 0x555555555367: file test.c, line 16.
(gdb) `***run***`
Starting program: /home/tyulis/plstek/test 1000000

Breakpoint 3, fill (array1=0x7ffff79fc010, array2=0x7ffff762b010, taille=1000000) at test.c:16
16      }
(gdb) `***disable***` 3
(gdb) `***enable***` 3
```
;;; doc
**`disable <n° de breakpoint ou watchpoint>`** : Désactive un breakpoint ou un watchpoint, en donnant le numéro donné quand vous l’avez créé
**`enable <n° de breakpoint ou watchpoint>`** : Réactive le breakpoint ou watchpoint
**`delete <n° de breakpoint ou watchpoint>`** : Supprime le breakpoint ou watchpoint
;;;

### Contrôle de l’exécution

;;; shell
```
(gdb) `***run***`
Breakpoint 1, main (argc=21845, argv=0x7ffff7fbe2e8 <__exit_funcs_lock>) at test.c:25
``` ```c
25      int main(int argc, char** argv) {
``` ```
(gdb) `***step***`
``` ```c
26              srand(time(NULL));
``` ```
(gdb) step
__srandom (x=1654383723) at random.c:209
209     random.c: No such file or directory.
```
;;; doc
**`step`** : Exécute juste la ligne suivante, en s’enfonçant dans les fonctions appelées (par exemple ici c’est descendu dans la fonction `srand`)
;;;

;;; shell
```
(gdb) `***run***`
Breakpoint 1, main (argc=21845, argv=0x7ffff7fbe2e8 <__exit_funcs_lock>) at test.c:25
``` ```c
25      int main(int argc, char** argv) {
``` ```
(gdb) `***next***`
``` ```c
26              srand(time(NULL));
``` ```
(gdb) `***next***`
``` ```c
27              if (argc < 2) {
```
;;; doc
**`next`** : Exécute juste la ligne suivante, sans s’enfoncer dans les fonctions appelées (ici ça a juste appelé `srand` et passé à la suite)
;;;

;;; shell
```
(gdb) `***run***`
Breakpoint 1, fill (array1=0x5555555554d0 <__libc_csu_init>, array2=0x7fffffffdfd0, taille=140737352469397) at test.c:13
``` ```c
13      void fill(int* array1, int* array2, long taille) {
``` ```
(gdb) `***finish***`
Run till exit from #0  fill (array1=0x5555555554d0 <__libc_csu_init>, array2=0x7fffffffdfd0, taille=140737352469397) at test.c:13
main (argc=2, argv=0x7fffffffdfd8) at test.c:38
``` ```c
38              long equal = numequal(array1, array2, taille);
```
;;; doc
**`finish`** : Continue et interrompt quand la fonction actuelle retourne (ça interrompt dans la fonction appelante, juste après l’appel de la fonction actuelle)
**`continue`** : Continue normalement jusqu’au prochain breakpoint ou watchpoint
;;;

### Informations

;;; shell
```
(gdb) `***run***`
Breakpoint 1, fill (array1=0x7ffff79fc010, array2=0x7ffff762b010, taille=1000000) at test.c:15
``` ```c
15                      generate(&(array1[i]), &(array2[i]));
``` ```
(gdb) `***display***` i
1: i = 0
(gdb) `***next***`
``` ```c
14              for (int i = 0; i < taille; i++)
``` ```
1: i = 0
(gdb) `***next***`
``` ```c
15                      generate(&(array1[i]), &(array2[i]));
``` ```
1: i = 1
```
;;; doc
**`display <expression>`** : Donne le résultat d’une expression, comme `print`, mais répète l’expression à chaque avancée dans l’exécution
**`disable display <n° de display>`**, **`enable display <n°>`**, **`undisplay <n°>`** : Désactive, réactive, et supprime, respectivement, un `display` avec le numéro donné quand vous le créez.
;;;

;;; shell
```
Breakpoint 1, fill (array1=0x7ffff79fc010, array2=0x7ffff762b010, taille=1000000) at test.c:15
``` ```c
15                      generate(&(array1[i]), &(array2[i]));
``` ```
(gdb) `***list***`
``` ```c
10              *value2 = *value1 + (rand()%1000) - (rand()%1000) + (rand()%1000) - (rand()%1000);
11      }
12
13      void fill(int* array1, int* array2, long taille) {
14              for (int i = 0; i < taille; i++)
15                      generate(&(array1[i]), &(array2[i]));
16      }
17
18      long numequal(int* array1, int* array2, long taille) {
19              long equal = 0;
```
;;; doc
**`list`** : Affiche le listing du code autour de la position actuelle
**`list <fonction>`** : Affiche le listing du code autour de la définition de la fonction donnée
**`list <fichier:ligne>`** : Affiche le listing du code autour de la position donnée
**`set listsize <nb lignes>`** : Paramètre le nombre de lignes que list affiche
;;;

;;; shell ```
(gdb) `***whatis***` taille
type = long```
;;; doc
**`whatis <variable>`** : Donne le type d’une variable
;;;

### La commande info

La commande `info` a de nombreuses options pour afficher des informations sur l’exécution en cours, comme par exemple

Commande           | Information
------------------ | -------------------------------------------
`info locals`      | Liste les variables locales
`info args`        | Liste les arguments de la fonction actuelle
`info breakpoints` | Liste les breakpoints
`info watchpoints` | Liste les watchpoints
`info display`     | Liste les expressions `display`

Ce sont les principales, il y en a encore beaucoup d’autres plus spécifiques que vous pouvez lister avec `help info`
