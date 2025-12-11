from googletrans import Translator


class SimpleGoogleTranslator:
    """
    Traducteur simple basé sur googletrans.
    Pas de clé API, pas de modèle local.
    """

    TARGET_LANGS = ["en", "es", "de", "ro", "fr"]

    def __init__(self):
        self.translator = Translator()

    def translate_text(self, text: str):
        if not text or not text.strip():
            return []

        results = []

        for lang in self.TARGET_LANGS:
            translated = self.translator.translate(text, dest=lang).text
            results.append({
                "target_lang": lang,
                "translated_text": translated
            })

        return results
