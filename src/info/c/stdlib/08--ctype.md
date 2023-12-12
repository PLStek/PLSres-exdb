//// title = "#include <ctype.h>"
//// description = "Description du contenu du header standard ctype.h"

# {=title}

Fonctions pour manipuler des classes de caractères.

## Test d’appartenance d’un caractère à une catégorie

;;; code
```c
bool isalnum(char c);  // Caractère alphanumérique
bool isalpha(char c);  // Lettre
bool islower(char c);  // Lettre minuscule
bool isupper(char c);  // Lettre majuscule
bool isdigit(char c);  // Chiffre
bool isxdigit(char c); // Chiffre hexadécimal (0123456789AaBbCcDdEeFf)

// Ponctuations (les caractères spéciaux ASCII !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
bool ispunct(char c);

// Espaces (espace, tabulation, saut de ligne, retour chariot \r)
bool isspace(char c);

// Caractères de contrôle (caractères ASCII de 0x00 à 0x1F et 0x7F. Ça inclut le caractère nul, le saut de ligne, la tabulation, ... (mais pas l’espace et les autres caractères spéciaux)
bool iscntrl(char c);

// Caractères graphiques (tout ce qui a un caractère à l’écran, donc tout sauf les espaces et les caractères de contrôle)
bool isgraph(char c);

// Caractères imprimables (tout sauf les caractères de contrôle)
bool isprint(char c);
```
;;;

## Conversion de catégorie de caractère

;;; code ```c
char toupper(char c)
char tolower(char c)
```
;;; doc
`toupper` transforme le caractère en majuscules
`tolower` transforme le caractère en minuscules
Ces fonctions renvoient le caractère transformé, ou le même caractère s’il n’y a pas de transformation à faire (si le caractère est déjà dans la bonne casse ou si ce n’est pas une lettre)
;;;
