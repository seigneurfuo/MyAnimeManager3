# TODO

## A faire
- Ajouter un bouton de suppression de l'image d'une série
- Remplacer les .where().where()... en mes combinant ? .where(xx and yyy)
- Ajouter la possibilité d'avoir des images sur les saisons
- ~~Déplacer le code pour calcul l'age d'un animé dans utils~~
- ~~Renommer le nom tiles pour l'onglet qui affiche les images~~
- ~~Correction autocomplete des animés sous Windows en .exe~~
- ~~Correction du choix image pour une série pas encore crée~~
- ~~Correction du choix de la selection du dossier pour une série pas encore crée~~

### Bugs
- Boutons supprimer et modifier d'une saison non grisés quand aucune n'est sélectionnée
- Pareil pour les séries ?

### En priorité
- Améliorer le responsive
- Modifier la colonne id dans la liste des élements vus
- Déplacer le code qui récupère la liste des épisodes vus dans le code de la fenetre
### Conventions des programmation
- Déplacer le chargement des données dans fill_data au lieu de les metre dans init_ui()

### Améliorations
- ~~Studios ?~~
- ~~Tags~~
- Rechercher par valeur de champ personalisé dans l'onglet list2
- Voir si dans la table Planning, on peut enlever la colonne serie comme on à déja la saison, on peut faire un season.serie pour récupérer les infos de la série.
- Passer les isdeleted en boolean ?
- Combiner des refresh et autre dans une fonction fait pour.
- Dialogue About + Licences logiciels + icônes
- Afficher le titre de la série quand le nom de la saison est vide ?
- Liste des séries et saisons supprimées:
  - Restaurer / supprimer définitivement

- Icones sur chaque modale (ui + manuellement crées)