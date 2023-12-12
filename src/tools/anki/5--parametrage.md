//// title = "Paramétrer ses révisions"
//// description = "Le paramétrage des paquets Anki"

# {=title}

Maintenant, on va voir comment paramétrer les options de ses paquets pour gérer plus précisément ses révisions.

## Les groupes d’options

Pour ouvrir les options d’un paquet, cliquez sur le petit engrenage à droite de la liste.

{!img: tools/anki/5-settings-button.png}

Les paramètres fonctionnent par « groupes d’options ». C’est pas le plus pratique, mais ça permet de garder les mêmes options pour plusieurs paquets. Vous avez la liste déroulante des groupes d’options en haut, où vous pouvez changer le groupe d’options du paquet sélectionné ; et juste à côté vous avez les options pour ajouter, dupliquer, renommer ou supprimer un groupe.

{!img: tools/anki/5-group-list.png}
{!img: tools/anki/5-group-settings.png}

## Paramétrer les révisions

Maintenant qu’on a le bon groupe, on peut paramétrer nos révisions. On va voir rapidement ce qu’il y a dans chaque section.

### Limites journalières

Limitations des nombres de cartes par jour.

- **Nouvelles cartes par jour** : Nombre de nouvelles cartes à introduire chaque jour.
- **Quota de révisions journalières** : Nombre maximal de cartes à revoir chaque jour, s’il y en a plus en attente elles seront remises au lendemain. Anki recommande de mettre ça à 10 fois le nombre de nouvelles cartes.

Ces paramètres sont ce qui conditionnent le plus la charge de travail pour le paquet. Le nombre de nouvelles cartes par jour donne le rythme d’augmentation de la charge. Dans les premières semaines le nombre de cartes à revoir chaque jour va augmenter rapidement, puis se stabiliser. En réalité, sur les gros paquets, à long terme (au bout de 2-3 mois réguliers), ça finira par se stabiliser autour de 5 fois les nouvelles cartes par jour (donc par exemple 20 nouvelles cartes par jour ⟶ 20 nouvelles + 80-100 revues par jour au bout de 2 mois). Les 10× pour la limite de revues permettent d’éponger deux jours si vous en ratez un.

### Nouvelles cartes

Définit le comportement des nouvelles cartes, en mode apprentissage.

- **Intervalle de passe** : L’intervalle d’une carte qui sort du mode apprentissage pour passer en mode révision, en jours
- **Intervalle pour les cartes faciles** : L’intervalle d’une carte qui sort du mode apprentissage par l’option « facile »
- **Ordre d’insertion** : Permet de faire apparaître les cartes dans l’ordre du paquet, ou dans un ordre aléatoire

### Chronomètre

Permet de se mettre un chrono pour la réponse

### Avancé

- **Intervalle maximum** : Par défaut, les intervalles augmentent plus ou moins à l’infini (’fin 100 ans mais bon). Pour quand même vous les rappeler à intervalles réguliers même quand les cartes sont très anciennes, vous pouvez mettre un intervalle maximal en jours. Notez que ça augmentera légèrement la charge de travail à long terme (plusieurs mois)
- **Facilité initiale** : Dans Anki, la *facilité* est le multiplicateur pour l’intervalle quand vous passez une carte avec « correct ». Pour mieux adapter la difficulté, passer une carte avec « difficile » réduit légèrement la facilité et « facile » l’augmente légèrement. Cette option donne la facilité de base : 2,5 indique que l’intervalle sera multiplié par 2,5 à chaque révision réussie.
- **Facilité bonus** : Multiplicateur de facilité quand vous passez une carte avec « facile »
- **Intervalle difficile** : Multiplicateur d’intervalle quand vous passez une carte avec « difficile »
- **Nouvel intervalle** : Permet de garder une portion de l’intervalle quand une révision est ratée (« à revoir ») plutôt que de le remettre à zéro.
