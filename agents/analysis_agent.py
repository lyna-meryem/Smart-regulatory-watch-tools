import re
from transformers import pipeline
from langdetect import detect
from datetime import datetime
import os

class AnalysisComparisonAgent:
    def __init__(self, summarizer_model="facebook/bart-large-cnn"):
        self.summarizer = pipeline("summarization", model=summarizer_model)

    def extract_text(self, file_path):
        ext = file_path.lower().split(".")[-1]
        if ext == "txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        elif ext == "pdf":
            import pdfplumber
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            return text
        elif ext in ("xml", "csv", "xlsx"):
            import pandas as pd
            if ext == "csv":
                df = pd.read_csv(file_path)
            elif ext == "xlsx":
                df = pd.read_excel(file_path)
            else:  # xml
                import xml.etree.ElementTree as ET
                tree = ET.parse(file_path)
                root = tree.getroot()
                text = "\n".join([elem.text for elem in root.iter() if elem.text])
                return text
            rows = [" - ".join([f"{col}: {row[col]}" for col in df.columns]) for _, row in df.iterrows()]
            return "\n".join(rows)
        else:
            raise ValueError(f"Format non supporté : {file_path}")

    def keyword_context(self, text, keyword, window=200):
        pattern = re.compile(keyword, re.IGNORECASE)
        matches = []
        for m in pattern.finditer(text):
            start = max(0, m.start() - window)
            end = min(len(text), m.end() + window)
            matches.append(text[start:end])
        return matches

    def compare_versions(self, old_text, new_text, keyword):
        old_ctx = " ".join(self.keyword_context(old_text, keyword))
        new_ctx = " ".join(self.keyword_context(new_text, keyword))
        keyword_found = bool(old_ctx.strip() or new_ctx.strip())
        return old_ctx, new_ctx, keyword_found

    def chunk_text(self, text, max_words=500):
        words = text.split()
        return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

    def summarize_change(self, text):
        if not text.strip():
            return "Pas assez de texte pour résumé."
        if len(text.split()) > 500:
            text = " ".join(text.split()[:500])
        summary = self.summarizer(text, max_length=150, min_length=40, do_sample=False)
        return summary[0]['summary_text']

    def summarize_large_text(self, text):
        chunks = self.chunk_text(text)
        summaries = [self.summarize_change(chunk) for chunk in chunks]
        return " ".join(summaries)

    def analyze_change(self, old_path, new_path, keywords, bank="Unknown"):
        if isinstance(keywords, str):
            keywords = [keywords]

        old_text = self.extract_text(old_path)
        new_text = self.extract_text(new_path)

        summaries = []
        for kw in keywords:
            _, new_ctx, found = self.compare_versions(old_text, new_text, kw)
            summary = self.summarize_large_text(new_ctx) if found else f"Mot-clé introuvable : {kw}"
            summaries.append(summary)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        analysis_result = {
            "filename": os.path.basename(new_path),
            "bank": bank,
            "keywords": keywords,
            "summary": " ".join(summaries),
            "timestamp": timestamp
        }
        return analysis_result
