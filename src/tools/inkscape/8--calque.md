//// title = "Groupes et calques"
//// description = "Les moyens de regrouper des objets dans Inkscape"

# {=title}

C’est souvent utile de pouvoir regrouper des objets de différentes façons pour les isoler ou les manipuler ensemble.

## Groupes

Dans Inkscape, vous pouvez *grouper* des objets. Ça fait que les objets groupés se manipuleront comme un seul objet, sur tous les plans. Pour ça, sélectionnez les objets à grouper, puis clic droit > grouper. Vous avez aussi le bouton {!svg: tools/inkscape/icons/object-group.svg} en bas à droite de l’interface, ou le menu `Objet > Grouper`.

{!img: tools/inkscape/8-group-button.png}
{!img: tools/inkscape/8-group-grouped.png}

À partir de là, ces objets ne font plus qu’un : on peut donc les déplacer et tourner en bloc, utiliser les options d’alignement dessus comme si c’était un seul objet, …
C’est donc essentiel dès lors que vous utilisez des objets composés.

Pour dégrouper les objets c’est pareil, clic droit > dégrouper, ou le bouton {!svg: tools/inkscape/icons/object-ungroup.svg} tout en bas à droite. Ça les ré-éclatera en objets individuels.

Cela dit, vous pouvez toujours manipuler les objets à l’intérieur d’un groupe sans dégrouper-regrouper à chaque fois. Vous pouvez ainsi sélectionner et manipuler un objet à l’intérieur d’un groupe avec l’outil sélection {!svg: tools/inkscape/icons/tool-pointer.svg} en maintenant ctrl.

Vous pouvez aussi entrer dans un groupe pour manipuler ses objets en double-cliquant dessus. De là, vous pouvez bricoler comme vous voulez dans le groupe comme si ce n’était pas groupé. Cliquez sur un objet hors du groupe pour sortir de ce mode.

## Calques

Si vous connaissez des éditeurs d’image comme GIMP / Photoshop vous savez ce que c’est qu’un calque, sinon un « calque » est comme un « couche » de l’image, que vous pouvez manipuler individuellement : vous pouvez bricoler les objets qui sont sur un calque sans interférer avec les autres calques, ce qui permet de mieux organiser et de largement faciliter la création de documents complexes. Ça permet aussi de gérer proprement la superposition par couche plutôt que de bidouiller individuellement des dizaines d’objets pour les mettre au-dessus ou en-dessous des autres.

Les contrôles de calques sont essentiellement dans le menu `Calque`, et en bas de l’interface

{!img: tools/inkscape/8-layer-control.png}

Mais surtout, pour maîtriser ça on va avoir besoin du dialogue *Calques et objets*. Pour l’ouvrir, c’est soit le menu `Calque > Calques et objets`, soit juste cliquer sur le bouton avec le nom du calque en bas de la fenêtre.

{!img: tools/inkscape/8-layer-dialog.png}

Beaucoup de choses là-dedans, on va voir tout ça au fur et à mesure.

D’abord, mettons qu’on a commencé un diagramme et que c’est un peu le bazar :

{!svg: tools/inkscape/8-layer-example.svg}

Dès qu’on veut bouger ou sélectionner des choses on est embêtés par l’arrière-plan qui se sélectionne en même temps. Avant de continuer à ajouter des choses il vaut mieux organiser ça en calques pour gagner en temps et en organisation. On voudrait donc deux calques : un pour l’arrière-plan, et un pour le diagramme. Pour ça, on doit commencer par ajouter un calque. Pour ça, c’est soit dans le menu `Calque > Ajouter un calque`, soit le bouton {!svg: tools/inkscape/icons/layer-new.svg} en haut à gauche du dialogue *Calques et objets*. Inkscape vous demande alors le nom et la position du calque à ajouter :

{!img: tools/inkscape/8-layer-new.png}

Vous avez trois options d’insertion, au-dessus du calque actif, en-dessous, ou comme *sous-calque*, il marchera alors comme un calque normal mais sera quand même inclus dans le calque de niveau supérieur, ça peut permettre d’organiser des documents complexes de façon arborescente. Ici on va juste le mettre au-dessus, et il apparaît dans la liste :

{!img: tools/inkscape/8-layer-list.png}

D’ailleurs tant qu’on est là, on peut aussi renommer le calque du bas, il suffit de double-cliquer dessus dans la liste.

{!img: tools/inkscape/8-layer-rename.png}

Si vous voulez rendre la liste un peu plus claire, le bouton en haut à gauche {!svg: tools/inkscape/icons/layer-duplicate.svg} permet de masquer / afficher les objets individuels em plus des calques

{!img: tools/inkscape/8-layer-show.png}

Super, maintenant, on va déplacer ce qui constitue le diagramme vers le calque *diagramme*. Pour ça, d’abord on les sélectionne, et ensuite plusieurs possibilités :

- Clic droit > déplacer vers le calque

{!img: tools/inkscape/8-layer-move-objects.png}

- Les objets sélectionnés sont aussi sélectionnés dans la liste, et vous avez exactement les mêmes options avec un clic droit

{!img: tools/inkscape/8-layer-move-list.png}

- Vous pouvez prendre les objets sélectionnés dans la liste et cliquer-glisser vers le calque cible dans la liste
- Ou encore utiliser les options de menu `Calque > Déplacer la sélection vers le calque supérieur`, `Calque > Déplacer la sélection vers le calque inférieur` pour déplacer vers un calque adjacent, ou `Calque > Déplacer la sélection vers le calque` pour décaler vers un calque au choix.

Maintenant qu’on a séparé nos calques, on sait qu’on a fini de bosser sur l’arrière-plan pour le moment, donc on veut qu’il ne vienne plus nous parasiter et être sûr qu’on ne va pas le déplacer par inadvertance. Pour cela, vous avez les contrôles en bas de la fenêtre ou en passant votre souris dessus dans la liste. Dans la liste, vous pouvez aussi faire ça sur les objets individuellement.

{!img: tools/inkscape/8-layer-controls.png}

- L’œil permet de cacher l’objet ou le calque entier
- Le cadenas permet de verrouiller l’objet ou le calque, c’est-à-dire que rien sur le calque ne pourra être sélectionné ou déplacé tant qu’il sera verrouillé

Ceci fait, on revient sur le calque *diagramme* en cliquant dessus dans la liste, et on n’a plus qu’à bricoler dessus.

Vous avez encore quelque options, notamment les quelques boutons en haut à droite de la liste :

{!img: tools/inkscape/8-layer-move.png}

- Les flèches permettent de déplacer les calques ou les objets dans la liste (les mettre plus ou moins à l’avant ou à l’arrière)
- La croix permet de supprimer l’objet ou le calque entier.

Les options du menu *Calque* sont toutes plus ou moins redondantes, avec de quoi changer de calque, ajouter / renommer / dupliquer / supprimer des calques, les verrouiller ou les caches, …
