# Génération de la classe de la base de données
python -m pwiz --preserve-order --engine sqlite "database2.sqlite3" > database.py

# Remplacement de l'emplacement de la BDD dans la classe générée
#sed -i "s/database = SqliteDatabase('database2.sqlite3')/database = DATABASE/g" database.py