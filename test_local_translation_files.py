from agents.document_loader import DocumentLoader
from agents.translate import SimpleGoogleTranslator

if __name__ == "__main__":
    loader = DocumentLoader()
    translator = SimpleGoogleTranslator()

    v1_text = loader.load("v1_doc1.txt")
    v2_text = loader.load("v2_doc2.txt")

    print("=== Traduction V1 ===")
    translations_v1 = translator.translate_text(v1_text)
    for t in translations_v1:
        print(f"\n--- {t['target_lang']} ---")
        print(t["translated_text"])

    print("\n=== Traduction V2 ===")
    translations_v2 = translator.translate_text(v2_text)
    for t in translations_v2:
        print(f"\n--- {t['target_lang']} ---")
        print(t["translated_text"])
