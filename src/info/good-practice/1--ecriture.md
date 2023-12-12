//// title = "Bien écrire"
//// description = "Les bonnes habitudes à prendre quand vous écrivez du code"

# {=title}

La première étape sera toujours que votre code soit lisible, ce qui repose sur plusieurs facteurs :

## Bien indenter

Je pense qu’il n’y a pas besoin d’expliquer pourquoi c’est capital :

;;; counterexample
```c
void analogWrite(uint8_t pin, uint32_t value, uint32_t valueMax) {
int channel = analogWriteChannel(pin);

// Make sure the pin was attached to a channel, if not do nothing
if (channel != -1 && channel < 16) {
  uint8_t resolution = _analog_write_channels[channel].resolution;
  uint32_t levels = pow(2, resolution);
   uint32_t duty = ((levels - 1) / valueMax) * min(value, valueMax);

// write duty to LEDC
   ledcWrite(channel, duty);
}
}
```
;;; code
```c
void analogWrite(uint8_t pin, uint32_t value, uint32_t valueMax) {
	int channel = analogWriteChannel(pin);

	// Make sure the pin was attached to a channel, if not do nothing
	if (channel != -1 && channel < 16) {
		uint8_t resolution = _analog_write_channels[channel].resolution;
		uint32_t levels = pow(2, resolution);
		uint32_t duty = ((levels - 1) / valueMax) * min(value, valueMax);

		// write duty to LEDC
		ledcWrite(channel, duty);
	}
}
```
;;;

Je n’épiloguerai pas à propos de quelle indentation utiliser parce que c’est les chocolatines de l’informatique, dans ce document tout utilise 4 espaces pour des raisons techniques, en pratique j’utilise des tabulations parce que ça s’adapte aux préférences de chacun mais c’est comme vous voulez. Par contre **assurez-vous que toute l’équipe utilise la même indentation**, sinon ça devient vite un cauchemar. Et par pitié, n’indentez pas avec 3 ou 5 espaces.

## Bien nommer

Beaucoup de vieux profs d’info utilisent des noms de variables à une lettre parce qu’à leur époque l’informatique était enseignée mathématiquement, ou des abréviations au-delà de la compréhension humaine.

**Utilisez TOUJOURS des noms de variables descriptifs**. Il faut toujours que le sens d’une variable soit évident rien qu’à son nom (au moins pour quelqu’un qui sait à quoi la fonction se rapporte), sans quoi il sera extrêmement difficile de reconstituer le sens du code dès que vous n’aurez plus la tête dedans pendant quelques jours. On voit souvent dans les tutos que « oui sinon si vous revenez sur votre projet dans 6 mois vous comprendrez plus rien » : c’est de la foutaise, un week-end suffit largement. Un compteur d’itération peut s’appeler `i` ou `j` (et c’est une information en soi tellement c’est habituel), mais c’est à peu près tout.

;;; counterexample
```c
// (Ça peut déjà paraître ridicule, et pourtant ici les abréviations sont bien meilleures
// et plus compréhensibles que dans beaucoup de codes qu’on peut trouver)
void send_anal(uint8_t p, uint32_t x, uint32_t xmax) {
	int ch = anal_chan(p);
	if (ch != -1 && ch < 16) {
		uint8_t res = anal_chs[ch].res;
		uint32_t l = pow(2, res);  // Le l, le 1 et le I se confondent facilement
		uint32_t dt = ((l - 1) / xmax) * min(x, xmax);
		ledcWrite(ch, dt);
	}
}
```
;;; code
```c
void analogWrite(uint8_t pin, uint32_t value, uint32_t valueMax) {
	int channel = analogWriteChannel(pin);
	if (channel != -1 && channel < 16) {
		uint8_t resolution = _analog_write_channels[channel].resolution;
		uint32_t levels = pow(2, resolution);
		uint32_t duty = ((levels - 1) / valueMax) * min(value, valueMax);
		ledcWrite(channel, duty);
	}
}
```
;;;

Ça s’applique bien sûr aussi aux noms de fonctions, constantes et de globalement tout ce qui a un nom.

### Les conventions de nommage

Vous noterez le format particulier de chaque type de nom dans l’exemple ci-dessus. En général, on a plusieurs moyens d’écrire des noms en plusieurs mots :

- `CamelCase` : première lettre de chaque mot en majuscule
- `dromedaryCase` : première lettre de chaque mot supplémentaire en majuscule
- `snake_case` : underscores à la place des espaces
- `SCREAMING_SNAKE_CASE` : tout en majuscule avec des underscores à la place des espaces
- `flatcase` : tout attaché (ça se tient si vous aimez pas la `snake_case` mais c’est pas terrible quand les noms sont longs)

Les conventions de nommage sont propres à chaque projet, personne ou langage. On a souvent certaines conventions qui s’imposent par cohérence avec la bibliothèque standard ou une librairie utilisée par le projet, mais ultimement c’est à votre préférence. On a souvent ce type de conventions (ou des combinaisons entre elles) :

Langage | Conventions fréquentes
------- | ----------------------
C       | `nomDeVariable`, `nomDeFonction()`, `UNE_CONSTANTE`, `VALEUR_ENUMEREE`, `MonType`\ `nom_de_variable`, `nom_de_fonction()`, `UNE_CONSTANTE`, `VALEUR_ENUMEREE`, `montype_t`
C++     | `nomDeVariable`, `nomDeFonction()`, `NomDeClasse` `UNE_CONSTANTE`, `MonEnum::ValeurEnumeree`
Java    | `nomDeVariable`, `nomDeMethode()`, `ClasseOuInterface`, `UNE_CONSTANTE`, `monpackage`
Python  | `nom_de_variable`, `nom_de_fonction()`, `NomDeClasse`, `UNE_CONSTANTE`, `monmodule`

On note presque universellement les constantes globales `EN_MAJUSCULES` et les classes `EnCamelCase`, mais le reste est assez libre tant que vous restez cohérent au sein du même projet.

Vous noterez `_analog_write_channels` dans l’exemple précédent : souvent, **commencer** le nom **par un underscore** dénote quelque chose d’**usage interne**, qui ne devrait pas être utilisé à l’extérieur : ici c’est un tableau de paramètres spécifiques au module.

On croise parfois des noms commençant par deux underscores, c’est plutôt pour indiquer des noms réservés au-delà du simple code, par exemple des méthodes spéciales en Python (comme pour surcharger les opérateurs arithmétiques : `__add__`, `__mul__`), ou en C/C++ des macros définies par le compilateur-même qui ont un usage très spécifique et ne doivent surtout pas être écrasées.

### Les nombres magiques

Dans le code, ce qu’on appelle un nombre magique, c’est une **valeur littérale** qui n’a **aucun sens apparent**. Exemple :

;;; counterexample ```c
int inputMode = getInputMode(user);
char buffer[50];
switch (inputMode) {
	case 0: strcpy(buffer, "<null>"); break;
	case 1: fgets(buffer, 50, stdin); break;
	case 2: {
		FILE* inputFile = fopen("data/input.dat", "r");
		if (inputFile != NULL) {
			fgets(buffer, 50, inputFile);
			fclose(inputFile);
		}
		break;
	default:
		fprintf(stderr, "Invalid input mode");
		break;
}
```
;;;

On remarque deux choses :

- On a une taille de tableau qu’on **répète 3 fois**, et c’est un paramètre qui peut causer des bugs pénibles s’il est mal renseigné. Une faute de frappe à un seul endroit du code pourra poser des problèmes, et si vous voulez changer la valeur il faudra la modifier manuellement partout (et si vous oubliez un endroit c’est le cauchemar).
- La valeur de `inputMode` est **opaque**, aucun moyen de savoir à quoi chaque valeur correspond sans creuser dans le code que ça conditionne,

Ce sont les exemples les plus courants de valeurs magiques, qu’il vaut mieux tous éviter dans la mesure du possible :

- Pour ne pas répéter plusieurs fois un même paramètre, il vaut mieux utiliser une constante de préprocesseur.
- Notre paramètre `inputMode` est un ensemble fini d’options qui ont chacune un sens particulier, ce qui est précisément à quoi servent les **énumérations**. D’ailleurs, avec une énumération vous aurez moins besoin de vérifier les valeurs invalides (ou alors si la valeur est invalide c’est que quelqu’un a très mal utilisé votre énumération)

;;; code
```c
#define INPUT_BUFFER_SIZE 50
#define INPUT_FILE_PATH "data/input.dat"

typedef enum {
    NO_INPUT, CONSOLE_INPUT, FILE_INPUT,
} inputmode_t;
// ...

inputmode_t inputMode = getInputMode(user);
char buffer[INPUT_BUFFER_SIZE];
switch (inputMode) {
	case NO_INPUT:      strcpy(buffer, "<null>"); break;
	case CONSOLE_INPUT: fgets(buffer, INPUT_BUFFER_SIZE, stdin); break;
	case FILE_INPUT: {
		FILE* inputFile = fopen(INPUT_FILE_PATH, "r");
		if (inputFile != NULL) {
			fgets(buffer, INPUT_BUFFER_SIZE, inputFile);
			fclose(inputFile);
		}
		break;
	}
}
```
;;;

## Bien aérer

Ça peut paraître bête,mais mettre des espaces et sauter des lignes là où c’est pertinent,c’est un énorme gain de lisibilité pour une perte de temps inexistante dès que vous avez un peu pris l’habitude,c’est comme d’habitude en typographie:on espace là où on peut prendre des repères,parce que sinon c’est moche et pénible à lire,et ça plus ne pas éclater en paragraphes,ça fait quelque chose à l’apparence d’un parpaing,et pareil pour le placement des commentaires,une ligne trop longue peut être pénible à lire voire à afficher,et un commentaire en fin de ligne attirera moins l’attention qu’un commentaire sur sa propre ligne,donc pour commenter l’effet général d’un bloc de code,ça peut être bien de faire ça sur une ligne à part.

;;; counterexample
```c
// (C’est à peine exagéré par rapport à une bonne moitié du code qu’on trouve sur internet et chez les étudiants)
void analogWrite(uint8_t pin,uint32_t value,uint32_t valueMax){
	int channel=analogWriteChannel(pin);
	if(channel!=-1&&channel<16){//Make sure the pin was attached to a channel, if not do nothing
		uint8_t resolution=_analog_write_channels[channel].resolution;
		uint32_t levels=pow(2,resolution);
		uint32_t duty=((levels-1)/valueMax)*min(value,valueMax);
		ledcWrite(channel,duty);//write duty to LEDC
	}
}
```
;;; code
```c
void analogWrite(uint8_t pin, uint32_t value, uint32_t valueMax) {
	int channel = analogWriteChannel(pin);

	// Make sure the pin was attached to a channel, if not do nothing
	if (channel != -1 && channel < 16) {
		uint8_t resolution = _analog_write_channels[channel].resolution;
		uint32_t levels = pow(2, resolution);
		uint32_t duty = ((levels - 1) / valueMax) * min(value, valueMax);

		// write duty to LEDC
		ledcWrite(channel, duty);
	}
}
```
;;;

Je n’épiloguerai pas non plus sur le placement des accolades, c’est un autre débat éternel et vide de sens.

Pour un exemple plus réel et un peu de rigolade :

;;; counterexample
```python
# Je vous présente un authentique code écrit par mon ancien moi de juin 2017
# Et ça c'est du Python, imaginez du C comme ça
nametable=struct.pack('<I',len(filenames))+nametable
hdrdata=ltbl+lmtl+lfnl+'\x00\x00\x00\x00'+nametable+symtable
data=hdrdata+sarc
lmtloffset=0x28+len(ltbl)
lfnloffset=lmtloffset+len(lmtl)
endlfnloffset=lfnloffset+len(lfnl)
hdrflag=int(fread('_alyt.repack.meta/alyt.flags'))
alytheader=struct.pack('<4sIIIIIIIII','ALYT',0x28,hdrflag,len(ltbl),lmtloffset,
len(lmtl),lfnloffset,len(lfnl),endlfnloffset,len(data)+0x28)
alyt=alytheader+data
finalname=fread('_alyt.repack.meta/alyt.bsname')+'.repacked'```
;;;
