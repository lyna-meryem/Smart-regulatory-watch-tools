import os

# Chemin du repository Git, au même niveau que 'agents'
repo_path = os.path.dirname(os.path.abspath(__file__))  # Répertoire actuel du script
download_folder = os.path.join(repo_path, "downloaded_files")

# Vérifier si le dossier 'downloaded_files' existe déjà
if not os.path.exists(download_folder):
    os.makedirs(download_folder)
    print(f"Dossier {download_folder} créé avec succès.")
else:
    print(f"Le dossier {download_folder} existe déjà.")


import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('scraped_files.db')
cursor = conn.cursor()

# Créer la table si elle n'existe pas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT NOT NULL,
        file_type TEXT NOT NULL,
        source_url TEXT NOT NULL,
        date_downloaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')