from app import create_table, DB_NAME
import sqlite3
from datetime import datetime


def test_create_table():
    # Supprimer la BDD si elle existe déjà pour un test propre
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    create_table()
    assert os.path.exists(DB_NAME), "❌ La base de données n’a pas été créée."

    # Vérifie que la table existe
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='facts'")
    table = cursor.fetchone()
    conn.close()

    assert table is not None, "❌ La table 'facts' n’a pas été créée."

def test_insert_fact():
    create_table()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    test_data = (
        "This is a test fact.",
        "en",
        "http://test.com",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    try:
        cursor.execute(
            "INSERT INTO facts (text, language, source_url, date_insertion) VALUES (?, ?, ?, ?)",
            test_data,
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # déjà présent
    finally:
        # Vérifie que le test_data a été inséré
        cursor.execute("SELECT text FROM facts WHERE text=?", (test_data[0],))
        row = cursor.fetchone()
        conn.close()

    assert row is not None, "❌ Le fait test n’a pas été inséré dans la base."
