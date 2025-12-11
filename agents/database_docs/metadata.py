import os
import csv
from datetime import datetime

# Utiliser le chemin absolu
directory = r'C:\Users\Ahmed Khalil KADRI\Documents\Smart-regulatory-watch-tools\agents\database_docs'

# Liste des fichiers dans le répertoire
files = os.listdir(directory)

# Créer une liste pour stocker les métadonnées des fichiers
metadata = []

# Parcourir les fichiers et récupérer les informations
for file in files:
    file_path = os.path.join(directory, file)
    
    if os.path.isfile(file_path):
        # Obtenir les informations du fichier
        file_size = os.path.getsize(file_path)  # Taille du fichier en octets
        creation_time = os.path.getctime(file_path)  # Temps de création
        creation_date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')  # Format de la date
        
        # Ajouter les métadonnées à la liste
        metadata.append({
            'Filename': file,
            'Size (bytes)': file_size,
            'Creation Date': creation_date
        })

# Chemin du fichier CSV de sortie
csv_file_path = os.path.join(directory, 'metadata.csv')

# Écrire les métadonnées dans un fichier CSV
with open(csv_file_path, mode='w', newline='') as csvfile:
    fieldnames = ['Filename', 'Size (bytes)', 'Creation Date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Écrire l'en-tête
    writer.writeheader()
    
    # Écrire les données des fichiers
    writer.writerows(metadata)

print(f'Métadonnées sauvegardées dans {csv_file_path}')
