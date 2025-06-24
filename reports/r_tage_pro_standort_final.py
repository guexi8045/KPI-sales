import pandas as pd
from reports.database import get_connection

def get_tage_gesamt_pro_standort():
    query_neukunden = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               besichtigungsstandort AS category_name,
               anzahl_tage AS tage
        FROM deals
        WHERE abschlussdatum IS NOT NULL
          AND anzahl_tage IS NOT NULL
          AND abschlussdatum::date >= CURRENT_DATE - INTERVAL '2 years'
    """

    query_mutationen_zunahme = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               standort AS category_name,
               mutation_tage_plus_minus AS tage
        FROM mutationen
        WHERE abschlussdatum IS NOT NULL
          AND mutation_tage_plus_minus > 0
          AND abschlussdatum::date >= CURRENT_DATE - INTERVAL '2 years'
    """

    query_abnahme_kuendigungen = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               standort AS category_name,
               kuendigungen_anzahl_tage AS tage
        FROM mutationen
        WHERE abschlussdatum IS NOT NULL
          AND kuendigungen_anzahl_tage < 0
          AND kuendigungsgrund != 'KIGA'
          AND abschlussdatum::date >= CURRENT_DATE - INTERVAL '2 years'
    """

    query_abnahme_mutationen = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               standort AS category_name,
               mutation_tage_plus_minus AS tage
        FROM mutationen
        WHERE abschlussdatum IS NOT NULL
          AND mutation_tage_plus_minus < 0
          AND abschlussdatum::date >= CURRENT_DATE - INTERVAL '2 years'
    """

    conn = get_connection()
    df_neukunden = pd.read_sql_query(query_neukunden, conn)
    df_mutationen = pd.read_sql_query(query_mutationen_zunahme, conn)
    df_abnahme_kuendigungen = pd.read_sql_query(query_abnahme_kuendigungen, conn)
    df_abnahme_mutationen = pd.read_sql_query(query_abnahme_mutationen, conn)
    conn.close()

    combined_df = pd.concat([df_neukunden, df_mutationen, df_abnahme_kuendigungen, df_abnahme_mutationen])
    result_df = combined_df.groupby(["month", "category_name"], as_index=False)["tage"].sum()

    return result_df.to_dict(orient="records")
