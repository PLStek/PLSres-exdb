//// title = "Positionnement"
//// description = "Les différents moyens de positionner proprement les choses"

# {=title}

C’est super, maintenant on sait faire plein de trucs, mais pour le moment c’est en vrac. Inkscape propose différents moyens de positionner les objets entre eux proprement et précisément, qui seront fondamentaux pour faire quelque chose d’harmonieux.

## Magnétisme

Ce qu’on appelle le magnétisme, c’est d’attirer la souris vers des points spéciaux on on veut souvent coller nos points ou objets. Pour ça, activez-le en haut à droite de l’écran :

{!img: tools/inkscape/7-magnet-ui.png}

Une fois activé, rien de plus simple : ça va naturellement vous attirer vers les points d’intérêt :

{!img: tools/inkscape/7-magnet-example-rectangles.png}
{!img: tools/inkscape/7-magnet-example-path.png}

Le menu déroulant juste à côté du bouton d’activation du magnétisme permet de paramétrer les types de points qui seront magnétiques :

{!img: tools/inkscape/7-magnet-settings-simple.png}

Ça c’est le mode facile, avec 3 options :

- **Boites englobantes** (bounding box) : magnétise les coins de la *bounding box*, en gros le plus petit rectangle qui contient l’objet, tout compris. Ça permet par exemple de magnétiser sur l’extérieur des contours, comme dans l’exemple des rectangles ci-dessus
- **Points** : magnétise aux chemins, donc sommets, centres, nœuds doux, points à chaque 90° sur le rebord des ellipses, milieux de segments, … Ça magnétisera aussi au tracé du chemin lui-même, hors des points intéressants, ainsi qu’aux rebords de la page.
- **Alignements** : magnétise en alignant à d’autres objets, par exemple sur la même ligne ou colonne que des coins ou centres d’autres objets.

Si vous voulez un contrôle plus fin, cliquez sur *mode avancé* dans le menu pour tout contrôler individuellement :

{!img: tools/inkscape/7-magnet-settings-full.png}

La plupart des options sont relativement évidentes, à vous de sélectionner ce dont vous avez besoin sur le moment

## Aligner et distribuer

L’autre base de la base pour faire des choses propres, c’est le dialogue *Aligner et distribuer*, que vous pouvez ouvrir depuis le menu *Objet* :

{!img: tools/inkscape/7-align-open.png}

Une fois le dialogue ouvert, mettez-le à un endroit confortable et ne le fermez plus, parce que vous allez vous en servir *souvent*.
*Aligner et distribuer* permet d’adapter la position des objets entre eux très facilement.

### Poignées d’alignement

La première option, la plus simple mais aussi la plus limitée, est d’utiliser les « poignées d’alignement ». Pour ça, il suffit d’activer l’option *Troisième clic pour les poignées d’alignement* :

{!img: tools/inkscape/7-handles-start.png}

Vous savez déjà que sélectionner un objet en cliquant dessus fait apparaître les poignées de redimensionnement, un deuxième clic donne les poignées de rotation — maintenant, un troisième clic active les poignées d’alignement. Sélectionnez tous les objets que vous voulez aligner, et vous pouvez les utiliser pour coller les objets sur le même côté, coin, ou tout centrer :

{!img: tools/inkscape/7-handles-example.png}

La poignée du centre centre seulement horizontalement par défaut, et verticalement en maintenant maj. Maintenir maj en cliquant sur les poignées latérales permet en plus de retourner la sélection.

### Options d’alignement

Maintenant, pour avoir quelque chose de plus avancé, on peut aller voir du côté des options d’alignement. C’est la première rangée de bouton dans le dialogue *Aligner et distribuer*. Vous avez différentes options d’alignement, chacune disponible verticalement et horizontalement.

{!img: tools/inkscape/7-align-options.png}

Pour les utiliser, d’abord sélectionnez l’objet de référence dans la liste déroulante. Les objets seront alignés par rapport à celui-ci :

{!img: tools/inkscape/7-align-references.png}

- *Dernier sélectionné* et *Premier sélectionné* prennent comme référence le dernier ou le premier objet dans l’ordre où vous les avez sélectionné
- *Objet le plus grand* et *Objet le plus petit* prennent comme référence le plus grand ou le plus petit objet de la sélection
- *Page* aligne par rapport à la page complète (par exemple, centrer mettra les objets au centre de la page)
- *Dessin* aligne par rapport à la zone utilisée, c’est-à-dire le rectangle qui contient tous les objets présents sur la page
- *Zone de sélection* aligne par rapport au rectangle contenant les objets sélectionnés

Et maintenant, plus qu’à sélectionner vos objets (éventuellement dans le bon ordre), puis à cliquer sur l’option d’alignement de votre choix. Dans tous les exemples, on aligne en prenant le carré noir comme référence

- {!svg: tools/inkscape/icons/align-vertical-top.svg} {!svg: tools/inkscape/icons/align-vertical-bottom.svg} {!svg: tools/inkscape/icons/align-horizontal-left.svg} {!svg: tools/inkscape/icons/align-horizontal-right.svg} Aligne les objets sur un des côtés de la référence

{!svg: tools/inkscape/7-align-example-side.svg}

- {!svg: tools/inkscape/icons/align-vertical-top-to-anchor.svg} {!svg: tools/inkscape/icons/align-vertical-bottom-to-anchor.svg} {!svg: tools/inkscape/icons/align-horizontal-left-to-anchor.svg} {!svg: tools/inkscape/icons/align-horizontal-right-to-anchor.svg} Aligne les objets sur le côté de la référence, mais à l’extérieur

{!svg: tools/inkscape/7-align-example-anchor.svg}

- {!svg: tools/inkscape/icons/align-vertical-center.svg} {!svg: tools/inkscape/icons/align-horizontal-center.svg} Centre les objets par rapport à la référence

{!svg: tools/inkscape/7-align-example-center.svg}

- {!svg: tools/inkscape/icons/align-vertical-baseline.svg} {!svg: tools/inkscape/icons/align-horizontal-baseline.svg} Aligne par rapport à la ligne de base des textes, parce que les lettres sont de tailles différentes et ne permettent donc pas toujours un bon alignement avec les autres options

{!svg: tools/inkscape/7-align-example-text.svg}

### Options de distribution //// distribute

Le dialogue *Aligner et distribuer* permet aussi de distribuer des objets, comme son nom l’indique. L’idée est de sélectionner les objets à organiser, et ça les répartira entre les deux aux extrémités à égales distances. C’est donc une aide indispensable pour faire des diagrammes harmonieux. Notez bien que les objets aux extrémités seront pris comme références et ne bougeront pas, les autres se répartiront entre ces deux-là.

- {!svg: tools/inkscape/icons/distribute-horizontal-left.svg} {!svg: tools/inkscape/icons/distribute-horizontal-right.svg} {!svg: tools/inkscape/icons/distribute-vertical-top.svg} {!svg: tools/inkscape/icons/distribute-vertical-bottom.svg} Distribue les objets selon une de leurs extrémités (haut, bas, gauche, droite) : Les extrémités choisies de chaque objet seront à égale distance
- {!svg: tools/inkscape/icons/distribute-horizontal-center.svg} {!svg: tools/inkscape/icons/distribute-vertical-center.svg} Distribue le centre des objets : Les centres de chaque objet seront à égale distance
- {!svg: tools/inkscape/icons/distribute-horizontal-gaps.svg} {!svg: tools/inkscape/icons/distribute-vertical-gaps.svg} Met les objets à égale distance les uns des autres : l’écart entre chaque objet sera égale.
- {!svg: tools/inkscape/icons/distribute-horizontal-baseline.svg} {!svg: tools/inkscape/icons/distribute-vertical-baseline.svg} Met les lignes de base du texte à égale distance — notamment pratique pour organiser du texte en lignes.

{!svg: tools/inkscape/7-distribution-example.svg}

### Réorganiser les objets

Encore en-dessous, vous pouvez réorganiser les objets sélectionnés selon certains critères :

- {!svg: tools/inkscape/icons/distribute-graph.svg} Réorganise un diagramme d’objets reliés par des connecteurs {!svg: tools/inkscape/icons/draw-connector.svg}. Comme d’habitude avec les connecteurs Inkscape a toute la bonne volonté du monde mais pour le moment c’est pas encore ça.
- {!svg: tools/inkscape/icons/exchange-positions.svg} Échange la position des objets selon l’ordre où ils ont été sélectionnés (en réalité ils se déplacent dans l’ordre inverse 3 ⟶ 2, 2 ⟶ 1, 1 ⟶ 3)
- {!svg: tools/inkscape/icons/exchange-positions-zorder.svg} Échange la position des objets de la même façon, mais en utilisant leur ordre de superposition (arrière-plan / avant-plan)
- {!svg: tools/inkscape/icons/exchange-positions-clockwise.svg} Échange la position des objets en tournant autour du centre, les objets se déplacent en sens inverse des aiguilles d’une montre
- {!svg: tools/inkscape/icons/distribute-randomize.svg} Déplace aléatoirement les objets les uns par rapport aux autres (ils restent toujours dans leur zone de sélection d’origine)
- {!svg: tools/inkscape/icons/distribute-unclump.svg} Étale les objets les uns par rapport aux autres petit à petit, en tendant à les amener vers une égale distance les uns des autres

Et surtout, encore juste en-dessous, vous avez l’option pour supprimer les chevauchements d’objets : vous pouvez entrer une distance minimale à respecter entre les objets, cliquez sur {!svg: tools/inkscape/icons/distribute-remove-overlaps.svg} et c’est plié.

{!svg: tools/inkscape/7-remove-overlaps.svg}

### Organisation en grille

Le deuxième onglet *Grille* permet d’organiser les objets sélectionnés sous forme d’une grille. Sélectionnez tous les objets à répartir, choisissez en combien de lignes et colonnes ils doivent être (ça choisit déjà plus ou moins automatiquement en fonction du nombre total d’objets), choisissez l’écart entre les objets, puis cliquez sur le bouton *Organiser* qui est un peu plus bas dans le dialogue.

{!img: tools/inkscape/7-grid-equal.png}

Si vos objets sont tous de la même taille, vous n’avez qu’à vous soucier du nombre de lignes et colonnes et de l’écartement :

- *Ajuster à la boite de sélection* égalisera les écartements pour remplir la boite de sélection d’origine
- *Définir l’écartement* vous permet de choisir les écartements manuellement

Le reste est au cas où vos objets n’auraient pas tous la même taille.

- *Égaliser la hauteur* et *Égaliser la largeur* permettent de choisir comment la taille des « cases » est déterminée : s’ils sont cochés, toutes les cases auront la taille du plus grand objet de tous, ça donnera des cases qui sont toutes de la même taille dans toute la grille ; s’ils sont décochés, ça choisira la taille ligne par ligne / colonne par colonne (respectivement), donc par exemple chaque colonne aura la largeur de l’objet le plus large de la colonne.
- L’*alignement* donne en fonction de quel point les objets sont répartis. Au final, ça fera exactement pareil que s’ils étaient distribués selon l’option choisie.

{!svg: tools/inkscape/7-grid-unequal.svg}

### Organisation circulaire

Le troisième onglet permet d’organiser vos objets sur une ellipse (comprendre, tout ce qui se fait avec l’outil ellipse : ellipses, cercles, arcs, secteurs, …). Pareil, sélectionnez les objets appropriés, les bonnes options puis cliquez sur *Organiser* en bas du dialogue.
Le *Point d’ancrage* sélectionne quel point de chaque objet sera positionné sur le cercle, vous pouvez aussi prendre le *centre de rotation*.
La partie la plus importante, c’est *Organiser sur*, qui va choisir sur quelle ellipse vous allez positionner vos objets. Les deux premiers choix permettent de prendre un objet ellipse existant et de répartir les objets dessus. Le truc *premier* ou *dernier* sélectionné c’est au cas où vous vouliez répartir des ellipses autour d’une autre ellipse, il faut bien choisir laquel sert de modèles et lesquelles sont réparties.

{!img: tools/inkscape/7-elliptic-existing.png}

Sinon, vous avez l’option *paramétré* pour entrez vous-même les paramètres :

- *Centre X/Y* : Coordonnées du centre par rapport à la page. C’est pas la peine de perdre du temps avec ça vu que vous pourrez déplacer le résultat après
- *Rayon X/Y* : Rayons de l’ellipse (égaux pour avoir un cercle)
- *Angle X/Y* : Rien à voir avec X/Y, ça permet de paramétrer un arc de cercle : le premier angle est le début (0° = gauche, 90° = bas), le deuxième est la fin. Respectivement 0 et 360 pour avoir l’ellipse / cercle complet.

{!img: tools/inkscape/7-elliptic-parametric.png}

## Les guides

Un *guide* est une droite virtuelle, horizontale ou verticale, qui permet de magnétiser sur une ligne quelconque.
Pour en créer, il suffit de cliquer-glisser à partir d’une des règles. Le guide apparaît, et vous pouvez le mettre où vous voulez, notamment en magnétisant sur un point existant.

{!img: tools/inkscape/7-guide-to-center.png}

Si les guides ne s’affichent pas, vérifiez l’option `Affichage > Guides`

Vous voyez le résultat, on a une droite magnétique, et une « origine » (le point qu’on a placé au centre de l’étoile pour positionner le guide). De là, vous avez quelques options de manipulation du guide avec l’outil pointeur {!svg: tools/inkscape/icons/tool-pointer.svg} :

- Appuyer sur la touche *suppr* avec la souris pointée dessus supprimera le guide
- Maintenir ctrl et cliquer-glisser sur le guide permet de déplacer l’origine
- Maintenir maj et cliquer-glisser permet de faire pivoter le guide autour de son origine, ce qui permet d’avoir plus que horizontal et vertical :

{!img: tools/inkscape/7-guide-oblique.png}

Vous avez aussi quelques autres options pratiques sur les guides en général :

- Le petit cadenas en haut à gauche de la zone de dessin permet de *verrouiller* ou déverrouiller tous les guides. Un guide verrouillé ne peut pas être modifié ni touché (pratique pour être sûr de ne pas décaler vos guides par inadvertance en essayant d’atteindre un objet qui était derrière). L’option du menu édition > verrouiller tous les guides fait la même chose
- `Édition > Créer des guides autour de la page` créera automatiquement des guides qui délimiteront la page
- `Édition > Supprimer tous les guides` supprimera tous les guides du document.
- `Affichage > Guides` permet d’afficher ou masquer les guides

## La grille

Vous pouvez aussi paramétrer une grille sur tout le document, qui vous permettra de magnétiser des choses dessus.
Pour ça, allez dans le menu `Fichier > Propriétés du document`, puis dans l’onglet *Grille*

{!img: tools/inkscape/7-grid-settings-initial.png}

De là, sélectionnez le type de grille que vous voulez (rectangulaire ou axonométrique = 3D isométrique), puis sur *Nouveau* pour ajouter une grille. Vous avez alors plein de paramètres pour la grille :

{!img: tools/inkscape/7-grid-rectangular.png}

- *Afficher des points plutôt que des lignes* permet de n’afficher que les points d’intersection de la grille (les lignes resteront magnétiquement actives)
- *Origine X et Y* permettent de déplacer manuellement le point d’origine. Vous avez aussi les boutons d’alignement pour mettre l’origine sur un des points principaux de la page
- *Espacement X et Y* est le paramètre le plus important, c’est l’écart entre deux lignes de grille, dans les deux directions
- Par défaut vous avez une *grille secondaire* et une *grille principale* : c’est comme dans vos cahiers, vous avez la grille secondaire avec toutes les subdivisions (c’est ça que l’*espacement* paramètre), et un trait plus épais pour marquer certains multiples (toutes les 5 cases par défaut). Vous pouvez changer ça avec la case en bas. Les couleurs ne sont que des options d’affichage, ça n’a aucune incidence sur le résultat final.

Pour une grille axonométrique, vous avez quelques paramètres qui changent :

{!img: tools/inkscape/7-grid-axonometric.png}

- Vous n’avez plus qu’un paramètre *Espacement*, les différences selon les axes dépendent des angles
- Et vous avez les paramètres *Angle X et Y* qui permettent de modifier l’angle des lignes de grille (si on prend ça comme une projection 3D, ça change l’angle de vue)

Le reste est identique.
