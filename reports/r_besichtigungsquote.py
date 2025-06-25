import pandas as pd
from reports.database import get_connection

def get_besichtigungsquote():
    query = '''
        SELECT b.month,
               COALESCE(b.num_deals, 0) AS num_deals_besichtigung,
               COALESCE(a.num_deals_absage, 0) AS num_deals_absage,
               CASE
                   WHEN (COALESCE(b.num_deals, 0) + COALESCE(a.num_deals_absage, 0)) > 0 THEN
                       1.0 * COALESCE(b.num_deals, 0) / (COALESCE(b.num_deals, 0) + COALESCE(a.num_deals_absage, 0))
                   ELSE 0.0
               END AS quote
        FROM (
            SELECT TO_CHAR(besichtigungsdatum::date, 'YYYY-MM') AS month,
                   COUNT(*) AS num_deals
            FROM deals
            WHERE besichtigungsdatum IS NOT NULL
              AND besichtigungsdatum::date >= CURRENT_DATE - INTERVAL '2 years'
            GROUP BY month
        ) b
        LEFT JOIN (
            SELECT TO_CHAR(absagedatum::date, 'YYYY-MM') AS month,
                   COUNT(*) AS num_deals_absage
            FROM deals
            WHERE absagedatum IS NOT NULL
              AND absagedatum::date >= CURRENT_DATE - INTERVAL '2 years'
              AND (besichtigungsdatum IS NULL OR besichtigungsdatum = '')
            GROUP BY month
        ) a ON b.month = a.month
    '''
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Format für Frontend-Kompatibilität
    df['category_name'] = 'Besichtigungsquote'
    df['num_deals'] = (df['quote'] * 100).round(2)  # Prozentwert für Diagramm

    return df[['month', 'category_name', 'num_deals']].to_dict(orient='records')
