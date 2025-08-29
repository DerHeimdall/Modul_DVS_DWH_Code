import random
from datetime import datetime, timedelta

# -------------------------
# Konfiguration
# -------------------------
output_file = "wetter_data.sql"

# Zeitraum
start_date = datetime(2025, 8, 18)
end_date = datetime(2025, 8, 24, 23, 45)  # letzte 15-min Periode am Sonntag

# Tageswetter-Muster
tage = {
    "2025-08-18": {"regen": True,  "temp_min":16, "temp_max":20},  # Montag
    "2025-08-19": {"regen": True,  "temp_min":16, "temp_max":20},  # Dienstag
    "2025-08-20": {"regen": False, "temp_min":20, "temp_max":24},  # Mittwoch
    "2025-08-21": {"regen": False, "temp_min":20, "temp_max":24},  # Donnerstag
    "2025-08-22": {"regen": False, "temp_min":25, "temp_max":30},  # Freitag
    "2025-08-23": {"regen": False, "temp_min":25, "temp_max":30},  # Samstag
    "2025-08-24": {"regen": False, "temp_min":25, "temp_max":30}   # Sonntag
}

# -------------------------
# SQL-Datei erzeugen
# -------------------------
with open(output_file, "w", encoding="utf-8") as f:
    f.write("-- Tabelle Wetter erstellen\n")
    f.write("DROP TABLE IF EXISTS wetter;\n")
    f.write("""
CREATE TABLE wetter (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Zeitstempel DATETIME NOT NULL,
    Temperatur DECIMAL(4,1) NOT NULL,
    UV_Index INT NOT NULL,
    Bewoelkung INT NOT NULL,
    Niederschlag DECIMAL(4,2) NOT NULL
);\n\n""")

    insert_prefix = "INSERT INTO wetter (Zeitstempel, Temperatur, UV_Index, Bewoelkung, Niederschlag) VALUES\n"
    all_inserts = []

    current_time = start_date
    while current_time <= end_date:
        datum_str = current_time.strftime("%Y-%m-%d")
        wetter_tag = tage[datum_str]
        hour = current_time.hour + current_time.minute/60

        # Temperatur: morgens niedrig, mittags hoch, abends sinkend, leicht zufällig
        temp_range = wetter_tag["temp_max"] - wetter_tag["temp_min"]
        if hour < 9:
            temp = wetter_tag["temp_min"] + temp_range * 0.2 * random.uniform(0.8,1.2)
        elif 9 <= hour < 12:
            temp = wetter_tag["temp_min"] + temp_range * 0.5 * random.uniform(0.9,1.1)
        elif 12 <= hour < 16:
            temp = wetter_tag["temp_min"] + temp_range * 0.9 * random.uniform(0.9,1.1)
        elif 16 <= hour < 20:
            temp = wetter_tag["temp_min"] + temp_range * 0.6 * random.uniform(0.9,1.1)
        else:
            temp = wetter_tag["temp_min"] + temp_range * 0.3 * random.uniform(0.9,1.1)
        temp = round(min(max(temp, wetter_tag["temp_min"]), wetter_tag["temp_max"]),1)

        # UV-Index ähnlich wie Temperatur, nachts 0
        if 6 <= hour <= 18:
            uv_max = 10 if not wetter_tag["regen"] else 2
            uv = int(min(max((uv_max * (temp - wetter_tag["temp_min"]) / temp_range) + random.randint(-1,1),0), uv_max))
        else:
            uv = 0

        # Bewölkung in %
        if wetter_tag["regen"]:
            bevoelkung = random.randint(70,100)
        else:
            # Freitags-Sonntags fast klar, Mittwoch/Donnerstag mittlerer Wert
            if datum_str in ["2025-08-22","2025-08-23","2025-08-24"]:
                bevoelkung = random.randint(0,20)
            else:
                bevoelkung = random.randint(30,60)

        # Niederschlag
        if wetter_tag["regen"]:
            niederschlag = round(random.uniform(0.1,1.0),2)
        else:
            if datum_str in ["2025-08-22","2025-08-23","2025-08-24"]:
                niederschlag = 0.0
            else:
                niederschlag = round(random.uniform(0.0,0.05),2)

        all_inserts.append(f"('{current_time.strftime('%Y-%m-%d %H:%M:%S')}', {temp}, {uv}, {bevoelkung}, {niederschlag})")

        current_time += timedelta(minutes=15)

    # SQL in Blöcken schreiben, z.B. 200 pro INSERT
    block_size = 200
    for i in range(0, len(all_inserts), block_size):
        f.write(insert_prefix + ",\n".join(all_inserts[i:i+block_size]) + ";\n\n")

print(f"SQL-Datei '{output_file}' erfolgreich erzeugt!")
