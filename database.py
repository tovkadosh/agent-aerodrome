import sqlite3

def init_db():
    conn = sqlite3.connect("aerodrome2.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        immatriculation TEXT NOT NULL,
        modele TEXT NOT NULL,
        compagnie TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vols (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_vol TEXT NOT NULL,
        avion_id INTEGER,
        origine TEXT NOT NULL,
        destination TEXT NOT NULL,
        heure_depart TEXT NOT NULL,
        statut TEXT NOT NULL,
        FOREIGN KEY (avion_id) REFERENCES avions(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pistes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT NOT NULL,
        longueur_m INTEGER NOT NULL,
        etat TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("Base de données initialisée avec succès.")

def seed_data():
    conn = sqlite3.connect("aerodrome2.db")
    cursor = conn.cursor()
    
    #vérification des doublons
    cursor.execute("SELECT COUNT (*) FROM avions")
    if cursor.fetchone()[0]>0:
        print("Donnée déjà présentes , on ne reinsère pas .")
        conn.close()
        return
    avions = [
        ("F-GKXA", "A320", "Air France"),
        ("F-HBNA", "A350", "Air France"),
        ("D-AIHF", "A380", "Lufthansa"),
        ("G-EUUO", "A319", "British Airways"),
        ("EC-MXV", "B737", "Iberia"),
    ]
    cursor.executemany("INSERT INTO avions (immatriculation, modele, compagnie) VALUES (?, ?, ?)", avions)

    vols = [
        ("AF1234", 1, "Paris-CDG", "New York-JFK", "2026-06-21 08:30", "à l'heure"),
        ("AF5678", 2, "Paris-CDG", "Tokyo-Narita", "2026-06-21 10:15", "retardé"),
        ("LH9012", 3, "Francfort", "Paris-CDG", "2026-06-21 14:00", "à l'heure"),
        ("BA3456", 4, "Londres-Heathrow", "Paris-Orly", "2026-06-21 09:45", "annulé"),
        ("IB7890", 5, "Madrid", "Paris-Orly", "2026-06-21 16:20", "à l'heure"),
    ]
    cursor.executemany("INSERT INTO vols (numero_vol, avion_id, origine, destination, heure_depart, statut) VALUES (?, ?, ?, ?, ?, ?)", vols)

    pistes = [
        ("09L/27R", 4200, "ouverte"),
        ("08L/26R", 3600, "ouverte"),
        ("06/24", 2900, "maintenance"),
    ]
    cursor.executemany("INSERT INTO pistes (numero, longueur_m, etat) VALUES (?, ?, ?)", pistes)

    conn.commit()
    conn.close()
    print("Données d'exemple insérées.")

if __name__ == "__main__":
    init_db()
    seed_data()    