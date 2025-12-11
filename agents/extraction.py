import logging
import os

# Configuration du log pour l'agent d'extraction
def setup_logger(agent_name):
    """Configure le logger pour un agent particulier"""
    log_dir = './logs/'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f'{agent_name}.log')
    
    # Création du logger
    logger = logging.getLogger(agent_name)
    logger.setLevel(logging.DEBUG)
    
    # Création du handler pour écrire les logs dans un fichier
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # Création du format du log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # Ajout du handler au logger
    logger.addHandler(file_handler)
    return logger

# Agent 1 : Extraction des fichiers
def agent_extraction(logger):
    try:
        logger.info("Début de l'extraction des fichiers.")
        
        # Logique d'extraction (exemple)
        # Par exemple, vous pouvez ajouter un traitement pour extraire des fichiers
        # from some_library import download_files
        # download_files(...)
        
        logger.info("Extraction terminée avec succès.")
    except Exception as e:
        logger.error(f"Erreur dans l'extraction des fichiers: {e}")

# Fonction principale pour l'exécution de l'agent d'extraction
def main():
    # Création du logger pour l'agent d'extraction
    extraction_logger = setup_logger('extraction')

    # Exécution de l'agent d'extraction avec logging
    agent_extraction(extraction_logger)

# Lancer l'exécution principale
if __name__ == "__main__":
    main()
=======
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import zipfile
from io import BytesIO

BASE_URL = "https://www.bcl.lu/en/Regulatory-reporting/Etablissements_credit/AnaCredit/Instructions/index.html"
OUTPUT_DIR = "database_docs"

# 1) Créer le dossier output
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2) Télécharger la page HTML
response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")

# 3) Parcourir tous les liens PDF + ZIP
for link in soup.find_all("a"):
    href = link.get("href")

    if not href:
        continue

    file_url = urljoin(BASE_URL, href)

    # 📌 PDF direct
    if href.lower().endswith(".pdf"):
        file_name = os.path.basename(href)
        file_path = os.path.join(OUTPUT_DIR, file_name)

        print(f"📥 Téléchargement PDF : {file_name}")
        pdf_content = requests.get(file_url).content

        with open(file_path, "wb") as f:
            f.write(pdf_content)

    # 📌 ZIP → extraction à plat (pas de sous-dossiers)
    elif href.lower().endswith(".zip"):
        zip_name = os.path.basename(href)
        print(f"📦 Téléchargement ZIP : {zip_name}")

        zip_content = requests.get(file_url).content

        # Lire le ZIP en mémoire
        with zipfile.ZipFile(BytesIO(zip_content)) as zipped:
            for file_inside in zipped.namelist():

                # Ignorer les dossiers internes
                if file_inside.endswith("/"):
                    continue

                # Extraire seulement le nom du fichier, pas le chemin
                clean_name = os.path.basename(file_inside)

                output_path = os.path.join(OUTPUT_DIR, clean_name)

                print(f"➡️ Extraction : {clean_name}")

                # EXTRACTION -- bien indentée
                with zipped.open(file_inside) as source, open(output_path, "wb") as target:
                    target.write(source.read())

print("\n✅ Terminé ! Tous les fichiers sont dans :", OUTPUT_DIR)

