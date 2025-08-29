import random
from datetime import datetime, timedelta

# -------------------------
# Konfiguration
# -------------------------
output_file = "verkauf_data.sql"

# Altersklassen
altersklassen = ["Kind", "Erwachsen", "Rentner"]

# Zahlarten
zahlarten = ["Bar", "Karte"]

# Sorten nach Kategorie-ID (wie in eissorte-Tabelle)
# Kategorie_ID: 1= Wassereis, 2=Milcheis-Fruchtig, 3=Milcheis-Klassisch, 4=Milcheis-Exotisch, 5=Sorbet, 6=Saison-Sommer, 7=Saison-Winter
sorten = {
    "Standard": [7,8,9,10],       # Milcheis-Klassisch
    "Fruchtig": [4,5,6,11],       # Milcheis-Fruchtig
    "Exotisch": [12,13,14,15],    # Milcheis-Exotisch
    "Wassereis": [1,2,3],
    "Sorbet": [16,17,18],
    "Saison-Sommer": [19,20],
    "Saison-Winter": [21,22,23]
}

# Tageswetter & Verkaufsmuster
tage = [
    {"datum":"2025-08-18", "regen": True,  "min_verkauf":300, "max_verkauf":400, "sorten":["Standard"]}, # Montag
    {"datum":"2025-08-19", "regen": True,  "min_verkauf":300, "max_verkauf":400, "sorten":["Standard"]}, # Dienstag
    {"datum":"2025-08-20", "regen": False, "min_verkauf":400, "max_verkauf":600, "sorten":["Standard","Fruchtig","Exotisch","Wassereis","Sorbet"]}, # Mittwoch
    {"datum":"2025-08-21", "regen": False, "min_verkauf":400, "max_verkauf":600, "sorten":["Standard","Fruchtig","Exotisch","Wassereis","Sorbet"]}, # Donnerstag
    {"datum":"2025-08-22", "regen": False, "min_verkauf":600, "max_verkauf":800, "sorten":["Standard","Fruchtig","Exotisch","Wassereis","Sorbet","Saison-Sommer"]}, # Freitag
    {"datum":"2025-08-23", "regen": False, "min_verkauf":600, "max_verkauf":800, "sorten":["Standard","Fruchtig","Exotisch","Wassereis","Sorbet","Saison-Sommer"]}, # Samstag
    {"datum":"2025-08-24", "regen": False, "min_verkauf":600, "max_verkauf":800, "sorten":["Standard","Fruchtig","Exotisch","Wassereis","Sorbet","Saison-Sommer"]}  # Sonntag
]

# Öffnungszeiten
oeffnungsstunden = list(range(9,19)) # 9 bis 18 Uhr

# -------------------------
# SQL-Datei erzeugen
# -------------------------
with open(output_file, "w", encoding="utf-8") as f:
    f.write("-- Tabelle Verkauf erstellen\n")
    f.write("DROP TABLE IF EXISTS verkauf;\n")
    f.write("""
CREATE TABLE verkauf (
    Verkaufs_ID INT AUTO_INCREMENT PRIMARY KEY,
    Zeitstempel DATETIME NOT NULL,
    Eissorte INT NOT NULL,
    Menge INT NOT NULL,
    Kunde_Altersklasse VARCHAR(20) NOT NULL,
    Zahlart VARCHAR(10) NOT NULL,
    FOREIGN KEY (Eissorte) REFERENCES eissorte(Sorten_ID)
);\n\n""")

    insert_prefix = "INSERT INTO verkauf (Zeitstempel, Eissorte, Menge, Kunde_Altersklasse, Zahlart) VALUES\n"
    all_inserts = []

    Verkaufs_ID_counter = 1

    for tag in tage:
        datum = tag["datum"]
        total_verkaeufe = random.randint(tag["min_verkauf"], tag["max_verkauf"])

        for _ in range(total_verkaeufe):
            # Uhrzeit: realistisch: Mittag & Nachmittag mehr
            hour = random.choices(
                population=oeffnungsstunden,
                weights=[1,1,2,3,4,3,2,1,1,1], # 9-18 Uhr, Mittags höher
                k=1
            )[0]
            minute = random.randint(0,59)
            second = random.randint(0,59)
            zeit = f"{datum} {hour:02d}:{minute:02d}:{second:02d}"

            # Altersklasse
            altersklasse = random.choices(
                altersklassen,
                weights=[0.3, 0.5, 0.2], # Erwachsene häufiger
                k=1
            )[0]

            # Menge: 1-4 Kugeln, meist 1-2
            menge = random.choices([1,2,3,4], weights=[0.6,0.3,0.08,0.02], k=1)[0]

            # Zahlart: ca. 65% Bar, 35% Karte
            zahlart = random.choices(zahlarten, weights=[0.65,0.35], k=1)[0]

            # Sorte: nach Schema oder random 50/50
            if random.random() < 0.5:
                # Schema
                if altersklasse=="Kind":
                    moegliche_sorten = []
                    if "Wassereis" in tag["sorten"]: moegliche_sorten += sorten["Wassereis"]
                    if "Fruchtig" in tag["sorten"]: moegliche_sorten += sorten["Fruchtig"]
                    if "Standard" in tag["sorten"]: moegliche_sorten += sorten["Standard"]
                elif altersklasse=="Erwachsen":
                    moegliche_sorten = []
                    for k in ["Standard","Fruchtig","Exotisch","Sorbet","Saison-Sommer"]:
                        if k in tag["sorten"]:
                            moegliche_sorten += sorten[k]
                elif altersklasse=="Rentner":
                    moegliche_sorten = []
                    if "Standard" in tag["sorten"]: moegliche_sorten += sorten["Standard"]
                    if "Fruchtig" in tag["sorten"]: moegliche_sorten += sorten["Fruchtig"]
                if not moegliche_sorten:
                    moegliche_sorten = sum([sorten[k] for k in tag["sorten"]], [])
                eissorte = random.choice(moegliche_sorten)
            else:
                # komplett random aus erlaubten Sorten des Tages
                moegliche_sorten = sum([sorten[k] for k in tag["sorten"]], [])
                eissorte = random.choice(moegliche_sorten)

            all_inserts.append(f"('{zeit}', {eissorte}, {menge}, '{altersklasse}', '{zahlart}')")

    # SQL in Blöcken schreiben, z.B. 500 pro INSERT
    block_size = 500
    for i in range(0, len(all_inserts), block_size):
        f.write(insert_prefix + ",\n".join(all_inserts[i:i+block_size]) + ";\n\n")

print(f"SQL-Datei '{output_file}' erfolgreich erzeugt!")
