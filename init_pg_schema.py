from reports.database import get_connection

def create_deals_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY,
            status TEXT,
            empfehlung TEXT,
            finanzierung TEXT,
            alter_beim_eintritt TEXT,
            anzahl_tage INTEGER,
            absagegrund TEXT,
            besichtigungsstandort TEXT,
            krippenleitung TEXT,
            abschlussdatum TEXT,
            besichtigungsdatum TEXT,
            herkunft TEXT,
            kanal TEXT,
            anfragedatum TEXT,
            notitzen_subventionen TEXT,
            absagedatum TEXT,
            eintrittsdatum TEXT
        );
    """)

def create_mutationen_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mutationen (
            id INTEGER PRIMARY KEY,
            kuendigungen_anzahl_tage INTEGER,
            mutation_tage_plus_minus INTEGER,
            abschlussdatum TEXT,
            kuendigungsgrund TEXT,
            standort TEXT
        );
    """)

def init_schema():
    conn = get_connection()
    cursor = conn.cursor()
    create_deals_table(cursor)
    create_mutationen_table(cursor)
    conn.commit()
    conn.close()
    print("Tabellen wurden erstellt oder existierten bereits.")

if __name__ == "__main__":
    init_schema()
