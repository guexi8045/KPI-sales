from reports.database import get_connection
import pandas as pd

def get_abschluesse_anzahl_tage():
    query = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               COALESCE(anzahl_tage::TEXT, 'Unbekannt') AS category_name,
               COUNT(*) AS num_deals
        FROM deals
        WHERE abschlussdatum IS NOT NULL
          AND abschlussdatum::date >= CURRENT_DATE - INTERVAL '2 years'
        GROUP BY month, category_name
        ORDER BY month;
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")
