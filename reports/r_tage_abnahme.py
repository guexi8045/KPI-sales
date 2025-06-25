import pandas as pd
from reports.database import get_connection

def get_abnahme_tage():
    query = '''
        SELECT *
        FROM (
            SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
                   'Abnahme Tage Mutationen' AS category_name,
                   SUM(mutation_tage_plus_minus) AS num_deals
            FROM mutationen
            WHERE mutation_tage_plus_minus < 0
              AND abschlussdatum IS NOT NULL
              AND abschlussdatum::date >= CURRENT_DATE - INTERVAL '2 years'
            GROUP BY month

            UNION ALL

            SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
                   'Abnahme Tage Kündigungen' AS category_name,
                   SUM(kuendigungen_anzahl_tage) AS num_deals
            FROM mutationen
            WHERE kuendigungen_anzahl_tage < 0
              AND kuendigungsgrund != 'KIGA'
              AND abschlussdatum IS NOT NULL
              AND abschlussdatum::date >= CURRENT_DATE - INTERVAL '2 years'
            GROUP BY month
        ) abnahmen
        ORDER BY month
    '''

    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")
