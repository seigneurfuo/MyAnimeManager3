- Passer tout les select uniques avec un where sur une ID et remplacer par un GET
  Par exemple: Series().get(Series.id == current_season_id)

- Changer le nom des évènements de on en when:
  self.on_

- Voir si dans la table Planning, on peut enlever la colonne serie comme on à déja la saison, on peut faire un season.serie pour récupérer les infos de la série.
- Afficher les dates pour cette saison
- Retirer l'épisode vu du planning
- Double cliquer ou bien bouton pour aller directement sur la série / saison dans l'onglet full_list_tab