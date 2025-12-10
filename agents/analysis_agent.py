from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from agent.document_loader import DocumentLoader


class AnalysisComparisonAgent:

    def __init__(self):
        # Chargeur de documents multi-format
        self.loader = DocumentLoader()

        # Embedding gratuit pour comparaison IA
        self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # Résumeur IA gratuit
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            tokenizer="facebook/bart-large-cnn",
        )

    # --- extrait le contexte d’un mot-clé ---
    def extract_keyword_context(self, text, keyword, window=80):
        text_lower = text.lower()
        keyword_lower = keyword.lower()

        if keyword_lower not in text_lower:
            return None

        pos = text_lower.index(keyword_lower)

        start = max(0, pos - window)
        end = min(len(text), pos + len(keyword) + window)

        return text[start:end]

    # --- IA : comparaison sémantique ---
    def compare_texts(self, text_old, text_new):
        emb_old = self.embedder.encode(text_old or "")
        emb_new = self.embedder.encode(text_new or "")
        score = float(util.cos_sim(emb_old, emb_new))
        return score

    # --- IA : résumé du changement ---
    def summarize_changes(self, old_ctx, new_ctx):
        if not old_ctx:
            old_ctx = "No previous regulation."

        if not new_ctx:
            new_ctx = "No update found."

        text = (
            f"Old version:\n{old_ctx}\n\n"
            f"New version:\n{new_ctx}\n\n"
            "Summarize the change."
        )

        summary = self.summarizer(
            text,
            max_length=150,
            min_length=50,
            do_sample=False
        )[0]["summary_text"]

        return summary

    # --- Pipeline complet ---
    def analyze_change(self, old_path, new_path, keyword):
        # 1. Load documents
        old_text = self.loader.load(old_path)
        new_text = self.loader.load(new_path)

        # 2. Extract keyword context
        old_ctx = self.extract_keyword_context(old_text, keyword)
        new_ctx = self.extract_keyword_context(new_text, keyword)

        if old_ctx is None and new_ctx is None:
            return {
                "keyword_found": False,
                "message": "Mot clé introuvable dans les deux documents."
            }

        # 3. IA Comparison
        similarity = self.compare_texts(old_ctx or "", new_ctx or "")

        # 4. AI Summary
        summary = self.summarize_changes(old_ctx, new_ctx)

        # 5. Build response
        return {
            "keyword_found": True,
            "old_context": old_ctx,
            "new_context": new_ctx,
            "similarity_score": similarity,
            "summary": summary
        }
