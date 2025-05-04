from flask import Flask, render_template_string
import random
import re

app = Flask(__name__)

# === 1. Chargement du corpus ===
raw_corpus = [
    "Liam", "Noah", "Olivia", "Emma", "Jackson", "Owen", "Isabella", "Ava",
    "Samuel", "Evelyn", "Alexandar", "Alice", "Margaret", "Sophia", "Hazel",
    "Charles", "George", "Anne", "Victoria", "James", "Benjamin", "Scarlett",
    "Amelia", "Charlotte", "Emily", "Luna", "Harriet", "Florence"
]

# === 2. Découpe simplifiée en syllabes ===
def split_syllables(name):
    return re.findall(r'[^aeiouy]*[aeiouy]+(?:[^aeiouy]*)', name.lower())

# === 3. Construction du modèle Markov sur syllabes ===
def build_markov_model(corpus):
    model = {}
    for name in corpus:
        syllables = split_syllables(name)
        for i in range(len(syllables) - 1):
            model.setdefault(syllables[i], []).append(syllables[i + 1])
    return model

# === 4. Génération d’un nom à partir du modèle ===
def generate_from_model(model, min_len=2, max_len=4):
    name = [random.choice(list(model.keys()))]
    while len(name) < max_len:
        last = name[-1]
        if last not in model:
            break
        name.append(random.choice(model[last]))
    if len(name) < min_len:
        return generate_from_model(model, min_len, max_len)
    return ''.join(name).capitalize()

# === 5. Mutation naturelle ===
def mutate(name):
    if len(name) < 4:
        return name
    i = random.randint(1, len(name)-2)
    if name[i] in "aeiouy":
        new_char = random.choice("aeiouy".replace(name[i], ""))
    else:
        new_char = random.choice("bcdfghjklmnpqrstvwxyz")
    return name[:i] + new_char + name[i+1:]

# === 6. Validation ===
def is_valid(name):
    name = name.lower()
    if not re.search(r'[aeiouy]', name): return False
    if re.search(r'[bcdfghjklmnpqrstvwxyz]{4,}', name): return False
    if len(name) < 4 or len(name) > 12: return False
    return True

# === 7. Génération finale ===
def generate_name(model):
    for _ in range(30):
        base = generate_from_model(model)
        final = mutate(base)
        if is_valid(final):
            return final.capitalize()
    return "Nameless"

# === 8. Interface Web ===
@app.route("/")
def index():
    model = build_markov_model(raw_corpus)
    names = [generate_name(model) for _ in range(10)]
    html = """
    <html>
    <head><title>Nom Generator</title></head>
    <body style="font-family:sans-serif; text-align:center; padding-top:50px;">
        <h1>Noms générés</h1>
        <ul style="list-style:none;">
            {% for name in names %}
                <li style="font-size:1.5em; margin:10px;">{{ name }}</li>
            {% endfor %}
        </ul>
        <a href="/" style="font-size:1.2em;">↻ Recharger</a>
    </body>
    </html>
    """
    return render_template_string(html, names=names)

if __name__ == "__main__":
    app.run(debug=True, port=5002)