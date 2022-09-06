# TODO

## A faire

- ~~Type~~
- Studio
- ~~Favoris~~
- Tags

- ~~Passer tout les select uniques avec un where sur une ID et remplacer par un GET
  Par exemple: Series().get(Series.id == current_season_id)~~

- Passer tout les get en unique. Remplacer par exemple **Series().get(Series.id == current_season_id)** **par Series().get(current_season_id)**

- Voir si dans la table Planning, on peut enlever la colonne serie comme on à déja la saison, on peut faire un season.serie pour récupérer les infos de la série.
- Retirer l'épisode vu du planning
- Double cliquer ou bien bouton pour aller directement sur la série / saison dans l'onglet full_list_tab
- Combiner des refresh et autre dans une fonction fait pour

- ~~Changer le nom des évènements de on en when: self.on_~~
- Système de MAJ
- Dialogue About + Licences logiciels + icones
- Fichier de paramétrage json
- Passer les isdeleted en boolean ?
- Afficher le titre de la série quand le nom de la saison est vide ?
- Liste des séries et saisons supprimées:
  - Restaurer / supprimer définitivement