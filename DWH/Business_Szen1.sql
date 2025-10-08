USE db_reporting;

-- #########################################################
-- Tabelle tab_szenario_1 neu erstellen
-- #########################################################
DROP TABLE IF EXISTS tab_szenario_1;

CREATE TABLE tab_szenario_1 (
    Szenario1_ID INT AUTO_INCREMENT PRIMARY KEY,
    Temperatur_Bereich VARCHAR(20),
    Eissorte_Name VARCHAR(255),
    Durchschnitt_Stueckzahl_pro_15min DECIMAL(10,2)
);

INSERT INTO tab_szenario_1 (Temperatur_Bereich, Eissorte_Name, Durchschnitt_Stueckzahl_pro_15min)
SELECT
  CONCAT(
    CAST(bucket_start AS CHAR), 
    '-', 
    CAST(CAST(bucket_start + 4.9 AS DECIMAL(5,1)) AS CHAR)
  ) AS Temperatur_Bereich,
  t.Eissorte_Name,
  CAST(AVG(t.Stueck_je_15min) AS DECIMAL(10,2)) AS Durchschnitt_Stueckzahl_pro_15min
FROM (
    SELECT
      cf.Eissorte_Name,
      cf.Wetterzeit,
      SUM(cf.Menge) AS Stueck_je_15min,
      FLOOR(MAX(cf.Temperatur) / 5) * 5 AS bucket_start
    FROM db_core.Core_Fakten cf
    WHERE HOUR(cf.Wetterzeit) BETWEEN 9 AND 18
      AND (HOUR(cf.Wetterzeit) < 18 OR (HOUR(cf.Wetterzeit) = 18 AND MINUTE(cf.Wetterzeit) = 0))
    GROUP BY cf.Eissorte_Name, cf.Wetterzeit
) t
GROUP BY bucket_start, t.Eissorte_Name
ORDER BY bucket_start, t.Eissorte_Name;
