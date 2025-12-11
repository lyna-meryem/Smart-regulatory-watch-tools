# agents/document_loader.py

import os


class DocumentLoader:
    """
    Charge un document texte (.txt) et retourne son contenu sous forme de string.
    (Version simple pour tes tests de traduction.)
    """

    def load(self, path: str) -> str:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Fichier introuvable : {path}")

        if not path.endswith(".txt"):
            raise ValueError(f"Format non supporté pour l'instant (seulement .txt) : {path}")

        with open(path, "r", encoding="utf-8") as f:
            return f.read()
