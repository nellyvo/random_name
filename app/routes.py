from flask import Blueprint, render_template, request, session
import random

from .data_loader import load_names, load_surnames
from .generator import generate_name, generate_full_name, build_markov_model

main = Blueprint("main", __name__)

surnames = load_surnames()

@main.route("/")
def index():
    genre = request.args.get("genre", "mixte")
    count = int(request.args.get("nombre", 10))
    prenoms = session.get("prenoms", ["—"] * count)
    noms = session.get("noms", ["—"] * count)
    names = [f"{p} {n}" for p, n in zip(prenoms, noms)]
    return render_template("index.html", names=names, genre=genre, count=count)

@main.route("/generer_prenoms")
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

@main.route("/generer_noms")
def generer_noms():
    count = int(request.args.get("nombre", 10))
    noms = [random.choice(surnames) for _ in range(count)]
    prenoms = session.get("prenoms", ["—"] * count)
    genre = session.get("genre", "mixte")
    session["prenoms"] = prenoms
    session["noms"] = noms
    names = [f"{p} {n}" for p, n in zip(prenoms, noms)]
    return render_template("index.html", names=names, genre=genre, count=count)

@main.route("/generer_tout")
def generer_tout():
    genre = session.get("genre", "mixte")
    count = int(request.args.get("nombre", 10))
    raw_corpus = load_names(genre)
    model = build_markov_model(raw_corpus)
    prenoms = [generate_name(model) for _ in range(count)]
    noms = [random.choice(surnames) for _ in range(count)]
    session["prenoms"] = prenoms
    session["noms"] = noms
    names = [f"{p} {n}" for p, n in zip(prenoms, noms)]
    return render_template("index.html", names=names, genre=genre, count=count)