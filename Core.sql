-- #########################################################
-- 1) Ziel-Datenbank anlegen
-- #########################################################
CREATE DATABASE IF NOT EXISTS db_core
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

USE db_core;

-- #########################################################
-- 2) Hilfsspalten in db_staging ergänzen (gerundete Timestamps)
-- #########################################################

-- In Wetter: Zeitstempel in 15-Minuten-Schema umwandeln
ALTER TABLE db_staging.Tab_Staging_Wetter
  ADD COLUMN Zeitstempel_15min BIGINT;

UPDATE db_staging.Tab_Staging_Wetter
SET Zeitstempel_15min = DATE_FORMAT(
    FROM_UNIXTIME(UNIX_TIMESTAMP(Zeitstempel) - (MINUTE(Zeitstempel) % 15)*60),
    '%Y%m%d%H%i'
);

-- In Verkauf: Zeitstempel auf 15 Minuten runden
ALTER TABLE db_staging.Tab_Staging_Verkauf
  ADD COLUMN Zeitstempel_15min BIGINT;

UPDATE db_staging.Tab_Staging_Verkauf
SET Zeitstempel_15min = DATE_FORMAT(
    FROM_UNIXTIME(UNIX_TIMESTAMP(Zeitstempel) - (MINUTE(Zeitstempel) % 15)*60),
    '%Y%m%d%H%i'
);

-- #########################################################
-- 3) Zieltabelle anlegen
-- #########################################################
DROP TABLE IF EXISTS Core_Fakten;

CREATE TABLE Core_Fakten (
    Core_ID INT AUTO_INCREMENT PRIMARY KEY,
    Verkaufs_ID INT,
    Verkaufszeit DATETIME,
    Eissorte_ID INT,
    Eissorte_Name VARCHAR(100),
    Kategorie_ID INT,
    Kategorie_Name VARCHAR(100),
    Menge INT,
    Kunde_Altersklasse VARCHAR(20),
    Wetter_ID INT,
    Wetterzeit DATETIME,
    Temperatur DECIMAL(4,1),
    UV_Index INT,
    Bewoelkung INT,
    Niederschlag DECIMAL(4,2)
);

-- #########################################################
-- 4) Insert in Zieltabelle mit allen Joins
-- #########################################################
INSERT INTO Core_Fakten (
    Verkaufs_ID, Verkaufszeit, Eissorte_ID, Eissorte_Name,
    Kategorie_ID, Kategorie_Name, Menge, Kunde_Altersklasse,
    Wetter_ID, Wetterzeit, Temperatur, UV_Index, Bewoelkung, Niederschlag
)
SELECT
    v.Verkaufs_ID,
    v.Zeitstempel AS Verkaufszeit,
    e.Sorten_ID AS Eissorte_ID,
    e.Name AS Eissorte_Name,
    k.Kategorie_ID,
    k.Name AS Kategorie_Name,
    v.Menge,
    v.Kunde_Altersklasse,
    w.ID AS Wetter_ID,
    w.Zeitstempel AS Wetterzeit,
    w.Temperatur,
    w.UV_Index,
    w.Bewoelkung,
    w.Niederschlag
FROM db_staging.Tab_Staging_Verkauf v
JOIN db_staging.Tab_Staging_Eissorte e ON v.Eissorte = e.Sorten_ID
JOIN db_staging.Tab_Staging_Kategorie k ON e.Kategorie_ID = k.Kategorie_ID
JOIN db_staging.Tab_Staging_Wetter w ON v.Zeitstempel_15min = w.Zeitstempel_15min
WHERE HOUR(w.Zeitstempel) BETWEEN 9 AND 18;

-- #########################################################
-- Fertig 🎉
-- #########################################################
