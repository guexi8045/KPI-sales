from reports.database import get_connection
import pandas as pd

def get_besichtigungs_abschlussquote():
    query = """
        WITH besichtigungen AS (
            SELECT TO_CHAR(besichtigungsdatum::date, 'YYYY-MM') AS month,
                   COUNT(*) AS num_deals_besichtigung
            FROM deals
            WHERE besichtigungsdatum IS NOT NULL
              AND besichtigungsdatum >= CURRENT_DATE - INTERVAL '2 years'
            GROUP BY month
        ),
        absagen_besichtigung AS (
            SELECT TO_CHAR(absagedatum::date, 'YYYY-MM') AS month,
                   COUNT(*) AS num_deals_absage
            FROM deals
            WHERE absagedatum >= CURRENT_DATE - INTERVAL '2 years'
              AND (besichtigungsdatum IS NULL OR besichtigungsdatum = '')
            GROUP BY month
        ),
        abschluss AS (
            SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
                   COUNT(*) AS num_deals_abschluss
            FROM deals
            WHERE abschlussdatum IS NOT NULL
              AND abschlussdatum >= CURRENT_DATE - INTERVAL '2 years'
            GROUP BY month
        ),
        absagen_abschluss AS (
            SELECT TO_CHAR(absagedatum::date, 'YYYY-MM') AS month,
                   COUNT(*) AS num_deals_absage
            FROM deals
            WHERE abschlussdatum IS NULL
              AND besichtigungsdatum IS NOT NULL
              AND absagedatum >= CURRENT_DATE - INTERVAL '2 years'
            GROUP BY month
        )

        SELECT COALESCE(b.month, a.month) AS month,
               COALESCE(num_deals_besichtigung, 0) AS num_deals_besichtigung,
               COALESCE(abs_b.num_deals_absage, 0) AS num_deals_absage_besichtigung,
               COALESCE(num_deals_abschluss, 0) AS num_deals_abschluss,
               COALESCE(abs_a.num_deals_absage, 0) AS num_deals_absage_abschluss
        FROM besichtigungen b
        FULL OUTER JOIN absagen_besichtigung abs_b ON b.month = abs_b.month
        FULL OUTER JOIN abschluss a ON COALESCE(b.month, abs_b.month) = a.month
        FULL OUTER JOIN absagen_abschluss abs_a ON COALESCE(b.month, abs_b.month) = abs_a.month
        ORDER BY month;
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()

    df['quote_besichtigung'] = df['num_deals_besichtigung'] / (
        df['num_deals_besichtigung'] + df['num_deals_absage_besichtigung'].replace(0, 1))

    df['quote_abschluss'] = df['num_deals_abschluss'] / (
        df['num_deals_abschluss'] + df['num_deals_absage_abschluss'].replace(0, 1))

    return df.to_dict(orient="records")
