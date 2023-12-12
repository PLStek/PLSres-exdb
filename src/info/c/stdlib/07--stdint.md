//// title = "#include <stdint.h>"
//// description = "Documentation du contenu de stdint.h"

# {=title}

Les types entiers fondamentaux en C ont certaines caractéristiques garanties par le standard, mais restent assez nébuleux :

Type        | Contenance                               | signed                                                    | unsigned
----------  | ---------------------------------------- | --------------------------------------------------------- | --------
`char`      | Peut contenir un caractère de la machine | `[-128, 127]`                                             | `[0, 255]`
`short`     | Au moins 16 bits                         | `[-32768, 32767]`                                         | `[0, 65536]`
`int`       | Au moins 16 bits,\ mais généralement 32  | `[-32768, 32767]`\ `[-2 147 483 647, 2 147 483 648]`      | `[0, 65536]`\ `[0, 4 294 967 295]`
`long`      | Au moins 32 bits                         | `[-2 147 483 647, 2 147 483 648]`                         | `[0, 4 294 967 295]`
`long long` | Au moins 64 bits                         | `[-9 223 372 036 854 776 000, 9 223 372 036 854 776 000]` | `[0, 18 446 744 073 709 552 000]`

Tout ça nous donne une amplitude minimale, mais un type peut contenir virtuellement n’importe quoi du moment que ça respecte ces conditions : un `short` pourrait aussi bien faire 64 bits — d’ailleurs on se repose souvent sur le fait qu’un `int` fait 32 bits parce que la majorité des machines et des compilateurs le font comme ça, mais personne n’y est obligé, et ce n’est pas rare d’en trouver de 16 bits en embarqué.

Pour avoir plus de garanties sur la contenance de nos types, ce qui peut avoir beaucoup d’importance en embarqué, optimisation, ou en bas niveau en général, `stdint.h` donne des définitions de types entiers avec plus de garanties :

Types signés                                                      | Types non-signés                                                      | Garanties
----------------------------------------------------------------- | --------------------------------------------------------------------- | ---------------------------------------------------
`intmax_t`                                                        | `uintmax_t`                                                           | Plus long type entier supporté (au minimum 64 bits)
`int8_t`\ `int16_t`\ `int32_t`\ `int64_t`                         | `uint8_t`\ `uint16_t`\ `uint32_t`\ `uint64_t`                         | Ces types ont exactement la taille demandée (en bits), ni plus, ni moins. Ils sont **optionnels** dans le standard, c’est-à-dire qu’ils seront souvent définis, mais c’est n’est **pas obligatoire**, vérifiez avant
`int_least8_t`\ `int_least16_t`\ `int_least32_t`\ `int_least64_t` | `uint_least8_t`\ `uint_least16_t`\ `uint_least32_t`\ `uint_least64_t` | Pas forcément exactement la bonne taille, mais garantissent d’avoir le plus petit type supporté qui fasse au minimum la taille demandée
`int_fast8_t`\ `int_fast16_t`\ `int_fast32_t`\ `int_fast64_t`     | `uint_fast8_t`\ `uint_fast16_t`\ `uint_fast32_t`\ `uint_fast64_t`     | Donnent le type le plus efficace (en termes de performances) qui fasse au minimum la taille demandée
`intptr_t`                                                        | `uintptr_t`                                                           | Type entier capable de contenir une adresse mémoire sur la machine. Ces types sont **optionnels** dans le standard, donc ne seront pas obligatoirement définis mais ils le seront dans les implémentations communes.

`stdint.h` définit également des constantes pour avoir les **limites** réelles de chacun de ces types, ainsi que des types `size_t` et `ptrdiff_t` contenus dans {>info.c.stdlib.stddef : `stddef.h`} :

Types signés     | Constantes                             || Types non-signés  | Constantes
---------------- | -------------------------------------- || ----------------- | ------------------------
`intmax_t`       | `INTMAX_MIN`\ `INTMAX_MAX`             || `uintmax_t`       | `0`\ `UINTMAX_MAX`
`int<N>_t`       | `INT<N>_MIN`\ `INT<N>_MAX`             || `uint<N>_t`       | `0`\ `UINT<N>_MAX`
`int_least<N>_t` | `INT_LEAST<N>_MIN`\ `INT_LEAST<N>_MAX` || `uint_least<N>_t` | `0`\ `UINT_LEAST<N>_MAX`
`int_fast<N>_t`  | `INT_FAST<N>_MIN`\ `INT_FAST<N>_MAX`   || `uint_fast<N>_t`  | `0`\ `UINT_FAST<N>_MAX`
`intptr_t`       | `INTPTR_MIN`\ `INTPTR_MAX`             || `uintptr_t`       | `0`\ `UINTPTR_MAX`
`ptrdiff_t`      | `PTRDIFF_MIN`\ `PTRDIFF_MAX`           ||                   |
                 |                                        || `size_t`          | `0`\ `SIZE_MAX`
