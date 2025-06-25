import pandas as pd
from reports.database import get_connection

def get_datenbereinigung_mutationen_ids():
    query = """
        SELECT id
        FROM mutationen
        WHERE 
            (abschlussdatum IS NOT NULL AND standort = 'Unbekannt')
            OR
            (abschlussdatum IS NOT NULL AND 
            (mutation_tage_plus_minus = 0 AND kuendigungen_anzahl_tage = 0))
            OR
            (kuendigungen_anzahl_tage > 0 AND kuendigungsgrund = 'Unbekannt');
    """
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df["id"].tolist()
