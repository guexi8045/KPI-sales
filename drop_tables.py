from reports.database import get_connection

def drop_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS deals;")
    cursor.execute("DROP TABLE IF EXISTS mutationen;")

    conn.commit()
    conn.close()
    print("Tabellen 'deals' und 'mutationen' wurden gelöscht.")

if __name__ == "__main__":
    drop_tables()
