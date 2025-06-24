from reports.database import get_connection
import pandas as pd

def get_besichtigungen_pro_monat():
    query = """
        SELECT TO_CHAR(besichtigungsdatum::date, 'YYYY-MM') AS month,
               'Besichtigung' AS category_name,
               COUNT(*) AS num_deals
        FROM deals
        WHERE besichtigungsdatum IS NOT NULL
          AND besichtigungsdatum::date >= CURRENT_DATE - INTERVAL '2 years'
        GROUP BY month
        ORDER BY month;
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")
