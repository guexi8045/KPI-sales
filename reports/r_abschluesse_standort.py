from reports.database import get_connection
import pandas as pd

def get_abschluesse_standort():
    query = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               besichtigungsstandort AS category_name,
               COUNT(*) AS num_deals
        FROM deals
        WHERE abschlussdatum IS NOT NULL
          AND abschlussdatum::date >= CURRENT_DATE - INTERVAL '2 years'
        GROUP BY month, besichtigungsstandort
        ORDER BY month;
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")
