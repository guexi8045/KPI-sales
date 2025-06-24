from reports.database import get_connection
import pandas as pd

def get_abschluesse_nach_finanzierung():
    query = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               finanzierung AS category_name,
               SUM(CAST(anzahl_tage AS INTEGER)) AS total_days
        FROM deals
        WHERE abschlussdatum IS NOT NULL
          AND anzahl_tage IS NOT NULL
          AND abschlussdatum::date >= CURRENT_DATE - INTERVAL '2 years'
        GROUP BY month, finanzierung
        ORDER BY month;
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")
