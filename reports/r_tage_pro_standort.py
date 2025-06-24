import pandas as pd
from reports.database import get_connection

def get_tage_pro_standort():
    conn = get_connection()

    neukunden_query = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               besichtigungsstandort AS category_name,
               SUM(anzahl_tage) AS num_deals
        FROM deals
        WHERE abschlussdatum IS NOT NULL
          AND anzahl_tage IS NOT NULL
          AND abschlussdatum >= CURRENT_DATE - INTERVAL '2 years'
        GROUP BY month, besichtigungsstandort
    """

    mutationen_query = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               standort AS category_name,
               SUM(mutation_tage_plus_minus) AS num_deals
        FROM mutationen
        WHERE abschlussdatum IS NOT NULL
          AND mutation_tage_plus_minus > 0
          AND abschlussdatum >= CURRENT_DATE - INTERVAL '2 years'
        GROUP BY month, standort
    """

    abnahme_mutationen_query = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               standort AS category_name,
               SUM(mutation_tage_plus_minus) AS num_deals
        FROM mutationen
        WHERE abschlussdatum IS NOT NULL
          AND mutation_tage_plus_minus < 0
          AND abschlussdatum >= CURRENT_DATE - INTERVAL '2 years'
        GROUP BY month, standort
    """

    abnahme_kuendigungen_query = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               standort AS category_name,
               SUM(kuendigungen_anzahl_tage) AS num_deals
        FROM mutationen
        WHERE abschlussdatum IS NOT NULL
          AND kuendigungsgrund != 'KIGA'
          AND kuendigungen_anzahl_tage IS NOT NULL
          AND abschlussdatum >= CURRENT_DATE - INTERVAL '2 years'
        GROUP BY month, standort
    """

    df_neukunden = pd.read_sql_query(neukunden_query, conn)
    df_mutationen = pd.read_sql_query(mutationen_query, conn)
    df_abnahme_mutationen = pd.read_sql_query(abnahme_mutationen_query, conn)
    df_abnahme_kuendigungen = pd.read_sql_query(abnahme_kuendigungen_query, conn)
    conn.close()

    df_zunahme = pd.concat([df_neukunden, df_mutationen])
    df_abnahme = pd.concat([df_abnahme_mutationen, df_abnahme_kuendigungen])

    return {
        "zunahme": df_zunahme.to_dict(orient="records"),
        "abnahme": df_abnahme.to_dict(orient="records")
    }
