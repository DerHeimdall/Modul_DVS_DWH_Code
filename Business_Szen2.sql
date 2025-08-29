USE db_reporting;

-- #########################################################
-- Tabelle tab_szenario_2 neu erstellen
-- #########################################################
DROP TABLE IF EXISTS tab_szenario_2;

CREATE TABLE tab_szenario_2 (
    Szenario2_ID INT AUTO_INCREMENT PRIMARY KEY,
    UV_Index INT,
    Kategorie_Name VARCHAR(255),
    Gesamt_Stueck INT,
    Platz INT
);

INSERT INTO tab_szenario_2 (UV_Index, Kategorie_Name, Gesamt_Stueck, Platz)
WITH summen AS (
    SELECT
        cf.UV_Index,
        cf.Kategorie_Name,
        SUM(cf.Menge) AS Gesamt_Stueck
    FROM db_core.Core_Fakten cf
    WHERE HOUR(cf.Wetterzeit) BETWEEN 9 AND 18
      AND (HOUR(cf.Wetterzeit) < 18 OR (HOUR(cf.Wetterzeit) = 18 AND MINUTE(cf.Wetterzeit) = 0))
    GROUP BY cf.UV_Index, cf.Kategorie_Name
),
ranking AS (
    SELECT
        s.*,
        ROW_NUMBER() OVER (PARTITION BY s.UV_Index ORDER BY s.Gesamt_Stueck DESC) AS Platz
    FROM summen s
)
SELECT
    UV_Index,
    Kategorie_Name,
    Gesamt_Stueck,
    Platz
FROM ranking
WHERE Platz <= 3
ORDER BY UV_Index, Platz;
