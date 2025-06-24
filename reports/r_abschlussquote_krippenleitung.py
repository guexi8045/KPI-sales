import pandas as pd
from reports.database import get_connection

def get_abschlussquote_krippenleitung():
    query = """
        SELECT TO_CHAR(a.abschlussmonat, 'YYYY-MM') AS month,
               a.kl AS category_name,
               COALESCE(a.count, 0) AS num_deals_abschluss,
               COALESCE(b.count, 0) AS num_deals_absage,
               CASE
                   WHEN (COALESCE(a.count, 0) + COALESCE(b.count, 0)) > 0 THEN
                       ROUND(1.0 * COALESCE(a.count, 0) / (COALESCE(a.count, 0) + COALESCE(b.count, 0)), 2)
                   ELSE 0.0
               END AS quote
        FROM (
            SELECT TO_DATE(abschlussdatum, 'YYYY-MM-DD')::date AS abschlussmonat,
                   krippenleitung AS kl,
                   COUNT(*) AS count
            FROM deals
            WHERE abschlussdatum IS NOT NULL
              AND TO_DATE(abschlussdatum, 'YYYY-MM-DD') >= CURRENT_DATE - INTERVAL '2 years'
            GROUP BY abschlussmonat, kl
        ) a
        LEFT JOIN (
            SELECT TO_DATE(absagedatum, 'YYYY-MM-DD')::date AS absagemonat,
                   krippenleitung AS kl,
                   COUNT(*) AS count
            FROM deals
            WHERE abschlussdatum IS NULL
              AND besichtigungsdatum IS NOT NULL
              AND TO_DATE(absagedatum, 'YYYY-MM-DD') >= CURRENT_DATE - INTERVAL '2 years'
            GROUP BY absagemonat, kl
        ) b ON a.abschlussmonat = b.absagemonat AND a.kl = b.kl
        ORDER BY month;
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")
