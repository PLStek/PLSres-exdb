//// title = "Couleur et style"
//// description = "Utilisation des couleurs, du fond et des contours dans Inkscape"

# {=title}

Rien de bien complexe ici, mais quelques petits rappels ne font jamais de mal.

## Bases

Dans Inkscape, un objet peut avoir une couleur de fond (remplissage) et un contour.
Pour les changer, vous aurez besoin de la boite *fond et contour*, que vous pouvez ouvrir dans le menu objet > fond et contour, dans le menu contextuel quand vous cliquez droit sur un objet, ou simplement avec le bouton {!svg: tools/inkscape/icons/dialog-fill-and-stroke.svg} en bas à droite de la fenêtre. Gardez cette boite là où vous pouvez toujours l’atteindre, vous allez vous en servir souvent.

{!img: tools/inkscape/5-fill-stroke-dialog.png}

## Modifier les couleurs d’un objet

Pour cela rien de plus simple : sélectionnez l’objet, puis appliquer les couleurs. Vous avez pour ça les palettes en bas de l’écran (clic normal pour changer la couleur de fond, maj+clic pour changer la couleur de contour), ou vous avez le dialogue fond et contour, avec les onglets *fond* et *contour* où vous pouvez sélectionner les couleurs.

### Les modes de remplissage

Dans le dialogue fond et contour, dans les onglets fond et contour, vous pouvez appliquer différents modes de remplissage.

{!img: tools/inkscape/5-modes.png}

Pour évacuer la question des icones à droite :

- {!svg: tools/inkscape/icons/fill-rule-even-odd.svg} Fait que ça ne remplira pas là où l’objet se superpose à lui-même
- {!svg: tools/inkscape/icons/fill-rule-nonzero.svg} Et ce mode-là remplira l’objet indépendamment de l’auto-superposition

{!svg: tools/inkscape/5-gkey.svg}

Ensuite, on va passer sur les différents modes de remplissage. Tout ça marche aussi bien pour le fond que pour les contours. Dans tous les cas, l’option sans remplissage {!svg: tools/inkscape/icons/paint-none.svg} fera que le fond ou le contour n’existera pas du tout (fond transparent, ou pas de contour).

#### {!svg: tools/inkscape/icons/paint-solid.svg} Remplissage uni

Ça donne juste une couleur uniforme. Là-dessous, vous avez de quoi sélectionner une couleur avec plein d’options :

- {!svg: tools/inkscape/icons/color-selector-hsx.svg} TSV (Teinte-Saturation-Valeur) / HSV (Hue-Saturation-Value)
- {!svg: tools/inkscape/icons/color-selector-hsx.svg} TSL (Teinte-Saturation-Luminosité) / HSL (Hue-Saturation-Lightness) : Un peu pareil, sauf qu’en HSL la pleine luminosité donne du blanc alors qu’en HSV la pleine valeur donne la couleur pleinement saturée (en HSL elle est à 50% de luminosité). Ces deux modes représentent bien comment on perçoit les couleurs.
- {!svg: tools/inkscape/icons/color-selector-rgb.svg} RVB (Rouge-Vert-Bleu) / RGB (Red-Green-Blue) : Les couleurs comme on les définit souvent sur des écrans, vu que c’est comme ça qu’on compose avec la lumière
- {!svg: tools/inkscape/icons/color-selector-cmyk.svg} CMJN (Cyan-Magenta-Jaune-Noir) / CMYK (Cyan-Magenta-Yellow-blacK) : Les couleurs comme on les définit en termes de proportion d’encre, utilisé plutôt en imprimerie
- {!svg: tools/inkscape/icons/color-selector-hsluv.svg} HSLuv ressemble pas mal à TSL, mais pour être cohérent avec la vision humaine, plutôt qu’avec la physique. Exemple :

{!svg: tools/inkscape/5-hsluv.svg}

- En TSL, bien que les deux couleurs aient exactement les mêmes valeurs de saturation et de luminosité (et c’est vrai, physiquement ça correspond bien à un même éclairage), leur luminosité *perçue* n’est pas du tout la même, comme en témoigne le texte en noir qui est beaucoup moins lisible sur le fond bleu. En HSLuv, la même valeur de luminosité ≈ la même luminosité perçue, donc pour les deux à 90 ici, l’intelligibilité du texte dessus est la même. C’est donc très pratique pour du design en général (UI, diagrammes, brochures, …) pour avoir des palettes de couleurs variées sans se prendre la tête pour que tout soit à peu près aussi lisible et cohérent partout.

Dans tous les cas, en dessous vous avez la valeur alpha qui correspond à l’opacité. Vous avez aussi la valeur hexadécimale de la couleur sélectionnée au cas où.

#### {!svg: tools/inkscape/icons/paint-gradient-linear.svg} Dégradé linéaire

Comme son nom l’indique, ça remplit avec un dégradé linéaire

{!img: tools/inkscape/5-gradient.png}

- La liste déroulante donne accès aux autres dégradés déjà définis sur d’autres objets du document, pour pouvoir les réutiliser
- Vous avez 3 modes de répétition : *aucun* (ça ne se répète pas du tout), *direct* (ça se répète dans le même ordre), et *réfléchi* (ça se répète dans l’ordre inverse)

{!svg: tools/inkscape/5-gradient-repeat-modes.svg}

- Le reste vous permet de définir des étapes dans votre dégradé, avec une position et un sélecteur de couleur comme tous les autres (attention, par défaut l’alpha de certaines étapes peut être à zéro, ça peut avoir l’air bloqué sur blanc mais en fait c’est que c’est transparent)

C’est là que l’outil dégradé {!svg: tools/inkscape/icons/color-gradient.svg} est utile : il permet de modifier les bornes et l’orientation du dégradé sur l’objet.

#### {!svg: tools/inkscape/icons/paint-gradient-radial.svg} Dégradé radial

Ça marche exactement pareil, sauf que le dégradé est radial (à partir du centre). Pour tracer ces dégradés avec l’outil dégradé {!svg: tools/inkscape/icons/color-gradient.svg}, c’est les deux premières options à gauche dans la barre d’outil.

#### {!svg: tools/inkscape/icons/paint-gradient-mesh.svg} Filet de dégradé (mesh gradient)

Les filets de dégradés permettent une gestion très fine des dégradés, ce qui s’avère utile notamment en dessin pour faire des dégradés complexes

{!svg: tools/inkscape/5-mesh-gradient.svg}

L’option dans fond et contour ne permet que de réutiliser des filets existants, pour en créer vous aurez besoin de l’outil filet de dégradé {!svg: tools/inkscape/icons/mesh-gradient.svg}.

{!img: tools/inkscape/5-mesh-gradient-tools.png}

Avant usage, sélectionnez le mode (grille / conique), le nombre de lignes et de colonnes dans la grille (pour un filet conique, ça correspondra respectivement aux ellipses intermédiaires et aux rayons), puis double-cliquez sur l’objet où appliquer le filet de dégradé. De là, vous aurez une grille de poignées.

- Les losanges sont comme les « étapes » du dégradé, auxquelles vous pouvez assigner des couleurs différentes (pour cela sélectionnez la poignée et changez la couleur dans fond et contour ou avec une palette)
- Les cercles (ou flèches) permettent de modifier les courbes entre les points, qui changeront où la transition entre les couleurs adjacentes se fera.

Ensuite, vous pouvez éventuellement réutiliser un filet existant sur un autre objet depuis le dialogue fond et contour.

#### {!svg: tools/inkscape/icons/paint-pattern.svg} Motif

Dans l’onglet motif, vous avez tout un tas de motifs prédéfinis : rayures, damiers, pois, … Vous avez juste à en sélectionner un de la liste.

Pour modifier le motif, utilisez l’outil édition de chemin {!svg: tools/inkscape/icons/tool-node-editor.svg} (ou double-clic). En haut à gauche, vous avez trois nouvelles poignées :

- La croix contrôle l’origine du motif
- Le carré contrôle son échelle
- Le cercle contrôle son orientation

{!img: tools/inkscape/5-pattern-edit.png}

#### {!svg: tools/inkscape/icons/paint-swatch.svg} Échantillon

Les échantillons (swatches) permettent d’enregistrer simplement la couleur d’un objet, et de la rendre réutilisable. Pour ça rien de plus simple, allez-y, choisissez la couleur avec le sélecteur de couleur en bas, et la couleur restera échantillonnée, vous pourrez la resélectionner pour d’autres objets en retournant dans l’onglet échantillon.

C’est aussi un bon moyen de se faire des palettes à partir de dégradés : créez deux chemins quelconques avec les deux couleurs extrèmes (ça doit être des chemins, si c’est autre chose convertissez-les d’abord avec objet > objet en chemin), sélectionnez les deux, puis utilisez l’extension extensions > génerer à partir du chemin > interpoler, cochez bien *interpoler le style*, choisissez le nombre d’étapes (au final il y aura n+2 couleurs vu que vous avez déjà les 2 extrémités), lancez.
Ensuite, vous n’avez qu’à cliquer sur le premier, aller sur l’option échantillon dans fond et contour, et ça enregistrera sa couleur. Plus qu’à faire pareil pour chacune des autres couleurs et vous aurez votre palette dans vos échantillons :

{!img: tools/inkscape/5-gradient-palette.png}

## Le style de contour

Dans le dialogue fond et contour, vous avez un troisième onglet, style de contour, qui donne des options pour changer l’apparence du contour et ses interactions avec le reste.

{!img: tools/inkscape/5-stroke-style.png}

- L’*épaisseur* donne simplement l’épaisseur du trait
- Vous avez toute une liste d’option de *pointillés*, le nombre à côté permet de décaler le pointillé. Quand vous avez un pointillé de sélectionné, vous avez une boite *motif* en-dessous qui permet de créer un pointillé personnalisé en donnant les longueurs des éléments. Par exemple ici, on a un tiret de 2 épaisseurs de long, un espace de 2 épaisseurs de long, un tiret de 1 épaisseur, un espace de 1, un tiret de 1, et un espace de 2.

{!img: tools/inkscape/5-custom-dash.png}

- Les *marqueurs* permettent de placer des motifs, comme des flèches, des points, ... aux différents points d’un objet. Celui de gauche change le marqueur à la première extrémité du chemin, celui de droite à l’autre extrémité, et celui du milieu mettra des marqueurs à chaque point intermédiaire du chemin.
- Le *raccord* donne la forme des angles

{!svg: tools/inkscape/5-stroke-joins.svg}

- La *terminaison* donne l’apparence des extrémités du chemin. Dans l’exemple ci-dessous, on s’intéresse au chemin noir, le trait rouge est en-dessous et calé pour que l’extrémité du chemin noir soit exactement là où passe le trait rouge (pour la différence entre la terminaison droite et la terminaison carrée)

{!svg: tools/inkscape/5-stroke-cap.svg}

- Enfin, l’*ordre de rendu* spécifie l’ordre dans lequel seront rendus les composants du chemin (fond, contour, marqueurs). Par défaut c’est le fond derrière, le contour ensuite et les marqueurs tout au-dessus, mais parfois on peut vouloir autre chose (par exemple le fond par-dessus le contour pour que le fond fasse bien toute la taille de l’objet au lieu d’être partiellement recouvert). Dans les icones, le rectangle bleu représente le fond, le cadre représente le contour et le cercle les marqueurs.

{!img: tools/inkscape/5-paint-order.png}

- Avoir les contours ou les marqueurs en premier ne change rien sauf si le contour est en dégradé, comme les marqeurs ne seront pas dégradés dans ce cas (mais ils prendront la même couleur unie ou le même motif le cas échéant)

## Options de rendu

Tout en bas du dialogue fond et contour, vous avez deux curseurs qui permettent de modifier le rendu de l’objet en général :

- Le *flou* pour flouter l’objet
- L’*opacité* pour rendre l’objet plus ou moins opaque ou transparent. Et ça modifie bien tout l’objet, pas juste la transparence d’une couleur

### Le mode de fondu

Toujours en bas du dialogue, vous avez une liste déroulante intitulée « mode de fondu » (blending mode), qui définit comment l’objet apparaîtra en fonction de ce qu’il y a en-dessous.
Par défault, tout est en mode « normal », qui affiche bêtement l’objet au-dessus de ceux qui sont derrière lui, mais il y a plein d’autres options, qui font d’autres opérations entre les deux. Prenons un exemple, avec à droite ce qu’on mettra par-dessus.

{!img: tools/inkscape/5-blend-base.png}

Exemples des différents modes avec différents niveaux d’opacité :

#### Mode normal

- **Normal** : Simple superposition

{!img: tools/inkscape/5-blend-normal.png}

#### Modes assombrissants

Dans ces modes, le blanc est neutre (il ne change rien), et le noir est prédominant (il s’affiche par-dessus tout)

- **Produit** (multiply) : Multiplication des coordonnées RGB, correspond à l’effet d’un filtre de couleur. Donne toujours une couleur plus sombre.

{!img: tools/inkscape/5-blend-multiply.png}

- **Obscurcir** (darken) : Garde les coordonnées RGB les plus sombres des deux.

{!img: tools/inkscape/5-blend-darken.png}

- **Brûlage de couleur** (color-burn) : « Crame » l’objet en-dessous avec un effet similaire au produit avec un contraste très accentué. Avec une opacité moyenne, plutôt que comme réelle combinaison, ça peut servir à réhausser le contraste des zones claires de quelque chose.

{!img: tools/inkscape/5-blend-burn.png}

#### Modes éclaircissant

Dans ces modes, le noir est neutre et le blanc est prédominant.

- **Écran** (screen) : Opposé du produit des opposés des coordonnées RGB, correspond plus ou moins à une synthèse additive. Donne toujours une couleur plus claire.

{!img: tools/inkscape/5-blend-screen.png}

- **Éclaircir** (lighten) : Garde les coordonnées RGB les plus claires des deux.

{!img: tools/inkscape/5-blend-lighten.png}

- **Estompage de couleur** (color-dodge) : « Crame » aussi l’objet en-dessous, mais vers les tons clairs, donc réhausse plutôt le contraste des zones foncées.

̣{!img: tools/inkscape/5-blend-dodge.png}

#### Modes contrastants

Dans ces modes, le gris à 50% de luminosité est neutre.

- **Superposition** (overlay) : Combine les couleurs de façon plus ou moins « neutre » (contrairement à produit et écran qui biaisent vers les tons foncés ou clairs), en réhaussant le contraste

{!img: tools/inkscape/5-blend-overlay.png}

- **Lumière douce** (soft-light) : C’est un peu pareil, mais sans le côté plus contrasté, donc c’est plus léger

{!img: tools/inkscape/5-blend-soft.png}

- **Lumière crue** (hard-light) : C’est aussi un peu pareil, sauf que les couleurs de l’objet au-dessus écrasent vraiment celles d’en-dessous

{!img: tools/inkscape/5-blend-hard.png}

#### Modes inverseurs

Ces modes auront tendance à inverser les couleurs

- **Différence** (difference) : Soustrait les deux objets et prend la valeur absolue. Le noir n’a aucun effet, le blanc inverse complètement les couleurs.

{!img: tools/inkscape/5-blend-difference.png}

- **Exclusion** (exclusion) : C’est à peu près pareil, avec une inversion plus relative à l’objet filtré (du coup le gris à 50% de luminosité absorbe complètement les couleurs)

{!img:tools/inkscape/5-blend-exclusion.png}

#### Modes de composition

Ces modes servent à paramétrer les couleurs TSL/TSV de l’objet en-dessous avec l’objet au-dessus

- **Teinte** (hue) : Garde la luminosité et la saturation de l’objet filtré avec la teinte du filtre.

{!img: tools/inkscape/5-blend-hue.png}

- **Saturation** (saturation) : Garde la teinte et la luminosité de l’objet filtré avec la saturation du filtre. Attention, certaines couleurs qui ont l’air de gris peuvent ne pas être complètement pures, et un filtre à haute saturation comme ici va remonter cette invisible saturation au maximum, d’où l’aspect cramé ici, c’est juste du gris qui est mal passé.

{!img: tools/inkscape/5-blend-saturation.png}

- **Couleur** (color) : Garde la luminosité de l’objet filtré avec la teinte et la saturation du filtre. C’est ce qui permet de coloriser du noir-et-blanc par exemple (vu que le noir et blanc c’est juste une info de luminosité)

{!img: tools/inkscape/5-blend-color.png}

- **Luminosité** (luminosity) : Garde la teinte et la saturation de l’objet filtré avec la luminosité du filtre
