
import sqlite3
from collections import Counter
import matplotlib.pyplot as plt

# Texte du livre intégré (chapitre I)
text = """
Title: A Tale of Two Cities
Author: Charles Dickens

CHAPTER I. THE PERIOD

It was the best of times, it was the worst of times, it was the age of wisdom,
it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity,
it was the season of Light, it was the season of Darkness, it was the spring of hope,
it was the winter of despair, we had everything before us, we had nothing before us,
we were all going direct to Heaven, we were all going direct the other way—
in short, the period was so far like the present period...

There were a king with a large jaw and a queen with a plain face, on the throne of England;
there were a king with a large jaw and a queen with a fair face, on the throne of France.
In both countries it was clearer than crystal to the lords of the State preserves...

It was the year of Our Lord one thousand seven hundred and seventy-five.
Spiritual revelations were conceded to England at that favoured period, as at this.
Mrs. Southcott had recently attained her five-and-twentieth blessed birthday...
"""

# --- Extraction du chapitre ---
title = "A Tale of Two Cities"
author = "Charles Dickens"
chapter = text.split("CHAPTER I.")[1].strip()

# --- Analyse des paragraphes ---
paragraphs = [p.strip() for p in chapter.split("\n") if len(p.strip()) > 20]
word_counts = [len(p.split()) for p in paragraphs]
rounded_counts = [round(wc, -1) for wc in word_counts]
distribution = dict(sorted(Counter(rounded_counts).items()))

# --- Création base SQLite ---
conn = sqlite3.connect("elisa_paragraphs.db")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS stats")
cur.execute("CREATE TABLE stats (id INTEGER PRIMARY KEY, paragraph TEXT, words INTEGER, rounded INTEGER)")

for p, wc, rc in zip(paragraphs, word_counts, rounded_counts):
    cur.execute("INSERT INTO stats (paragraph, words, rounded) VALUES (?, ?, ?)", (p, wc, rc))

conn.commit()
conn.close()

# --- Création du graphique ---
plt.figure(figsize=(10, 5))
plt.bar(distribution.keys(), distribution.values(), color="cornflowerblue")
plt.title("Distribution des longueurs des paragraphes (Chapitre I)")
plt.xlabel("Nombre de mots (arrondi à la dizaine)")
plt.ylabel("Nombre de paragraphes")
plt.tight_layout()
plt.savefig("elisa_distribution_graphique.png")
plt.close()

print("✅ Projet terminé : base de données et graphique générés.")
