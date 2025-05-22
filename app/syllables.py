import re
import random

def split_syllables(name):
    pattern = r'[^aeiouy]*[aeiouy]+(?:[^aeiouy]*)'
    return re.findall(pattern, name.lower())

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

def syllable_structure(name):
    vowels = "aeiouy"
    structure = ""
    for char in name.lower():
        if char in vowels:
            structure += "V"
        elif char.isalpha():
            structure += "C"
    return structure

def is_valid(name):
    name = name.lower()
    return (
        re.search(r'[aeiouy]', name) and
        not re.search(r'[bcdfghjklmnpqrstvwxyz]{4,}', name) and
        4 <= len(name) <= 12
    )