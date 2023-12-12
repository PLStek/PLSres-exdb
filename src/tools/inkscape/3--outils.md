//// title = "Les outils"
//// description = "Les outils disponibles dans Inkscape"

# {=title}

C’est parti, on va commencer par parler des différents outils disponibles dans Inkscape. Ils sont dans la barre d’outils de gauche :

- {!svg: tools/inkscape/icons/tool-pointer.svg} Sélection
- {!svg: tools/inkscape/icons/tool-node-editor.svg} Édition de chemin
- {!svg: tools/inkscape/icons/draw-rectangle.svg} Rectangle
- {!svg: tools/inkscape/icons/draw-ellipse.svg} Ellipse
- {!svg: tools/inkscape/icons/draw-polygon-star.svg} Polygone ou étoile
- {!svg: tools/inkscape/icons/draw-cuboid.svg} Boite 3D
- {!svg: tools/inkscape/icons/draw-spiral.svg} Spirale
- {!svg: tools/inkscape/icons/draw-path.svg} Chemin
- {!svg: tools/inkscape/icons/draw-freehand.svg} Tracé à main levée
- {!svg: tools/inkscape/icons/draw-calligraphic.svg} Tracé calligraphique
- {!svg: tools/inkscape/icons/draw-text.svg} Texte
- {!svg: tools/inkscape/icons/color-gradient.svg} Dégradé
- {!svg: tools/inkscape/icons/mesh-gradient.svg} Filet de dégradé
- {!svg: tools/inkscape/icons/color-picker.svg} Extraction de couleur
- {!svg: tools/inkscape/icons/color-fill.svg} Remplissage
- {!svg: tools/inkscape/icons/tool-tweak.svg} Édition fine
- {!svg: tools/inkscape/icons/tool-spray.svg} Spray
- {!svg: tools/inkscape/icons/draw-eraser.svg} Gomme
- {!svg: tools/inkscape/icons/draw-connector.svg} Connecteur
- {!svg: tools/inkscape/icons/tool-measure.svg} Mesure de distance / angle
- {!svg: tools/inkscape/icons/tool-pages.svg} Édition de page

On va parler de tous ces outils, sauf les {> tools.inkscape.chemin: chemins} et le {> tools.inkscape.texte: texte} qui sont tellements vastes et importants qu’il ont leur propre page, de même que les {> tools.inkscape.couleur: options de colorisations}.

Pour chaque outil, vous avez :

- Son utilité de base, évidemment,
- Souvent des modificateurs, en appuyant sur la touche ctrl, maj ou alt en même temps que vous l’utilisez, qui permettent souvent de changer ou de contraindre ce que ça fait (par exemple pour l’outil rectangle, maintenir ctrl contraint les proportions, et maj le fait tracer à partir du centre)
- Des options que vous trouverez dans la barre du haut

En général, cliquer sur un élément en ayant activé l’outil qui l’a créé, ou double-cliquer sur l’objet avec l’outil sélection, redonnera les options spécifiques de l’outil que vous pouvez appliquer.

## {!svg: tools/inkscape/icons/tool-pointer.svg} Sélection

L’outil de sélection est sans doute le plus important, il permet de sélectionner des objets, et d’appliquer certaines modifications dessus

- En maintenant maj, vous pouvez sélectionner plusieurs objets à la fois
- En maintenant ctrl, vous pouvez sélectionner des objets à l’intérieur de groupes plutôt que le groupe complet
- En maintenant alt, vous sélectionnerez tout les objets que vous toucherez pendant un cliquer-glisser

{!img: tools/inkscape/3-pointer-tools.png}

Tout d’abord, la manière la plus simple de sélectionner un ou des objets est de simplement cliquer dessus. Pour sélectionner plusieurs objets, vous pouvez cliquer-glisser pour englober les objets que vous voulez, et/ou maintenir maj. Vous avez également quelques autres options en barre d’outil :

- {!svg: tools/inkscape/icons/edit-select-all-symbolic.svg} Sélectionner tous les objets du {> tools.inkscape.calque: calque} actuel (raccourci Ctrl + A)
- {!svg: tools/inkscape/icons/edit-select-all-layers.svg} Sélectionner tous les objets de tous les calques visibles
- {!svg: tools/inkscape/icons/edit-select-none.svg} Tout désélectionner

Vous avez également l’option {!svg: tools/inkscape/icons/selection-touch.svg} : par défaut, le cliquer-glisser sélectionnera tous les objets que vous *englobez entièrement* — avec cette option, ça sélectionnera tout ce que vous *toucherez* simplement.

Une fois vos objets sélectionnés, vous aurez ce type d’options dessus :

{!img: tools/inkscape/3-pointer-resize.png}

Les poignées permettent de redimensionner l’objet. Si vous avez plusieurs objets sélectionnés, ça les redimensionnera tous ensemble, pas un par un.

- Maintenir maj pendant que vous redimensionnez fera redimensionner à partir du centre de l’objet (l’étirement sera symétrique)
- Mainterir ctrl forcera à conserver les proportions

Attention, le resultat sera différent en fonction des options sélectionnées tout à droite de la barre d’outils :

- {!svg: tools/inkscape/icons/transform-affect-stroke.svg} Préserver la proportion de l’épaisseur des contours par rapport à la forme en redimensionnant : activé, ça redimensionnera les contours avec, désactivé les contours garderont toujours la même épaisseur après redimensionnement

{!svg: tools/inkscape/3-select-transform-stroke.svg}

- {!svg: tools/inkscape/icons/transform-affect-rounded-corners.svg} Préserver la proportion de l’arrondissement des coins par rapport au rectangle complet : activé, les arrondis seront étirés avec le reste, désactivé, l’arrondi gardera la même taille et les côtés seront rallongés/raccourcis sans eux

{!svg: tools/inkscape/3-select-transform-corners.svg}

- {!svg: tools/inkscape/icons/transform-affect-gradient.svg} Associer le dégradé à la forme dans le redimensionnement : activé, le dégradé sera étiré avec la forme, désactivé, le dégradé sera statique et la forme sera étirée « au-dessus »

{!svg: tools/inkscape/3-select-transform-gradient.svg}

- {!svg: tools/inkscape/icons/transform-affect-pattern.svg} Fait pareil mais pour les remplissages par motifs : activé, le motif est étiré avec la forme, désactivé, le motif reste le même et la forme est étirée dedans

{!svg: tools/inkscape/3-select-transform-pattern.svg}

Si vous cliquez une deuxième fois sur l’objet, vous aurez les poignées de rotation :

{!img: tools/inkscape/3-pointer-rotate.png}

Les poignées dans les coins permettent de faire tourner l’objet. Par défaut, l’objet tourne autour de son centre de rotation, qui est le point en surbrillance au milieu : vous pouvez le déplacer par un cliquer-glisser.

- Maintenir maj pendant la rotation fera tourner par rapport au coin opposé au lieu du centre de rotation de l’objet
- Maintenir ctrl fera tourner selon des angles précis (multiples de 15°)

Pareil, avec plusieurs objets sélectionnés ça les fera tourner en bloc.
Les poignées sur les côtés déforment l’objet en « l’inclinant ». Maintenir alt pendant la déformation fera incliner par incréments de 15°.

{!svg: tools/inkscape/3-select-rotate-example.svg}

Enfin, double-cliquer sur l’objet ramènera ses options d’origines, pour avoir les options spécifiques à l’objet.

La barre d’outil donne encore plusieurs options pour modifier ou déplacer l’objet sélectionné :

- {!svg: tools/inkscape/icons/object-rotate-left.svg} Tourne l’objet de 90° vers la gauche
- {!svg: tools/inkscape/icons/object-rotate-right.svg} Tourne l’objet de 90° vers la droite. Ces deux options sont équivalentes à utiliser les poignées de rotation, donc ça tient compte du centre de rotation
- {!svg: tools/inkscape/icons/object-flip-horizontal.svg} Retourne l’objet horizontalement (miroir)
- {!svg: tools/inkscape/icons/object-flip-vertical.svg} Retourne l’objet verticalement. Ces deux options sont équivalentes à utiliser les poignées d’inclinaison sur un demi-tour complet, donc ça tient aussi compte du centre de rotation

- {!svg: tools/inkscape/icons/selection-top.svg} Met l’objet au premier plan (il s’affichera par-dessus tous les autres qui se superposent avec lui)
- {!svg: tools/inkscape/icons/selection-raise.svg} Monte l’objet d’un cran par rapport aux autres (il s’affichera par-dessus un autre qui se superpose avec lui)
- {!svg: tools/inkscape/icons/selection-lower.svg} Descend l’objet d’un cran par rapport aux autres
- {!svg: tools/inkscape/icons/selection-bottom.svg} Met l’objet à l’arrière-plan (il s’affichera en-dessous de tous les autres)

- Les valeurs *X* et *Y* sont les coordonnées du coin supérieur gauche de l’objet
- Les valeurs *H* et *L* sont respectivement la hauteur et la largeur de l’objet. Ces options donnent la taille de la boite englobante complète, contour inclus, donc si vous voulez modifier ça à la source sans tenir compte du contour, utilisez l’outil d’origine (double-clic)
- {!svg: tools/inkscape/icons/object-unlocked.svg} Conserve les proportions quand vous modifiez *H* et *L*

## Outils de formes
### {!svg: tools/inkscape/icons/draw-rectangle.svg} Rectangle

Rien de bien exotique, ça fait des rectangles.

{!svg: tools/inkscape/3-rectangle.svg}

- En maintenant ctrl, ça contraindra les proportions (1:1 pour un carré, 1:1.618 (nombre d’or), 1:2, 1:3, etc.)
- En maintenant maj, ça étendra à partir du centre au lieu du coin supérieur gauche

Quand vous créez un nouveau rectangle, si vous cliquez de nouveau sur un rectangle existant avec l’outil rectangle, ou si vous double-cliquez dessus avec l’outil sélection, vous avez des options pour modifier votre rectangle :

{!img: tools/inkscape/3-rectangle-tools.png}

- Les petits carrés servent à agrandir ou rétrécir le rectangle
- Les petits cercles permettent de changer l’arrondissement des angles. Bougez-en un et l’arrondissement sera symétrique, ou vous pouvez utiliser les deux pour avoir un arrondi différent dans les deux sens.

{!svg: tools/inkscape/3-rectangle-round.svg}

La barre d’options vous donne juste de quoi éditer numériquement les dimensions du rectangle et les arrondis, et le dernier bouton à droite remet les coins en pointe si vous les avez arrondis au-delà du réparable.

### {!svg: tools/inkscape/icons/draw-ellipse.svg} Ellipse

Autre base fondamentale, les ellipses

{!svg: tools/inkscape/3-ellipse.svg}

Les modificateurs sont pareils que pour les rectangles :

- En maintenant ctrl vous contraindrez les proportions, ça permet notamment de faire des cercles
- En maintenant maj vous tracez en partant du centre

Les options sont les suivantes :

{!img: tools/inkscape/3-ellipse-tools.png}

- Les carrés servent toujours à agrandir ou réduire l’ellipse dans un sens ou dans l’autre
- Cette fois, les ronds permettent de tracer des parties d’ellipse / de cercle :
	- Les déplacer avec la souris à l’intérieur de l’ellipse tracera une corde
	- Les déplacer avec la souris à l’extérieur de l’ellipse tracera un secteur
- Dans tous les cas, vous avez les boutons dans la barre d’outil pour convertir en secteur, arc ouvert, arc fermé ou pour revenir à l’ellipse d’origine

{!svg: tools/inkscape/3-ellipse-sector.svg}

### {!svg: tools/inkscape/icons/draw-polygon-star.svg} Polygone

Cet outil permet de bidouiller à peu près n’importe quoi avec des polygones, et contrairement à ce que peut laisser penser l’icone ça ne sert pas qu’à faire des étoiles :

{!svg: tools/inkscape/3-polygon.svg}

La barre d’outil est déjà plus fournie. L’outil a deux modes : le mode polygone, qui permet de faire des polygones bien propres ; et le mode étoile, qui donne quelques options en plus pour faire des formes plus ou moins étoilées.

{!img: tools/inkscape/3-polygon-tools.png}

- Les petits losanges sur la forme permettent de bouger les sommets :
	- En mode polygone, ça permet juste de modifier la taille et l’orientation du polygone
	- En mode étoile :
		- Sur le sommet extérieur, c’est aussi pour la taille et l’orientation
		- Sur le sommet intérieur, vous pouvez bouger comme vous voulez pour modifier les proportions des branches, mais aussi leur angle, pour faire par exemple le genre de motif ci-dessus ; vous pouvez même croiser et faire tout un tas d’autres motifs.
- Comme son nom l’indique, le paramètre « sommets » permet de sélectionner le nombre de sommets
- *Ratio des segments* donne la proportion des branches de l’étoile (à quel point ils sont « enfoncés »)
- *Arrondi* permet d’arrondir les arètes, ça peut donner des formes comme le triangle arrondi plus haut
- *Hasard* disperse plus ou moins aléatoirement les sommets, bien utilisé ça peut faire des trucs comme la tache ci-dessus
- Et enfin le dernier bouton remet les paramètres par défaut

### {!svg: tools/inkscape/icons/draw-cuboid.svg} Boite 3D

Plutôt un outil de positionnement pour le dessin, ça crée des boites 3D en vous permettant de bidouiller la taille et les points de fuite :

{!img: tools/inkscape/3-3dbox.png}

Au bout des traits bleus, jaunes et rouges vous avez les points de fuites, les poignées permettent de bouger les sommets. Les boutons dans la barre d’outils permettent de mettre les différents points de fuite à l’infini, et dans ce cas vous pourrez adapter l’angle. Mettre les 3 points de fuite à l’infini vous donnera une projection orthogonale.

### {!svg: tools/inkscape/icons/draw-spiral.svg} Spirale

On ne dessine pas souvent des spirales, par contre comme on le verra après on peut positionner des objets par rapport à d’autres, donc ça peut bien servir en positionnement.

{!img: tools/inkscape/3-spiral.png}

La barre d’outil permet de bricoler un peu la forme de la spirale :

- *Tours* change le nombre de tours que fait la spirale entre ses extrémités
- *Divergence* permet des changements de densité :
 	- Une divergence à 1 donnera une densité uniforme
	- Une divergence supérieure à 1 fera que les tours seront de plus en plus rapprochés en approchant du centre
	- Une divergence inférieure à 1 fera que les tours seront de plus en plus rapprochés en approchant de l’extérieur
- *Rayon intérieur* permet d’éliminer une certaine proportion du centre de la spirale, plutôt que de commencer au centre

## Tracé

Comme dit précédemment, les {> tools.inkscape.chemin: chemins} et le {> tools.inkscape.texte: texte} sont sur une page dédiée

### {!svg: tools/inkscape/icons/draw-freehand.svg} Tracé à main levée

De façon assez évidente, ça vous permet de tracer des chemins à main levée

{!svg: tools/inkscape/3-handwriting.svg}

- Maintenir ctrl créera un simple point
- Maintenir maj continuera le chemin sélectionné (ça permet de grouper un tracé en plusieurs traits en un seul objet)

{!img: tools/inkscape/3-handwriting-tools.png}

- Le *mode* définit comment les courbes seront rendues, vous verrez à quoi ça correspond avec les {> tools.inkscape.chemin: chemins}
- Le *lissage* permet de lisser le trait pour gommer les tremblements et les imperfections
- Le bouton à côté permet de simplifier le tracé en direct, c’est-à-dire d’éliminer en direct les points jugés inutiles
- La *forme* permet d’appliquer une certaine forme au tracé : par exemple, le *PL$tek* du bas ci-dessus est tracé avec l’option *Ellipse*

On en reparlera plus tard, mais l’option du menu `chemin > simplifier` (par défaut Ctrl + L) permet de simplifier les chemins (éliminer intelligemment des points intermédiaires). Dans le cas présent, ça permet par exemple de garder le côté écrit à la main sans que ce soit pollué par les hésitations et les tremblements — par exemple, c’est la différence entre les deux premiers *PL$tek* ci-dessus. Vous pouvez repasser plusieurs fois la simplification jusqu’à ce que ce soit satisfaisant.

### {!svg: tools/inkscape/icons/draw-calligraphic.svg} Tracé calligraphique

Permet de faire des tracés comme à la plume (ou d’autres choses selon les paramètres)

{!img: tools/inkscape/3-calligraphy-tools.png}

Vous avez beaucoup d’options de tracé dans la barre d’outils :

- Quelques paramètres prédéfinis, vous pouvez aussi enregistrer les vôtres si besoin
- La *largeur* pour adapter la largeur du trait
- Si vous écrivez avec un stylet vous avec l’option d’utiliser la pression et l’angle appliqués avec le stylet directement, sinon vous pouvez bricoler ça avec les autres paramètres
- Immédiatement à droite vous avez un bouton pour que l’épaisseur du trait corresponde à la luminosité de l’arrière-plan, ça permet d’utiliser une heatmap
- L’*amincissement* permet de choisir comment la vitesse du tracé affecte l’épaisseur :
	- 0 rendra l’épaisseur indépendante de la vitesse
	- Une valeur supérieure à zéro amincira le tracé avec la vitesse
	- Une valeur inférieure à zéro épaissira le tracé avec la vitesse
- L’*inertie* va faire traîner la plume derrière vous, comme si elle était plus « lourde », ce qui réduira les tremblements et aura tendance à lisser le trait
- L’*angle* de la plume : avec un angle de 0° la tranche du trait sera horizontale, de là vous pouvez changer l’orientation de la plume entre -90 et 90°
- La *fixité* définit l’évolution de l’angle de la plume :
	- À 0, l’orientation est toujours perpendiculaire au tracé (la plume tourne en même temps que le trait)
	- Les valeurs supérieures à 0 rendront l’angle de plus en plus fixe
	- Les valeurs inférieures à 0 auront tendance à opposer l’angle à la direction du tracé
- Le paramètre *terminaisons* définit le niveau d’arrondissement des extrémités du trait
- Les *tremblements* introduisent des tremblements dans le tracé
- L’*agitation* introduit comme des hésitations dans le tracé

## Outils de modification

### {!svg: tools/inkscape/icons/tool-tweak.svg} Déformation

Un outil avec plein de modes différents pour modifier légèrement un objet à vue. Sélectionnez d’abord un objet avec l’outil sélection {!svg: tools/inkscape/icons/tool-pointer.svg}, puis prenez l’outil déformation et utilisez le mode que vous voulez avec un cliquer-glisser sur l’objet.

{!img: tools/inkscape/3-tweak-tools.png}

Les modes sont, de gauche à droite (vous pouvez passer votre souris dessus pour avoir la description de chacun) :

- {!svg: tools/inkscape/icons/object-tweak-push.svg} Décaler l’objet avec votre curseur
- {!svg: tools/inkscape/icons/object-tweak-attract.svg} Décaler le centre de l’objet vers votre curseur, ou à l’opposé en maintenant maj.
- {!svg: tools/inkscape/icons/object-tweak-randomize.svg} Bouge l’objet aléatoirement
- {!svg: tools/inkscape/icons/object-tweak-shrink.svg} Rétrécit l’objet complet, ou l’agrandit en maintenant maj.
- {!svg: tools/inkscape/icons/object-tweak-rotate.svg} Fait tourner l’objet dans le sens horaire, ou anti-horaire en maintenant maj.
- {!svg: tools/inkscape/icons/object-tweak-duplicate.svg} Duplique les objets, ou les efface en maintenant maj.
- {!svg: tools/inkscape/icons/path-tweak-push.svg} Déforme le chemin avec votre curseur
- {!svg: tools/inkscape/icons/path-tweak-shrink.svg} Affine le chemin à la position du curseur, ou l’élargit en maintenant maj.
- {!svg: tools/inkscape/icons/path-tweak-push.svg} Attire les points du chemin vers la position du curseur, ou les repousse en maintenant maj.
- {!svg: tools/inkscape/icons/path-tweak-roughen.svg} Donne un effet rugueux au contour du chemin
- {!svg: tools/inkscape/icons/object-tweak-paint.svg} Rapproche la couleur de l’objet de la couleur définie comme couleur active (dans `fonds et contours` ou la palette)
- {!svg: tools/inkscape/icons/object-tweak-jitter-color.svg} Modifie la couleur de l’objet aléatoirement
- {!svg: tools/inkscape/icons/object-tweak-blur.svg} Floute l’objet

Dans tous les cas vous avez quelques paramètres :

- La *largeur* donne la taille de la zone à modifier, par rapport à la taille de la vue (ça dépend du zoom donc)
- La *force* donne la force de l’ajustement
- La *fidélité* dit à quel point il faut préserver la qualité de la forme. Plus elle est élevée, plus la déformation sera de « bonne qualité », par contre comme ça rajoutera plus de points faites attention au poids et aux performances.
- Et pour les modes liés à la couleur, vous pouvez sélectionner les canaux à affecter (teinte, saturation, luminosité, transparence, on en reparlera)

### {!svg: tools/inkscape/icons/tool-spray.svg} Spray

Dissémine des copies d’un objet là où vous dessinez. Pour l’utiliser, sélectionnez d’abord un objet avec l’outil sélection {!svg: tools/inkscape/icons/tool-spray.svg}, puis prenez l’outil spray et dessinez où vous voulez.

{!img: tools/inkscape/3-spray-tools.png}

L’outil a quatre modes, de gauche à droite :

- Créer des copies indépendantes
- Créer des clones : dans Inkscape, un *clone* est une copie dépendante d’un objet : toute modification de l’original sera répercutée sur ses clones
- Créer un seul chemin : ça créera des copies indépendantes, mais ça laissera le tout en un seul objet à la fin
- Effacer des objets préalablement pulvérisés, utile pour nettoyer les bords sans tout faire à la main et sans avoir à se préoccuper du reste vu que ça n’éliminera que les objets pulvérisés selon l’original sélectionné

Vous avez divers autres paramètres :

- La *largeur* donne la largeur de la zone de dispersion de part et d’autre du curseur (dépend du niveau de zoom actuel)
- La *quantité* donne la fréquence des objets à disperser
- La *rotation* et l’*échelle* permettent des variations aléatoire d’angle et de taille
- *Éparpiller* permet de disperser plus aléatoirement, sinon ça suivra quand même nettement le curseur
- Le *rayon* est la zone où disperser : à 0 ça ne dispersera pas du tout (ça restera directement sous le curseur), à 100 ça pourra aller n’importe où dans la *largeur*.

Les dernières options à droite concernent le comportement vis-à-vis des zones transparentes et permettent d’éviter la superposition.

### {!svg: tools/inkscape/icons/draw-eraser.svg} Gomme

La gomme permet d’effacer simplement des choses à la main, en faisant un cliquer-glisser comme pour un tracé à main levée. Comme ce n’est qu’à main levée ça ne peut faire que des choses assez grossières, pour du précis il y a de quoi faire dans les {> tools.inkscape.chemin#interactions: interactions entre chemins}

{!img: tools/inkscape/3-eraser-tools.png}

La gomme a trois modes différents, de gauche à droite :

- Le premier supprime les objets entiers quand vous passez dessus avec votre souris
- Le deuxième modifie le chemin en ajoutant des points pour supprimer la partie gommée
- Le troisième crée un « chemin de découpe », qui se superpose à l’objet pour masquer ce qui est effacé, ce qui permet notamment de tailler des objets « spéciaux » (ellipses, rectangles, polygones, …) sans perdre la possibilité d’utiliser les outils spécifiques à ces objets

Les autres paramètres sont relativement similaires aux autres tracés à main levée :

- La *largeur* change la largeur du trait, qui dépend du niveau de zoom
- L’*amincissement* permet d’amincir le trait en fonction de la vitesse, ce qui peut faire des effets comme ci-dessus
- Le paramètre *terminaisons* donne un arrondi aux extrémités du trait
- Le *tremblement* introduit des tremblements dans le tracé
- L’*inertie* du tracé implique un certain lissage en faisant trainer le tracé derrière vous

### {!svg: tools/inkscape/icons/draw-connector.svg} Connecteur

Crée des connecteurs entre d’autres objets, qui se comportent entièrement comme des connecteurs (s’arrêtent au contour de l’objet, suivent quand l’objet est déplacé, …)
Pour le moment, l’outil est relativement limité, il ne gère pas bien les terminaisons (flèches, …), et n’est pas très permissif au niveau de la forme du connecteur. Si vous voulez quelque chose de plus précis, vous devrez faire ça vous-même (non pas que ce soit particulièrement compliqué).

{!img: tools/inkscape/3-connector-tools.png}

- Si vous sélectionnez des objets, et que vous créez un connecteur, les deux premiers boutons peuvent faire éviter (ou ignorer) ces objets par le connecteur
- Le troisième bouton à gauche permet de faire seulement des lignes brisées horizontales et verticales
- La *courbure* autorise à faire des courbes
- L’*espacement* donne la distance à laisser entre un connecteur qui évite un objet et un objet évité

### {!svg: tools/inkscape/icons/tool-measure.svg} Règle

Cet outil sert juste à mesurer des distances et des angles, il suffit de cliquer-glisser pour avoir la distance entre les deux points

### {!svg: tools/inkscape/icons/tool-pages.svg} Pages

Depuis peu, Inkscape permet de créer des documents à plusieurs pages, ce qui peut être utile pour votre propre organisation, ou pour vraiment créer des documents à plusieurs pages (brochures, …), comme vous pouvez directement exporter en PDF par exemple

{!img: tools/inkscape/3-page-tools.png}

- Pour créer une page, vous avez le bouton à gauche qui crée une nouvelle page dans le format sélectionné — sinon, vous pouvez juste tracer une page comme vous voulez dans la zone de dessin
- Le sélecteur de format (ou les poignées) permet aussi de changer la taille d’une page existante
- Vous pouvez adapter la taille d’une page à son contenu, la page sera alors coupée pour n’avoir aucune marge superflue
