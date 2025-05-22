def load_names(genre="mixte"):
    garcons, filles = [], []
    with open("data/prenoms_garcons.txt", encoding="utf-8") as fg:
        garcons = [line.strip() for line in fg if line.strip()]
    with open("data/prenoms_filles.txt", encoding="utf-8") as ff:
        filles = [line.strip() for line in ff if line.strip()]
    if genre == "garcon":
        return garcons
    elif genre == "fille":
        return filles
    return garcons + filles

def load_surnames():
    with open("data/noms_famille.txt", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]