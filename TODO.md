# TODO

## En priorité
- Passer tout les get en unique. Remplacer par exemple **Series().get(Series.id == current_season_id)** **par Series().get(current_season_id)**
- Améliorer le responsive
  - Améliorer l'affichage sous Windows 

- Thême sombre windows
- Studios ?
- Tags

## Conventions des programmation
- ~~Passer tout les select uniques avec un where sur une ID et remplacer par un GET Par exemple: Series().get(Series.id == current_season_id)~~
- ~~Changer le nom des évènements de on en when: self.on_~~
- Déplacer le chargement des données dans fill_dat aau lieu de les metre dans init_ui()
- Utiliser Serie.seasons pour récupérer toutes les saison d'une série au lieu de faire: seasons.serie_id == XXX
- ~~Renommer toutes les classes dialog en Dialog à la fin du nom de la classe~~
- ~~Changer les _is_clicked en _clicked~~

## Améliorations
- Voir si dans la table Planning, on peut enlever la colonne serie comme on à déja la saison, on peut faire un season.serie pour récupérer les infos de la série.
- Retirer la date vue du planning <- Pas compris
- Double cliquer ou bien bouton pour aller directement sur la série / saison dans l'onglet full_list_tab
- Combiner des refresh et autre dans une fonction fait pour

- Système de MAJ
- Dialogue About + Licences logiciels + icones
- Fichier de paramétrage json
- Passer les isdeleted en boolean ?
- Afficher le titre de la série quand le nom de la saison est vide ?
- Liste des séries et saisons supprimées:
  - Restaurer / supprimer définitivement

- Icones sur chaque modale (ui + manuellement crées)