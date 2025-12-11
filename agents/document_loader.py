import pdfplumber
import pandas as pd


class DocumentLoader:

    def load(self, path):
        """
        Charge un document (PDF, TXT, XLSX, CSV) et retourne un texte brut.
        """
        if path.endswith(".pdf"):
            return self._load_pdf(path)

        elif path.endswith(".txt"):
            return self._load_txt(path)

        elif path.endswith((".xlsx", ".xls", ".csv")):
            return self._load_excel(path)

        else:
            raise ValueError(f"Format non supporté : {path}")

    # --- EXTRACT PDF ---
    def _load_pdf(self, path):
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text

    # --- EXTRACT TXT ---
    def _load_txt(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    # --- EXTRACT EXCEL OR CSV ---
    def _load_excel(self, path):
        if path.endswith(".csv"):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)

        rows = []
        for _, row in df.iterrows():
            line = " - ".join([f"{col}: {row[col]}" for col in df.columns])
            rows.append(line)

        return "\n".join(rows)
