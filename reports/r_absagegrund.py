import pandas as pd
from reports.database import get_connection

def get_absagegruende():
    query = '''
        SELECT TO_CHAR(absagedatum::date, 'YYYY-MM') AS month,
               absagegrund AS category_name,
               COUNT(*) AS num_deals
        FROM deals
        WHERE absagegrund IS NOT NULL
          AND absagedatum IS NOT NULL
          AND absagedatum::date >= CURRENT_DATE - INTERVAL '2 years'
        GROUP BY month, absagegrund
        ORDER BY month;
    '''
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")
