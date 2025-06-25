import pandas as pd
from reports.database import get_connection

def get_datenbereinigung_ids():
    query = '''
        SELECT id
        FROM deals
        WHERE 
            (
                abschlussdatum IS NOT NULL AND (
                    besichtigungsstandort = 'Unbekannt' OR
                    anzahl_tage IS NULL OR
                    (krippenleitung = 'Keine Besichtigung' AND besichtigungsdatum IS NOT NULL) OR
                    alter_beim_eintritt IS NULL OR
                    absagedatum IS NOT NULL OR
                    (besichtigungsdatum IS NULL AND krippenleitung <> 'Keine Besichtigung')
                )
            )
            OR
            (
                (absagedatum IS NOT NULL AND absagegrund = 'Unbekannt')
                OR (absagegrund <> 'Unbekannt' AND absagedatum IS NULL)
            );
    '''
    conn = get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df["id"].tolist()
