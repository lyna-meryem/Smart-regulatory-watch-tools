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
