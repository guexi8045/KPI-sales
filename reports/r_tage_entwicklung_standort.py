import pandas as pd
from reports.database import get_connection

def get_tage_entwicklung_standort():
    query = '''
        SELECT *
        FROM (
            SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
                   besichtigungsstandort AS category_name,
                   SUM(anzahl_tage) AS num_deals
            FROM deals
            WHERE anzahl_tage > 0
              AND abschlussdatum IS NOT NULL
              AND abschlussdatum::date >= CURRENT_DATE - INTERVAL '2 years'
            GROUP BY month, besichtigungsstandort

            UNION ALL

            SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
                   standort AS category_name,
                   SUM(mutation_tage_plus_minus) AS num_deals
            FROM mutationen
            WHERE abschlussdatum IS NOT NULL
              AND abschlussdatum::date >= CURRENT_DATE - INTERVAL '2 years'
            GROUP BY month, standort

            UNION ALL

            SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
                   standort AS category_name,
                   SUM(kuendigungen_anzahl_tage) AS num_deals
            FROM mutationen
            WHERE kuendigungen_anzahl_tage < 0
              AND kuendigungsgrund != 'KIGA'
              AND abschlussdatum IS NOT NULL
              AND abschlussdatum::date >= CURRENT_DATE - INTERVAL '2 years'
            GROUP BY month, standort
        ) AS unified
        ORDER BY month
    '''

    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()

    df = df.groupby(['month', 'category_name'], as_index=False)['num_deals'].sum()
    return df.to_dict(orient="records")
