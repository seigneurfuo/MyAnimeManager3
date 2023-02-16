# TODO

## A faire

### Bugs
- Boutons supprimer et modifier d'une saison non grisés quand aucune n'est sélectionnée
- Pareil pour les séries ?

### En priorité
- Améliorer le responsive

### Conventions des programmation
- Déplacer le chargement des données dans fill_data au lieu de les metre dans init_ui()

### Améliorations
- Studios ?
- Tags
- Voir si dans la table Planning, on peut enlever la colonne serie comme on à déja la saison, on peut faire un season.serie pour récupérer les infos de la série.
- Passer les isdeleted en boolean ?

- Combiner des refresh et autre dans une fonction fait pour.

- Dialogue About + Licences logiciels + icones

- Afficher le titre de la série quand le nom de la saison est vide ?
- Liste des séries et saisons supprimées:
  - Restaurer / supprimer définitivement

- Icones sur chaque modale (ui + manuellement crées)

## Faits 
- ~~Retirer la date vue du planning~~
- ~~Utiliser Serie.seasons pour récupérer toutes les saison d'une série au lieu de faire: seasons.serie_id == XXX~~
- ~~Système de notification de MAJ~~
- ~~Fichier de paramétrage json~~
- ~~Thême sombre windows~~
- ~~Passer tout les get en unique. Remplacer par exemple **Series().get(Series.id == current_season_id)** **par Series().get(current_season_id)**~~
- ~~Supprimer les self.current_serie_id et self.current_season_id~~