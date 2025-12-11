import os
from analysis_agent import AnalysisComparisonAgent

def main():
    base_path = os.path.dirname(__file__)

    # --- Demander à l'utilisateur les chemins des fichiers ---
    old_file = input(f"Chemin du premier fichier (v1) [{base_path}/v1_doc1.txt] : ") or os.path.join(base_path, "v1_doc1.txt")
    new_file = input(f"Chemin du deuxième fichier (v2) [{base_path}/v2_doc2.txt] : ") or os.path.join(base_path, "v2_doc2.txt")

    # --- Demander les mots-clés ---
    keywords_input = input("Mots-clés à analyser (séparés par des virgules) : ").strip()
    if not keywords_input:
        print("Erreur : aucun mot-clé fourni.")
        return
    keywords = [kw.strip() for kw in keywords_input.split(",") if kw.strip()]

    # --- Demander le nom de la banque ---
    bank = input("Nom de la banque [BCL] : ").strip() or "BCL"

    # --- Initialisation de l'agent ---
    agent = AnalysisComparisonAgent()

    # --- Analyse et résumé ---
    result = agent.analyze_change(old_file, new_file, keywords, bank=bank)

    # --- Affichage du résultat final ---
    print("\n--- Résultat de l'analyse ---")
    print(f"Fichier : {result['filename']}")
    print(f"Banque : {result['bank']}")
    print(f"Mots-clés : {', '.join(result['keywords'])}")
    print(f"Timestamp : {result['timestamp']}")
    print("\n--- Résumé global ---")
    print(result['summary'])

if __name__ == "__main__":
    main()
