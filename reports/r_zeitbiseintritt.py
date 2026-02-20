import pandas as pd
from reports.database import get_connection

def get_zeitbiseintritt():
    query = """
        SELECT 
            id,
            abschlussdatum::date AS abschlussdatum,
            eintrittsdatum::date AS eintrittsdatum,
            TO_CHAR(abschlussdatum::date, 'YYYY-MM') AS month,
            (eintrittsdatum::date - abschlussdatum::date) AS anzahl_tage
        FROM deals
        WHERE abschlussdatum IS NOT NULL
          AND eintrittsdatum IS NOT NULL
        ORDER BY month ASC, abschlussdatum ASC, eintrittsdatum ASC, id ASC
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()

    return df.to_dict(orient="records")
