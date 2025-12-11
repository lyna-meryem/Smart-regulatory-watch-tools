import hashlib
import os
import csv
from datetime import datetime

# Chemin du répertoire contenant les fichiers
directory_path = './database_docs/'

# Fonction pour calculer le hash SHA-256 d'un fichier
def hash_file(file_path):
    """Retourne le hash SHA-256 d'un fichier"""
    sha256_hash = hashlib.sha256()

    try:
        # Ouvre le fichier en mode binaire
        with open(file_path, "rb") as f:
            # Lire par morceaux de 4k
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        # Retourne le hash hexadécimal
        return sha256_hash.hexdigest()

    except FileNotFoundError:
        print(f"⚠️ Le fichier {file_path} est introuvable.")
        return None

# Création du chemin pour le fichier CSV
csv_file_path = './metadonnees.csv'

# Titre des colonnes du CSV
header = ['File Name', 'SHA-256 Hash']

# Ouverture du fichier CSV en mode écriture
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(header)  # Écrire l'en-tête

    # Parcours de tous les fichiers dans le répertoire
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)

        # Vérification que c'est bien un fichier (pas un répertoire)
        if os.path.isfile(file_path):
            # Calculer le hash SHA-256 du fichier
            file_hash = hash_file(file_path)

            if file_hash:
                # Écrire le nom du fichier et son hash dans le CSV
                writer.writerow([file_name, file_hash])

print(f"✔️ Tous les fichiers ont été traités et les hashes sont enregistrés dans {csv_file_path}.")
