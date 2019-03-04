# Génération du fichier .py
python -m pwiz -e sqlite database.sqlite3 > database.py

# Remplacement de l'emplacement de la bdd
# sed  'database.sqlite3'
