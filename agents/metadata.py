import os
import json
from pathlib import Path
from datetime import datetime
from langdetect import detect

def extract_text(file_path):
    """Extraction simple pour txt/md."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except:
        return ""

def detect_language(text):
    """Détecte la langue d'un texte."""
    if not text.strip():
        return "unknown"
    try:
        return detect(text)
    except:
        return "unknown"

def generate_metadata(directory_path="database_docs", output_file="metadata.json"):
    directory = Path(directory_path)

    if not directory.exists():
        raise Exception(f"Le dossier {directory_path} n'existe pas.")

    metadata = {
        "directory": directory_path,
        "generated_at": datetime.now().isoformat(),
        "total_files": 0,
        "total_size_bytes": 0,
        "files_by_type": {},
        "files": []
    }

    for file_path in directory.glob("**/*"):
        if file_path.is_file():
            file_stats = file_path.stat()

            # Extraction du texte
            text = ""
            if file_path.suffix.lower() in [".txt", ".md"]:
                text = extract_text(file_path)

            # Détection langue
            language = detect_language(text)

            file_info = {
                "name": file_path.name,
                "path": str(file_path),
                "extension": file_path.suffix.lower(),
                "size_bytes": file_stats.st_size,
                "last_modified": datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
                "language": language
            }

            metadata["files"].append(file_info)
            metadata["total_files"] += 1
            metadata["total_size_bytes"] += file_stats.st_size

            ext = file_path.suffix.lower()
            metadata["files_by_type"].setdefault(ext, 0)
            metadata["files_by_type"][ext] += 1

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    print(f"✅ Fichier metadata généré → {output_file}")

if __name__ == "__main__":
    generate_metadata()
