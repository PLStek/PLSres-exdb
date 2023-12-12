//// title = "#include <math.h>"
//// description = "Description du contenu du header standard math.h"

# {=title}

Fonctions mathématiques courantes.

Attention : sur certaines plateformes (la plupart des UNIX-like avec GCC), la librairie associée à `math.h` est séparée, il faudra lier votre programme avec l’option `-lm`.
Depuis C99, ces fonctions ont des équivalents pour les `float` en ajoutant un `f` au nom de la fonction (`cos` ⟶  `cosf`).
Il y a encore plein d’autres fonctions dans `math.h`, celles-ci sont les plus courantes :

;;; code
```c
// Fonctions génériques
int abs(int x);  // Valeur absolue, définie dans stdlib.h
double fabs(double x);  // Valeur absolue d’un réel
double fmod(double numerateur, double denominateur);  // Opération modulo pour des réels
double fmax(double x, double y);  // Maximum de deux nombres réels
double fmin(double x, double y);  // Minimum de deux nombres réels

// Arrondis
double ceil(double x);   // Arrondit à l’entier supérieur
double floor(double x);  // Arrondit à l’entier inférieur
double trunc(double x);  // Tronque à l’entier dont la valeur absolue est immédiatement inférieure
double round(double x);  // Arrondit à l’entier le plus proche

// Puissances
double pow(double x, double puissance);  // x^puissance
double sqrt(double x);  // racine carrée
double hypot(double x, double y);  // √(x² + y²), très pratique pour calculer des distances euclidiennes

// Fonctions trigonométriques
double sin(double x);  // sinus (en radians)
double cos(double x);  // cosinus (en radians)
double tan(double x);  // tangente (en radians)

double asin(double x);  // arc-sinus (en radians)
double acos(double x);  // arc-cosinus (en radians)
double atan(double x);  // arc-tangente (en radians). Ne peut retourner que sur la tangente positive.
double atan2(double x, double y);  // angle en radians entre l’axe trigonométrique et le vecteur (x, y). Arc-tangente de y/x, permet d’avoir toujours le bon quadrant, contrairement à atan

// Fonctions hyperboliques
double sinh(double x);  // sinus (en radians)
double cosh(double x);  // cosinus (en radians)
double tanh(double x);  // tangente (en radians)

double asinh(double x);  // arc-sinus (en radians)
double acosh(double x);  // arc-cosinus (en radians)
double atanh(double x);  // arc-tangente (en radians). Ne peut retourner que sur la tangente positive.

// Exponentielles et logarithmes
double exp(double x);    // eˣ
double exp2(double x);   // 2ˣ
double log(double x);     // ln(x)
double log2(double x);   // log₂(x)
double log10(double x);  // log₁₀(x)

// Classification
bool isfinite(double x);  // Nombre fini (pas d’infini ou de NaN)
bool isinf(double x);  // Infini (+inf ou -inf)
bool isnan(double x);  // Not-a-Number (NaN)
```
;;;
