//// title = "#include <stddef.h>"
//// description = "Description du contenu du header standard stddef.h"

# {=title}

Ce header contient quelques définitions fondamentales, utilisées dans toute la bibliothèque standard. Comme ce header est inclus dans beaucoup d’autres de la bibliothèque standard (`stdlib.h`, `stdio.h`, `string.h`, `time.h`, …), pas besoin de l’inclure vous-même, à moins de ne rien utiliser de tout ça vous aurez toujours ces définitions.

## Types

- **`size_t`** : Type entier non signé utilisé pour représenter une taille de tableau dans la plupart des fonctions de la librairie standard. En général le compilateur se débrouille tout seul pour convertir entre `size_t` et vos autres types entiers si besoin
- **`ptrdiff_t`** : Type entier signé garanti d’être capable de contenir le résultat de la soustraction de deux pointeurs, si jamais vous avez besoin de bricoler des distances dans un tableau à partir de pointeurs sur ses éléments.

## Macros

- **`NULL`** : Valeur spéciale utilisée pour représenter un pointeur invalide (nul). Vaut en général `(void*)0`, mais pas nécessairement.
- **`offsetof(type, champ)`** : donne l’espace en octets entre le début d’une structure du type donné et la position du champ demandé dans cette structure, ce qui peut servir quand vous manipulez des données encodées dans un fichier par exemple. Faire des sommes de `sizeof()` pour ça est une mauvaise idée car vous risquez de changer la définition de la structure, et même sans ça les contraintes d’alignement en mémoire peuvent décaler des valeurs selon la machine.
