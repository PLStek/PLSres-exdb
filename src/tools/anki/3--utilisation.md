//// title = "Utilisation de base"
//// description = "Comment utiliser la fonctionnalité de base d’Anki"

# {=title}

À la {> tools.anki.setup: page précédente} on a vu comment ajouter des paquets préexistants, maintenant on va les utiliser.

## Apprendre des cartes

Pour commencer, il suffit de cliquer sur le paquet que vous voulez réviser :

{!img: tools/anki/3-decks.png}

Un paquet est un ensemble de cartes. Chaque carte a un recto, qui demande ce dont vous devez vous rappeler — ici, mettons que j’ai ce mot allemand, et que je dois me rappeler de son sens :

{!img: tools/anki/3-recto.png}

Je retrouve ce dont je dois me rappeler, puis une fois que j’ai trouvé (ou que j’ai laissé tomber), j’appuie sur *afficher la réponse* pour vérifier. À ce moment-là, le verso s’affiche, avec la réponse :

{!img: tools/anki/3-verso.png}

Vous voyez les 4 boutons en bas de l’écran, ce sont mes options pour ce que je peux faire de la carte :

- **À revoir** : Je ne me suis pas rappelé de l’information, donc je la renvoie en révision immédiate. Comme vous le voyez ici, ça la répètera dans environ 1 minute.
- **Difficile** : J’ai eu du mal à me rappeler de l’information, elle était donc *un peu trop* oubliée, donc on la ramène à un intervalle plus court que la normale (ici 6 minutes)
- **Correct** : J’estime que ma connaissance est à un niveau satisfaisant, c’est l’option normale pour une carte que j’ai bien retrouvé
- **Facile** : J’estime que retrouver cette information était trivial, et que je n’ai pas besoin de la revoir aussi vite. Ça repassera la carte avec un intervalle plus long (ici 4 jours)

Les cartes ont en gros deux « modes » : le mode apprentissage, et le mode revue. La carte ci-dessus était en mode apprentissage, c’est dans ce mode que les cartes arrivent pour la première fois, ou après avoir sélectionné *à revoir* : Anki vous repasse la carte plusieurs fois à des intervalles très courts pour que vous l’appreniez. Ensuite, après quelques passages réussis, l’intervalle augmentera et la carte passera en mode revue :

{!img: tools/anki/3-graduating.png}

Comme vous le voyez, l’intervalle correct passe à 1 jour, la carte sera donc ramenée le lendemain, et à partir de là la carte sera repassée à intervalles exponentiellement plus importants, comme on l’a vue sur la courbe de l’oubli. Par exemple, j’ai déjà revu cette carte plusieurs fois et ses intervalles sont de plus en plus long :

{!img: tools/anki/3-review.png}

Sur la liste des paquets, ou quand la carte est côté recto, vous pouvez voir des nombres ici :

{!img: tools/anki/3-counts-deck.png}
{!img: tools/anki/3-counts.png}

Le nombre en bleu est le nombre de nouvelles cartes en attente, le nombre en rouge est le nombre de cartes en cours d’apprentissage, le nombre de cartes en vert est le nombre de cartes à revoir. Chaque jour, vous aurez un certain nombre de nouvelles cartes, et des cartes des jours précédents à revoir. Tant que vous êtes régulier, vous avancerez comme ça efficacement, en quelques minutes par jour. On verra plus tard comment paramétrer tout ça.

Une fois que vous avez passé toutes les cartes du paquet que vous deviez revoir dans la journée, vous finissez sur cet écran :

{!img: tools/anki/3-finish.png}

Vous n’avez plus qu’à cliquer sur le bouton *paquets* pour revenir à la liste des paquets. Sur Android, pensez à synchroniser à ce moment-là, l’application ne le fait pas toujours toute seule. À part ça, tout cela est parfaitement identique sur toutes les versions de l’application.

Félicitations : à présent, vous savez comment utiliser Anki. Les prochaines pages iront un peu plus loin, pour {> tools.anki.creer: créer vos propres paquets et vos propres cartes}, et {> tools.anki.parametrage: personnaliser vos révisions}
