# TODO

## En priorité
- ~~Passer tout les get en unique. Remplacer par exemple **Series().get(Series.id == current_season_id)** **par Series().get(current_season_id)**~~
- Supprimer les self.current_serie_id et self.current_season_id
- Améliorer le responsive
  - ~~Améliorer l'affichage sous Windows~~ 

- ~~Thême sombre windows~~
- Studios ?
- Tags

## Conventions des programmation
- Déplacer le chargement des données dans fill_data au lieu de les metre dans init_ui()
- ~~Utiliser Serie.seasons pour récupérer toutes les saison d'une série au lieu de faire: seasons.serie_id == XXX~~

## Améliorations
- Voir si dans la table Planning, on peut enlever la colonne serie comme on à déja la saison, on peut faire un season.serie pour récupérer les infos de la série.
- ~~Retirer la date vue du planning~~
- Double cliquer ou bien bouton pour aller directement sur la série / saison dans l'onglet full_list_tab
- Combiner des refresh et autre dans une fonction fait pour

- Système de MAJ
- Dialogue About + Licences logiciels + icones
- ~~Fichier de paramétrage json~~
- Passer les isdeleted en boolean ?
- Afficher le titre de la série quand le nom de la saison est vide ?
- Liste des séries et saisons supprimées:
  - Restaurer / supprimer définitivement

- Icones sur chaque modale (ui + manuellement crées)