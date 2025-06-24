import pandas as pd
from reports.database import get_connection

def get_kuendigungen_nach_grund():
    query = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               kuendigungsgrund AS category_name,
               COUNT(*) AS num_deals
        FROM mutationen
        WHERE kuendigungsgrund IS NOT NULL
          AND abschlussdatum IS NOT NULL
          AND abschlussdatum::date >= CURRENT_DATE - INTERVAL '2 years'
        GROUP BY month, kuendigungsgrund
        ORDER BY month;
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")