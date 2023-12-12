//// title = "Bit-fields"
//// description = "Utiliser des données au niveau du bit"

# {=title}

Jusque-là, on a utilisé des types de variables qui se comptent en octets, parce que c’est la plus petite unité d’addressage de la mémoire. Sauf que concrètement, on n’a pas toujours besoin d’autant. Mettons par exemple qu’on a ce type de structure qui contient les informations sur un évènement quelconque :

;;; code
```c/result/linenos; includes=["stdbool.h", "stdio.h"]
typedef enum {  // Il y en a 5
	EVENT_NOP, EVENT_ACTIVATE, EVENT_START, EVENT_STOP, EVENT_DEACTIVATE,
} event_type_t;

typedef enum {  // Il y en a 10
	COMPONENT_INPUT, COMPONENT_OUTPUT, COMPONENT_LOG, COMPONENT_DISPATCH,
	COMPONENT_LAYER1, COMPONENT_LAYER2, COMPONENT_LAYER3, COMPONENT_LAYER4,
	COMPONENT_MERGE, COMPONENT_BUFFER,
} component_id_t;

typedef struct {
	event_type_t type;
	component_id_t source;
	component_id_t destination;
	bool keep_active;
	bool full_report;
	int accuracy;  // 0-3
	int strength;  // 0-3
} event_t;

int main() {
	printf("Simple structure : %d bits\n", sizeof(event_t) * 8);
	return 0;
}
```
;;;

Ça marche parfaitement bien, mais on bouffe **24 octets soit 192 bits** pour l’équivalent de **17 bits d’information**. D’habitude c’est pas bien grave, vous avez de la place. Cependant, dès que vous commencez à mouliner quelques milliers / millions de ce genre de structures, ça chiffre sérieusement. Et même sans ça, il y a des situations où la mémoire est une ressource rare, comme en **embarqué**, où ce type d’économie est très important. Pour cela, on peut utiliser ce qu’on appelle des ***bit-fields***. Ça permet de faire des structures avec des champs d’une taille inférieure à l’octet, ce qui permet de caler beaucoup plus d’information dans moins de mémoire quand vous savez quelle information vous retenez. Pour cela, chaque champ doit être défini comme `type nom : bits;`. Pour reprendre notre évènement ci-dessus :

;;; code
```c/result/linenos; includes=["stdbool.h", "stdio.h"]
typedef enum {  // Il y en a 5
	EVENT_NOP, EVENT_ACTIVATE, EVENT_START, EVENT_STOP, EVENT_DEACTIVATE,
} event_type_t;

typedef enum {  // Il y en a 10
	COMPONENT_INPUT, COMPONENT_OUTPUT, COMPONENT_LOG, COMPONENT_DISPATCH,
	COMPONENT_LAYER1, COMPONENT_LAYER2, COMPONENT_LAYER3, COMPONENT_LAYER4,
	COMPONENT_MERGE, COMPONENT_BUFFER,
} component_id_t;

typedef struct {
	event_type_t type          : 3;  // 5 valeurs ⟶ 3 bits (max 8)
	component_id_t source      : 4;  // 10 valeurs ⟶ 4 bits (max 16)
	component_id_t destination : 4;  // pareil
	unsigned int keep_active   : 1;
	unsigned int full_report   : 1;
	unsigned int accuracy      : 2;  // 0-3 ⟶ 2 bits
	unsigned int strength      : 2;  // 0-3 ⟶ 2 bits
} event_t;

int main() {
    printf("Bit-fields : %d bits\n", sizeof(event_t) * 8);
    return 0;
}
```
;;;

On donne à chaque fois le nombre de bits que chaque champ occupe. Quelques trucs où il faut faire attention :

- **Notez bien `signed` ou `unsigned`**. Sans ça, ça prendra le type signé par défaut, d’habitude c’est pas un problème mais là si on a 2 bits ça veut dire que les bits `11` font -1 et `10` font -2, ce qui est rarement le but.
- Vous pouvez utiliser des **types énumérés**, mais ça ne comptera pas les valeurs possibles pour vous, vous devrez choisir vous-même la taille du champ. Si vous rajoutez des valeurs énumérées par la suite, faites donc attention à mettre à jour le bit-field si nécessaire. Le compilateur vous donnera des warnings si la taille du champ est trop faible.
- **`bool` / `_Bool` ne marche pas**. Vous pouvez l’utiliser, mais il consommera invariablement 8 bits, même si vous lui demandez de n’en prendre qu’un. Utilisez juste un `unsigned int` d’un bit pour ça, ça marchera exactement pareil.

Résultat, ici on est passé de 192 à 32 bits occupés pour la même information (on a 17 bits d’information, mais pour des raisons d’alignement mémoire ça arrondira généralement à la taille d’un mot machine).

Ensuite, pour accéder à un champ, ça marche exactement comme d’habitude pour une structure :

;;; example ```c
printf("%d", event.accuracy);
event.accuracy = 1;```
;;;

Pour des raisons évidentes, un champ de ce type n’a pas d’adresse mémoire à lui seul, donc vous ne pouvez pas prendre `&event.accuracy`.

Vous pouvez d’ailleurs mélanger des bit-fields et des champs normaux (sans restreindre la taille en bits) dans la même structure : dans ce cas, le compilateur s’arrangera pour mettre les bit-fields ensemble et optimiser au mieux l’espace mémoire, tout en gardant les champs normaux.

Tout ça a l’air très chouette, mais ne soyez pas trop optimistes : **l’ordre réel des champs est indéterminé**. Donc par exemple, si c’est pour un protocole de communication ou pour remplir un registre mappé bit par bit en embarqué, il faudra faire vous-même vos masques parce que les bit-fields ne peuvent pas garantir que vos champs ressortiront dans l’ordre. En fait, il ne ressortiront probablement *pas* dans l’ordre parce que le compilateur optimise souvent par rapport à l’alignement en mémoire (par exemple, il va souvent décaler des champs pour qu’un champ ne soit pas coupé sur deux octets différents). Du coup, ça limite pratiquement leur utilisation à l’optimisation de l’espace mémoire. En plus comme les compilateurs font un peu ce qu’ils veulent, vous ne pouvez pas non plus être certain de l’optimisation réalisée sur différentes plateformes.
