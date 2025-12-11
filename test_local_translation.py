from agents.translate import SimpleGoogleTranslator

if __name__ == "__main__":
    agent = SimpleGoogleTranslator()

    text = "Les institutions financières doivent protéger les données des clients."

    translations = agent.translate_text(text)

    for t in translations:
        print(f"\n--- {t['target_lang']} ---")
        print(t["translated_text"])

