//// title = "Le texte"
//// description = "Utilisation de l’outil texte dans Inkscape"

# {=title}

L’outil texte {!svg: tools/inkscape/icons/draw-text.svg} sert évidemment à écrire du texte. Il a plein d’options qu’on va voir rapidement ici.

## Créer un objet texte

Pour ça rien de plus simple, il suffit de prendre l’outil texte, cliquer là où vous voulez le mettre et taper votre texte.

{!img: tools/inkscape/6-text-tool.png}

Déjà vous avez plus ou moins les mêmes fonctionnalités que n’importe quoi où vous pouvez taper du texte. L’espèce de losange à droite délimite la largeur d’une ligne, par défaut elle bouge avec le texte donc tout sera sur une ligne, mais vous pouvez la déplacer pour avoir des sauts de ligne automatiques.

La barre d’outil contient tout ce à quoi on peut s’attendre pour éditer du texte, de gauche à droite :

- Police d’écriture
- Style (gras, italique)
- Taille de police
- Hauteur des interlignes
- Alignement (gauche, droite, centré)
- Indice et exposant
- Espacements entre les caractères et entre les mots
- Orientation du texte

{!img: tools/inkscape/6-text-tools.png}

## Contour et remplissage

Pour changer la couleur du texte, tout se passe exactement comme n’importe quel autre objet, dans le dialogue *Fond et contour*. Toutes les options habituelles sont disponibles (uni, dégradé, motif, …). Notez bien que pour changer la couleur du texte lui-même vous devrez passer par la couleur de **fond**, la couleur de contour ajoute un contour au texte (qui peut être stylisé avec toutes les options habituelles aussi).

{!svg: tools/inkscape/6-text-stroke.svg}

## Texte et police

Le dialogue *Texte et police* offre des options plus avancée pour la police d’écriture de votre texte. Pour l’ouvrir, clic droit sur un objet texte > Texte et police ou menu `Texte > Texte et police`

{!img: tools/inkscape/6-dialog.png}

Le premier onglet donne les options de base, et permet notamment de définir les options par défaut quand vous créez un nouvel objet texte. Vous pouvez choisir la police d’écriture à gauche, les styles en haut à droite, la taille, et un exemple en bas. Pour tout ce que vous ferez dans ce dialogue, il faudra cliquer sur le bouton *Appliquer* pour que ça s’applique aux objets texte sélectionnés. Le bouton *Définir comme valeur par défaut* enregistre les options actuelles en tant qu’options initiales pour tous les nouveaux textes.

Le troisième onglet, *Texte*, permet de taper sans formatage avant de l’appliquer à un objet texte, c’est pratique quand vous faites des choses moyennement lisibles en direct (style qui ressort mal, orientations bizarres, polices spéciales ou de symboles, …). Pareil, *Appliquer* pour appliquer les modifications à un objet texte.

{!img: tools/inkscape/6-dialog-text.png}

Là où il y a les vrais détails, c’est dans le deuxième onglet, *Caractéristiques*. Vous avez plusieurs groupes d’options. Notez que les options disponibles dépendent de la police d’écriture, si elle ne les définit pas elles ne seront pas disponibles. Donc pour des fonctionnalités vraiment particulières (ligatures historiques, certains styles de capitalisation), vous aurez peut-être besoin de polices spécifiques. Ça fait aussi que les polices font ce qu’elles veulent, donc ça peut parfois un peu dériver des fonctionnalités de base.

- Les *ligatures* sont des effets de style qui relient certains caractères, comme `ffi` dans efficace ⟶ eﬃcace. Il n’y en a pas tant que ça en latin, par contre c’est important dans d’autres systèmes d’écriture (comme l’arabe).
- La *position* en indice ou exposant
- Les *capitales* donnent un style de capitalisation (petites majuscules avec ou sans capitales, « unicasse » qui normalement met majuscules et minuscules à la même taille, …)

{!img: tools/inkscape/6-capital-styles.png}

- Vous avez différentes options de style pour les chiffres (chaque fois, « par défaut » donne l’option préférée par la police d’écriture, qui peut être l’une des deux options présentées)
	- Le *style* permet de choisir entre le style moderne (chiffres tous de la même taille et posés sur la ligne de base) et ancien (taille et position spécifiques à chaque chiffre)
	- La *largeur* permet de choisir entre une largeur adaptative (selon la largeur graphique) ou « tabulaire » (tous les chiffres de la même largeur, par exemple pour faire des colonnes bien alignées dans un tableau)
	- Le *style de fraction* permet de mettre les fractions en diagonale (¼) ou verticales (*la police d’écriture du site ne le permet pas mais vous voyez l’idée*)
	- Dans certaines polices vous pouvez aussi avoir des *ordinaux* (les 1ᵉʳ, 2ᵉ, … tous faits), et éventuellement des *0 barrés* (`0`)

{!img: tools/inkscape/6-digit-style.png}
{!img: tools/inkscape/6-digit-width.png}

## Organiser du texte sur un chemin

On a parlé précédemment d’utiliser des objets pour en positionner d’autres — c’est exactement ce qu’on peut faire avec du texte. Pour cela, sélectionnez l’objet (ça peut être n’importe quoi, ellipses, spirales, chemins, …), l’objet texte, puis utilisez l’option `Texte > Mettre suivant un chemin`

{!svg: tools/inkscape/6-text-path.svg}

Le texte suit alors le contour de l’objet, et vous pouvez toujours éditer le texte et le support individuellement. Pour retirer le texte de l’objet, c’est l’option inverse `Texte > Retirer du chemin`.

## Insérer des caractères spéciaux

Vous avez accès à une table de caractères spéciaux pour insérer ce que vous voulez dans vos texte. C’est un peu sommaire, mais ça marche. Pour l’ouvrir, c’est dans `Texte > Caractères unicode`. Ça vous ouvrira ce dialogue :

{!img: tools/inkscape/6-unicode-table.png}

Choisissez la police d’écriture pour vous donner les caractères disponibles dans cette police, le style n’est que pour l’affichage ici, une fois inséré ça se conformera au reste de l’objet texte.
Vous avez donc des listes déroulantes pour choisir parmi les systèmes d’écriture et les tables de caractères disponibles, qui affichent ensuite une table de caractères disponibles (il est possible qu’à la première ouverture ça n’affiche rien, changez de sous-ensemble et revenez pour corriger le problème). Vous avez une boite de texte en bas à gauche où vous pouvez taper. Vous pouvez y mettre des caractères spéciaux en double-cliquant sur un caractère de la table.

{!img: tools/inkscape/6-unicode-box.png}

Ceci fait, plus qu’à cliquer sur *Ajouter* pour insérer le texte dans l’objet texte sélectionné

{!svg: tools/inkscape/6-unicode-inserted.svg}
