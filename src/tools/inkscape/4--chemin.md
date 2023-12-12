//// title = "Les chemins"
//// description = "Utiliser directement les chemins dans Inkscape"

# {=title}

Ce qu’on appelle « chemin » est la base fondamentale de tout ce qu’il y aura de plus complexe que des formes simples dans Inkscape (et en SVG en général). C’est simple : un chemin est un ensemble de points reliés par des lignes ou des courbes. Vous pouvez faire quasiment tout avec des chemins, donc le sujet est vaste.

## {!svg: tools/inkscape/icons/draw-path.svg} Tracer un chemin

L’outil chemin {!svg: tools/inkscape/icons/draw-path.svg} est à la base de la création de chemins. À la base, cliquez juste là où vous voulez placer les points. Maintenez ctrl pour placer les points à des angles précis (par incréments de 15°)

{!img: tools/inkscape/4-toolbar.png}

L’option « forme » permet de donner des formes particulières au contour, mais ce qui est vraiment intéressant, c’est les 5 modes de tracé à gauche de la barre d’outil :

- {!svg: tools/inkscape/icons/path-mode-bezier.svg} Courbes de Bézier : entre chaque point, vous pouvez (ou pas) mettre une courbe de Bézier — pour la définir, cliquez-glisser quand vous ajoutez un point au lieu de seulement cliquer

{!img: tools/inkscape/4-bezier.png}

- {!svg: tools/inkscape/icons/path-mode-spiro.svg} Courbes spirographiques
- {!svg: tools/inkscape/icons/path-mode-bspline.svg} B-splines entre les points définis
- {!svg: tools/inkscape/icons/path-mode-polyline.svg} Simple ligne brisée entre les points
- {!svg: tools/inkscape/icons/path-mode-polyline-paraxial.svg} Ligne brisée à angles droits

Pendant que vous créez un chemin, vous pouvez utiliser Ctrl+Z pour supprimer le dernier point ajouté. Pour fermer le chemin, il suffit de mettre le dernier point sur la poignée de la première extrémité :

{!img: tools/inkscape/4-close.png}

Sinon, vous pouvez terminer le chemin avec un clic droit, double clic ou entrée, ou annuler le tracé avec échap.

Il est également possible de continuer un chemin existant en le sélectionnant et en partant de la poignée à une des extrémités : ça poursuivra alors ce même chemin plutôt que d’en créer un nouveau.

{!img: tools/inkscape/4-continue.png}

## {!svg: tools/inkscape/icons/tool-node-editor.svg} Modifier un chemin

L’outil d’édition de chemin {!svg: tools/inkscape/icons/tool-node-editor.svg} permet de bricoler le chemin après coup, en détails.

{!img: tools/inkscape/4-edit-nodes.png}

Tout d’abord, vous voyez chaque point du chemin sous forme de poignées, qui ont 3 formes possibles :

- Les losanges sont des « nœuds durs », qui forment des angles
- Les carrés sont des « nœuds doux », qui forment des courbes
- Les cercles sont des « nœuds automatiques », qui sont comme des nœuds doux mais qui adapteront leur propre paramétrage si vous les déplacez sur la courbe pour ne pas la dénaturer.

Vous pouvez déplacer ces nœuds individuellement, ou en groupes en les sélectionnant en maintenant maj ou en les englobant par un cliquer-glisser. Utiliser la molette de la souris en pointant un nœud sélectionnera les nœuds adjacents de proche en proche. Vous voyez aussi comme des tangentes avec des poignées à chaque bout, ce sont les contrôles de courbure, vous pouvez aussi les déplacer pour paramétrer les courbes. Pendant que vous cliquez-glissez sur un nœud, maintenir maj étendra un nouveau contrôle de courbure à partir du nœud, et maintenir ctrl forcera à garder le nœud à la même abcisse ou ordonnée que sa position d’origine pendant le déplacement.

Vous avez également des pelletées d’options pour manipuler directement le chemin. La première section permet d’ajouter ou de supprimer directement des nœuds arbitraires :

- {!svg: tools/inkscape/icons/node-add.svg} Ajoute un nœud au milieu de chaque segment sélectionnés (un segment = deux nœuds contigus sélectionnés). Les nouveaux nœuds sont ajustés automatiquement pour garder l’apparence du chemin identique.
- {!svg: tools/inkscape/icons/node-delete.svg} Supprime le ou les nœuds sélectionnés. Les nœuds adjacents seront ajustés pour compenser au mieux (avec des résultats de qualité variable)
- Le petit menu déroulant a des options pour rajouter des nœuds à différentes positions du segment sélectionné (abcisse ou ordonnée minimale ou maximale)

Les options suivantes permettent de casser ou rejoindre des morceaux du chemin au niveau d’un nœud :

- {!svg: tools/inkscape/icons/node-join.svg} Rejoint deux nœuds en un seul, en essayant d’adapter au mieux pour modifier le moins possible l’apparence du chemin
- {!svg: tools/inkscape/icons/node-break.svg} Casse le nœud sélectionné en deux nœuds distincts que vous pouvez ensuite bouger séparément (ils sont initialement superposés, bougez-en un et vous verrez)

La section suivante casse ou rejoint le chemin, mais cette fois au niveau d’un segment :

- {!svg: tools/inkscape/icons/node-join-segment.svg} Prend les deux nœuds disjoints sélectionnés, et les relie par un segment
- {!svg: tools/inkscape/icons/node-delete-segment.svg} Prend les deux nœuds joints sélectionnés, et supprime le segment entre les deux (ils seront donc disjoints après l’opération)

Vous avez aussi des options pour modifier les types de nœuds :

- {!svg: tools/inkscape/icons/node-type-cusp.svg} Transforme en nœud dur (angle)
- {!svg: tools/inkscape/icons/node-type-smooth.svg} Transforme en nœud doux (courbe)
- {!svg: tools/inkscape/icons/node-type-symmetric.svg} Rend le contrôle de courbure d’un nœud doux symétrique (pour rendre la courbe symétrique par rapport à ce nœud)
- {!svg: tools/inkscape/icons/node-type-auto-smooth.svg} Transforme en nœud automatique, qui s’adaptera tout seul pour modifier aussi peu que possible l’apparence du chemin quand vous le déplacez (par exemple en adaptant sa courbure pour conserver la courbure existante même après déplacement, contrairement à un nœud doux classique qui garde le même contrôle)

- {!svg: tools/inkscape/icons/node-segment-line.svg} Rend le segment (deux nœuds adjacents sélectionnés) droit, donc supprime la courbure entre les deux nœuds
- {!svg: tools/inkscape/icons/node-segment-curve.svg} Rend le segment sélectionné courbe. Ça ne le rend pas directement courbe, mais ça crée des contrôles sur les deux extrémités pour éditer vous-même la courbure

Les deux options suivantes servent à la conversion d’autres objets en chemins

- {!svg: tools/inkscape/icons/object-to-path.svg} Convertit un autre objet (rectangle, ellipse, etc.) en chemin, pour pouvoir directement manipuler les points plutôt que la figure en général
- {!svg: tools/inkscape/icons/stroke-to-path.svg} Convertit un contour en chemin. Ça prend donc le contour d’un autre objet, tel qu’il apparaît (y compris tous les effets de style dessus), et ça le transforme en un chemin à la forme de ce contour.

Vous avez ensuite la position du chemin par rapport au document, puis quelques options d’affichage :

- {!svg: tools/inkscape/icons/path-clip-edit.svg} Voir et modifier le « chemin de découpe » (clipping) de l’objet. On verra juste après comment faire ça, mais en gros c’est un chemin qui va permettre d’en découper un autre (par exemple, la gomme en mode chemin de découpe utilise ça)
- {!svg: tools/inkscape/icons/path-mask-edit.svg} Voir et modifier le masque, un objet qui permet de contrôler ce qui s’affiche plus ou moins dans un autre (pareil, on verra ça un peu plus loin sur cette page)

## Autres outils de modification

Dans le menu chemin, vous avez quelques autres options pour modifier un chemin :

- Les options *objet en chemin* et *contour en chemin* sont les mêmes que dans la barre d’outil de l’édition de chemin
- L’option *séparer* permet de séparer des sous-chemins (parties disjointes d’un même chemin) en chemins distincts. Par exemple, j’ai ici un chemin qui était à la base une seule forme, mais dont j’ai bricoler quelques segments, et maintenant j’ai deux parties mais en un seul et même chemin. Pour les séparer proprement en deux objets distincts, je peux utiliser l’option *séparer*

{!img: tools/inkscape/4-subpaths.png}

- Et à l’inverse, l’option *combiner* permet de rassembler deux objets en un seul et même chemin, ce qui peut ensuite vous permettre de les relier comme vous voulez en éditant les segments et les sommets

Vous avez ensuite les options de manipulation directe du chemin :

{!svg: tools/inkscape/4-path-unops.svg}

- L’option *éroder* va en quelque sorte réduire l’épaisseur du chemin en grattant une même épaisseur sur tous les contours
- À l’inverse, *dilater* épaissit le chemin

Ces deux options ne sont pas très flexibles, c’est pour ça que vous avez le *décalage dynamique* :

- L’option *décalage dynamique* convertit le chemin en un objet de décalage dynamique, quand vous utilisez l’éditeur de chemin {!svg: tools/inkscape/icons/tool-node-editor.svg} dessus, vous aurez une unique poignée qui vous permettra de dilater ou éroder comme vous le souhaitez
- Le *décalage lié* crée un objet de décalage dynamique en tant que clone (donc une copie qui suivra certaines modifications de l’original, mais que vous pouvez éroder ou dilater séparément)

Enfin, l’option *simplifier* réduit le nombre de points du chemin en essayant de perdre au minimum la forme du chemin.

## Interaction entre les chemins

Jusque-là, on a vu comment créer et bricoler des chemins, ce qui représente une bonne partie de leur utilité, mais toute leur puissance vient de ce que peuvent faire leurs interactions. Notez qu’ici je parle de chemins, mais ça marche avec n’importe quel objet, les autres types d’objets seront juste convertis en chemin au passage sans autre problème.

### Opérations logiques

Le menu chemin offre plusieurs opérations booléennes entre chemins. On prendra ceci comme base, une ellipse et un rectangle superposés. L’ordre de superposition est important : c’est toujours l’objet de dessous qui est modifié par celui de dessus. Ici, dans tous les cas, l’ellipse est sélectionnée en premier et le rectangle en deuxième.

{!svg: tools/inkscape/4-boolean-base.svg}

- {!svg: tools/inkscape/icons/path-union.svg} L’union combine la forme des deux chemins

{!svg: tools/inkscape/4-boolean-union.svg}

- {!svg: tools/inkscape/icons/path-difference.svg} La différence exclut la forme de l’objet du dessus de l’objet du dessous

{!svg: tools/inkscape/4-boolean-difference.svg}

- {!svg: tools/inkscape/icons/path-intersection.svg} L’intersection ne garde que les parties du chemin du dessous qui sont au même endroit que des parties de celui du dessus

{!svg: tools/inkscape/4-boolean-intersection.svg}

- {!svg: tools/inkscape/icons/path-exclusion.svg} L’exclusion conserve seulement les parties qui sont dans l’un des deux objets mais pas dans les deux

{!svg: tools/inkscape/4-boolean-exclusion.svg}

- {!svg: tools/inkscape/icons/path-division.svg} La division découpe le chemin de dessous en plusieurs objets là où le contour de celui de dessus le recoupe (par exemple ci-dessous vous le voyez au contour des trois objets résultants)

{!svg: tools/inkscape/4-boolean-division.svg}

- {!svg: tools/inkscape/icons/path-cut.svg} Le découpage éclate complètement le contour de l’objet du dessous là où celui du dessus le recoupe. Du coup ça ne garde que le contour, découpé à chaque intersection entre le contour des deux objets. Pour l’exemple ci-dessous, chaque partie découpée a été colorée différemment pour la démo.

{!svg: tools/inkscape/4-boolean-cut.svg}

### Le clipping

Un chemin peut être spécifié comme zone de clipping d’un autre. Seules les zones du chemin clippé qui sont à l’intérieur de la zone de clipping seront alors apparentes.
Mettons que j’ai une étoile dont je veux éliminer les pointes. J’ai mon étoile, je crée un cercle (ici en rouge) qui servira de zone de clipping, que je place au centre de l’étoile. Ensuite, il suffit de sélectionner d’abord l’objet à clipper (l’étoile), puis la zone de clipping (le cercle) en maintenant maj, et aller dans le menu objet > découpe > créer une découpe.

{!svg: tools/inkscape/4-clipping.svg}

Ça fait à peu près la même chose qu’une intersection, sauf qu’avec une zone de clipping les deux chemins seront conservés, vous pouvez donc revenir plus tard et supprimer le clipping avec objet > découpe > relâcher la découpe, ou bien le modifier avec l’option adaptée ({!svg: tools/inkscape/icons/path-clip-edit.svg}) de l’éditeur de chemin {!svg: tools/inkscape/icons/tool-node-editor.svg}.

Vous pouvez aussi avoir la logique inverse, ne laisser que les parties hors de la zone de clipping apparente, pour faire comme une différence avec les mêmes avantages. Pour cela, même manip, mais avec objet > découpe > découpe inversée.

{!svg: tools/inkscape/4-inverse-clipping.svg}

### Les masques

Un masque se comporte un peu comme une zone de découpe, mais en définissant la transparence de l’objet masqué en fonction du masque plutôt que de simplement découper. Le masque peut donc être n’importe quel objet, et plus sa couleur sera claire, plus l’objet masqué sera opaque à cet endroit. Pour cela même chose, on sélectionne d’abord l’objet à masquer, puis le masque et c’est dans le menu objet > masque > définir un masque. Par exemple, ici on utilise une étoile grise avec un contour blanc. Ça veut dire que là où il y a le fond gris, l’objet masqué sera partiellement translucide (proportionnellement à la luminosité de la couleur), et là où il y a le contour blanc, l’objet masqué sera totalement opaque. Les endroits noirs ou vides dans le masque donneront des zones totalement transparentes. Dans l’exemple ci-dessous, le rectangle bleu est juste derrière pour montrer la transparence.

{!svg: tools/inkscape/4-mask.svg}

On peut faire un « masque inversé » avec objet > masque > définir un masque inversé. Ça marche pareil, sauf que les parties où le masque est vide restent opaques au lieu de devenir transparentes

{!svg: tools/inkscape/4-mask-test.svg}
