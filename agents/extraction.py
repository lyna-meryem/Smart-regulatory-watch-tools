import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.bcl.lu/en/Regulatory-reporting/Etablissements_credit/AnaCredit/Instructions/index.html"
OUTPUT_DIR = "downloaded_files"

# 1) Création du dossier local si nécessaire
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2) Récupération du HTML de la page
response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")

# 3) Filtrer tous les liens PDF et ZIP
for link in soup.find_all("a"):
    href = link.get("href")
    if href and (href.lower().endswith(".pdf") or href.lower().endswith(".zip")):
        file_url = urljoin(BASE_URL, href)

        # 4) Préparer chemin local du fichier
        file_name = os.path.basename(file_url)
        local_path = os.path.join(OUTPUT_DIR, file_name)

        # 5) Télécharger chaque fichier
        print(f"Downloading {file_name} ...")
        file_resp = requests.get(file_url)
        with open(local_path, "wb") as f:
            f.write(file_resp.content)

        print(f"✔ Saved {file_name} in {OUTPUT_DIR}")
