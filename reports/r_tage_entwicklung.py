import pandas as pd
from reports.database import get_connection

def get_tage_entwicklung():
    mutationen_query = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               'Zunahme Tage Mutationen' AS category_name,
               SUM(mutation_tage_plus_minus) AS num_deals
        FROM mutationen
        WHERE abschlussdatum IS NOT NULL
              AND mutation_tage_plus_minus > 0
        GROUP BY month
    """

    neukunden_query = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               'Zunahme Tage Neukunden' AS category_name,
               SUM(CASE
                       WHEN anzahl_tage ~ '^[0-9]+$' THEN CAST(anzahl_tage AS INTEGER)
                       ELSE 0
                   END) AS num_deals
        FROM deals
        WHERE abschlussdatum IS NOT NULL
        GROUP BY month
    """

    abnahme_kuendigungen_query = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               'Abnahme Tage Kündigungen' AS category_name,
               SUM(kuendigungen_anzahl_tage) AS num_deals
        FROM mutationen
        WHERE abschlussdatum IS NOT NULL
              AND kuendigungsgrund != 'KIGA'
              AND kuendigungen_anzahl_tage < 0
        GROUP BY month
    """

    abnahme_mutationen_query = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               'Abnahme Tage Mutationen' AS category_name,
               SUM(mutation_tage_plus_minus) AS num_deals
        FROM mutationen
        WHERE abschlussdatum IS NOT NULL
              AND mutation_tage_plus_minus < 0
        GROUP BY month
    """

    conn = get_connection()
    df_mutationen = pd.read_sql_query(mutationen_query, conn)
    df_neukunden = pd.read_sql_query(neukunden_query, conn)
    df_abnahme_kuendigungen = pd.read_sql_query(abnahme_kuendigungen_query, conn)
    df_abnahme_mutationen = pd.read_sql_query(abnahme_mutationen_query, conn)
    conn.close()

    df_zunahme = pd.concat([df_mutationen, df_neukunden])
    df_abnahme = pd.concat([df_abnahme_kuendigungen, df_abnahme_mutationen])

    return {
        "zunahme": df_zunahme.to_dict(orient="records"),
        "abnahme": df_abnahme.to_dict(orient="records")
    }
