from reports.database import get_connection
import pandas as pd

def get_anfragen_nach_kanal():
    query = """
        SELECT TO_CHAR(anfragedatum::date, 'YYYY-MM') AS month,
               kanal AS category_name,
               COUNT(*) AS num_deals
        FROM deals
        WHERE anfragedatum IS NOT NULL
          AND anfragedatum::date >= CURRENT_DATE - INTERVAL '2 years'
        GROUP BY month, kanal
        ORDER BY month;
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")
