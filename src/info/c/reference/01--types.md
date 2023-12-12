//// title = "Types de variable de base"
//// description = "Les types de base disponibles en C"

# {=title}

;;; code
```c//linenos
// Ceci est un commentaire qui ne dure que jusqu’à la fin de la ligne
/* Ceci est un commentaire
   sur plusieurs lignes */
   
// Caractère ASCII ou entier signé 8-bits (-128 - 127)
char caractère = 'a';
// Entier machine signé (typiquement -2’147’483’648 - 2’147’483’647)
int entier = -12;
// Entier non signé (typiquement 0 - 4’294’967’295)
unsigned int entier2 = 115;
// Entier long (minimum 64 bits, soit -2⁶³ - 2⁶³)
long long gros_entier = 999999999999999999;

// Nombre réel à virgule flottante, environ 7 chiffres significatifs.
float reel = 1.234;
// Flottant double-précision (64-bits), environ 15 chiffres significatifs
double pi = 3.141592653589793;
```
;;;

Les types de base sont essentiellement des nombres, et quasiment tout en est dérivé.
Vous avez différents types entiers de différentes tailles (qui ne sont pas toujours garanties, reportez-vous à {>info.c.stdlib.stdint: la section sur `stdint.h`}), qui ont chacun une version signée, donc avec un signe (`+` / `-`), par défaut ; et une version non signée, qui peut donc aller deux fois plus haut mais ne peut pas contenir de nombres négatifs, en ajoutant `unsigned` devant.
Globalement, on utilise des `int` tant qu’on n’a pas besoin d’autre chose. Attention à ne pas confondre des valeurs signées et non-signées, généralement le compilateur se débrouille mais ça peut causer des problèmes. Avec les warnings activés (option `-Wall`) il vous dira quand ça ne va pas.
