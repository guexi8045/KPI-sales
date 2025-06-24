from reports.database import get_connection

def test():
    try:
        conn = get_connection()
        print("Verbindung zu PostgreSQL erfolgreich.")
        conn.close()
    except Exception as e:
        print("Fehler:", e)

if __name__ == "__main__":
    test()
