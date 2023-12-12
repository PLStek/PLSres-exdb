//// title = "#include <stdbool.h>"
//// description = "Description du contenu du header standard stdbool.h"

# {=title}

Depuis C99, il existe un type appelé `_Bool` qui est garanti de ne prendre que les valeurs 0 et 1 pour gérer les booléens proprement. Le header `stdbool.h` permet une utilisation plus esthétique :

- `bool` : Typedef sur `_Bool`, ne peut prendre que les valeurs 0 et 1 (contrairement aux entiers habituels qui peuvent prendre d’autres valeurs et donc causer des problèmes dans certaines situations)
- `true` : Valeur d’un booléen vrai (1)
- `false` : Valeur d’un booléen false (0)

Ces trois valeurs deviendront des mots-clés en C23 et disponibles hors de `<stdbool.h>`.

;;; example
```c
#include <stdbool.h>

bool est_vrai = true;
bool est_faux = false;
if (est_vrai && est_faux)
    // Choses utiles (?)
```
;;;

Dans beaucoup de librairies et de projets faits pour être compatibles ANSI, `true` et `false` sont redéfinis par des `#define` dans le projet. Pour un projet C99, vous pouvez faire ça mais utiliser `stdbool.h` est beaucoup mieux.
