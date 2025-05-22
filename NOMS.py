import requests
from bs4 import BeautifulSoup

url = "https://probablyhelpful.com/most_common_surnames.htm"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.content, "html.parser")

surnames = []

for row in soup.select("table tr"):
    cells = row.find_all("td")
    if len(cells) >= 1:
        nom = cells[0].text.strip()
        if nom.isalpha():  # évite les cellules vides ou avec des chiffres
            surnames.append(nom)

# Sauvegarde dans un fichier texte
with open("noms_famille.txt", "w") as f:
    for nom in surnames:
        f.write(nom + "\n")

print(f"{len(surnames)} noms de famille trouvés.")
print(surnames[:20])