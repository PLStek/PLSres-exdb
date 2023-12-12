//// title = "Le concept d'algorithme"
//// description = "Le mode de pensée algorithmique"

# {=title}
## La conception algorithmique

De façon très basique, un **algorithme** est une **description** précise des **actions** nécessaires pour réaliser une tâche. Précise comme « interprétable par une machine » (un ordi c'est très, *très* con).

Vous verrez en gros deux définition du terme « algorithme » :

- La définition commune, qui est en gros la façon (abstraite) de réaliser une tâche dans un programme
- La définition de beaucoup de cours d'informatique théorique, où un algorithme est un document de conception du code qui réalisera la tâche

### Le fond d'un algorithme

L'algo est la façon de réaliser la tâche dans un programme informatique. C'est globalement l'idée, la façon de conceptualiser et de formaliser la résolution d'un problème. L'exemple typique est celui de la recette de cuisine : on décrit étape par étape la façon de faire.

### La forme d'un algorithme

Là c'est plus compliqué et plus controversé. Par définition, un algorithme n'a pas de forme propre, cela dit c'est souvent intéressant de le sortir sous forme écrite, ne serait-ce que pour le documenter ou l'expliquer de façon générique. Certains profs décrivent ça sous une syntaxe formelle et un niveau spécifique, qui serait prétendument universelle, générique et compréhensible quel que soit le bac de connaissances de chacun. C'est un peu idéaliste, pour plein de raisons :

- Déjà, ces modes d'écriture impliquent généralement un paradigme **impératif** (où on décrit la *manière* de faire), ce qui est loin d'être le cas de tous les langages : beaucoup sont plus ou moins déclaratifs (on dit *ce qu'on veut faire* et pas forcément *comment*), voire des choses un peu plus transverses, comme le paradigme fonctionnel. Une telle écriture de l'algorithme a donc déjà forcément des préjugés sur la technologie finale.
- Mais ça c'est encore peu de chose : quand on décrit un algorithme, on doit choisir un certain niveau d'abstraction. On ne peut pas être parfaitement générique, si on écrit quelque chose on a déjà des préjugés. À vous de voir le niveau d'abstraction qui est pertinent dans votre cas
- Et même en dehors des considérations techniques, il peut y avoir d'autres barrières : langue, niveau de compréhension, ... Il faut aussi adapter la documentation à son public. Ne sous-estimez pas les représentations **schématiques**.

En général, ce doc va utiliser des syntaxes diverses et variées et des niveaux d'abstractions qui changent selon ce qui est pertinent, donc ne vous attachez pas trop à la syntaxe. Si vos profs demandaient une syntaxe particulière, suivez leurs directives.

{!exercise: info.algo.syntaxe-algorithme}
