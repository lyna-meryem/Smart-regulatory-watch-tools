import pandas as pd
import difflib
import re
from openai import OpenAI

class RegChangeAnalysisAgent:
    def __init__(self, keyword_file: str, api_key: str):
        self.keyword_file = keyword_file
        self.keywords = self.load_keywords()
        self.client = OpenAI(api_key=api_key)

    # 1. Charger les mots-clés
    def load_keywords(self):
        df = pd.read_excel(self.keyword_file)
        df["keyword"] = df["keyword"].str.lower()
        return df

    # 2. Extraire les sections contenant les mots-clés
    def extract_keyword_sections(self, text: str):
        sections = []
        paragraphs = text.split("\n")

        for paragraph in paragraphs:
            p = paragraph.lower()
            for _, row in self.keywords.iterrows():
                if row["keyword"] in p:
                    sections.append({
                        "keyword": row["keyword"],
                        "category": row["category"],
                        "paragraph": paragraph.strip(),
                    })

        return sections

    # 3. Comparer deux versions d’une même section
    def compare_sections(self, old_text: str, new_text: str):
        diff = difflib.unified_diff(
            old_text.splitlines(),
            new_text.splitlines(),
            lineterm="",
            n=2
        )
        return "\n".join(list(diff))

    # 4. Résumer automatiquement le changement via IA
    def summarize_change(self, keyword, diff_text):
        if not diff_text.strip():
            return f"Aucun changement détecté pour le mot-clé : {keyword}"

        prompt = f"""
Tu es un expert compliance/finance.
Voici un extrait de réglementation qui a changé concernant le mot-clé "{keyword}".

Diff :
{diff_text}

Résume clairement :
1. Ce qui a changé
2. Le sens du changement (plus strict ? plus flexible ?)
3. Impact potentiel sur une banque
"""

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return completion.choices[0].message["content"]

    # 5. Analyse complète : toutes les versions
    def analyze_versions(self, old_doc: str, new_doc: str):
        old_sections = self.extract_keyword_sections(old_doc)
        new_sections = self.extract_keyword_sections(new_doc)

        results = []

        for new in new_sections:
            keyword = new["keyword"]

            # trouver section ancienne correspondante
            old = next((o for o in old_sections if o["keyword"] == keyword), None)

            diff = None
            summary = None

            if old:
                diff = self.compare_sections(old["paragraph"], new["paragraph"])
                summary = self.summarize_change(keyword, diff)

            else:
                summary = f"La section contenant '{keyword}' est nouvelle dans cette version."

            results.append({
                "keyword": keyword,
                "category": new["category"],
                "old": old["paragraph"] if old else None,
                "new": new["paragraph"],
                "diff": diff,
                "summary": summary,
            })

        return results
