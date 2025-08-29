-- Ziel-Datenbank anlegen (falls noch nicht vorhanden)
CREATE DATABASE IF NOT EXISTS db_staging
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

USE db_staging;

-- Wetterdaten kopieren (ohne Orts_ID)
DROP TABLE IF EXISTS Tab_Staging_Wetter;
CREATE TABLE Tab_Staging_Wetter AS
SELECT ID, Zeitstempel, Temperatur, UV_Index, Bewoelkung, Niederschlag
FROM db_wetterdaten.wetter;

-- Eissorten kopieren (ohne Preis)
DROP TABLE IF EXISTS Tab_Staging_Eissorte;
CREATE TABLE Tab_Staging_Eissorte AS
SELECT Sorten_ID, Name, Kategorie_ID
FROM db_eisdiele.eissorte;

-- Kategorien kopieren (unverändert)
DROP TABLE IF EXISTS Tab_Staging_Kategorie;
CREATE TABLE Tab_Staging_Kategorie AS
SELECT Kategorie_ID, Name
FROM db_eisdiele.kategorie;

-- Verkäufe kopieren (ohne Zahlart)
DROP TABLE IF EXISTS Tab_Staging_Verkauf;
CREATE TABLE Tab_Staging_Verkauf AS
SELECT Verkaufs_ID, Zeitstempel, Eissorte, Menge, Kunde_Altersklasse
FROM db_eisdiele.verkauf;
