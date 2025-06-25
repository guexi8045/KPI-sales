import pandas as pd
from reports.database import get_connection

def get_abschlussquote_krippenleitung_rohdaten():
    query = '''
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               krippenleitung AS category_name,
               COUNT(*) AS num_deals_abschluss,
               0 AS num_deals_absage
        FROM deals
        WHERE abschlussdatum IS NOT NULL
              AND abschlussdatum::date >= CURRENT_DATE - INTERVAL '2 years'
        GROUP BY month, krippenleitung

        UNION ALL

        SELECT TO_CHAR(absagedatum::date, 'YYYY-MM') AS month,
               krippenleitung AS category_name,
               0 AS num_deals_abschluss,
               COUNT(*) AS num_deals_absage
        FROM deals
        WHERE abschlussdatum IS NULL
              AND besichtigungsdatum IS NOT NULL
              AND absagedatum IS NOT NULL
              AND absagedatum::date >= CURRENT_DATE - INTERVAL '2 years'
        GROUP BY month, krippenleitung
    '''

    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()

    grouped = df.groupby(['month', 'category_name'], as_index=False).sum()
    return grouped.to_dict(orient="records")
