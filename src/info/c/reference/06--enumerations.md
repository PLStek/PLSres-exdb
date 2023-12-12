//// title = "Énumérations"
//// description = "Les types énumérés en C"

# {=title}

Une énumération définit un **type** qui ne peut prendre que **certaines valeurs nommées**

;;; code
```c//linenos
typedef enum {
	ROUGE, VERT,
	BLEU, JAUNE,
} couleur_t;


// ...
couleur_t background = BLEU;

if (background == JAUNE) {
	//...
}

switch (background) {
	case ROUGE:
		// ...
		break;
	// ...
}
```
;;;

Une énumération permet d’éviter de dire implicitement que `1` correspond à bleu, `2` à jaune, etc. : ça **améliore** nettement la **lisibilité** et la **fiabilité** du code dans ces cas-là.

Si vous activez tous les warnings (`-Wall`), GCC vous préviendra si vous avez oublié une option quand vous utilisez une énumération dans un `switch` sans `default`.

Une valeur énumérée est implicitement associée à un nombre entier. Dans certaines situations, il peut être utile d’utiliser ces valeurs explicitement :

;;; example
```c
typedef enum {
	COL_ID = 0,
	COL_VALEUR = 1,
	COL_TIMESTAMP = 2,
} colonne_t;
```
;;;

Avec ça, vous pourrez utiliser la valeur entière définie. Attention toutefois à ne pas faire n’importe quoi avec, si vous vous retrouvez avec une valeur entière qui ne correspond à aucun membre de l’énumération ça peut vous causer de gros problèmes.
