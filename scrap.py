import requests
from bs4 import BeautifulSoup

url = "https://www.ssa.gov/oact/babynames/decades/century.html"
headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.content, "html.parser")

table = soup.find("table", {"class": "t-stripe"})
rows = table.find_all("tr")[1:]

prenoms_garcons = []
prenoms_filles = []

for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 5:
        prenoms_garcons.append(cols[1].text.strip())
        prenoms_filles.append(cols[3].text.strip())

# Sauvegarde dans des fichiers texte
with open("prenoms_garcons.txt", "w") as f:
    for prenom in prenoms_garcons:
        f.write(prenom + "\n")

with open("prenoms_filles.txt", "w") as f:
    for prenom in prenoms_filles:
        f.write(prenom + "\n")

print(f"{len(prenoms_garcons)} prénoms garçons et {len(prenoms_filles)} prénoms filles écrits dans les fichiers.")