import tkinter as tk
from tkinter import messagebox, simpledialog, font, colorchooser
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import requests

API_URL = "https://uselessfacts.jsph.pl/random.json?language=en"
DB_NAME = "useless_facts.db"


# Créer la base de données si elle n'existe pas
def create_table():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT UNIQUE,
                language TEXT,
                source_url TEXT,
                date_insertion TEXT
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erreur BDD", f"Erreur création de table : {e}")


# Télécharger un fait inutile et l'ajouter à la base
def download_fact():
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO facts (text, language, source_url, date_insertion)
            VALUES (?, ?, ?, ?)
        """,
            (
                data["text"],
                data["language"],
                data["source_url"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        conn.commit()
        conn.close()
        status_label.config(text="✅ Fait ajouté : " + data["text"])

    except requests.exceptions.RequestException:
        messagebox.showerror("Erreur réseau", "Impossible de contacter l'API.")
    except sqlite3.IntegrityError:
        status_label.config(text="⚠️ Ce fait existe déjà")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")


# Effacer toutes les données de la base
def clear_db():
    if messagebox.askyesno("Confirmation", "Effacer toute la base ?"):
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM facts")
            conn.commit()
            conn.close()
            status_label.config(text="🗑️ Base de données vidée.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de vider la base : {e}")


# Calculer et afficher la moyenne des longueurs de faits
def show_average_length():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(LENGTH(text)) FROM facts")
        avg = cursor.fetchone()[0]
        conn.close()

        if avg:
            messagebox.showinfo(
                "Longueur moyenne", f"📐 Moyenne : {int(avg)} caractères"
            )
        else:
            messagebox.showinfo("Info", "Aucune donnée pour calculer la moyenne.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de calculer la moyenne : {e}")


# Afficher un graphique des 10 derniers faits
def show_graph():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, LENGTH(text) FROM facts ORDER BY id DESC LIMIT 10")
        data = cursor.fetchall()
        conn.close()

        if not data:
            messagebox.showinfo("Info", "Aucune donnée pour le graphique")
            return

        ids = [str(row[0]) for row in data]
        lengths = [row[1] for row in data]

        plt.bar(ids, lengths)
        plt.title("Longueur des 10 derniers faits")
        plt.xlabel("ID des faits")
        plt.ylabel("Nombre de caractères")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'afficher le graphique : {e}")


# Changer la couleur de fond
def change_background():
    color = colorchooser.askcolor(title="Choisir une couleur de fond")[1]
    if color:
        root.configure(bg=color)
        status_label.configure(bg=color)
        btn_graph.configure(bg=color)
        btn_avg.configure(bg=color)


# Changer la police du label de statut
def change_font():
    new_font = simpledialog.askstring(
        "Police", "Entrer le nom de la police (ex: Arial)"
    )
    if new_font:
        try:
            current_font = font.Font(font=status_label["font"])
            current_font.configure(family=new_font)
            status_label.configure(font=current_font)
        except tk.TclError:
            messagebox.showerror("Erreur", "Police inconnue.")


# ----- Interface -----
create_table()
root = tk.Tk()
root.title("Useless Facts App")

# Menu principal
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Menu Actions
actions_menu = tk.Menu(menu_bar, tearoff=0)
actions_menu.add_command(label="Télécharger un fait", command=download_fact)
actions_menu.add_command(label="Effacer la base", command=clear_db)
menu_bar.add_cascade(label="Actions", menu=actions_menu)

# Menu Options
options_menu = tk.Menu(menu_bar, tearoff=0)
options_menu.add_command(label="🎨 Couleur de fond", command=change_background)
options_menu.add_command(label="🖋️ Changer la police", command=change_font)
menu_bar.add_cascade(label="Options", menu=options_menu)

# Boutons
btn_graph = tk.Button(root, text="📊 Afficher le graphique", command=show_graph)
btn_graph.pack(pady=10)

btn_avg = tk.Button(root, text="📐 Moyenne des longueurs", command=show_average_length)
btn_avg.pack(pady=5)

# Label de statut
status_label = tk.Label(
    root, text="Bienvenue dans l'app !", wraplength=400, justify="left"
)
status_label.pack(pady=10)

root.mainloop()
