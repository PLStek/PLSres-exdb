//// title = "Créer vos cartes et paquets"
//// description = "Comment créer et personnaliser vos propres paquets et vos propres cartes"

# {=title}

Les paquets préexistants sont très bien, mais pour réviser vos UV vous aurez sans doute besoin de quelque chose de plus spécifique. C’est pour ça que savoir créer ses propres cartes est essentiel. Notez qu’ici on se basera sur l’application de bureau. On verra aussi comment rajouter rapidement des cartes avec l’application Android. L’application iOS est assez similaire à la version de bureau.

La version web est très sommaire sur cet aspect, vous pouvez créer un paquet avec le bouton *Create deck* en bas de la liste des paquets, et créer des cartes de façon sommaire dans l’onglet *Add* en haut de l’écran.

## Créer un paquet

Pour cela, rien de plus simple : cliquez sur le bouton *créer un paquet* en bas de la fenêtre :

{!img: tools/anki/4-create-deck.png}

Entrez le nom du paquet

{!img: tools/anki/4-create-deck-form.png}

Et c’est fait, vous avez créé un paquet vide.

## Ajouter des cartes
### Avant de commencer

Il va falloir comprendre un concept supplémentaire : les *notes*. Dans Anki, vous avez des *paquets*, qui contiennent des *notes*, auxquelles correspondent une ou plusieurs *cartes*. Par exemple, mettons que j’ai le mot allemand *Schwerkraft*, qui correspondrait à la *gravité*. Ça peut être intéressant de l’apprendre dans les deux sens, allemand ⟶ français et français ⟶ allemand. Le système de *notes* permet ça : je crée une note qui fait correspondre *Schwerkraft* à *gravité*, et cette note produit 2 cartes, une dans chaque sens. Ce qu’on va ajouter, c’est donc des notes, qu’on peut largement personnaliser pour faire plusieurs cartes chacune comme ça.

### Ajouter des notes

Pour ajouter des notes à un paquet existant, c’est par le bouton *Ajouter* en haut de l’écran :

{!img: tools/anki/4-add-button.png}

Ça ouvre le dialogue de création de cartes. La première étape est de choisir dans quel paquet vous souhaitez ajouter des cartes :

{!img: tools/anki/4-select-deck.png}
{!img: tools/anki/4-select-deck-dialog.png}

Double-cliquez sur le paquet où vous voulez ajouter la carte, ou cliquez sur le paquet puis sur le bouton *choisir*. Ensuite, la boite *type* en haut à gauche vous permet de choisir le type de note :

{!img: tools/anki/4-select-type.png}
{!img: tools/anki/4-select-type-dialog.png}

À la base vous avez les types *Basique*, là j’en ai quelques autres, on verra bientôt comment créer nos propres types de carte très bientôt.

Les types basiques correspondent à ça :

- Basique : simple carte avec un recto et un verso
- Basique (envers facultatif) : Une carte recto ⟶ verso, et la carte inverse verso ⟶ recto seulement si vous mettez quelque chose dans le champ *Ajouter un envers*
- Basique (et envers de la carte) : Deux cartes, une dans chaque sens (recto ⟶ verso et verso ⟶ recto)
- Basique (saisissez la réponse) : Une carte recto ⟶ verso, qui vous demandera de taper la réponse et qui vous montrera vos éventuelles fautes d’orthographe

Ici c’est du vocabulaire, on va mettre *Basique (et envers de la carte)*

{!img: tools/anki/4-add-dialog.png}

Reste plus qu’à remplir la note. Ici on a deux champs à remplir : `recto`, pour un côté de la carte, et `verso` pour l’autre. juste au-dessus, vous avez des options de formatage très ressemblante à ce que vous pouvez trouver sous Word et consorts. On parlera des boutons *Champs* et *Cartes* quand on créera nos propres types de notes.

Une fois vos champs remplis, vous n’avez plus qu’à cliquer sur *Ajouter* ou appuyer sur Maj+Entrée, et la carte sera enregistrée. Si par hasard vous vous rendez compte après que vous avez fait une erreur, vous avez le bouton *Historique* en bas de la fenêtre pour revenir à une carte précédente :

{!img: tools/anki/4-history.png}
{!img: tools/anki/4-correction.png}

Vous tombez sur la fenêtre *Parcourir* qu’on verra juste après, mais d’ici là vous pouvez corriger votre carte en bas à droite. Elle sera enregistrée automatiquement.

Félicitations ! Vous savez ajouter des nouvelles cartes. Vos paramètres sont persistants, pour ajouter plusieurs cartes d’affilée vous avez juste à remplir de nouveau les champs et à ajouter la carte.

## Modifier des notes existantes

Pour modifier des notes existantes (ou les supprimer), vous pouvez utiliser la fenêtre *Parcourir*

{!img: tools/anki/4-browse.png}
{!img: tools/anki/4-browse-dialog.png}

Beaucoup de choses à voir ici, on ne verra pas tout tout de suite.
À gauche de la fenêtre, vous avez les nombreux critères de sélection. Cliquer sur l’un d’entre eux affichera toutes les cartes qui correspondent (tous paquets confondus). En haut à droite, vous avez les cartes qui correspondent au critère choisi, et en bas à droite, vous pouvez modifier la carte choisie (et en voir un *aperçu*). Et tout en haut à droite, vous avez une barre de recherche pour faire une recherche normale dans vos cartes.

- **Aujourd’hui** : Donne les cartes avec lesquelles vous avez intéragi aujourd’hui, comme celles que vous avez étudié, modifié, les nouvelles cartes, les cartes dues dans la journée, etc.
- **Marqueurs** : Liste les cartes par marqueur de couleur. Pour ajouter un marqueur à une carte, trouvez-la dans la liste en haut à droite, clic droit dessus > marqueur.
- **État de la carte** : Liste selon l’état de la carte (nouvelles cartes pour aujourd’hui, en apprentissage, à revoir, etc.)
- **Paquets** : Liste toutes les cartes du paquet sélectionné.
- **Types de notes** : Liste toutes les notes du type demandé.

Une fois les cartes que vous voulez listées, vous pouvez fouiller la liste des cartes, cliquer sur celle qui vous intéresse et la modifier en bas à droite. Vous avez une colonne avec des mentions *Carte 1*, *Carte 2*, … : ce sont les cartes qui correspondent à une même note. Par exemple, une carte *Basique (et envers de la carte)* aura une carte 1 (recto ⟶ verso) et une carte 2 (verso ⟶ recto). Pas la peine de modifier les deux, si vous modifiez l’une l’autre suivra.

Un clic droit sur une carte vous donnera la plupart des options utiles dessus. En particulier, vous pouvez la changer de paquet si nécessaire. Pour supprimer la note (ça supprimera la note donc toutes les cartes associées), c’est dans *Notes > Supprimer*.

{!img: tools/anki/4-delete.png}

## Créer de nouveaux types de cartes
### Créer le type de note

Tout ça est très chouette, mais très insuffisant pour beaucoup de choses. Par exemple, j’ai toujours mon mot *Schwerkraft*. Sauf qu’il n’y a pas que le mot, il y a son genre et son pluriel. Or actuellement, le recto de la carte ressemble à ça :

{!img: tools/anki/4-insufficient.png}

J’aimerais bien que l’article et le pluriel ne s’affichent qu’après avoir retourné la carte. C’est pour ça que je vais devoir créer un nouveau type de carte. Pour cela, dans la fenêtre pour ajouter des cartes, quand on va sélectionner le type de note, on va cliquer sur *Gérer*

{!img: tools/anki/4-manage-button.png}
{!img: tools/anki/4-manage.png}

On a ici tous les types de cartes existants, on peut les renommer, les supprimer, mais surtout en ajouter de nouveaux avec le bouton *Ajouter*

{!img: tools/anki/4-add-type.png}

Après avoir cliqué sur *Ajouter*, vous pouvez sélectionner le modèle de votre nouveau type de notes, choisissez le plus proche de ce que vous voulez faire. Ici je veux des cartes double face (allemand ⟶ français et français ⟶ allemand), donc on va partir de *Basique (et envers de la carte)*. Entrez un nom pour votre type de note, appuyez sur Entrée, et votre type de note est créé. Fermez la fenêtre de gestion des types de cartes, choisissez votre nouveau type dans l’autre fenêtre, et revenez à la fenêtre d’ajout de note.

### Modifier les champs

Maintenant, on va modifier les champs pour accommoder nos besoins. Pour cela, c’est le bouton *Champs* :

{!img: tools/anki/4-fields-button.png}
{!img: tools/anki/4-fields.png}

Vous avez la liste des champs, actuellement on a *recto* et *verso*. Vous pouvez les supprimer, renommer ou repositionner avec les boutons à droite, et en ajouter de nouveau. Avec tout ça, on peut créer les champs dont on a besoin : l’allemand recto, l’allemand verso avec l’article et le pluriel, et le français :

{!img: tools/anki/4-fields-edited.png}

Plus qu’à cliquer sur *Enregistrer* en bas, et on a nos champs. Reste plus qu’à faire la présentation des cartes.

### Modifier la présentation des cartes

Pour ça, c’est avec le bouton *Cartes* de la fenêtre d’ajout de notes :

{!img: tools/anki/4-cards-button.png}
{!img: tools/anki/4-cards.png}

Tout d’abord, allez dans le menu déroulant *Options* de l’aperçu et cochez *Remplir les champs vides*, ça évitera les messages d’erreur « la carte est vide » et vous pourrez vraiment voir la présentation à droite.

{!img: tools/anki/4-fill-empty-fields.png}

Ensuite, on va créer la template de nos cartes. On aura besoin d’une carte *DE-Recto* vers *DE-Verso* et *FR*, et d’une *FR* vers *DE-Verso* et *FR*. C’est un langage de templating assez simple, rien de bien complexe pour le moment. Pour inclure un champ, mettez `{{nom du champ}}`. Par exemple ici, pour le recto on affiche juste l’allemand recto, donc `{{DE-recto}}` :

{!img: tools/anki/4-card-de-recto.png}

Comme vous le voyez dans l’aperçu, le recto de la carte présentera le champ `DE-recto`. Maintenant, passons au *modèle du verso* pour faire la présentation du verso. Au verso de ces cartes, on veut le champ allemand complet *DE-verso*, donc `{{DE-verso}}`, et le champ français, donc `{{FR}}`. Cette fois, on va appliquer un peu de formatage pour améliorer la présentation. Pour le formatage c’est à base de HTML, si vous connaissez pas de problème, sinon il suffit juste de mettre ces balises où c’est pertinent :

- `<b>Contenu</b>` : Met le contenu en **gras**
- `<i>Contenu</i>` : Met le contenu en **italique**
- `<u>Contenu</u>` : **Souligne** le contenu
- `<hr />` : Affiche une ligne horizontale

Vous pouvez utiliser quasiment n’importe quoi en HTML, et même utiliser des styles CSS dans l’onglet *styles* si vous connaissez, mais en principe vous n’aurez pas besoin de beaucoup plus que ça. Donc ici, ça donne :

{!img: tools/anki/4-card-verso.png}

On a fait notre carte allemand ⟶ français, maintenant reste à faire la carte français ⟶ allemand. Pour ça, sélectionnez la carte 2 dans la liste déroulante en haut de la fenêtre :

{!img: tools/anki/4-card-select.png}

Plus qu’à faire pareil en mettant `{{FR}}` au recto et `{{FR}}` et `{{DE-verso}}` au verso :

{!img: tools/anki/4-card-fr-recto.png}
{!img: tools/anki/4-card-fr-verso.png}

Vous remarquerez que j’ai utilisé `{{FrontSide}}` : Ça permet de remettre exactement le contenu du recto, présentation incluse, donc pour cette carte c’est parfait (pas pour la première vu qu’il fallait changer entre `DE-recto` et `DE-verso`)

Et voilà ! Plus qu’à cliquer sur *Enregistrer* en bas à droite de la fenêtre et c’est plié. Vous pouvez éventuellement gérer les cartes qui vont avec le type de notes dans le menu *Options* à droite du sélecteur de cartes.

Félicitations : vous savez créer votre propre type de cartes. À présent, vous pouvez le sélectionner comme les autres et faire des cartes avec :

{!img: tools/anki/4-fill-note.png}
{!img: tools/anki/4-test-card-recto.png}
{!img: tools/anki/4-test-card-verso.png}
