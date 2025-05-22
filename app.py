from flask import Flask, render_template, request, session
import random
import re

app = Flask(__name__)
app.secret_key = "randomsecretkey"

# === 1. Charger les prénoms depuis les fichiers ===
def load_names(genre="mixte"):
    garcons, filles = [], []
    with open("prenoms_garcons.txt") as fg:
        garcons = [line.strip() for line in fg if line.strip()]
    with open("prenoms_filles.txt") as ff:
        filles = [line.strip() for line in ff if line.strip()]
    if genre == "garcon":
        return garcons
    elif genre == "fille":
        return filles
    return garcons + filles

def load_surnames():
    with open("noms_famille.txt") as f:
        return [line.strip() for line in f if line.strip()]

surnames = load_surnames()

# === 2. Découpe syllabique améliorée ===
def split_syllables(name):
    pattern = r'[^aeiouy]*[aeiouy]+(?:[^aeiouy]*)'
    return re.findall(pattern, name.lower())

# === 3. Construction du modèle de Markov (avec start/end) ===
def build_markov_model(corpus):
    model = {'__start__': [], '__end__': []}
    for name in corpus:
        syllables = split_syllables(name)
        if not syllables:
            continue
        model['__start__'].append(syllables[0])
        model.setdefault(syllables[-1], []).append('__end__')
        for i in range(len(syllables) - 1):
            model.setdefault(syllables[i], []).append(syllables[i + 1])
    return model

# === 4. Génération avec Markov et limite de tentatives ===
def generate_from_model(model, max_syll=4):
    for _ in range(20):
        sylls = []
        current = random.choice(model['__start__'])
        sylls.append(current)
        while len(sylls) < max_syll:
            next_choices = model.get(current, [])
            if not next_choices:
                break
            next_syll = random.choice(next_choices)
            if next_syll == '__end__':
                break
            sylls.append(next_syll)
            current = next_syll
        if 2 <= len(sylls) <= max_syll:
            return ''.join(sylls).capitalize()
    return "Nameless"

# === 5. Mutation phonétique basée sur des règles ===
PHONETIC_MAP = {
    'k': ['c', 'ch', 'q'],
    'e': ['ae', 'i', 'a'],
    'j': ['g', 'zh', 'z'],
    's': ['c', 'z', 'x'],
    'f': ['ph', 'v'],
    'o': ['u', 'ou', 'au'],
    't': ['d', 'th'],
    'y': ['i', 'ie']
}

def phonetic_mutate(name):
    name = name.lower()
    if len(name) < 3:
        return name.capitalize()
    i = random.randint(1, len(name)-2)
    c = name[i]
    if c in PHONETIC_MAP:
        alt = random.choice(PHONETIC_MAP[c])
        name = name[:i] + alt + name[i+1:]
    return name.capitalize()

# === 5b. Analyse de la structure syllabique ===
def syllable_structure(name):
    vowels = "aeiouy"
    structure = ""
    for char in name.lower():
        if char in vowels:
            structure += "V"
        elif char.isalpha():
            structure += "C"
    return structure

# === 6. Validation plus équilibrée ===
def is_valid(name):
    name = name.lower()
    return (
        re.search(r'[aeiouy]', name) and
        not re.search(r'[bcdfghjklmnpqrstvwxyz]{4,}', name) and
        4 <= len(name) <= 12
    )

# === 7. Génération finale avec structure syllabique réaliste ===
def generate_name(model):
    target_structures = ["CVCV", "VCV", "CVVC", "CVCC"]
    for _ in range(50):
        name = generate_from_model(model)
        name = phonetic_mutate(name)
        struct = syllable_structure(name)
        if is_valid(name) and any(struct.startswith(ts) for ts in target_structures):
            return name
    return "Nameless"

def generate_full_name(model):
    prenom = generate_name(model)
    nom = random.choice(surnames)
    return f"{prenom} {nom}"

# === 8. Interface Web ===
@app.route("/")
def index():
    genre = request.args.get("genre", "mixte")
    count = int(request.args.get("nombre", 10))
    prenoms = session.get("prenoms", ["—"] * count)
    noms = session.get("noms", ["—"] * count)
    names = [f"{p} {n}" for p, n in zip(prenoms, noms)]
    return render_template("index.html", names=names, genre=genre, count=count)

@app.route("/generer_prenoms")
def generer_prenoms():
    genre = request.args.get("genre", "mixte")
    count = int(request.args.get("nombre", 10))
    raw_corpus = load_names(genre)
    model = build_markov_model(raw_corpus)
    prenoms = [generate_name(model) for _ in range(count)]
    noms = session.get("noms", ["—"] * count)
    session["prenoms"] = prenoms
    session["noms"] = noms
    session["genre"] = genre
    names = [f"{p} {n}" for p, n in zip(prenoms, noms)]
    return render_template("index.html", names=names, genre=genre, count=count)

@app.route("/generer_noms")
def generer_noms():
    count = int(request.args.get("nombre", 10))
    noms = [random.choice(surnames) for _ in range(count)]
    prenoms = session.get("prenoms", ["—"] * count)
    genre = session.get("genre", "mixte")
    session["prenoms"] = prenoms
    session["noms"] = noms
    names = [f"{p} {n}" for p, n in zip(prenoms, noms)]
    return render_template("index.html", names=names, genre=genre, count=count)

if __name__ == "__main__":
    app.run(debug=True, port=5000)