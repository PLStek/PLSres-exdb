//// title = "Les unions"
//// description = "L’utilisation des unions en C"

# {=title}

En C, une `union` est une zone mémoire qui peut avoir plusieurs types différents à la fois. Autrement dit, une union permet d’interpréter une même zone mémoire de différentes façons. Ça se définit un peu comme une structure, sauf que les champs seront superposés sur la même zone mémoire au lieu d’être les uns à la suite des autres.

;;; code ```c
typedef union {
	int value;
	uint8_t bytes[4];
} int_split_t;

int_split_t variable = {.value = 155};
printf("%c %c %c %c\n", variable.bytes[0], variable.bytes[1], variable.bytes[2], variable.bytes[3]);
```
;;;

Ça sert globalement à deux choses :

- Interpréter les mêmes données sous plusieurs formes différentes
- Permettre plusieurs types possibles pour une même variable. Dans ce cas il faudra l’information du type réel de la valeur, donc ce sera souvent dans une structure de ce type :

;;; example ```c
typedef struct {
	bool is_integer;
	union {
		int integer;
		char* string;
	} value;
} int_or_string;

int_or_string variable = {.is_integer = true, .value = {.integer = 2}};
if (variable.is_integer)
	printf("%d\n", variable.value.integer);
else
	printf("%s\n", variable.value.string);```
;;;

C’est une approche qui n’est pas très recommandée, C est un langage typé fortement et statiquement pour de bonnes raisons, et les unions court-circuitent un peu ça. Du coup, le compilateur est beaucoup moins capable de détecter les erreurs de typage avec des unions. Cela dit, c’est déjà beaucoup mieux contrôlé que des pointeurs sur `void`. C’est aussi assez nettement plus lourd à l’écriture, et ça mène parfois à des horreurs comme ce magnifique exemple d’unions anonymes dans une structure (non seulement ce sont des champs sans noms ce qui est vraiment pas bien, mais en plus c’est des unions donc ça rend l’accès encore plus compliqué dans le code), ce qui est une des pires abominations que vous pouvez faire en C, tiré d’une authentique librairie SPI :

;;; counterexample ```c
struct spi_transaction_t {
   uint32_t flags;                 ///< Bitwise OR of SPI_TRANS_* flags
   uint16_t cmd;                   /**< Command data, of which the length is set in the ``command_bits`` of spi_device_interface_config_t.
                                     *
                                     *  <b>NOTE: this field, used to be "command" in ESP-IDF 2.1 and before, is re-written to be used in a new way in ESP-IDF 3.0.</b>
                                     *
                                     *  Example: write 0x0123 and command_bits=12 to send command 0x12, 0x3_ (in previous version, you may have to write 0x3_12).
                                     */
   uint64_t addr;                  /**< Address data, of which the length is set in the ``address_bits`` of spi_device_interface_config_t.
                                     *
                                     *  <b>NOTE: this field, used to be "address" in ESP-IDF 2.1 and before, is re-written to be used in a new way in ESP-IDF3.0.</b>
                                     *
                                     *  Example: write 0x123400 and address_bits=24 to send address of 0x12, 0x34, 0x00 (in previous version, you may have to write 0x12340000).
                                     */
   size_t length;                  ///< Total data length, in bits
   size_t rxlength;                ///< Total data length received, should be not greater than ``length`` in full-duplex mode (0 defaults this to the value of ``length``).
   void *user;                     ///< User-defined variable. Can be used to store eg transaction ID.
   union {
       const void *tx_buffer;      ///< Pointer to transmit buffer, or NULL for no MOSI phase
       uint8_t tx_data[4];         ///< If SPI_USE_TXDATA is set, data set here is sent directly from this variable.
   };
   union {
       void *rx_buffer;            ///< Pointer to receive buffer, or NULL for no MISO phase. Written by 4 bytes-unit if DMA is used.
       uint8_t rx_data[4];         ///< If SPI_USE_RXDATA is set, data is received directly to this variable
   };
} ;        //the rx data should start from a 32-bit aligned address to get around dma issue.
```
;;;
