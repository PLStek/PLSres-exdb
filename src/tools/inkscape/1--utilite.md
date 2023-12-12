//// title = "À quoi ça sert"
//// description = "L’utilité d’Inkscape et du dessin vectoriel"

# {=title}

## Le dessin vectoriel

Les images habituelles (JPEG, PNG, GIF, etc.) sont dites *matricielles*, parce qu’elles sont constituées d’une grille de pixels, chaque pixel ayant sa valeur de couleur.
Les images dites *vectorielles* ont un paradigme complètement différent : plutôt que de stocker une grille de pixels, on stocke la description d’objets géométriques. Ça implique beaucoup de différences :

- Une image vectorielle a une résolution virtuellement infinie, vu que c’est une description géométrique, alors qu’une image matricielle a une résolution finie et si vous zoomez trop ça va se voir
- Une image vectorielle garde toute l’information des formes géométriques qui la composent, que vous pouvez toujours modifier comme des formes géométriques et non comme des tas de pixels
- Une image matricielle de bonne résolution doit stocker une matrice de (largeur × hauteur × nombre de canaux de couleur), donc on arrive vite à des (1920×1080×4) = 8.3Mo, et ça se compresse pas toujours très bien. Le vectoriel contient des définitions géométriques d’objets sur l’image, donc sera généralement plus léger.
- Forcément, le vectoriel a ses limites, et est particulièrement adapté aux logos, icones, diagrammes, graphiques, …, mais pas aux photos et autres images pas aussi géométriques

En résumé, pour tout ce qui est diagrammes, logos, icones, graphiques, …, utilisez du vectoriel !

### Le format SVG

SVG (*Scalable Vector Graphics*) est un format d’images vectorielles à base de XML, et normalisé par le [W3C](https://www.w3.org/Graphics/SVG/) (World Wide Web Consortium). C’est donc une technologie du web, qui a plein d’avantages :

- C’est de très, *très* loin le format vectoriel le plus utilisé (à part le langage PostScript dans les PDF)
- C’est un standard ouvert
- C’est une technologie de base du web, qui peut s’intégrer directement dans des pages web dans à peu près n’importe quel navigateur (à un moment ceux qui utilisent encore IE8 tant pis pour eux)
	- Ça s’intègre autant comme contenu externe que directement dans la page HTML
	- Et comme ça se redimensionne à volonté c’est parfait pour les arranger sous tous les formats d’écran
	- Vous pouvez même utiliser du CSS dessus
- C’est léger et ça se compresse bien
- C’est un standard largement accepté et utilisé par de nombreux logiciels et de nombreuses technologies.
- Et enfin, c’est le format qu’utilise Inkscape à la base

## Inkscape

Inkscape est un logiciel libre d’édition d’image vectoriel, que vous pouvez trouver ici : [https://inkscape.org/](https://inkscape.org/) \
C’est globalement le logiciel libre le plus reconnu pour ça, si vous cherchez du plus lourd vous trouverez du côté d’Adobe Illustrator ou ce genre de choses. Il est dispo sur tous les systèmes majeurs.

Connaître un minimum un logiciel de dessin vectoriel vous permettra de faire vos logos, schémas et diagrammes de façon beaucoup plus nette, propre et éventuellement complexe que ce que vous pouvez faire avec un éditeur d’images classique ou les 2-3 crotouilles qu’il y a dans les logiciels de type Office. Ça fera beaucoup plus classe dans tous vos rapports, vos projets, et comme vous saurez faire vos diagrammes vous serez moins dépendants de Google Images et de ses images de 40px² avec une watermark immense.

Vous pouvez faire virtuellement n’importe quoi avec Inkscape, ici ce sera plutôt orienté schémas et diagrammes vu que c’est surtout pour ça que c’est utile pour les études mais ça va de ça au design graphique, au dessin, à la création de polices d’écritures ou à la découpe laser.

En l’état on est sur Inkscape 1.2, on essaiera de tenir ça à jour si des gros trucs changent. Une bonne partie de l’interface est personnalisable, si vous voulez tout pareil qu’ici, c’est dans le menu édition > préférences > interface > thème, tout sera en thème Adwaita clair avec les icones non symboliques.

### Exemples

Quelques exemples réels et faits maison pour des rapports, des présentations et même ce site. D’ailleurs une bonne partie des schémas de ce doc sont des SVG faits avec Inkscape :

{!svg: tools/inkscape/1-pipeline1.svg}

---

{!svg: tools/inkscape/1-calendrier-stats.svg}

---

{!svg: tools/inkscape/1-roulette.svg}

---

{!svg: tools/inkscape/1-chromosomes.svg}

---

{!svg: tools/inkscape/1-adn-arn.svg}

---

{!svg: info/c/compilation-chaine.svg}

---

{!svg: tools/inkscape/1-state.svg}
