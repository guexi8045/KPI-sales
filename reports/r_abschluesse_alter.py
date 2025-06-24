from reports.database import get_connection
import pandas as pd

def get_abschluesse_nach_alter():
    query = """
        SELECT TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
               alter_beim_eintritt AS category_name,
               SUM(CAST(anzahl_tage AS INTEGER)) AS total_days
        FROM deals
        WHERE abschlussdatum IS NOT NULL
          AND alter_beim_eintritt IS NOT NULL
          AND anzahl_tage IS NOT NULL
          AND abschlussdatum::date >= CURRENT_DATE - INTERVAL '2 years'
        GROUP BY month, alter_beim_eintritt
        ORDER BY month;
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict(orient="records")
