import random
from .syllables import split_syllables, phonetic_mutate, syllable_structure, is_valid

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