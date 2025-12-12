from openai import OpenAI
import os


class SimpleGoogleTranslator:
    """
    Traducteur basé sur l'API OpenAI.
    Traduit un texte dans plusieurs langues et renvoie un dict {code_langue: texte_traduit}.
    """

    TARGET_LANGS = {
        "en": "English",
        "fr": "French",
        "es": "Spanish",
        "de": "German",
        "ro": "Romanian",
    }

    def __init__(self):
        # La clé doit être dans la variable d'environnement OPENAI_API_KEY
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("❌ Variable d'environnement OPENAI_API_KEY manquante.")
        self.client = OpenAI(api_key=api_key)

    def translate_text(self, text: str) -> dict:
        """
        Traduit le texte dans toutes les langues définies dans TARGET_LANGS.
        Retourne un dict : { 'en': '...', 'fr': '...', ... }
        """
        if not text or not text.strip():
            raise ValueError("Le texte à traduire est vide.")

        results = {}

        for lang_code, lang_name in self.TARGET_LANGS.items():
            print(f"➡️ Traduction vers {lang_name} ({lang_code})...")

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"You are a professional translator. "
                            f"Translate the user text into {lang_name}. "
                            f"Keep the structure, numbering and technical terminology."
                        ),
                    },
                    {
                        "role": "user",
                        "content": text,
                    },
                ],
            )

            translated_text = response.choices[0].message.content
            results[lang_code] = translated_text

        return results
