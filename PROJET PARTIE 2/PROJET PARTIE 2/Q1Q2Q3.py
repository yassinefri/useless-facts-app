import sqlite3
import matplotlib.pyplot as plt
from collections import Counter

# --- Connexion à la base de données ---
conn = sqlite3.connect("elisa_paragraphs.db")
cur = conn.cursor()

# --- Récupérer les tailles arrondies des paragraphes ---
cur.execute("SELECT rounded FROM stats")
data = cur.fetchall()
conn.close()

# --- Comptage de la distribution ---
rounded_counts = [row[0] for row in data]
distribution = dict(sorted(Counter(rounded_counts).items()))

# --- Génération du graphique ---
plt.figure(figsize=(10, 5))
plt.bar(distribution.keys(), distribution.values(), color="cornflowerblue")
plt.title("Distribution des longueurs des paragraphes (Chapitre I)")
plt.xlabel("Nombre de mots (arrondi à la dizaine)")
plt.ylabel("Nombre de paragraphes")
plt.tight_layout()
plt.savefig("elisa_distribution_graphique.png")
plt.close()

print("✅ Graphique enregistré sous : elisa_distribution_graphique.png")
